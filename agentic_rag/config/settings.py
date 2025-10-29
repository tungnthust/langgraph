"""
Configuration settings for Agentic RAG System
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT.parent
DOCUMENTS_DIR = DATA_DIR
QUESTIONS_FILE = DATA_DIR / "question.csv"
ANSWERS_FILE = DATA_DIR / "answers.csv"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

# Qdrant settings
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "vietnamese_technical_docs")
QDRANT_VECTOR_SIZE = 1024  # BGE-M3 embedding dimension

# Embedding model settings
EMBEDDING_MODEL_NAME = "BAAI/bge-m3"
EMBEDDING_BATCH_SIZE = 32
EMBEDDING_DEVICE = "cuda" if os.getenv("USE_GPU", "true").lower() == "true" else "cpu"

# Vietnamese NER model for keyword extraction
NER_MODEL_NAME = os.getenv("NER_MODEL_NAME", "NlpHUST/ner-vietnamese-electra-base")
NER_DEVICE = "cuda" if os.getenv("USE_GPU", "true").lower() == "true" else "cpu"
ENABLE_KEYWORD_EXTRACTION = os.getenv("ENABLE_KEYWORD_EXTRACTION", "true").lower() == "true"

# LLM settings (vLLM with Qwen2.5-3B-Instruct)
LLM_MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"
LLM_API_BASE = os.getenv("VLLM_API_BASE", "http://localhost:8000/v1")
LLM_API_KEY = os.getenv("VLLM_API_KEY", "EMPTY")
LLM_MAX_TOKENS = 2048
LLM_TEMPERATURE = 0.1

# Chunking settings
TEXT_CHUNK_SIZE = 512
TEXT_CHUNK_OVERLAP = 64
TABLE_MAX_ROWS_PER_CHUNK = 20
TABLE_MIN_ROWS_FOR_SPLIT = 25

# Retrieval settings
TOP_K_RETRIEVAL = 10
RELEVANCE_THRESHOLD = 0.3
CONTEXT_EXPANSION_WINDOW = 2  # Number of adjacent chunks to retrieve for tables

# Hybrid search settings
ENABLE_HYBRID_SEARCH = os.getenv("ENABLE_HYBRID_SEARCH", "true").lower() == "true"
SEMANTIC_WEIGHT = float(os.getenv("SEMANTIC_WEIGHT", "0.7"))  # Weight for semantic search
KEYWORD_WEIGHT = float(os.getenv("KEYWORD_WEIGHT", "0.3"))  # Weight for keyword search

# Document patterns
MD_FILE_PATTERN = "Public_*.md"
