"""
Agentic RAG system using LangGraph.
Implements intelligent retrieval and answer generation workflow.
"""
from typing import TypedDict, List, Dict, Annotated
import operator
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode


class AgentState(TypedDict):
    """State for the agentic RAG workflow"""
    question: str
    choices: Dict[str, str]  # A, B, C, D -> choice text
    
    # Analysis
    question_type: str  # 'filename_specific', 'table_specific', 'content_specific'
    target_document: str  # Which document to search
    search_strategy: str  # 'semantic', 'keyword', 'hybrid'
    
    # Retrieval
    retrieved_chunks: List[Dict]
    relevant_chunks: List[Dict]
    
    # Answer generation
    answer: str
    selected_choices: List[str]  # e.g., ['A', 'C']
    confidence: float
    reasoning: str


class AgenticRAG:
    """Agentic RAG system with intelligent retrieval and reasoning"""
    
    def __init__(self, embedding_indexer, llm_api_base: str, llm_api_key: str,
                 llm_model_name: str, max_tokens: int = 2048, temperature: float = 0.1):
        self.indexer = embedding_indexer
        
        # Initialize LLM (vLLM server compatible with OpenAI API)
        self.llm = ChatOpenAI(
            base_url=llm_api_base,
            api_key=llm_api_key,
            model=llm_model_name,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyze_question", self._analyze_question)
        workflow.add_node("retrieve_chunks", self._retrieve_chunks)
        workflow.add_node("evaluate_relevance", self._evaluate_relevance)
        workflow.add_node("expand_context", self._expand_context)
        workflow.add_node("generate_answer", self._generate_answer)
        
        # Define edges
        workflow.set_entry_point("analyze_question")
        workflow.add_edge("analyze_question", "retrieve_chunks")
        workflow.add_edge("retrieve_chunks", "evaluate_relevance")
        workflow.add_conditional_edges(
            "evaluate_relevance",
            self._should_expand_context,
            {
                "expand": "expand_context",
                "generate": "generate_answer"
            }
        )
        workflow.add_edge("expand_context", "generate_answer")
        workflow.add_edge("generate_answer", END)
        
        return workflow.compile()
    
    def _analyze_question(self, state: AgentState) -> AgentState:
        """Analyze the question to determine search strategy"""
        question = state['question']
        
        # Create analysis prompt
        analysis_prompt = f"""Analyze this multiple-choice question and determine:
1. Question type: Does it mention a specific filename (e.g., "Public_628"), a table, or general content?
2. Target document: Which document filename should we search (if mentioned)?
3. Search strategy: Should we use 'semantic' (meaning-based), 'keyword' (exact matches), or 'hybrid'?

Question: {question}

Respond in JSON format:
{{
    "question_type": "filename_specific|table_specific|content_specific",
    "target_document": "Public_XXX or null",
    "search_strategy": "semantic|keyword|hybrid",
    "reasoning": "brief explanation"
}}"""
        
        messages = [SystemMessage(content="You are an expert at analyzing questions."),
                   HumanMessage(content=analysis_prompt)]
        
        response = self.llm.invoke(messages)
        
        # Parse response (simplified - in production, use proper JSON parsing)
        response_text = response.content
        
        # Extract information
        import json
        import re
        
        # Try to extract JSON
        json_match = re.search(r'\{[^}]+\}', response_text, re.DOTALL)
        if json_match:
            try:
                analysis = json.loads(json_match.group())
                state['question_type'] = analysis.get('question_type', 'content_specific')
                state['target_document'] = analysis.get('target_document', '')
                state['search_strategy'] = analysis.get('search_strategy', 'hybrid')
            except:
                # Fallback
                state['question_type'] = 'content_specific'
                state['target_document'] = ''
                state['search_strategy'] = 'hybrid'
        else:
            # Heuristic fallback
            if 'Public_' in question:
                state['question_type'] = 'filename_specific'
                # Extract filename
                match = re.search(r'Public_\d+', question)
                if match:
                    state['target_document'] = match.group()
                state['search_strategy'] = 'keyword'
            elif 'bảng' in question.lower() or 'table' in question.lower():
                state['question_type'] = 'table_specific'
                state['target_document'] = ''
                state['search_strategy'] = 'hybrid'
            else:
                state['question_type'] = 'content_specific'
                state['target_document'] = ''
                state['search_strategy'] = 'semantic'
        
        return state
    
    def _retrieve_chunks(self, state: AgentState) -> AgentState:
        """Retrieve relevant chunks based on analysis"""
        question = state['question']
        choices = state['choices']
        search_strategy = state['search_strategy']
        target_document = state['target_document']
        
        # Combine question and choices for better retrieval
        query_text = f"{question}\n\nChoices:\n"
        for key, value in choices.items():
            query_text += f"{key}. {value}\n"
        
        # Prepare filter
        filter_dict = {}
        if target_document:
            filter_dict['filename'] = target_document
        
        # Retrieve chunks
        retrieved = self.indexer.search(
            query_text=query_text,
            top_k=10,
            filter_dict=filter_dict if filter_dict else None
        )
        
        state['retrieved_chunks'] = retrieved
        
        return state
    
    def _evaluate_relevance(self, state: AgentState) -> AgentState:
        """Evaluate which chunks are truly relevant"""
        question = state['question']
        retrieved_chunks = state['retrieved_chunks']
        
        # Group chunks by document
        chunks_by_doc = {}
        for chunk in retrieved_chunks:
            filename = chunk['metadata']['filename']
            if filename not in chunks_by_doc:
                chunks_by_doc[filename] = []
            chunks_by_doc[filename].append(chunk)
        
        # If chunks are from multiple documents, keep only the most relevant document
        if len(chunks_by_doc) > 1:
            # Score documents by average chunk score
            doc_scores = {}
            for filename, chunks in chunks_by_doc.items():
                avg_score = sum(c['score'] for c in chunks) / len(chunks)
                doc_scores[filename] = avg_score
            
            # Keep only the top document
            best_doc = max(doc_scores.items(), key=lambda x: x[1])[0]
            relevant_chunks = chunks_by_doc[best_doc]
        else:
            relevant_chunks = retrieved_chunks
        
        # Filter by relevance threshold
        threshold = 0.3
        relevant_chunks = [c for c in relevant_chunks if c['score'] >= threshold]
        
        state['relevant_chunks'] = relevant_chunks[:5]  # Keep top 5
        
        return state
    
    def _should_expand_context(self, state: AgentState) -> str:
        """Decide whether to expand context for table chunks"""
        relevant_chunks = state['relevant_chunks']
        
        # Check if any chunk is a table
        has_table = any(c['metadata'].get('chunk_type') == 'table' for c in relevant_chunks)
        has_multipart_table = any(c['metadata'].get('is_multi_part_table', False) for c in relevant_chunks)
        
        if has_table and has_multipart_table:
            return "expand"
        return "generate"
    
    def _expand_context(self, state: AgentState) -> AgentState:
        """Expand context by retrieving adjacent chunks for tables"""
        relevant_chunks = state['relevant_chunks']
        expanded_chunks = []
        
        for chunk in relevant_chunks:
            expanded_chunks.append(chunk)
            
            # If it's a multi-part table, get adjacent parts
            if chunk['metadata'].get('is_multi_part_table', False):
                chunk_id = chunk['chunk_id']
                adjacent = self.indexer.get_adjacent_chunks(chunk_id, window=2)
                
                # Add adjacent chunks if they're from the same table
                for adj_chunk in adjacent:
                    if adj_chunk['metadata'].get('chunk_type') == 'table':
                        # Check if not already in expanded_chunks
                        if not any(ec['chunk_id'] == adj_chunk['chunk_id'] for ec in expanded_chunks):
                            expanded_chunks.append(adj_chunk)
        
        state['relevant_chunks'] = expanded_chunks
        
        return state
    
    def _generate_answer(self, state: AgentState) -> AgentState:
        """Generate answer based on retrieved context"""
        question = state['question']
        choices = state['choices']
        relevant_chunks = state['relevant_chunks']
        
        # Build context from chunks (use original HTML content)
        context_parts = []
        for idx, chunk in enumerate(relevant_chunks):
            context_parts.append(f"--- Context {idx + 1} ---")
            context_parts.append(f"Source: {chunk['metadata']['filename']}")
            if chunk['metadata'].get('table_title') != 'N/A':
                context_parts.append(f"Table: {chunk['metadata']['table_title']}")
            context_parts.append(f"Content:\n{chunk['content']}")
            context_parts.append("")
        
        context = "\n".join(context_parts)
        
        # Build choices text
        choices_text = "\n".join([f"{key}. {value}" for key, value in choices.items()])
        
        # Create prompt
        system_prompt = """You are an expert at answering multiple-choice questions based on technical documents.
Analyze the provided context carefully and select the correct answer(s).

IMPORTANT:
- The question may have one or more correct answers
- Base your answer ONLY on the provided context
- Provide your reasoning
- Format your response as JSON"""
        
        user_prompt = f"""Context:
{context}

Question:
{question}

Choices:
{choices_text}

Instructions:
1. Carefully read the context and question
2. Determine how many correct answers there are (1-4)
3. Select the correct choice(s) based on the context
4. Provide brief reasoning

Respond in JSON format:
{{
    "num_correct_answers": <number>,
    "selected_choices": ["A", "B", ...],
    "confidence": <0.0-1.0>,
    "reasoning": "brief explanation"
}}"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Parse response
        import json
        import re
        
        response_text = response.content
        
        # Try to extract JSON
        json_match = re.search(r'\{[^}]+\}', response_text, re.DOTALL)
        if json_match:
            try:
                answer_data = json.loads(json_match.group())
                state['selected_choices'] = answer_data.get('selected_choices', ['A'])
                state['confidence'] = answer_data.get('confidence', 0.5)
                state['reasoning'] = answer_data.get('reasoning', '')
                
                # Format answer for CSV
                num_correct = answer_data.get('num_correct_answers', len(state['selected_choices']))
                selected = ','.join(sorted(state['selected_choices']))
                state['answer'] = f"{num_correct},{selected}"
            except Exception as e:
                print(f"Error parsing JSON response: {e}")
                # Fallback
                state['selected_choices'] = ['A']
                state['confidence'] = 0.3
                state['reasoning'] = 'Parsing error'
                state['answer'] = "1,A"
        else:
            # Fallback - try to extract choices from text
            choices_found = []
            for choice in ['A', 'B', 'C', 'D']:
                if choice in response_text:
                    choices_found.append(choice)
            
            if choices_found:
                state['selected_choices'] = choices_found
                state['answer'] = f"{len(choices_found)},{','.join(sorted(choices_found))}"
            else:
                state['selected_choices'] = ['A']
                state['answer'] = "1,A"
            
            state['confidence'] = 0.3
            state['reasoning'] = 'Fallback parsing'
        
        return state
    
    def answer_question(self, question: str, choices: Dict[str, str]) -> Dict:
        """Answer a single question"""
        initial_state = {
            'question': question,
            'choices': choices,
            'question_type': '',
            'target_document': '',
            'search_strategy': '',
            'retrieved_chunks': [],
            'relevant_chunks': [],
            'answer': '',
            'selected_choices': [],
            'confidence': 0.0,
            'reasoning': ''
        }
        
        # Run the graph
        final_state = self.graph.invoke(initial_state)
        
        return {
            'answer': final_state['answer'],
            'selected_choices': final_state['selected_choices'],
            'confidence': final_state['confidence'],
            'reasoning': final_state['reasoning'],
            'question_type': final_state['question_type'],
            'search_strategy': final_state['search_strategy']
        }
