"""
文本分块处理器
将长文本分割成适合向量化的小块
"""
import re
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class TextChunker:
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str) -> List[str]:
        """分割文本为块"""
        # 按句子分割
        sentences = re.split(r'[。！？；\n]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # 如果添加这个句子会超过chunk_size，先保存当前块
            if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                # 保留重叠部分
                overlap_text = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else current_chunk
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # 添加最后一个块
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def chunk_document(self, document: Dict) -> List[Dict]:
        """将文档分割成文本块"""
        content = document['content']
        chunks = self.split_text(content)
        
        chunk_docs = []
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) < 50:  # 跳过太短的块
                continue
                
            chunk_doc = {
                'id': f"{document['id']}_chunk_{i}",
                'content': chunk.strip(),
                'source_doc_id': document['id'],
                'source_filename': document['filename'],
                'chunk_index': i,
                'metadata': {
                    'source': document['source'],
                    'filename': document['filename'],
                    'chunk_size': len(chunk),
                    'total_chunks': len(chunks)
                }
            }
            chunk_docs.append(chunk_doc)
        
        logger.info(f"Document {document['id']} split into {len(chunk_docs)} chunks")
        return chunk_docs
    
    def chunk_all_documents(self, documents: List[Dict]) -> List[Dict]:
        """处理所有文档的分块"""
        all_chunks = []
        
        for doc in documents:
            chunks = self.chunk_document(doc)
            all_chunks.extend(chunks)
        
        logger.info(f"Generated {len(all_chunks)} text chunks in total")
        return all_chunks
    
    def create_chunk_reference(self, chunk: Dict) -> str:
        """为文本块创建引用信息"""
        return f"Document {chunk['source_filename']} Segment {chunk['chunk_index'] + 1}"