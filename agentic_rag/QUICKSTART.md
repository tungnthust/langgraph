# Quick Start Guide for Agentic RAG System

This guide will help you get started quickly with the Agentic RAG system.

## Prerequisites Checklist

- [ ] Python 3.9 or higher installed
- [ ] GPU available (recommended but optional)
- [ ] At least 8GB RAM
- [ ] Internet connection for downloading models

## Step 1: Installation

```bash
cd agentic_rag

# Run setup script
./setup.sh

# Or manually:
pip install -r requirements.txt
```

## Step 2: Start Required Services

### Option A: Using Docker (Recommended)

```bash
# Terminal 1: Start Qdrant
docker run -d -p 6333:6333 --name qdrant qdrant/qdrant

# Terminal 2: Start vLLM (requires GPU)
docker run -d --gpus all \
    -p 8000:8000 \
    --name vllm \
    vllm/vllm-openai:latest \
    --model Qwen/Qwen2.5-3B-Instruct \
    --dtype half
```

### Option B: Manual Installation

#### Start Qdrant

**Using Docker:**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**Or download binary:**
- Visit https://qdrant.tech/documentation/quick-start/
- Download for your OS
- Run: `./qdrant`

#### Start vLLM Server

```bash
# Install vLLM
pip install vllm

# Start server (GPU)
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-3B-Instruct \
    --dtype half \
    --max-model-len 4096 \
    --port 8000

# Or for CPU (slower)
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-3B-Instruct \
    --dtype float32 \
    --max-model-len 2048 \
    --port 8000
```

**Note:** First run will download the model (~6GB). This may take a few minutes.

## Step 3: Verify Services

```bash
# Check Qdrant
curl http://localhost:6333/health

# Check vLLM
curl http://localhost:8000/v1/models
```

Both should return successful responses.

## Step 4: Ingest Documents

```bash
cd agentic_rag
python ingest_documents.py
```

Expected output:
```
Found 4 markdown documents:
  - Public_475.md
  - Public_584.md
  - Public_621.md
  - Public_632.md

Processing: Public_475.md
  Generated 12 chunks
    - Text chunks: 8
    - Table chunks: 4

...

Indexed 248 chunks to collection 'vietnamese_technical_docs'
```

This process may take 5-15 minutes depending on your hardware.

## Step 5: Test with Demo

```bash
python demo.py
```

This will run a sample question and show the complete workflow.

## Step 6: Answer All Questions

```bash
python answer_questions.py
```

This will:
- Load all questions from `../question.csv`
- Process each question through the agentic workflow
- Save answers to `../answers.csv`

Expected time: 15-30 minutes for ~287 questions (depending on hardware).

## Troubleshooting

### "Connection refused" for Qdrant
- Ensure Qdrant is running: `docker ps | grep qdrant`
- Check port 6333 is available: `netstat -an | grep 6333`

### "Model not found" error
- Wait for vLLM to finish downloading the model
- Check vLLM logs: `docker logs vllm` (if using Docker)
- Verify model endpoint: `curl http://localhost:8000/v1/models`

### Out of Memory
For systems with limited RAM/GPU:

1. **Reduce batch sizes** in `config/settings.py`:
   ```python
   EMBEDDING_BATCH_SIZE = 16  # from 32
   ```

2. **Use CPU for embeddings**:
   ```bash
   export USE_GPU=false
   ```

3. **Reduce LLM context**:
   ```python
   LLM_MAX_TOKENS = 1024  # from 2048
   ```

### Slow Performance

**For faster embedding:**
- Use GPU: `export USE_GPU=true`
- Increase batch size: `EMBEDDING_BATCH_SIZE = 64`

**For faster LLM inference:**
- Use quantized model (4-bit or 8-bit)
- Increase vLLM GPU memory fraction
- Use a smaller model (Qwen2.5-1.5B-Instruct)

## Configuration Tips

### Using a Different LLM

Edit `config/settings.py`:
```python
# For larger, more accurate model
LLM_MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"

# For faster inference
LLM_MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"

# For multilingual
LLM_MODEL_NAME = "google/gemma-2b-it"
```

### Adjusting Retrieval

```python
# More chunks for complex questions
TOP_K_RETRIEVAL = 15  # from 10

# Stricter relevance filtering
RELEVANCE_THRESHOLD = 0.5  # from 0.3

# Wider context for tables
CONTEXT_EXPANSION_WINDOW = 3  # from 2
```

### Custom Chunking

```python
# Larger chunks for better context
TEXT_CHUNK_SIZE = 1024  # from 512

# More overlap for continuity
TEXT_CHUNK_OVERLAP = 128  # from 64

# Smaller table chunks
TABLE_MAX_ROWS_PER_CHUNK = 15  # from 20
```

## Next Steps

1. **Review Results**: Check `answers.csv` for accuracy
2. **Fine-tune**: Adjust parameters based on performance
3. **Customize**: Modify the agentic workflow for your needs
4. **Scale**: Add more documents, improve chunking strategy
5. **Evaluate**: Compare answers with ground truth if available

## Monitoring Progress

While processing questions, you'll see:
```
[Question 1/287]
Q: Nếu một website bị vi phạm...
  A. Quản lý tài chính & tạo phiếu chi
  B. Công cụ quản lý & truy cập database
  C. Website – Đình chỉ website & quản lý thông tin khách hàng
  D. Cấu hình API & Tích hợp robots, sitemap
Answer: 1,C
Reasoning: Based on context about website management...
Confidence: 0.85
Strategy: semantic
```

## Getting Help

- Check `README.md` for detailed documentation
- Review error logs in console output
- Ensure all services are running: `docker ps`
- Verify configuration in `config/settings.py`

## Performance Benchmarks

Typical performance on different hardware:

| Component | CPU (8-core) | GPU (RTX 3090) |
|-----------|--------------|----------------|
| Ingestion | 15 min | 5 min |
| Per Question | 5-8 sec | 2-3 sec |
| Total (287 Q) | 30-40 min | 10-15 min |

## Summary of Commands

```bash
# Setup
cd agentic_rag
./setup.sh

# Start services
docker run -d -p 6333:6333 qdrant/qdrant
python -m vllm.entrypoints.openai.api_server --model Qwen/Qwen2.5-3B-Instruct --port 8000

# Run pipeline
python ingest_documents.py
python answer_questions.py

# Check results
cat ../answers.csv
```

Enjoy using the Agentic RAG system! 🚀
