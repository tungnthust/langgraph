"""
Demo script to test the Agentic RAG system with a sample question.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config.settings import *
from src.embedding_indexer import EmbeddingIndexer
from src.agentic_rag import AgenticRAG


def main():
    """Run a demo query"""
    print("=" * 80)
    print("AGENTIC RAG - DEMO")
    print("=" * 80)
    
    # Sample question
    sample_question = "Giá bán lẻ niêm yết thấp nhất của Toyota Raize 2024 là bao nhiêu?"
    sample_choices = {
        'A': '510.000.000 đồng',
        'B': '498.000.000 đồng',
        'C': '506.000.000 đồng',
        'D': '500.000.000 đồng'
    }
    
    print("\nSample Question:")
    print(f"Q: {sample_question}")
    for key, value in sample_choices.items():
        print(f"  {key}. {value}")
    
    # Initialize systems
    print("\n" + "-" * 80)
    print("Initializing systems...")
    
    try:
        # Initialize indexer
        indexer = EmbeddingIndexer(
            qdrant_host=QDRANT_HOST,
            qdrant_port=QDRANT_PORT,
            collection_name=QDRANT_COLLECTION,
            embedding_model_name=EMBEDDING_MODEL_NAME,
            vector_size=QDRANT_VECTOR_SIZE,
            batch_size=EMBEDDING_BATCH_SIZE,
            device=EMBEDDING_DEVICE,
            semantic_weight=SEMANTIC_WEIGHT,
            keyword_weight=KEYWORD_WEIGHT
        )
        
        # Initialize RAG
        rag_system = AgenticRAG(
            embedding_indexer=indexer,
            llm_api_base=LLM_API_BASE,
            llm_api_key=LLM_API_KEY,
            llm_model_name=LLM_MODEL_NAME,
            max_tokens=LLM_MAX_TOKENS,
            temperature=LLM_TEMPERATURE
        )
        
        print("✓ Systems initialized")
        
        # Get answer
        print("\n" + "-" * 80)
        print("Processing question...")
        
        result = rag_system.answer_question(sample_question, sample_choices)
        
        print("\n" + "=" * 80)
        print("RESULT")
        print("=" * 80)
        print(f"Answer: {result['answer']}")
        print(f"Selected: {', '.join(result['selected_choices'])}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"\nReasoning: {result['reasoning']}")
        print(f"\nQuestion Type: {result['question_type']}")
        print(f"Search Strategy: {result['search_strategy']}")
        print("=" * 80)
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\nMake sure:")
        print("1. Qdrant is running (docker run -p 6333:6333 qdrant/qdrant)")
        print("2. vLLM server is running (python -m vllm.entrypoints.openai.api_server ...)")
        print("3. Documents have been ingested (python ingest_documents.py)")


if __name__ == "__main__":
    main()
