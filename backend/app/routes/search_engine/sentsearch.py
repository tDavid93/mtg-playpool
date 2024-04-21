import faiss
import idlelib
import numpy as np
from sentence_transformers import SentenceTransformer

import os
import gc
import time

from FlagEmbedding import FlagReranker
import pandas as pd



class SentenceSearch:
    model = None
    index = None
    name = None
    model_name = ''
    
   # ner_model = spacy.load("hu_core_news_lg")

    def __init__(self, item_desc, captions,model_paths, rerankers):
        self.item_desc = item_desc
        self.captions = captions
        self.reranker = rerankers
        self.model_paths = model_paths
        
        self.embeddings = None
        self.collection = pd.read_csv('all_my_cards.csv')
        self.collection['scryfalloracleid'] = self.collection.apply(lambda x: ', '.join(item_desc[item_desc['name'] == x['Card Name']]['scryfalloracleid'].unique()), axis=1)
        self.filter_ids = set(self.collection['scryfalloracleid'].values)

    def load_and_unload_model(self, model_name , rebuild_embeddings=False):
        """
        Load a new model and its FAISS index, unloading any previously loaded model.
        """
        self.model_name = model_name

        # Unload the current model
        if self.model is not None:
            del self.model
            del self.index
            gc.collect()

        self.model = SentenceTransformer(self.model_name, trust_remote_code=True, device='cuda')
        if not os.path.exists(f"embeddings/{self.model_name}.npy") or rebuild_embeddings:
            print(f"Creating embeddings for {self.model_name}")
            self.create_embeddings()
        else: 
            self.embeddings = np.load(f"embeddings/{self.model_name}.npy")
        self.index = self.create_faiss_vector_store()

        return f"Model {model_name} loaded successfully."
    
    def load_reranker(self, reranker_name):
        """
        Load a reranker model.
        """
        self.reranker = FlagReranker(reranker_name)
        return f"Reranker {reranker_name} loaded successfully."

    def create_embeddings(self):
        """
        Create embeddings for the entire dataset.
        """
        self.embeddings = self.model.encode(self.captions, convert_to_numpy=True, show_progress_bar=True)

        if not os.path.exists(f'embeddings/{self.model_name}.py'):
            print(f'Creating directory embeddings/{self.model_name}')
            os.makedirs(f'embeddings/{self.model_name}')
        

        np.save(f"embeddings/{self.model_name}.npy", self.embeddings)



    def create_faiss_vector_store(self):
        """
        Create an HNSW FAISS index for storing vectors.
        """
        print("Creating FAISS index")
        embedding_dimension = self.embeddings.shape[1]
        
        # Create an HNSW index
        index = faiss.IndexHNSWFlat(embedding_dimension, 32)  # Example: M=32
        index.hnsw.efConstruction = 200  # Example value, adjust based on dataset size and desired precision
        faiss.normalize_L2(self.embeddings)  # Ensure embeddings are normalized if not already
        
        # Wrap the HNSW index with an IDMap
        index_with_ids = faiss.IndexIDMap(index)
        index_with_ids.add_with_ids(self.embeddings, np.arange(len(self.embeddings)))

        return index_with_ids


    def extract_entities(self, text):
        """
        Extract named entities from the text using spaCy.
        """
        print("Extracting entities")
        doc = self.ner_model(text)
        entities = {ent.text: ent.label_ for ent in doc.ents}
        print("Entities extracted: ", entities)
        return entities

    def enhance_query_with_entities(self, query_text):
        """
        Enhance the search query by identifying and prioritizing entities.
        """
        print(f"Query text: {query_text}")
        entities = self.extract_entities(query_text)
        # You can modify this part to customize how you want to enhance the query based on extracted entities
        enhanced_query = query_text
        for entity, label in entities.items():
            if label in ['ORG', 'PRODUCT']:  # Customize based on your needs
                
                enhanced_query += f" {entity}"
        
        print(f"Enhanced query: {enhanced_query}")
        return enhanced_query
    
    def preprocess_query(self, query):
    # Example preprocessing to better align with card data
        return f"Find card that match: {query}"

    def search(self, query_text, top_k=30, use_reranker=True, filtered_by_collection=True):
        """
        Search the FAISS HNSW index for the top_k closest vectors to the query text.
        """
        print("Searching")
        try:
            query_text = self.preprocess_query(query_text)
            
            if self.model_name == 'mixedbread-ai/mxbai-embed-large-v1':
                query_text = f'Represent this sentence for searching relevant passages: {query_text}'
            
            query_embedding = self.model.encode(query_text, convert_to_numpy=True)
            l2_norm = np.linalg.norm(query_embedding)
            query_embedding /= l2_norm

            matches = None
            max_iterations = 10
            iteration = 0
            found_enough_matches = False

            while iteration < max_iterations and not found_enough_matches:
                if isinstance(self.index, faiss.IndexIDMap):
                    hnsw_index = faiss.downcast_index(self.index.index)
                    hnsw_index.hnsw.efSearch = 100  # Adjust this value based on desired search precision
                    distances, retrieved_ids = self.index.search(np.expand_dims(query_embedding, axis=0), top_k)
                else:
                    print("Index is not of type IndexIDMap with an HNSW index.")
                    return None

                if len(retrieved_ids[0]) == 0:
                    print("No matches found in this iteration.")
                    iteration += 1
                    top_k *= 2  # Increase the search scope
                    continue

                current_matches = self.item_desc.iloc[retrieved_ids[0]].reset_index(drop=True)

                if filtered_by_collection:
                    # Ensure that current_matches filtering by 'scryfalloracleid' does not use a list directly if it's unhashable
                    
                    
                    current_matches = current_matches[current_matches['scryfalloracleid'].isin(self.filter_ids)]
                    print(f"Iteration {iteration + 1}: Found {len(current_matches)} matches in collection.")

                print(f"Iteration {iteration + 1}: Found {len(current_matches)} matches.")
                if matches is None:
                    matches = current_matches
                else:
                    print(f"Current matches: {current_matches.shape}, Total matches: {matches.shape}.")
                    matches = pd.concat([matches, current_matches], ignore_index=True)
                    matches = matches.drop_duplicates(subset=['scryfalloracleid'])

                if len(matches) >= top_k:
                    found_enough_matches = True
                    matches = matches.head(top_k)
                    print("Found enough matches.")
                else:
                    iteration += 1
                    top_k *= 2  # Increase the search scope

                if top_k > 1000:
                    print("Reached upper limit for search breadth.")
                    break

            if use_reranker and self.reranker is not None:
                retrieved_text = self.captions.iloc[retrieved_ids[0]]
                scores = self.reranker.compute_score([(query_text, rt) for rt in retrieved_text])
                matches['scores'] = scores
                matches = matches.sort_values(by='scores', ascending=False).reset_index(drop=True)
                print("Reranked matches: ", matches)

            return matches

        except Exception as e:
            print(f"An error occurred during search: {e}")
            return None


    def gradio_search(self, query, use_reranker,filtered_by_collection, top_k=30):
        """
        Perform a search using the currently loaded model.
        """
        start = time.time()
        
        if self.model is None:
            return "No model is loaded. Please load a model first."

        #print(f"Searching with model {self.model_name} and reranker {self.reranker.model}.")
        results = self.search(query, top_k, use_reranker, filtered_by_collection)

        if results is None:
            return "No matches found."

        #categories = self.get_categories(results)
        #print(type(categories))

        if use_reranker:
            results = results.sort_values(by='scores', ascending=False).reset_index(drop=True)
        
        query_time = time.time() - start
        time_text = f"Query time: {query_time:.4f} seconds {'With' if use_reranker else 'Without'} reranker"
        self.results = results
        
        
        results = results.to_dict(orient='records')
        
        return results,  time_text 
    
    

    def filter_results(self, categories):
        if not categories:
            filtered_df = self.results
        else:
            filtered_df = self.results[self.results['category'].isin(categories)]

        return filtered_df






    def get_single_embedding(self, text):
        return self.model.encode(text, convert_to_numpy=True)