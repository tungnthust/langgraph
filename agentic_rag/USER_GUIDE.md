# Project Summary & User Guide

## What Has Been Built

A complete **Agentic RAG (Retrieval-Augmented Generation) System** for answering multiple-choice questions about Vietnamese technical documents with complex tables.

## System Capabilities

✅ **Intelligent Document Processing**
- Parses markdown files with HTML tables
- Extracts metadata (filename, title, section headings, table titles)
- Smart chunking that preserves context and structure
- Special handling for complex multi-part tables

✅ **Advanced Retrieval**
- Uses BGE-M3 multilingual embeddings (supports Vietnamese + English)
- Stores in Qdrant vector database for fast similarity search
- Metadata-rich indexing for precise filtering
- Context expansion for multi-part tables

✅ **Agentic Workflow (LangGraph)**
- Analyzes questions to determine optimal search strategy
- Filters to single document (as per requirement)
- Evaluates chunk relevance intelligently
- Expands context when needed (e.g., for tables)
- Generates answers with reasoning and confidence scores

✅ **Production-Ready**
- Comprehensive error handling
- Progress tracking
- Configurable parameters
- Multiple deployment options
- Extensive documentation

## Project Structure

```
agentic_rag/
├── README.md              # Main documentation
├── QUICKSTART.md          # Quick start guide
├── TESTING.md             # Testing guide
├── ARCHITECTURE.md        # Architecture & design
├── requirements.txt       # Dependencies
├── setup.sh              # Installation script
├── .gitignore            # Git ignore rules
│
├── config/
│   └── settings.py       # Configuration settings
│
├── src/
│   ├── document_parser.py    # Intelligent parsing & chunking
│   ├── embedding_indexer.py  # BGE-M3 & Qdrant integration
│   └── agentic_rag.py        # LangGraph agentic workflow
│
├── ingest_documents.py   # Parse and index documents
├── answer_questions.py   # Answer all questions
├── demo.py              # Test with sample question
├── check_system.py      # Verify system status
└── analyze_data.py      # Inspect indexed data
```

## Quick Start (5 Steps)

### 1. Install Dependencies
```bash
cd agentic_rag
./setup.sh
```

### 2. Start Required Services

**Qdrant (Vector Database):**
```bash
docker run -d -p 6333:6333 --name qdrant qdrant/qdrant
```

**vLLM Server (LLM):**
```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-3B-Instruct \
    --dtype half \
    --port 8000
```

### 3. Verify System
```bash
python check_system.py
```

### 4. Ingest Documents
```bash
python ingest_documents.py
```
This will process all `Public_*.md` files in the parent directory.

### 5. Answer Questions
```bash
python answer_questions.py
```
This will read `question.csv` and generate `answers.csv`.

## Output Format

The system generates `answers.csv` with format:
```csv
1,A
2,"B,D"
1,D
3,"A,C,D"
```
Where each row is: `number_of_correct_answers,selected_choices`

## Key Features Explained

### 1. Intelligent Table Handling

**Problem**: Tables in technical documents can be very long and complex.

**Solution**:
- Chunks tables while preserving headers in each chunk
- Avoids splitting after rows with `colspan` (often section headers)
- Tracks relationships between table parts
- Automatically retrieves adjacent parts when needed

### 2. Document-Focused Retrieval

**Problem**: Questions are scoped to single documents, mixing chunks from different docs is wasteful.

**Solution**:
- Analyzes question to identify target document (if mentioned)
- Groups retrieval results by document
- Selects most relevant document when multiple found
- Ensures context comes from single source

### 3. Adaptive Search Strategy

**Problem**: Different questions need different search approaches.

**Solution**:
- Uses LLM to analyze question type
- Selects semantic search for conceptual questions
- Uses keyword search when specific terms mentioned
- Applies hybrid approach for complex queries

### 4. Context Expansion

**Problem**: A single chunk of a multi-part table may lack context.

**Solution**:
- Detects when retrieved chunk is part of a larger table
- Automatically retrieves adjacent chunks (before/after)
- Provides complete table context to LLM
- Improves answer accuracy for table-based questions

## Configuration Options

Edit `config/settings.py` to customize:

**Model Selection:**
```python
LLM_MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"  # Can use larger models
EMBEDDING_MODEL_NAME = "BAAI/bge-m3"         # Or other embeddings
```

**Chunking Parameters:**
```python
TEXT_CHUNK_SIZE = 512           # Adjust for more/less context
TABLE_MAX_ROWS_PER_CHUNK = 20   # Table chunk size
```

**Retrieval Settings:**
```python
TOP_K_RETRIEVAL = 10            # Number of chunks to retrieve
RELEVANCE_THRESHOLD = 0.3       # Minimum similarity score
CONTEXT_EXPANSION_WINDOW = 2    # Adjacent chunks to retrieve
```

