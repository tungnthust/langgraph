# Architecture & Design Document

## System Overview

The Agentic RAG system is designed to answer multiple-choice questions about Vietnamese technical documents with complex tables. It uses LangGraph for agentic workflows, BGE-M3 for multilingual embeddings, and Qdrant for vector storage.

## Design Principles

1. **Intelligent Document Processing**: Preserve structure and context
2. **Agentic Reasoning**: Use LLM to analyze and strategize
3. **Metadata-Rich Indexing**: Enable precise filtering and retrieval
4. **Context Awareness**: Expand context for multi-part tables
5. **Modular Architecture**: Easy to customize and extend

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                              │
│  (ingest_documents.py, answer_questions.py, demo.py)               │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────────┐
│                    APPLICATION LAYER                                │
│                                                                     │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐ │
│  │ Document Parser  │  │  Agentic RAG     │  │ Embedding       │ │
│  │                  │  │  (LangGraph)     │  │ Indexer         │ │
│  │ - Parse MD      │  │                  │  │                 │ │
│  │ - Extract meta  │  │ - Analyze Q      │  │ - BGE-M3        │ │
│  │ - Chunk smart   │  │ - Retrieve       │  │ - Index/Search  │ │
│  │ - Track tables  │  │ - Evaluate       │  │ - Context exp.  │ │
│  └──────────────────┘  │ - Expand context │  └─────────────────┘ │
│                        │ - Generate ans.  │                       │
│                        └──────────────────┘                       │
└────────────────────────────┬────────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────────┐
│                     INFRASTRUCTURE LAYER                            │
│                                                                     │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐ │
│  │ Qdrant           │  │ vLLM Server      │  │ BGE-M3 Model    │ │
│  │ Vector Store     │  │ (Qwen2.5-3B)     │  │ (Local/GPU)     │ │
│  │                  │  │                  │  │                 │ │
│  │ - Store vectors  │  │ - LLM inference  │  │ - Embeddings    │ │
│  │ - Metadata idx   │  │ - OpenAI API     │  │ - Multilingual  │ │
│  │ - Similarity     │  │ - Fast inference │  │ - 1024 dims     │ │
│  └──────────────────┘  └──────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Ingestion Pipeline

```
Markdown Files
    │
    ├─> Document Parser
    │       │
    │       ├─> Extract Metadata (filename, title)
    │       │       │
    │       │       └─> Store in chunk metadata
    │       │
    │       ├─> Split into Elements
    │       │       │
    │       │       ├─> Text Sections
    │       │       │       │
    │       │       │       └─> Semantic Chunking
    │       │       │               │
    │       │       │               └─> Add heading context
    │       │       │
    │       │       └─> HTML Tables
    │       │               │
    │       │               ├─> Extract table title
    │       │               │
    │       │               └─> Smart Chunking
    │       │                       │
    │       │                       ├─> Preserve headers
    │       │                       ├─> Avoid colspan splits
    │       │                       └─> Track relationships
    │       │
    │       └─> Generate Chunks
    │               │
    │               ├─> Original Content (HTML)
    │               ├─> Embedding Content (clean)
    │               └─> Rich Metadata
    │
    └─> Embedding Indexer
            │
            ├─> Generate Embeddings (BGE-M3)
            │       │
            │       └─> Batch processing
            │
            └─> Index to Qdrant
                    │
                    └─> Store vectors + metadata
```

### Question Answering Pipeline

```
Question + Choices
    │
    └─> Agentic RAG Workflow (LangGraph)
            │
            ├─> Node 1: Analyze Question
            │       │
            │       ├─> Determine question type
            │       │   (filename-specific, table, content)
            │       │
            │       ├─> Extract target document
            │       │
            │       └─> Select search strategy
            │           (semantic, keyword, hybrid)
            │
            ├─> Node 2: Retrieve Chunks
            │       │
            │       ├─> Build query (Q + choices)
            │       │
            │       ├─> Apply filters (document)
            │       │
            │       └─> Search Qdrant (top-K)
            │
            ├─> Node 3: Evaluate Relevance
            │       │
            │       ├─> Group by document
            │       │
            │       ├─> Filter multi-doc results
            │       │
            │       └─> Apply threshold
            │
            ├─> Node 4: Expand Context (conditional)
            │       │
            │       ├─> Detect multi-part tables
            │       │
            │       └─> Retrieve adjacent chunks
            │
            └─> Node 5: Generate Answer
                    │
                    ├─> Build context (original HTML)
                    │
                    ├─> Create prompt
                    │
                    ├─> Call LLM (vLLM)
                    │
                    └─> Parse response
                            │
                            └─> Format: "count,choices"
```

## Component Design

### 1. Document Parser

**Purpose**: Transform markdown documents into intelligent chunks

**Key Methods**:
- `parse_document()`: Main entry point
- `_chunk_text()`: Semantic text chunking with overlap
- `_chunk_table()`: Smart table chunking
- `_row_has_colspan()`: Detect section headers
- `_get_current_heading()`: Extract heading hierarchy

**Design Decisions**:
- **Preserve HTML**: Tables stored as HTML to maintain structure
- **Dual Content**: Original (HTML) + clean (for embedding)
- **Metadata First**: Rich metadata for filtering and context
- **Chunk Relationships**: Track table parts for expansion

### 2. Embedding Indexer

**Purpose**: Generate embeddings and manage Qdrant vector store

**Key Methods**:
- `initialize_collection()`: Create/overwrite collection
- `embed_texts()`: Generate BGE-M3 embeddings
- `index_documents()`: Batch index chunks
- `search()`: Semantic search with filters
- `get_adjacent_chunks()`: Context expansion

