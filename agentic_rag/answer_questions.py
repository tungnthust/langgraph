"""
Question answering script using Agentic RAG.
Processes questions from CSV and generates answers.
"""
import sys
from pathlib import Path
import pandas as pd
from tqdm import tqdm

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import *
from src.embedding_indexer import EmbeddingIndexer
from src.agentic_rag import AgenticRAG


def load_questions(csv_path: Path) -> pd.DataFrame:
    """Load questions from CSV file"""
    df = pd.read_csv(csv_path)
    return df


def main():
    """Main question answering pipeline"""
    print("=" * 80)
    print("AGENTIC RAG - QUESTION ANSWERING PIPELINE")
    print("=" * 80)
    
    # Check if questions file exists
    if not QUESTIONS_FILE.exists():
        print(f"ERROR: Questions file not found: {QUESTIONS_FILE}")
        return
    
    # Load questions
    print(f"\nLoading questions from: {QUESTIONS_FILE}")
    questions_df = load_questions(QUESTIONS_FILE)
    print(f"Loaded {len(questions_df)} questions")
    
    # Initialize embedding indexer (for retrieval)
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
    
    # Initialize Agentic RAG system
    print("\nInitializing Agentic RAG system...")
    print(f"LLM: {LLM_MODEL_NAME}")
    print(f"API Base: {LLM_API_BASE}")
    
    rag_system = AgenticRAG(
        embedding_indexer=indexer,
        llm_api_base=LLM_API_BASE,
        llm_api_key=LLM_API_KEY,
        llm_model_name=LLM_MODEL_NAME,
        max_tokens=LLM_MAX_TOKENS,
        temperature=LLM_TEMPERATURE
    )
    
    # Process questions
    print("\nProcessing questions...")
    print("=" * 80)
    
    answers = []
    
    for idx, row in tqdm(questions_df.iterrows(), total=len(questions_df), desc="Answering questions"):
        question = row['Question']
        choices = {
            'A': row['A'],
            'B': row['B'],
            'C': row['C'],
            'D': row['D']
        }
        
        # Display question
        print(f"\n[Question {idx + 1}/{len(questions_df)}]")
        print(f"Q: {question}")
        for key, value in choices.items():
            print(f"  {key}. {value}")
        
        try:
            # Get answer from RAG system
            result = rag_system.answer_question(question, choices)
            
            answer = result['answer']
            answers.append(answer)
            
            print(f"Answer: {answer}")
            print(f"Reasoning: {result['reasoning']}")
            print(f"Confidence: {result['confidence']:.2f}")
            print(f"Strategy: {result['search_strategy']}")
            
        except Exception as e:
            print(f"ERROR processing question {idx + 1}: {e}")
            import traceback
            traceback.print_exc()
            
            # Fallback answer
            answers.append("1,A")
            print("Using fallback answer: 1,A")
    
    # Save answers to CSV
    print("\n" + "=" * 80)
    print("Saving answers...")
    
    # Create answers DataFrame
    answers_df = pd.DataFrame(answers, columns=['Answer'])
    
    # Split into two columns: number and choices
    answers_df[['Number', 'Choices']] = answers_df['Answer'].str.split(',', n=1, expand=True)
    answers_df = answers_df[['Number', 'Choices']]
    
    # Save without header
    answers_df.to_csv(ANSWERS_FILE, index=False, header=False)
    
    print(f"Answers saved to: {ANSWERS_FILE}")
    print("=" * 80)
    print("QUESTION ANSWERING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    main()
