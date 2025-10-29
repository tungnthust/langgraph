#!/usr/bin/env python3
"""
System status checker for Agentic RAG.
Verifies all components are ready.
"""
import sys
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config.settings import *


def check_qdrant():
    """Check if Qdrant is running"""
    try:
        response = requests.get(f"http://{QDRANT_HOST}:{QDRANT_PORT}/health", timeout=5)
        if response.status_code == 200:
            print("✓ Qdrant: Running")
            return True
        else:
            print(f"✗ Qdrant: Unexpected status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Qdrant: Not accessible ({e})")
        print(f"  Start with: docker run -p 6333:6333 qdrant/qdrant")
        return False


def check_vllm():
    """Check if vLLM server is running"""
    try:
        response = requests.get(f"{LLM_API_BASE}/models", timeout=10)
        if response.status_code == 200:
            models = response.json()
            print(f"✓ vLLM: Running")
            if 'data' in models and models['data']:
                print(f"  Available models: {', '.join([m['id'] for m in models['data']])}")
            return True
        else:
            print(f"✗ vLLM: Unexpected status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ vLLM: Not accessible ({e})")
        print(f"  Start with: python -m vllm.entrypoints.openai.api_server --model {LLM_MODEL_NAME}")
        return False


def check_documents():
    """Check if documents exist"""
    docs = list(DOCUMENTS_DIR.glob(MD_FILE_PATTERN))
    if docs:
        print(f"✓ Documents: Found {len(docs)} files")
        for doc in docs:
            print(f"    - {doc.name}")
        return True
    else:
        print(f"✗ Documents: No files matching {MD_FILE_PATTERN} found in {DOCUMENTS_DIR}")
        return False


def check_questions():
    """Check if questions file exists"""
    if QUESTIONS_FILE.exists():
        import pandas as pd
        df = pd.read_csv(QUESTIONS_FILE)
        print(f"✓ Questions: Found {len(df)} questions in {QUESTIONS_FILE.name}")
        return True
    else:
        print(f"✗ Questions: File not found: {QUESTIONS_FILE}")
        return False


def check_qdrant_collection():
    """Check if Qdrant collection exists"""
    try:
        from qdrant_client import QdrantClient
        client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
        collections = client.get_collections().collections
        
        collection_exists = any(c.name == QDRANT_COLLECTION for c in collections)
        
        if collection_exists:
            collection_info = client.get_collection(QDRANT_COLLECTION)
            points_count = collection_info.points_count
            print(f"✓ Qdrant Collection: '{QDRANT_COLLECTION}' exists with {points_count} chunks")
            return True
        else:
            print(f"✗ Qdrant Collection: '{QDRANT_COLLECTION}' not found")
            print(f"  Run: python ingest_documents.py")
            return False
    except Exception as e:
        print(f"✗ Qdrant Collection: Error checking ({e})")
        return False


def check_python_packages():
    """Check if required packages are installed"""
    required_packages = [
        'langgraph',
        'langchain',
        'qdrant_client',
        'FlagEmbedding',
        'beautifulsoup4',
        'pandas',
        'openai'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if not missing:
        print(f"✓ Python Packages: All required packages installed")
        return True
    else:
        print(f"✗ Python Packages: Missing packages: {', '.join(missing)}")
        print(f"  Install with: pip install -r requirements.txt")
        return False


def main():
    """Run all checks"""
    print("=" * 80)
    print("AGENTIC RAG SYSTEM STATUS")
    print("=" * 80)
    print()
    
    checks = [
        ("Python Packages", check_python_packages),
        ("Qdrant Server", check_qdrant),
        ("vLLM Server", check_vllm),
        ("Documents", check_documents),
        ("Questions File", check_questions),
        ("Qdrant Collection", check_qdrant_collection),
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n[{name}]")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ {name}: Error during check ({e})")
            results.append((name, False))
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {name}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✓ System is ready!")
        print("\nNext steps:")
        if any(name == "Qdrant Collection" and not result for name, result in results):
            print("1. Run: python ingest_documents.py")
            print("2. Run: python answer_questions.py")
        else:
            print("1. Run: python answer_questions.py")
        return 0
    else:
        print("\n✗ System not ready. Please fix the failed checks above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
