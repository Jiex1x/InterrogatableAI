"""
RAG System Main Controller
Integrates all components to provide complete Q&A functionality
"""
import os
from typing import List, Dict, Optional
import logging

from config import Config
from pdf_processor import PDFProcessor
from text_chunker import TextChunker
from vector_store import VectorStore
from llm_client import LLMClient

logger = logging.getLogger(__name__)

class RAGSystem:
    def __init__(self):
        self.config = Config()
        
        # Initialize components
        self.pdf_processor = PDFProcessor(self.config.PDF_DIR)
        self.text_chunker = TextChunker(
            chunk_size=self.config.CHUNK_SIZE,
            chunk_overlap=self.config.CHUNK_OVERLAP
        )
        self.vector_store = VectorStore(
            db_path=self.config.VECTOR_DB_PATH,
            collection_name=self.config.COLLECTION_NAME,
            embedding_model=self.config.EMBEDDING_MODEL
        )
        
        # Initialize LLM client
        if self.config.LLM_API_KEY:
            self.llm_client = LLMClient(
                api_key=self.config.LLM_API_KEY,
                base_url=self.config.LLM_BASE_URL,
                model=self.config.LLM_MODEL
            )
        else:
            logger.warning("LLM API key not set, Q&A functionality will be unavailable")
            self.llm_client = None
    
    def build_knowledge_base(self, force_rebuild: bool = False):
        """Build knowledge base"""
        logger.info("Starting knowledge base construction...")
        
        # Check if rebuild is needed
        if not force_rebuild and self.vector_store.get_collection_info()['document_count'] > 0:
            logger.info("Knowledge base already exists, skipping construction")
            return
        
        # Clear existing data
        if force_rebuild:
            self.vector_store.clear_collection()
        
        # Process PDF documents
        logger.info("Processing PDF documents...")
        documents = self.pdf_processor.process_all_pdfs()
        
        if not documents:
            logger.error("No PDF documents found")
            return
        
        # Text chunking
        logger.info("Performing text chunking...")
        chunks = self.text_chunker.chunk_all_documents(documents)
        
        # Store to vector database
        logger.info("Storing to vector database...")
        self.vector_store.add_documents(chunks)
        
        logger.info("Knowledge base construction completed!")
    
    def ask_question(self, question: str) -> Dict:
        """Answer question"""
        if not self.llm_client:
            # Even without LLM, show retrieval results
            logger.info(f"Processing question: {question}")
            
            # Retrieve relevant documents
            search_results = self.vector_store.search(
                query=question,
                top_k=self.config.TOP_K_RESULTS,
                similarity_threshold=self.config.SIMILARITY_THRESHOLD
            )
            
            if not search_results:
                return {
                    'answer': 'Based on the provided documents, I cannot find relevant information to answer this question.',
                    'sources': [],
                    'success': True
                }
            
            # Build answer based on search results
            answer_parts = [f"Based on document retrieval, found {len(search_results)} relevant segments:\n"]
            
            for i, result in enumerate(search_results, 1):
                answer_parts.append(f"【Segment {i}】Similarity: {result['similarity']:.3f}")
                answer_parts.append(f"Source: {result['metadata']['filename']} Segment {result['metadata'].get('chunk_index', 0) + 1}")
                # Show full content without truncation
                answer_parts.append(f"Content: {result['content']}")
                answer_parts.append("")
            
            return {
                'answer': '\n'.join(answer_parts),
                'sources': [{
                    'filename': result['metadata']['filename'],
                    'chunk_index': result['metadata'].get('chunk_index', 0),
                    'similarity': result['similarity'],
                    'content_preview': result['content'][:300] + "..." if len(result['content']) > 300 else result['content']
                } for result in search_results],
                'success': True
            }
        
        logger.info(f"Processing question: {question}")
        
        # Retrieve relevant documents
        search_results = self.vector_store.search(
            query=question,
            top_k=self.config.TOP_K_RESULTS,
            similarity_threshold=self.config.SIMILARITY_THRESHOLD
        )
        
        if not search_results:
            return {
                'answer': 'Based on the provided documents, I cannot find relevant information to answer this question.',
                'sources': [],
                'success': True
            }
        
        # Check relevance
        if not self.llm_client.check_relevance(question, search_results):
            return {
                'answer': 'Based on the provided documents, I cannot find relevant information to answer this question.',
                'sources': [],
                'success': True
            }
        
        # Generate response
        response = self.llm_client.generate_response(
            query=question,
            context_docs=search_results,
            max_tokens=self.config.MAX_TOKENS,
            temperature=self.config.TEMPERATURE
        )
        
        return response
    
    def get_system_info(self) -> Dict:
        """Get system information"""
        vector_info = self.vector_store.get_collection_info()
        
        return {
            'vector_db': vector_info,
            'llm_configured': self.llm_client is not None,
            'config': {
                'chunk_size': self.config.CHUNK_SIZE,
                'top_k_results': self.config.TOP_K_RESULTS,
                'similarity_threshold': self.config.SIMILARITY_THRESHOLD
            }
        }

