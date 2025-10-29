#!/bin/bash
# Setup script for Agentic RAG System

set -e  # Exit on error

echo "=================================="
echo "Agentic RAG System - Setup"
echo "=================================="

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
required_version="3.9"

if (( $(echo "$python_version < $required_version" | bc -l) )); then
    echo "Error: Python $required_version+ is required. Found: $python_version"
    exit 1
fi

echo "✓ Python version: $python_version"

# Create virtual environment (optional but recommended)
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "=================================="
echo "Setup Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Start Qdrant vector database:"
echo "   docker run -p 6333:6333 qdrant/qdrant"
echo ""
echo "2. Start vLLM server with Qwen2.5-3B-Instruct:"
echo "   python -m vllm.entrypoints.openai.api_server \\"
echo "       --model Qwen/Qwen2.5-3B-Instruct \\"
echo "       --dtype half \\"
echo "       --max-model-len 4096 \\"
echo "       --port 8000"
echo ""
echo "3. Run document ingestion:"
echo "   python ingest_documents.py"
echo ""
echo "4. Answer questions:"
echo "   python answer_questions.py"
echo ""
