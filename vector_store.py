"""
向量数据库管理器
负责文档的向量化存储和检索
"""
import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, db_path: str, collection_name: str, embedding_model: str):
        self.db_path = db_path
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model
        
        # 初始化ChromaDB
        os.makedirs(db_path, exist_ok=True)
        self.client = chromadb.PersistentClient(
            path=db_path,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # 初始化嵌入模型
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # 获取或创建集合
        try:
            self.collection = self.client.get_collection(collection_name)
            logger.info(f"Using existing collection: {collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            logger.info(f"Created new collection: {collection_name}")
    
    def add_documents(self, chunks: List[Dict]):
        """将文档块添加到向量数据库"""
        if not chunks:
            logger.warning("No document chunks to add")
            return
        
        # 分批处理，避免批处理大小限制
        batch_size = 1000  # 每批处理1000个文档
        total_batches = (len(chunks) + batch_size - 1) // batch_size
        
        logger.info(f"Processing {len(chunks)} document chunks in batches, total {total_batches} batches")
        
        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i:i + batch_size]
            batch_num = i // batch_size + 1
            
            logger.info(f"Processing batch {batch_num}/{total_batches}, containing {len(batch_chunks)} document chunks")
            
            # 准备当前批次的数据
            ids = [chunk['id'] for chunk in batch_chunks]
            documents = [chunk['content'] for chunk in batch_chunks]
            metadatas = [chunk['metadata'] for chunk in batch_chunks]
            
            # 生成嵌入向量
            embeddings = self.embedding_model.encode(documents).tolist()
            
            # 添加到数据库
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )
            
            logger.info(f"Batch {batch_num} processing completed")
        
        logger.info(f"Successfully added {len(chunks)} document chunks to vector database")
    
    def search(self, query: str, top_k: int = 5, similarity_threshold: float = 0.7) -> List[Dict]:
        """搜索相关文档"""
        # 生成查询向量
        query_embedding = self.embedding_model.encode([query]).tolist()[0]
        
        # 执行搜索
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )
        
        # 处理结果
        search_results = []
        if results['documents'] and results['documents'][0]:
            for i, (doc, metadata, distance) in enumerate(zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            )):
                # 将距离转换为相似度分数
                similarity = 1 - distance
                
                if similarity >= similarity_threshold:
                    search_results.append({
                        'content': doc,
                        'metadata': metadata,
                        'similarity': similarity,
                        'rank': i + 1
                    })
        
        logger.info(f"Found {len(search_results)} relevant document segments")
        return search_results
    
    def get_collection_info(self) -> Dict:
        """获取集合信息"""
        count = self.collection.count()
        return {
            'collection_name': self.collection_name,
            'document_count': count,
            'embedding_model': self.embedding_model_name
        }
    
    def clear_collection(self):
        """清空集合"""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info("Collection cleared")

