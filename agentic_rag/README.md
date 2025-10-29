# Agentic RAG System for Vietnamese Technical Documents

An intelligent Retrieval-Augmented Generation (RAG) system built with LangGraph for answering questions about Vietnamese technical documents with complex tables.

## Features

### Intelligent Document Processing
- **Smart Parsing**: Extracts metadata (filename, title, section headings)
- **HTML Table Handling**: Preserves table structure, extracts table titles
- **Intelligent Chunking**:
  - Text: Semantic chunking with heading hierarchy
  - Tables: Smart chunking that maintains headers and avoids splitting after colspan rows
  - Tracks chunk relationships for multi-part tables

### Advanced Embedding & Retrieval
- **BGE-M3 Embeddings**: Multilingual embeddings optimized for semantic search
- **Qdrant Vector Store**: High-performance vector database
- **Metadata-Rich Indexing**: Filename, document title, section, table title, chunk type, position
- **Dual Content Storage**: Embedded content (HTML removed) + original HTML content

### Agentic Workflow (LangGraph)
The agent intelligently:
1. **Analyzes Questions**: Determines question type and optimal search strategy
2. **Retrieval Strategy**: Chooses semantic, keyword, or hybrid search
3. **Document Filtering**: Focuses on single document (as questions are scoped to one document)
4. **Chunk Retrieval**: Retrieves relevant chunks based on strategy
5. **Relevance Evaluation**: Filters and ranks chunks
6. **Context Expansion**: For tables, retrieves adjacent chunks for complete context
7. **Answer Generation**: Uses LLM to generate answers based on context

### LLM Integration
- **vLLM Server**: Supports Qwen2.5-3B-Instruct with fp16
- **OpenAI-Compatible API**: Easy integration and swapping of models

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Document Ingestion                      │
│                                                             │
│  MD Files → Parser → Intelligent Chunks → Embedding        │
│               ↓           ↓                    ↓           │
│         Metadata   Tables/Text        BGE-M3 Vectors       │
│                           ↓                    ↓           │
│                      Qdrant Vector Store                   │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   Agentic RAG Workflow                      │
│                                                             │
│   Question → Analyze → Retrieve → Evaluate → Expand        │
│                ↓          ↓          ↓          ↓          │
│            Strategy   Qdrant    Filter    Adjacent Chunks  │
│                                   ↓                         │
│                            Generate Answer                  │
│                                   ↓                         │
│                          LLM (Qwen2.5-3B)                  │
└─────────────────────────────────────────────────────────────┘
```

## Project Structure

```
agentic_rag/
├── config/
│   └── settings.py          # Configuration settings
├── src/
│   ├── document_parser.py   # Intelligent document parsing and chunking
│   ├── embedding_indexer.py # BGE-M3 embedding and Qdrant indexing
│   └── agentic_rag.py       # LangGraph-based agentic RAG system
├── ingest_documents.py      # Document ingestion pipeline
├── answer_questions.py      # Question answering pipeline
└── requirements.txt         # Python dependencies
```

## Setup

### Prerequisites

1. **Python 3.9+**
2. **Qdrant** - Vector database
3. **vLLM Server** - LLM inference server

### Install Dependencies

```bash
cd agentic_rag
pip install -r requirements.txt
```

### Start Qdrant

Using Docker:
```bash
docker run -p 6333:6333 qdrant/qdrant
```

Or download and run locally from https://qdrant.tech/

### Start vLLM Server

```bash
# Install vLLM
pip install vllm

# Start server with Qwen2.5-3B-Instruct
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-3B-Instruct \
    --dtype half \
    --max-model-len 4096 \
    --port 8000
```

## Configuration

Edit `config/settings.py` to customize:

- **Qdrant settings**: Host, port, collection name
- **Embedding model**: Model name, batch size, device (CPU/GPU)
- **LLM settings**: Model, API endpoint, temperature
- **Chunking parameters**: Chunk sizes, overlap, table splitting
- **Retrieval settings**: Top-K, relevance threshold, context window

### Environment Variables

You can also use environment variables:

```bash
export QDRANT_HOST=localhost
export QDRANT_PORT=6333
export VLLM_API_BASE=http://localhost:8000/v1
export USE_GPU=true  # or false for CPU
```

## Usage

### 1. Ingest Documents

Parse and index markdown documents into Qdrant:

```bash
cd agentic_rag
python ingest_documents.py
```

This will:
- Find all `Public_*.md` files in the parent directory
- Parse them with intelligent chunking
- Generate BGE-M3 embeddings
- Index to Qdrant (overwrites existing collection)

### 2. Answer Questions

Process questions from CSV and generate answers:

```bash
python answer_questions.py
```

This will:
- Load questions from `question.csv`
- Use the agentic RAG workflow to answer each question
- Save answers to `answers.csv` in the format: `number_of_correct_answers,choices`

### Example Output Format (answers.csv)

```csv
1,A
2,"B,D"
1,D
3,"A,C,D"
```

## Key Features Explained

### Intelligent Table Chunking

Tables are chunked intelligently:
- Headers are preserved in each chunk
- Avoids splitting after rows with `colspan` (often section headers)
- Tracks multi-part tables with metadata
- Can retrieve adjacent parts for complete context

### Context Expansion

When a relevant chunk is part of a multi-part table:
1. The system detects this via metadata
2. Automatically retrieves adjacent chunks (before/after)
3. Provides complete table context to the LLM

### Document-Focused Retrieval

Since questions are scoped to single documents:
- System filters to most relevant document first
- Avoids mixing chunks from different documents
- Improves answer accuracy

### Adaptive Search Strategy

The agent analyzes each question to determine:
- **Keyword search**: For questions mentioning specific filenames
- **Semantic search**: For conceptual questions
- **Hybrid search**: For complex queries

## Troubleshooting

### "Model not found" error
- Ensure vLLM server is running
- Check that the model is downloaded: `huggingface-cli download Qwen/Qwen2.5-3B-Instruct`

### "Qdrant connection refused"
- Ensure Qdrant is running on the configured host/port
- Check firewall settings

### Out of memory
- Reduce `EMBEDDING_BATCH_SIZE` in settings
- Reduce `LLM_MAX_TOKENS`
- Use CPU instead of GPU for embeddings: `export USE_GPU=false`

### Slow processing
- Use GPU for embeddings if available
- Increase `EMBEDDING_BATCH_SIZE`
- Consider using a smaller embedding model

## Advanced Customization

### Using Different LLM Models

Edit `config/settings.py`:

```python
LLM_MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"  # Larger model
# or
LLM_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"
```

### Custom Chunking Strategy

Modify `src/document_parser.py`:
- Adjust `TEXT_CHUNK_SIZE` and `TEXT_CHUNK_OVERLAP`
- Customize table splitting logic in `_chunk_table()`

### Enhanced Metadata

Add custom metadata in `DocumentParser._create_text_chunk()` and `_create_table_chunk()`:

```python
metadata = {
    # ... existing metadata
    'custom_field': your_value,
}
```

## Research References

This system incorporates best practices from:
- LangGraph agentic patterns
- BGE-M3 multilingual embeddings
- Adaptive RAG techniques
- Corrective RAG (CRAG)
- Self-RAG approaches

## License

[Your License]

## Contributing

[Contribution guidelines]