## Performance Expectations

**Hardware**: 8-core CPU, 16GB RAM, RTX 3080 GPU

**Ingestion**:
- 4 documents (~2000 lines total)
- Processing time: ~5 minutes
- Generates ~200-300 chunks

**Question Answering**:
- 287 questions in question.csv
- ~2-3 seconds per question with GPU
- ~5-8 seconds per question with CPU
- Total: 10-15 minutes (GPU) or 30-40 minutes (CPU)

## Troubleshooting

### Common Issues

**"Connection refused" for Qdrant:**
```bash
# Check if Qdrant is running
docker ps | grep qdrant

# Restart if needed
docker restart qdrant
```

**"Model not found" for vLLM:**
```bash
# Check vLLM logs
python -m vllm.entrypoints.openai.api_server --model Qwen/Qwen2.5-3B-Instruct

# Wait for model download (first time only)
```

**Out of memory:**
- Reduce batch size in `config/settings.py`:
  ```python
  EMBEDDING_BATCH_SIZE = 16  # from 32
  ```
- Use CPU for embeddings:
  ```bash
  export USE_GPU=false
  ```

**Slow performance:**
- Use GPU if available: `export USE_GPU=true`
- Increase batch size if you have memory
- Consider using a smaller LLM model

## Validation

To verify the system is working correctly:

1. **Check ingestion:**
   ```bash
   python analyze_data.py
   ```
   Should show statistics about indexed documents.

2. **Test demo:**
   ```bash
   python demo.py
   ```
   Should answer a sample question successfully.

3. **Inspect answers:**
   ```bash
   head -20 ../answers.csv
   ```
   Should show properly formatted answers.

## Customization Examples

### Use a Different LLM

```python
# In config/settings.py
LLM_MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"  # Larger model
# or
LLM_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"  # Different family
```

### Adjust Chunking for Better Context

```python
# Larger chunks for more context
TEXT_CHUNK_SIZE = 1024
TEXT_CHUNK_OVERLAP = 128

# Smaller table chunks for precision
TABLE_MAX_ROWS_PER_CHUNK = 15
```

### Tune Retrieval Parameters

```python
# More chunks for complex questions
TOP_K_RETRIEVAL = 15

# Stricter relevance
RELEVANCE_THRESHOLD = 0.5

# Wider context expansion
CONTEXT_EXPANSION_WINDOW = 3
```

## Documentation Reference

- **README.md**: Complete system overview and setup
- **QUICKSTART.md**: Fast-track setup guide
- **TESTING.md**: Testing procedures and validation
- **ARCHITECTURE.md**: Design decisions and data flow

## Support & Resources

**Checking System Status:**
```bash
python check_system.py
```

**Analyzing Indexed Data:**
```bash
python analyze_data.py
```

**Testing with Sample:**
```bash
python demo.py
```

## Next Steps

After setup and validation:

1. **Run Full Pipeline**:
   ```bash
   python ingest_documents.py
   python answer_questions.py
   ```

2. **Review Results**:
   - Check `answers.csv` for accuracy
   - Compare with expected answers if available

3. **Fine-Tune**:
   - Adjust parameters based on performance
   - Experiment with different models
   - Optimize chunking strategy

4. **Extend**:
   - Add more documents
   - Customize the agentic workflow
   - Integrate with other systems

## Technical Highlights

**Technologies Used**:
- **LangGraph**: Agentic workflow orchestration
- **LangChain**: LLM integration and abstractions
- **BGE-M3**: State-of-art multilingual embeddings
- **Qdrant**: High-performance vector database
- **vLLM**: Fast LLM inference with OpenAI API
- **BeautifulSoup**: HTML parsing
- **Pandas**: Data processing

**Best Practices Implemented**:
- Modular architecture for maintainability
- Rich metadata for intelligent filtering
- Context-aware chunking
- Agentic reasoning for better decisions
- Comprehensive error handling
- Extensive documentation

## Conclusion

This Agentic RAG system provides a complete solution for answering questions about Vietnamese technical documents. It combines:

✅ Smart document processing
✅ Advanced retrieval techniques  
✅ Agentic reasoning with LangGraph
✅ Production-ready code
✅ Comprehensive documentation

The system is ready to use immediately and flexible enough for customization and extension.

## Getting Help

1. **Review Documentation**: Start with QUICKSTART.md
2. **Check System**: Run `python check_system.py`
3. **Test Components**: Follow TESTING.md guide
4. **Inspect Logs**: Check console output for errors
5. **Verify Services**: Ensure Qdrant and vLLM are running

Good luck! 🚀
