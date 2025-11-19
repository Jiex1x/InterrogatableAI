"""
Text Chunking Processor
Splits long text into small chunks suitable for vectorization
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
        """Split text into chunks"""
        # Split by sentences
        sentences = re.split(r'[。！？；\n]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # If adding this sentence would exceed chunk_size, save current chunk first
            if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                # Keep overlap portion
                overlap_text = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else current_chunk
                current_chunk = overlap_text + " " + sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def chunk_document(self, document: Dict) -> List[Dict]:
        """Split document into text chunks"""
        content = document['content']
        chunks = self.split_text(content)
        
        chunk_docs = []
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) < 50:  # Skip chunks that are too short
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
        """Process chunking for all documents"""
        all_chunks = []
        
        for doc in documents:
            chunks = self.chunk_document(doc)
            all_chunks.extend(chunks)
        
        logger.info(f"Generated {len(all_chunks)} text chunks in total")
        return all_chunks
    
    def create_chunk_reference(self, chunk: Dict) -> str:
        """Create reference information for text chunk"""
        return f"Document {chunk['source_filename']} Segment {chunk['chunk_index'] + 1}"