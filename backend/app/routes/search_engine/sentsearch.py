import faiss
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

    def search(self, query_text, top_k=30, use_reranker=False, filtered_by_collection=True):
        """
        Search the FAISS HNSW index for the top_k closest vectors to the query text.
        """
        print("Searching")
        #enhanced_query = self.enhance_query_with_entities(query_text)
        
        if self.model_name == 'mixedbread-ai/mxbai-embed-large-v1':
            query_text = f'Represent this sentence for searching relevant passages: {query_text}'
        
        
        query_embedding = self.model.encode(query_text, convert_to_numpy=True)
        l2_norm = np.linalg.norm(query_embedding)
        query_embedding = query_embedding / l2_norm

        # Correctly access the hnsw index from IndexIDMap
        if isinstance(self.index, faiss.IndexIDMap):
            hnsw_index = faiss.downcast_index(self.index.index)  # Access the underlying HNSW index
            hnsw_index.hnsw.efSearch = 100  # Example value, adjust based on desired search precision
        else:
            print("Index is not of type IndexIDMap with an HNSW index.")
            return None

        _, retrieved_ids = self.index.search(np.expand_dims(query_embedding, axis=0), k=top_k)
        
            # The rest of the search method remains unchanged
        
        if len(retrieved_ids) == 0:
            return None
        
        matches = self.item_desc.iloc[retrieved_ids[0]]

        # Conditional reranking
        if use_reranker and self.reranker is not None:
            retrieved_text = self.captions.iloc[retrieved_ids[0]]
            scores = self.reranker.compute_score([(query_text, rt) for rt in retrieved_text])
            matches['scores'] = scores
            matches = matches.sort_values(by='scores', ascending=False).reset_index(drop=True)
            print("Reranked matches: ", matches)
            
         
        
        if filtered_by_collection:
            matches = matches[matches['scryfalloracleid'].isin(self.collection['scryfalloracleid'].values)]
        
        return matches


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