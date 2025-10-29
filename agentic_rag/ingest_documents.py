"""
Document ingestion script.
Parses markdown documents, chunks them intelligently, and indexes to Qdrant.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import *
from src.document_parser import DocumentParser
from src.embedding_indexer import EmbeddingIndexer


def main():
    """Main ingestion pipeline"""
    print("=" * 80)
    print("AGENTIC RAG - DOCUMENT INGESTION PIPELINE")
    print("=" * 80)
    
    # Find all markdown documents
    md_files = list(DOCUMENTS_DIR.glob(MD_FILE_PATTERN))
    print(f"\nFound {len(md_files)} markdown documents:")
    for f in md_files:
        print(f"  - {f.name}")
    
    if not md_files:
        print("No markdown documents found!")
        return
    
    # Initialize parser
    print("\nInitializing document parser...")
    parser = DocumentParser(
        text_chunk_size=TEXT_CHUNK_SIZE,
        text_chunk_overlap=TEXT_CHUNK_OVERLAP,
        table_max_rows=TABLE_MAX_ROWS_PER_CHUNK,
        table_min_rows_for_split=TABLE_MIN_ROWS_FOR_SPLIT,
        enable_keyword_extraction=ENABLE_KEYWORD_EXTRACTION,
        ner_model_name=NER_MODEL_NAME,
        ner_device=NER_DEVICE
    )
    
    # Parse all documents
    print("\nParsing documents...")
    all_chunks = []
    for md_file in md_files:
        print(f"\nProcessing: {md_file.name}")
        try:
            chunks = parser.parse_document(md_file)
            print(f"  Generated {len(chunks)} chunks")
            
            # Show chunk type distribution
            text_chunks = sum(1 for c in chunks if c.chunk_type == 'text')
            table_chunks = sum(1 for c in chunks if c.chunk_type == 'table')
            print(f"    - Text chunks: {text_chunks}")
            print(f"    - Table chunks: {table_chunks}")
            
            all_chunks.extend(chunks)
        except Exception as e:
            print(f"  ERROR processing {md_file.name}: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\nTotal chunks generated: {len(all_chunks)}")
    
    # Initialize embedding indexer
    print("\nInitializing embedding and indexing system...")
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
    
    # Initialize collection (overwrite if exists)
    print("\nInitializing Qdrant collection...")
    indexer.initialize_collection(overwrite=True)
    
    # Index documents
    print("\nIndexing documents to Qdrant...")
    indexer.index_documents(all_chunks, show_progress=True)
    
    print("\n" + "=" * 80)
    print("INGESTION COMPLETE")
    print("=" * 80)
    print(f"Indexed {len(all_chunks)} chunks to collection '{QDRANT_COLLECTION}'")
    print("Ready for querying!")


if __name__ == "__main__":
    main()
