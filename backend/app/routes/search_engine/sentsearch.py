import os
import gc
import time
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from FlagEmbedding import FlagReranker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelManager:
    """Handles model loading and resource management"""
    
    def __init__(self):
        self.current_model: Optional[SentenceTransformer] = None
        self.current_model_name: str = ""
        self.reranker: Optional[FlagReranker] = None
    
    def load_sentence_model(self, model_name: str) -> None:
        """Load a sentence transformer model"""
        if self.current_model_name == model_name and self.current_model is not None:
            logger.info(f"Model {model_name} already loaded")
            return
            
        self._cleanup_current_model()
        
        try:
            self.current_model = SentenceTransformer(
                model_name, 
                trust_remote_code=True, 
                device='cuda'
            )
            self.current_model_name = model_name
            logger.info(f"Successfully loaded model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            raise
    
    def load_reranker(self, reranker_name: str) -> None:
        """Load a reranker model"""
        try:
            self.reranker = FlagReranker(reranker_name)
            logger.info(f"Successfully loaded reranker: {reranker_name}")
        except Exception as e:
            logger.error(f"Failed to load reranker {reranker_name}: {e}")
            raise
    
    def _cleanup_current_model(self) -> None:
        """Clean up currently loaded model"""
        if self.current_model is not None:
            del self.current_model
            self.current_model = None
            self.current_model_name = ""
            gc.collect()


class EmbeddingManager:
    """Handles embedding creation and caching"""
    
    def __init__(self, embeddings_dir: str = "embeddings"):
        self.embeddings_dir = Path(embeddings_dir)
        self.embeddings_dir.mkdir(exist_ok=True)
    
    def get_embeddings_path(self, model_name: str) -> Path:
        """Get the path for cached embeddings"""
        # Clean model name for filesystem
        safe_name = model_name.replace('/', '_').replace('\\', '_')
        return self.embeddings_dir / f"{safe_name}.npy"
    
    def load_or_create_embeddings(
        self, 
        model: SentenceTransformer, 
        model_name: str, 
        texts: List[str],
        force_rebuild: bool = False
    ) -> np.ndarray:
        """Load cached embeddings or create new ones"""
        embeddings_path = self.get_embeddings_path(model_name)
        
        if embeddings_path.exists() and not force_rebuild:
            logger.info(f"Loading cached embeddings from {embeddings_path}")
            return np.load(embeddings_path)
        
        logger.info(f"Creating embeddings for {model_name}")
        embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
        
        # Cache the embeddings
        np.save(embeddings_path, embeddings)
        logger.info(f"Saved embeddings to {embeddings_path}")
        
        return embeddings


class FAISSIndexManager:
    """Handles FAISS index creation and management"""
    
    @staticmethod
    def create_hnsw_index(embeddings: np.ndarray, m: int = 32, ef_construction: int = 200) -> faiss.IndexIDMap:
        """Create an HNSW FAISS index"""
        logger.info("Creating FAISS HNSW index")
        
        embedding_dimension = embeddings.shape[1]
        
        # Create HNSW index
        index = faiss.IndexHNSWFlat(embedding_dimension, m)
        index.hnsw.efConstruction = ef_construction
        
        # Normalize embeddings
        normalized_embeddings = embeddings.copy()
        faiss.normalize_L2(normalized_embeddings)
        
        # Wrap with IDMap for ID support
        index_with_ids = faiss.IndexIDMap(index)
        index_with_ids.add_with_ids(normalized_embeddings, np.arange(len(embeddings)))
        
        logger.info(f"Created index with {len(embeddings)} vectors")
        return index_with_ids


class QueryProcessor:
    """Handles query preprocessing and enhancement"""
    
    @staticmethod
    def preprocess_query(query: str, model_name: str = "") -> str:
        """Preprocess query based on model requirements"""
        processed_query = f"Find card that match: {query}"
        
        # Model-specific preprocessing
        if 'mtg-commander-embeddings' in model_name:
            processed_query = f'Represent this sentence for searching relevant passages: {processed_query}'
        
        return processed_query


class SentenceSearch:
    """Main search class with improved architecture"""
    
    def __init__(self, item_desc: pd.DataFrame, captions: List[str], collection_path: str = 'all_my_cards.csv'):
        self.item_desc = item_desc
        self.captions = captions
        
        # Initialize managers
        self.model_manager = ModelManager()
        self.embedding_manager = EmbeddingManager()
        self.query_processor = QueryProcessor()
        
        # Load collection and create filter
        self.collection = self._load_collection(collection_path)
        self.filter_ids = self._create_filter_ids()
        
        # Search components
        self.embeddings: Optional[np.ndarray] = None
        self.index: Optional[faiss.IndexIDMap] = None
        self.last_results: Optional[pd.DataFrame] = None
    
    def _load_collection(self, collection_path: str) -> pd.DataFrame:
        """Load and prepare collection data"""
        if not os.path.exists(collection_path):
            logger.warning(f"Collection file {collection_path} not found")
            return pd.DataFrame()
        
        collection = pd.read_csv(collection_path)
        
        # Create scryfalloracleid mapping
        collection['scryfalloracleid'] = collection.apply(
            lambda x: ', '.join(
                self.item_desc[self.item_desc['name'] == x['Card Name']]['scryfalloracleid'].unique()
            ), 
            axis=1
        )
        
        return collection
    
    def _create_filter_ids(self) -> set:
        """Create set of filter IDs for collection filtering"""
        if self.collection.empty:
            return set()
        return set(self.collection['scryfalloracleid'].values)
    
    def load_model(self, model_name: str, rebuild_embeddings: bool = False) -> str:
        """Load model and prepare for searching"""
        try:
            # Load the model
            self.model_manager.load_sentence_model(model_name)
            
            # Create or load embeddings
            self.embeddings = self.embedding_manager.load_or_create_embeddings(
                self.model_manager.current_model,
                model_name,
                self.captions,
                rebuild_embeddings
            )
            
            # Create FAISS index
            self.index = FAISSIndexManager.create_hnsw_index(self.embeddings)
            
            return f"Model {model_name} loaded successfully"
            
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            return f"Failed to load model: {e}"
    
    def load_reranker(self, reranker_name: str) -> str:
        """Load reranker model"""
        try:
            self.model_manager.load_reranker(reranker_name)
            return f"Reranker {reranker_name} loaded successfully"
        except Exception as e:
            return f"Failed to load reranker: {e}"
    
    def search(
        self, 
        query: str, 
        top_k: int = 30, 
        use_reranker: bool = True, 
        filter_by_collection: bool = False,
        ef_search: int = 100
    ) -> Optional[pd.DataFrame]:
        """Perform semantic search"""
        
        if not self._is_ready_for_search():
            logger.error("Search components not ready")
            return None
        
        try:
            # Preprocess query
            processed_query = self.query_processor.preprocess_query(
                query, self.model_manager.current_model_name
            )
            
            # Get query embedding
            query_embedding = self._get_query_embedding(processed_query)
            
            # Search FAISS index
            results = self._search_faiss_index(query_embedding, top_k, ef_search)
            
            if results is None or len(results) == 0:
                logger.info("No results found")
                return None
            
            # Apply collection filter if requested
            if filter_by_collection and self.filter_ids:
                results = self._apply_collection_filter(results)
            
            # Apply reranking if requested
            if use_reranker and self.model_manager.reranker is not None:
                results = self._apply_reranking(results, processed_query, top_k)
            
            self.last_results = results
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return None
    
    def _is_ready_for_search(self) -> bool:
        """Check if all components are ready for search"""
        return all([
            self.model_manager.current_model is not None,
            self.embeddings is not None,
            self.index is not None
        ])
    
    def _get_query_embedding(self, query: str) -> np.ndarray:
        """Get normalized query embedding"""
        query_embedding = self.model_manager.current_model.encode(query, convert_to_numpy=True)
        # Normalize
        query_embedding = query_embedding / np.linalg.norm(query_embedding)
        return query_embedding
    
    def _search_faiss_index(self, query_embedding: np.ndarray, top_k: int, ef_search: int) -> pd.DataFrame:
        """Search the FAISS index"""
        # Set search parameters
        if isinstance(self.index, faiss.IndexIDMap):
            hnsw_index = faiss.downcast_index(self.index.index)
            hnsw_index.hnsw.efSearch = ef_search
        
        # Perform search
        distances, indices = self.index.search(np.expand_dims(query_embedding, axis=0), top_k)
        
        if len(indices[0]) == 0:
            return pd.DataFrame()
        
        # Get results
        results = self.item_desc.iloc[indices[0]].copy().reset_index(drop=True)
        results['search_distance'] = distances[0]
        results['search_rank'] = range(len(results))
        
        return results
    
    def _apply_collection_filter(self, results: pd.DataFrame) -> pd.DataFrame:
        """Filter results by collection"""
        if 'scryfalloracleid' not in results.columns:
            logger.warning("Cannot filter by collection: scryfalloracleid column missing")
            return results
        
        filtered = results[results['scryfalloracleid'].isin(self.filter_ids)]
        logger.info(f"Collection filter: {len(results)} -> {len(filtered)} results")
        return filtered
    
    def _apply_reranking(self, results: pd.DataFrame, query: str, top_k: int) -> pd.DataFrame:
        """Apply reranking to results"""
        if len(results) == 0:
            return results
        
        # Get text for reranking (assuming there's a text column or use captions)
        if 'text' in results.columns:
            texts = results['text'].tolist()
        else:
            # Use captions based on original indices
            texts = [self.captions[i] for i in results.index]
        
        # Compute reranking scores
        query_text_pairs = [(query, text) for text in texts]
        scores = self.model_manager.reranker.compute_score(query_text_pairs)
        
        # Add scores and rerank
        results = results.copy()
        results['rerank_score'] = scores
        results = results.sort_values('rerank_score', ascending=False).head(top_k)
        
        logger.info("Applied reranking")
        return results
    
    def gradio_search(
        self, 
        query: str, 
        use_reranker: bool = True, 
        filter_by_collection: bool = False, 
        top_k: int = 30
    ) -> Tuple[List[Dict[str, Any]], str]:
        """Gradio-compatible search interface"""
        start_time = time.time()
        
        if not self._is_ready_for_search():
            return [], "No model loaded. Please load a model first."
        
        results = self.search(query, top_k, use_reranker, filter_by_collection)
        
        if results is None or len(results) == 0:
            return [], "No matches found."
        
        query_time = time.time() - start_time
        time_text = f"Query time: {query_time:.4f}s {'with' if use_reranker else 'without'} reranker"
        
        return results.to_dict('records'), time_text
    
    def get_single_embedding(self, text: str) -> np.ndarray:
        """Get embedding for a single text"""
        if self.model_manager.current_model is None:
            raise ValueError("No model loaded")
        return self.model_manager.current_model.encode(text, convert_to_numpy=True)
    
    def cleanup(self) -> None:
        """Clean up resources"""
        self.model_manager._cleanup_current_model()
        if hasattr(self.model_manager, 'reranker') and self.model_manager.reranker is not None:
            del self.model_manager.reranker
        gc.collect()
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        self.cleanup()