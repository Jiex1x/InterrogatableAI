"""
RAG System Configuration File
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # PDF document directory path
    PDF_DIR = "."
    
    # Vector database configuration
    VECTOR_DB_PATH = "./vector_db"
    COLLECTION_NAME = "pdf_documents"
    
    # Text chunking configuration
    CHUNK_SIZE = 512  # Size of each text chunk
    CHUNK_OVERLAP = 50  # Overlap between text chunks
    
    # Embedding model
    EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    # LLM configuration
    LLM_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM_MODEL = "gpt-3.5-turbo"
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    
    # Retrieval configuration
    TOP_K_RESULTS = 15  # Retrieve top K most relevant document segments (increase retrieval count to cover more content)
    SIMILARITY_THRESHOLD = 0.5  # Similarity threshold (lower threshold to increase match rate)
    
    # Response configuration
    MAX_TOKENS = 2000  # Increase token limit to avoid truncated responses
    TEMPERATURE = 0.1

