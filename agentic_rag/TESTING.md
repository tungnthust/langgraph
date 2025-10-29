# Testing & Validation Guide

This guide covers testing procedures for the Agentic RAG system.

## Pre-Testing Checklist

Before running tests, ensure:

```bash
# 1. Check system status
python check_system.py

# 2. Verify all services are running
# - Qdrant (port 6333)
# - vLLM (port 8000)
```

## Test 1: Document Parsing

Test the document parser on sample files:

```python
# test_parser.py
from pathlib import Path
from src.document_parser import DocumentParser

# Initialize parser
parser = DocumentParser()

# Test on a document
doc_path = Path("../Public_475.md")
chunks = parser.parse_document(doc_path)

print(f"Generated {len(chunks)} chunks")

# Inspect chunks
for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- Chunk {i} ---")
    print(f"Type: {chunk.chunk_type}")
    print(f"Metadata: {chunk.metadata}")
    print(f"Content preview: {chunk.content[:100]}...")
```

**Expected Results:**
- Chunks generated without errors
- Metadata extracted correctly (filename, title)
- Tables and text separated properly
- Table titles identified

## Test 2: Embedding Generation

Test BGE-M3 embeddings:

```python
# test_embedding.py
from src.embedding_indexer import EmbeddingIndexer
from config.settings import *

indexer = EmbeddingIndexer(
    qdrant_host=QDRANT_HOST,
    qdrant_port=QDRANT_PORT,
    collection_name="test_collection",
    embedding_model_name=EMBEDDING_MODEL_NAME,
    vector_size=QDRANT_VECTOR_SIZE
)

# Test embedding
texts = [
    "Toyota Raize có giá bao nhiêu?",
    "What is the price of Toyota Raize?"
]

embeddings = indexer.embed_texts(texts)

print(f"Generated embeddings shape: {embeddings.shape}")
print(f"Embedding dimension: {embeddings.shape[1]}")

# Check similarity
from numpy import dot
from numpy.linalg import norm

similarity = dot(embeddings[0], embeddings[1]) / (norm(embeddings[0]) * norm(embeddings[1]))
print(f"Similarity between Vietnamese and English question: {similarity:.3f}")
```

**Expected Results:**
- Embedding shape: (2, 1024)
- Similarity > 0.7 (multilingual model should recognize similar questions)

## Test 3: Qdrant Indexing

Test document indexing:

```bash
# Run ingestion
python ingest_documents.py

# Analyze indexed data
python analyze_data.py
```

**Expected Results:**
- All documents processed without errors
- Chunks distributed across documents
- Both text and table chunks present
- Multi-part tables tracked correctly

## Test 4: Retrieval Quality

Test retrieval with known queries:

```python
# test_retrieval.py
from src.embedding_indexer import EmbeddingIndexer
from config.settings import *

indexer = EmbeddingIndexer(
    qdrant_host=QDRANT_HOST,
    qdrant_port=QDRANT_PORT,
    collection_name=QDRANT_COLLECTION,
    embedding_model_name=EMBEDDING_MODEL_NAME,
    vector_size=QDRANT_VECTOR_SIZE
)

# Test queries
test_queries = [
    "Giá xe Toyota Raize",
    "Kiến trúc ICT đô thị thông minh",
    "Máy X-quang kỹ thuật số"
]

for query in test_queries:
    print(f"\nQuery: {query}")
    results = indexer.search(query, top_k=3)
    
    for i, result in enumerate(results):
        print(f"  {i+1}. Score: {result['score']:.3f}")
        print(f"     Document: {result['metadata']['filename']}")
        print(f"     Type: {result['metadata']['chunk_type']}")
        if result['metadata']['chunk_type'] == 'table':
            print(f"     Table: {result['metadata']['table_title']}")
        print(f"     Preview: {result['content'][:100]}...")
```

**Expected Results:**
- Relevant documents retrieved for each query
- Scores > 0.5 for relevant results
- Correct document identified
- Table chunks retrieved for table-related queries

## Test 5: Context Expansion

Test adjacent chunk retrieval for tables:

```python
# test_context_expansion.py
from src.embedding_indexer import EmbeddingIndexer
from config.settings import *

indexer = EmbeddingIndexer(
    qdrant_host=QDRANT_HOST,
    qdrant_port=QDRANT_PORT,
    collection_name=QDRANT_COLLECTION,
    embedding_model_name=EMBEDDING_MODEL_NAME,
    vector_size=QDRANT_VECTOR_SIZE
)

# Find a multi-part table chunk
results = indexer.search("Bảng", top_k=20)

multi_part = None
for result in results:
    if result['metadata'].get('is_multi_part_table', False):
        multi_part = result
        break

if multi_part:
    chunk_id = multi_part['chunk_id']
    print(f"Found multi-part table: {chunk_id}")
    print(f"Part: {multi_part['metadata']['table_part_index'] + 1}/{multi_part['metadata']['table_total_parts']}")
    
    # Get adjacent chunks
    adjacent = indexer.get_adjacent_chunks(chunk_id, window=2)
    print(f"\nAdjacent chunks: {len(adjacent)}")
    
    for adj in adjacent:
        print(f"  - {adj['chunk_id']}")
        print(f"    Position: {adj['metadata']['chunk_position']}")
        print(f"    Type: {adj['metadata']['chunk_type']}")
```

