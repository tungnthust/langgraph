"""
Utility to analyze and inspect ingested documents in Qdrant.
"""
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent))

from config.settings import *
from qdrant_client import QdrantClient


def main():
    """Analyze ingested data"""
    print("=" * 80)
    print("AGENTIC RAG - DATA ANALYSIS")
    print("=" * 80)
    
    # Connect to Qdrant
    print(f"\nConnecting to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    
    # Check if collection exists
    collections = client.get_collections().collections
    if not any(c.name == QDRANT_COLLECTION for c in collections):
        print(f"\nCollection '{QDRANT_COLLECTION}' not found!")
        print("Run: python ingest_documents.py")
        return
    
    # Get collection info
    collection_info = client.get_collection(QDRANT_COLLECTION)
    total_chunks = collection_info.points_count
    
    print(f"\nCollection: {QDRANT_COLLECTION}")
    print(f"Total chunks: {total_chunks}")
    
    # Scroll through all points to gather statistics
    print("\nGathering statistics...")
    
    offset = None
    all_points = []
    
    while True:
        results, next_offset = client.scroll(
            collection_name=QDRANT_COLLECTION,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False
        )
        
        all_points.extend(results)
        
        if next_offset is None:
            break
        offset = next_offset
    
    print(f"Retrieved {len(all_points)} points")
    
    # Analyze by document
    docs_counter = Counter()
    chunk_types_counter = Counter()
    table_counter = Counter()
    multi_part_tables = 0
    
    for point in all_points:
        payload = point.payload
        
        filename = payload.get('filename', 'Unknown')
        docs_counter[filename] += 1
        
        chunk_type = payload.get('chunk_type', 'unknown')
        chunk_types_counter[chunk_type] += 1
        
        if chunk_type == 'table':
            table_counter[filename] += 1
            if payload.get('is_multi_part_table', False):
                multi_part_tables += 1
    
    # Display statistics
    print("\n" + "=" * 80)
    print("STATISTICS")
    print("=" * 80)
    
    print("\nChunks by Document:")
    for doc, count in sorted(docs_counter.items()):
        print(f"  {doc:20s} : {count:4d} chunks")
    
    print("\nChunks by Type:")
    for chunk_type, count in sorted(chunk_types_counter.items()):
        percentage = (count / total_chunks) * 100
        print(f"  {chunk_type:10s} : {count:4d} chunks ({percentage:.1f}%)")
    
    print("\nTable Chunks by Document:")
    for doc, count in sorted(table_counter.items()):
        print(f"  {doc:20s} : {count:4d} table chunks")
    
    print(f"\nMulti-part tables: {multi_part_tables}")
    
    # Sample chunks
    print("\n" + "=" * 80)
    print("SAMPLE CHUNKS")
    print("=" * 80)
    
    # Sample text chunk
    text_chunks = [p for p in all_points if p.payload.get('chunk_type') == 'text']
    if text_chunks:
        sample_text = text_chunks[0].payload
        print("\n[Sample Text Chunk]")
        print(f"Document: {sample_text.get('filename')}")
        print(f"Section: {sample_text.get('section_heading', 'N/A')}")
        print(f"Content preview: {sample_text.get('content_for_embedding', '')[:200]}...")
    
    # Sample table chunk
    table_chunks = [p for p in all_points if p.payload.get('chunk_type') == 'table']
    if table_chunks:
        sample_table = table_chunks[0].payload
        print("\n[Sample Table Chunk]")
        print(f"Document: {sample_table.get('filename')}")
        print(f"Table Title: {sample_table.get('table_title', 'N/A')}")
        print(f"Multi-part: {sample_table.get('is_multi_part_table', False)}")
        if sample_table.get('is_multi_part_table'):
            part = sample_table.get('table_part_index', 0)
            total = sample_table.get('table_total_parts', 0)
            print(f"Part: {part + 1}/{total}")
        print(f"Content preview (first 200 chars):")
        print(sample_table.get('content_for_embedding', '')[:200])
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