**Design Decisions**:
- **Batch Processing**: Efficient embedding generation
- **Metadata Indexing**: Full-text search capability
- **Flexible Filters**: Support document-level filtering
- **Adjacent Retrieval**: Context expansion for tables

### 3. Agentic RAG

**Purpose**: Intelligent question answering with reasoning

**Key Components**:
- **StateGraph**: LangGraph workflow
- **Analysis Node**: Question understanding
- **Retrieval Node**: Strategy-based search
- **Evaluation Node**: Relevance filtering
- **Expansion Node**: Context augmentation
- **Generation Node**: LLM-powered answering

**Design Decisions**:
- **Agentic Approach**: LLM decides strategy
- **Document Focus**: Single-document scope
- **Table Awareness**: Special handling for tables
- **Confidence Scoring**: Track answer quality

## Data Models

### DocumentChunk

```python
@dataclass
class DocumentChunk:
    content: str              # Original with HTML
    content_for_embedding: str  # Clean text
    metadata: Dict            # Rich metadata
    chunk_id: str            # Unique identifier
    chunk_type: str          # 'text' or 'table'
```

### Metadata Schema

**Text Chunk**:
```json
{
    "filename": "Public_XXX",
    "document_title": "...",
    "section_heading": "Level 1 > Level 2",
    "chunk_type": "text",
    "chunk_index_in_type": 0,
    "chunk_position": 5,
    "total_chunks": 20
}
```

**Table Chunk**:
```json
{
    "filename": "Public_XXX",
    "document_title": "...",
    "section_heading": "...",
    "table_title": "Bảng 3.2...",
    "chunk_type": "table",
    "is_multi_part_table": true,
    "table_part_index": 0,
    "table_total_parts": 3,
    "chunk_position": 8,
    "total_chunks": 20
}
```

### AgentState

```python
class AgentState(TypedDict):
    # Input
    question: str
    choices: Dict[str, str]
    
    # Analysis
    question_type: str
    target_document: str
    search_strategy: str
    
    # Retrieval
    retrieved_chunks: List[Dict]
    relevant_chunks: List[Dict]
    
    # Output
    answer: str
    selected_choices: List[str]
    confidence: float
    reasoning: str
```

## Configuration

### Key Parameters

**Chunking**:
- `TEXT_CHUNK_SIZE`: 512 tokens (balance context/precision)
- `TEXT_CHUNK_OVERLAP`: 64 tokens (maintain continuity)
- `TABLE_MAX_ROWS_PER_CHUNK`: 20 rows (readable table size)

**Retrieval**:
- `TOP_K_RETRIEVAL`: 10 chunks (broad initial retrieval)
- `RELEVANCE_THRESHOLD`: 0.3 (inclusive filtering)
- `CONTEXT_EXPANSION_WINDOW`: 2 chunks (local context)

**Models**:
- `EMBEDDING_MODEL_NAME`: "BAAI/bge-m3" (multilingual)
- `LLM_MODEL_NAME`: "Qwen/Qwen2.5-3B-Instruct" (Vietnamese support)

## Performance Optimization

### Ingestion
- **Batch Embeddings**: Process 32 texts at once
- **Parallel Processing**: Could parallelize document parsing
- **Efficient Storage**: Store only necessary data

### Retrieval
- **Document Filtering**: Reduce search space
- **Relevance Threshold**: Filter early
- **Metadata Indexing**: Fast filtering by metadata

### Generation
- **Context Pruning**: Only relevant chunks
- **Prompt Optimization**: Concise instructions
- **Caching**: Could cache embeddings

## Scalability

### Horizontal Scaling
- **Document Processing**: Parallel parsing
- **Embedding Generation**: Multiple GPUs
- **Qdrant**: Distributed deployment

### Vertical Scaling
- **Batch Size**: Increase with more RAM/GPU
- **Model Size**: Use larger models with more VRAM
- **Context Window**: Expand with more powerful LLMs

## Security Considerations

1. **Input Validation**: Sanitize file paths
2. **API Keys**: Use environment variables
3. **Resource Limits**: Prevent DoS via large inputs
4. **Data Privacy**: Keep documents local

## Testing Strategy

1. **Unit Tests**: Each component independently
2. **Integration Tests**: End-to-end workflows
3. **Performance Tests**: Benchmarking
4. **Regression Tests**: Ensure consistency

## Future Enhancements

### Short Term
- [ ] Add logging system
- [ ] Implement caching
- [ ] Add progress bars
- [ ] Error recovery

### Medium Term
- [ ] Support more document formats (PDF, DOCX)
- [ ] Add evaluation metrics
- [ ] Implement A/B testing
- [ ] Add web interface

### Long Term
- [ ] Multi-document reasoning
- [ ] Fine-tuned embeddings
- [ ] Custom LLM fine-tuning
- [ ] Real-time updates

## Maintenance

### Regular Tasks
- Update embedding model
- Update LLM model
- Re-index documents if schema changes
- Monitor performance metrics

### Monitoring
- Track answer accuracy
- Monitor processing time
- Check resource usage
- Review error rates

## Conclusion

The Agentic RAG system is designed for:
- **Accuracy**: Intelligent retrieval and reasoning
- **Flexibility**: Easy to customize and extend
- **Performance**: Optimized for speed and efficiency
- **Maintainability**: Modular, well-documented code

The architecture supports both immediate use and future enhancements, making it suitable for production deployment and ongoing development.