**Expected Results:**
- Multi-part table chunks identified
- Adjacent chunks retrieved correctly
- Chunk positions in correct sequence

## Test 6: LLM Integration

Test vLLM server integration:

```python
# test_llm.py
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from config.settings import *

llm = ChatOpenAI(
    base_url=LLM_API_BASE,
    api_key=LLM_API_KEY,
    model=LLM_MODEL_NAME,
    max_tokens=512,
    temperature=0.1
)

# Test generation
message = HumanMessage(content="Hello! Can you help me answer a question?")
response = llm.invoke([message])

print(f"Response: {response.content}")
```

**Expected Results:**
- Connection successful
- Coherent response generated
- No errors or timeouts

## Test 7: End-to-End Demo

Run the demo script:

```bash
python demo.py
```

**Expected Results:**
- Question processed successfully
- Context retrieved from correct document
- Answer generated with reasoning
- Confidence score reasonable (> 0.5 for good answers)

## Test 8: Question Answering Pipeline

Test on a subset of questions:

```python
# test_qa_subset.py
import pandas as pd
from src.embedding_indexer import EmbeddingIndexer
from src.agentic_rag import AgenticRAG
from config.settings import *

# Load first 5 questions
questions_df = pd.read_csv(QUESTIONS_FILE).head(5)

# Initialize systems
indexer = EmbeddingIndexer(
    qdrant_host=QDRANT_HOST,
    qdrant_port=QDRANT_PORT,
    collection_name=QDRANT_COLLECTION,
    embedding_model_name=EMBEDDING_MODEL_NAME,
    vector_size=QDRANT_VECTOR_SIZE
)

rag = AgenticRAG(
    embedding_indexer=indexer,
    llm_api_base=LLM_API_BASE,
    llm_api_key=LLM_API_KEY,
    llm_model_name=LLM_MODEL_NAME
)

# Process questions
for idx, row in questions_df.iterrows():
    print(f"\n[Question {idx + 1}]")
    print(f"Q: {row['Question']}")
    
    choices = {k: row[k] for k in ['A', 'B', 'C', 'D']}
    
    result = rag.answer_question(row['Question'], choices)
    
    print(f"Answer: {result['answer']}")
    print(f"Confidence: {result['confidence']:.2f}")
```

**Expected Results:**
- All 5 questions answered without errors
- Reasonable answers generated
- Processing time < 10 seconds per question

## Performance Benchmarks

Track performance metrics:

```python
# benchmark.py
import time
import pandas as pd
from config.settings import *

def benchmark_ingestion():
    """Benchmark document ingestion"""
    start = time.time()
    # Run ingest_documents.py logic
    # ...
    duration = time.time() - start
    
    print(f"Ingestion time: {duration:.2f} seconds")
    return duration

def benchmark_qa(num_questions=10):
    """Benchmark question answering"""
    questions_df = pd.read_csv(QUESTIONS_FILE).head(num_questions)
    
    times = []
    for idx, row in questions_df.iterrows():
        start = time.time()
        # Run QA logic
        # ...
        times.append(time.time() - start)
    
    avg_time = sum(times) / len(times)
    print(f"Average QA time: {avg_time:.2f} seconds per question")
    print(f"Estimated total time for {len(questions_df)} questions: {avg_time * len(questions_df) / 60:.1f} minutes")
```

## Validation Checklist

Before considering the system production-ready:

- [ ] All documents parse without errors
- [ ] Embeddings generate correctly
- [ ] Qdrant collection populated
- [ ] Retrieval returns relevant results
- [ ] Context expansion works for tables
- [ ] LLM generates coherent answers
- [ ] Answer format correct (num,choices)
- [ ] Processing time acceptable
- [ ] Memory usage reasonable
- [ ] No crashes or exceptions

## Troubleshooting Tests

### If tests fail:

1. **Check logs**: Look for error messages
2. **Verify services**: Run `check_system.py`
3. **Check resources**: Monitor CPU/GPU/RAM usage
4. **Review configuration**: Verify `config/settings.py`
5. **Test components individually**: Isolate the failing component

### Common Issues:

**Parsing errors:**
- Check markdown file encoding (UTF-8)
- Verify HTML table structure
- Look for malformed tags

**Embedding errors:**
- Check GPU availability
- Reduce batch size
- Verify model download

**Retrieval errors:**
- Confirm Qdrant collection exists
- Check query format
- Verify vector dimensions match

**LLM errors:**
- Confirm vLLM server running
- Check API endpoint
- Verify model loaded

## Automated Testing

For continuous testing, create a test suite:

```bash
# run_tests.sh
#!/bin/bash

echo "Running test suite..."

python test_parser.py
python test_embedding.py
python test_retrieval.py
python test_llm.py
python demo.py

echo "All tests complete!"
```

Make it executable: `chmod +x run_tests.sh`

Run: `./run_tests.sh`

## Next Steps After Testing

Once all tests pass:

1. Run full ingestion: `python ingest_documents.py`
2. Process all questions: `python answer_questions.py`
3. Review answers in `answers.csv`
4. Fine-tune parameters if needed
5. Re-run on updated configuration

## Logging

Enable detailed logging for debugging:

```python
# Add to top of scripts
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

This will show detailed information about each step of the process.
