"""
LLM Client
Responsible for interacting with language models
"""
import openai
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, api_key: str, base_url: str, model: str):
        """
        Initialize OpenAI client
        According to OpenAI official documentation: https://platform.openai.com/docs/api-reference
        """
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
    
    def generate_response(self, 
                         query: str, 
                         context_docs: List[Dict], 
                         max_tokens: int = 1000,
                         temperature: float = 0.1) -> Dict:
        """Generate response"""
        
        # Build context
        context_text = self._build_context(context_docs)
        
        # Build prompts
        system_prompt = """You are a professional academic assistant that answers questions based on provided document content.

Rules:
1. Only answer based on the provided document content
2. If there is no relevant information in the documents, clearly state "Based on the provided documents, I cannot find relevant information to answer this question"
3. When answering, cite sources using the exact format provided: "According to [Source X: filename, Chunk Y, Similarity: Z]..."
4. Provide comprehensive and detailed answers with all relevant information from the documents
5. Include specific details like numbers, measurements, gene names, and other technical information
6. Maintain accuracy and objectivity in your answers
7. If information is incomplete, please state the limitations"""

        user_prompt = f"""Based on the following document content, answer the question comprehensively:

Document Content:
{context_text}

Question: {query}

Instructions:
1. Provide a detailed and comprehensive answer with all relevant technical details
2. Include specific numbers, measurements, gene names, and other technical information found in the documents
3. Cite sources using the exact format provided in the document content
4. Structure your answer clearly with proper paragraphs
5. Ensure your answer is complete and not truncated
6. If information is incomplete, mention what additional details would be needed"""

        try:
            # Call Chat Completions API according to OpenAI official documentation
            # Reference: https://platform.openai.com/docs/api-reference/chat/create
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            # Extract answer content
            answer = response.choices[0].message.content
            
            return {
                'answer': answer,
                'sources': self._extract_sources(context_docs),
                'context_used': len(context_docs),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            return {
                'answer': f"Sorry, an error occurred while processing your question: {str(e)}",
                'sources': [],
                'context_used': 0,
                'success': False
            }
    
    def _build_context(self, context_docs: List[Dict]) -> str:
        """Build context text"""
        context_parts = []
        
        for i, doc in enumerate(context_docs, 1):
            filename = doc['metadata']['filename']
            chunk_index = doc['metadata'].get('chunk_index', 0)
            similarity = doc.get('similarity', 0)
            
            # Improved citation format: includes filename, chunk index, and similarity
            source_info = f"[Source {i}: {filename}, Chunk {chunk_index + 1}, Similarity: {similarity:.2f}]"
            context_parts.append(f"{source_info}\n{doc['content']}\n")
        
        return "\n".join(context_parts)
    
    def _extract_sources(self, context_docs: List[Dict]) -> List[Dict]:
        """Extract source information"""
        sources = []
        
        for doc in context_docs:
            sources.append({
                'filename': doc['metadata']['filename'],
                'chunk_index': doc['metadata'].get('chunk_index', 0),
                'similarity': doc.get('similarity', 0),
                'content_preview': doc['content'][:100] + "..." if len(doc['content']) > 100 else doc['content']
            })
        
        return sources
    
    def check_relevance(self, query: str, context_docs: List[Dict]) -> bool:
        """Check if documents are relevant to the question"""
        if not context_docs:
            return False
        
        # Improved relevance check: lower threshold to increase match rate
        max_similarity = max(doc.get('similarity', 0) for doc in context_docs)
        # Lower threshold to 0.4 to allow more documents to be considered relevant
        return max_similarity >= 0.4

