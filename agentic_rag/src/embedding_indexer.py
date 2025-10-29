"""
Embedding and indexing module for Qdrant vector store.
Uses BGE-M3 for multilingual embeddings.
"""
from typing import List, Dict, Optional
import numpy as np
from tqdm import tqdm
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue
)
from FlagEmbedding import BGEM3FlagModel


class EmbeddingIndexer:
    """Handle embedding generation and Qdrant indexing"""
    
    def __init__(self, qdrant_host: str, qdrant_port: int,
                 collection_name: str, embedding_model_name: str,
                 vector_size: int, batch_size: int = 32, device: str = "cuda"):
        self.qdrant_host = qdrant_host
        self.qdrant_port = qdrant_port
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.batch_size = batch_size
        
        print(f"Loading embedding model: {embedding_model_name}")
        # Load BGE-M3 model
        self.embedding_model = BGEM3FlagModel(
            embedding_model_name,
            use_fp16=True if device == "cuda" else False,
            device=device
        )
        
        print(f"Connecting to Qdrant at {qdrant_host}:{qdrant_port}")
        self.client = QdrantClient(host=qdrant_host, port=qdrant_port)
    
    def initialize_collection(self, overwrite: bool = True):
        """Initialize or recreate Qdrant collection"""
        # Check if collection exists
        collections = self.client.get_collections().collections
        collection_exists = any(c.name == self.collection_name for c in collections)
        
        if collection_exists:
            if overwrite:
                print(f"Deleting existing collection: {self.collection_name}")
                self.client.delete_collection(self.collection_name)
            else:
                print(f"Collection {self.collection_name} already exists")
                return
        
        print(f"Creating collection: {self.collection_name}")
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE
            )
        )
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts using BGE-M3"""
        embeddings = self.embedding_model.encode(
            texts,
            batch_size=self.batch_size,
            max_length=512
        )['dense_vecs']
        
        return np.array(embeddings)
    
    def index_documents(self, chunks: List, show_progress: bool = True):
        """Index document chunks into Qdrant"""
        print(f"Indexing {len(chunks)} chunks into Qdrant...")
        
        # Prepare texts for embedding
        texts = [chunk.content_for_embedding for chunk in chunks]
        
        # Generate embeddings in batches
        all_embeddings = []
        iterator = range(0, len(texts), self.batch_size)
        if show_progress:
            iterator = tqdm(iterator, desc="Generating embeddings")
        
        for i in iterator:
            batch_texts = texts[i:i + self.batch_size]
            batch_embeddings = self.embed_texts(batch_texts)
            all_embeddings.append(batch_embeddings)
        
        all_embeddings = np.vstack(all_embeddings)
        
        # Prepare points for Qdrant
        points = []
        for idx, (chunk, embedding) in enumerate(zip(chunks, all_embeddings)):
            # Prepare payload with metadata and original content
            payload = {
                'chunk_id': chunk.chunk_id,
                'content': chunk.content,  # Original content with HTML
                'content_for_embedding': chunk.content_for_embedding,
                **chunk.metadata
            }
            
            point = PointStruct(
                id=idx,
                vector=embedding.tolist(),
                payload=payload
            )
            points.append(point)
        
        # Upload to Qdrant in batches
        print("Uploading to Qdrant...")
        batch_size = 100
        for i in tqdm(range(0, len(points), batch_size), desc="Uploading batches"):
            batch_points = points[i:i + batch_size]
            self.client.upsert(
                collection_name=self.collection_name,
                points=batch_points
            )
        
        print(f"Successfully indexed {len(chunks)} chunks")
    
    def search(self, query_text: str, top_k: int = 10,
               filter_dict: Optional[Dict] = None) -> List[Dict]:
        """Search for similar chunks in Qdrant"""
        # Generate query embedding
        query_embedding = self.embed_texts([query_text])[0]
        
        # Prepare filter if provided
        query_filter = None
        if filter_dict:
            conditions = []
            for key, value in filter_dict.items():
                conditions.append(
                    FieldCondition(
                        key=key,
                        match=MatchValue(value=value)
                    )
                )
            query_filter = Filter(must=conditions)
        
        # Search
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding.tolist(),
            limit=top_k,
            query_filter=query_filter
        )
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                'score': result.score,
                'chunk_id': result.payload['chunk_id'],
                'content': result.payload['content'],
                'metadata': {k: v for k, v in result.payload.items() 
                           if k not in ['content', 'content_for_embedding', 'chunk_id']}
            })
        
        return formatted_results
    
    def get_chunk_by_id(self, chunk_id: str) -> Optional[Dict]:
        """Retrieve a specific chunk by its ID"""
        results = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="chunk_id",
                        match=MatchValue(value=chunk_id)
                    )
                ]
            ),
            limit=1
        )
        
        if results[0]:
            point = results[0][0]
            return {
                'chunk_id': point.payload['chunk_id'],
                'content': point.payload['content'],
                'metadata': {k: v for k, v in point.payload.items() 
                           if k not in ['content', 'content_for_embedding', 'chunk_id']}
            }
        return None
    
    def get_adjacent_chunks(self, chunk_id: str, window: int = 2) -> List[Dict]:
        """
        Get adjacent chunks for context expansion.
        Useful for retrieving surrounding chunks of a table.
        """
        # Get the current chunk
        current_chunk = self.get_chunk_by_id(chunk_id)
        if not current_chunk:
            return []
        
        metadata = current_chunk['metadata']
        filename = metadata['filename']
        chunk_position = metadata.get('chunk_position', 0)
        
        # Get chunks from the same document
        results = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="filename",
                        match=MatchValue(value=filename)
                    )
                ]
            ),
            limit=1000  # Assuming not more than 1000 chunks per document
        )
        
        # Filter and sort chunks by position
        document_chunks = []
        for point in results[0]:
            pos = point.payload.get('chunk_position', 0)
            document_chunks.append((pos, {
                'chunk_id': point.payload['chunk_id'],
                'content': point.payload['content'],
                'metadata': {k: v for k, v in point.payload.items() 
                           if k not in ['content', 'content_for_embedding', 'chunk_id']}
            }))
        
        document_chunks.sort(key=lambda x: x[0])
        
        # Find adjacent chunks
        adjacent = []
        for pos, chunk in document_chunks:
            if abs(pos - chunk_position) <= window and pos != chunk_position:
                adjacent.append(chunk)
        
        return adjacent
