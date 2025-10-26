"""
RAG系统配置文件
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # PDF文档路径
    PDF_DIR = "."
    
    # 向量数据库配置
    VECTOR_DB_PATH = "./vector_db"
    COLLECTION_NAME = "pdf_documents"
    
    # 文本分块配置
    CHUNK_SIZE = 512  # 每个文本块的大小
    CHUNK_OVERLAP = 50  # 文本块之间的重叠
    
    # 向量化模型
    EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    # LLM配置
    LLM_API_KEY = os.getenv("OPENAI_API_KEY")
    LLM_MODEL = "gpt-3.5-turbo"
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    
    # 检索配置
    TOP_K_RESULTS = 15  # 检索前K个最相关的文档片段 (增加检索数量，覆盖更多内容)
    SIMILARITY_THRESHOLD = 0.5  # 相似度阈值 (降低阈值，提高匹配率)
    
    # 回答配置
    MAX_TOKENS = 2000  # 增加token限制，避免回答被截断
    TEMPERATURE = 0.1

