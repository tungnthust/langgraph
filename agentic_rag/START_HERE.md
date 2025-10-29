# 🚀 START HERE - Agentic RAG System

## Welcome!

You've successfully cloned the Agentic RAG system for Vietnamese technical documents. This guide will get you up and running in minutes.

## 📋 What You Need

Before starting, make sure you have:

- [ ] **Python 3.9+** installed
- [ ] **Docker** (for Qdrant) OR ability to run Qdrant locally
- [ ] **8GB+ RAM** (16GB recommended)
- [ ] **GPU with 8GB+ VRAM** (optional but recommended)
- [ ] **10GB free disk space**
- [ ] **Internet connection** (for downloading models)

## 🎯 Quick Overview

This system:
1. **Parses** Vietnamese technical documents (markdown + HTML tables)
2. **Indexes** them into Qdrant vector database
3. **Answers** multiple-choice questions using agentic RAG
4. **Saves** results to answers.csv

## 📚 Choose Your Path

### 🏃 Path 1: Just Run It (Fastest)

If you just want to run the system quickly:

```bash
cd agentic_rag

# 1. Install (2 minutes)
./setup.sh

# 2. Start services (in separate terminals)
# Terminal 1:
docker run -p 6333:6333 qdrant/qdrant

# Terminal 2:
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-3B-Instruct --port 8000

# 3. Back in original terminal - verify
python check_system.py

# 4. Run pipeline (10-15 minutes)
python ingest_documents.py
python answer_questions.py

# 5. Check results
cat ../answers.csv
```

**→ See QUICKSTART.md for details**

### 📖 Path 2: Understand Then Run (Recommended)

If you want to understand the system first:

1. **Read** `USER_GUIDE.md` (10 min read)
   - Overview of what was built
   - Key features explained
   - Architecture overview

2. **Follow** `QUICKSTART.md` (5 min read)
   - Detailed setup steps
   - Service configuration
   - Troubleshooting

3. **Run** demo first
   ```bash
   python demo.py
   ```

4. **Then** run full pipeline

**→ Best for learning and customization**

### 🔬 Path 3: Deep Dive (For Developers)

If you want to understand everything:

1. **Start with** `PROJECT_SUMMARY.md`
   - Complete overview
   - By-the-numbers breakdown
   - All deliverables

2. **Read** `ARCHITECTURE.md`
   - System design
   - Data flow
   - Component details

3. **Study** `TESTING.md`
   - Validation procedures
   - Performance benchmarks
   - Testing strategy

4. **Explore** the code in `src/`

**→ Best for extending or modifying**

## 🎬 Your First Run

Let's do a simple test run:

```bash
# 1. Go to project directory
cd agentic_rag

# 2. Check if everything is installed
python check_system.py

# If all checks pass:
# ✓ Python Packages
# ✓ Qdrant Server
# ✓ vLLM Server
# ✓ Documents
# ✓ Questions File

# 3. Test with demo
python demo.py

# You should see:
# - Question displayed
# - System processing
# - Answer with reasoning
# - Confidence score
```

If this works, you're ready! 🎉

## 📊 What Happens Next

### During Ingestion (`ingest_documents.py`)

```
Finding documents...
  ✓ Found 4 files

Parsing documents...
  ✓ Public_475.md: 12 chunks
  ✓ Public_584.md: 85 chunks
  ✓ Public_621.md: 73 chunks
  ✓ Public_632.md: 78 chunks

Loading embeddings model...
  ✓ BGE-M3 loaded

Generating embeddings...
  [████████████████] 100%

Indexing to Qdrant...
  [████████████████] 100%

✓ Complete! 248 chunks indexed
```

**Time**: ~5 minutes

### During QA (`answer_questions.py`)

```
Loading questions...
  ✓ 287 questions loaded

Processing questions...
  [1/287] Q: Giá xe Toyota Raize...
  Answer: 1,B (Confidence: 0.85)
  
  [2/287] Q: Chức năng Website...
  Answer: 1,C (Confidence: 0.78)
  
  ...
  
  [287/287] Q: ...
  Answer: 2,"A,C" (Confidence: 0.92)

Saving answers...
  ✓ Saved to ../answers.csv

✓ Complete! All questions answered
```

**Time**: 10-15 minutes (GPU) or 30-40 minutes (CPU)

## 🎨 Example Output

**answers.csv format:**
```csv
1,A
2,"B,D"
1,D
3,"A,C,D"
```

Each row: `number_of_correct_answers,selected_choices`

## 🔍 Verify Your Results

```bash
# Check number of answers
wc -l ../answers.csv
# Should show: 287

# View first 10 answers
head -10 ../answers.csv

# Check for any errors
grep "ERROR" ../answers.csv
# Should be empty
```

## ⚙️ Common Adjustments

### If Out of Memory

Edit `config/settings.py`:
```python
EMBEDDING_BATCH_SIZE = 16  # reduce from 32
LLM_MAX_TOKENS = 1024      # reduce from 2048
```

### If Too Slow

```bash
# Use GPU for embeddings
export USE_GPU=true

# Or use smaller model
# Edit config/settings.py:
LLM_MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
```

### If Answers Seem Wrong

Adjust retrieval in `config/settings.py`:
```python
TOP_K_RETRIEVAL = 15           # increase from 10
RELEVANCE_THRESHOLD = 0.5      # increase from 0.3
CONTEXT_EXPANSION_WINDOW = 3   # increase from 2
```

## 📞 Need Help?

**Quick Checks:**
```bash
# System status
python check_system.py

# Data inspection
python analyze_data.py

# Test demo
python demo.py
```

**Documentation:**
- Stuck? → Check `QUICKSTART.md`
- Errors? → See `TESTING.md`
- Understanding? → Read `ARCHITECTURE.md`
- Overview? → Read `USER_GUIDE.md`

## 🎯 Success Checklist

- [ ] Installed dependencies
- [ ] Started Qdrant
- [ ] Started vLLM
- [ ] Ran `check_system.py` - all pass
- [ ] Ran `demo.py` - got answer
- [ ] Ran `ingest_documents.py` - indexed docs
- [ ] Ran `answer_questions.py` - generated answers
- [ ] Found `answers.csv` with 287 lines
- [ ] Spot-checked some answers

If all checked ✅, you're done! 🎉

## 🚀 Next Steps

1. **Validate Results**: Compare answers with expectations
2. **Experiment**: Try different configuration parameters
3. **Customize**: Modify the code for your needs
4. **Extend**: Add more documents or features
5. **Deploy**: Use in production if satisfied

## 📚 Full Documentation

- `README.md` - Complete system documentation
- `QUICKSTART.md` - Fast setup guide
- `USER_GUIDE.md` - Usage and examples
- `ARCHITECTURE.md` - Design and implementation
- `TESTING.md` - Testing and validation
- `PROJECT_SUMMARY.md` - Complete overview

## 💡 Pro Tips

1. **Start small**: Test with demo before full run
2. **Check logs**: Watch console output for errors
3. **Monitor resources**: Keep an eye on RAM/GPU usage
4. **Backup settings**: Keep copy of working `settings.py`
5. **Document changes**: Note any modifications you make

## 🎊 You're Ready!

The system is production-ready and fully documented. Choose your path above and get started!

Good luck! 🚀

---

**Questions?** Check the documentation in this directory.
**Issues?** Run `check_system.py` for diagnostics.
**Ready?** Start with `demo.py` for a quick test!
