"""
LLM客户端
负责与语言模型交互
"""
import openai
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, api_key: str, base_url: str, model: str):
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
        """生成回答"""
        
        # 构建上下文
        context_text = self._build_context(context_docs)
        
        # 构建提示词
        system_prompt = """You are a professional academic assistant that answers questions based on provided document content.

Rules:
1. Only answer based on the provided document content
2. If there is no relevant information in the documents, clearly state "Based on the provided documents, I cannot find relevant information to answer this question"
3. When answering, accurately cite sources in the format: According to [document name] segment X...
4. Maintain accuracy and objectivity in your answers
5. If information is incomplete, please state the limitations"""

        user_prompt = f"""Based on the following document content, answer the question:

Document Content:
{context_text}

Question: {query}

Please answer the question based on the above document content and accurately cite sources. If there is no relevant information in the documents, please clearly state so."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            answer = response.choices[0].message.content
            
            return {
                'answer': answer,
                'sources': self._extract_sources(context_docs),
                'context_used': len(context_docs),
                'success': True
            }
            
        except Exception as e:
            logger.error(f"LLM调用失败: {e}")
            return {
                'answer': f"抱歉，处理您的问题时出现错误: {str(e)}",
                'sources': [],
                'context_used': 0,
                'success': False
            }
    
    def _build_context(self, context_docs: List[Dict]) -> str:
        """构建上下文文本"""
        context_parts = []
        
        for i, doc in enumerate(context_docs, 1):
            source_info = f"[文档 {doc['metadata']['filename']} 第 {doc['metadata'].get('chunk_index', 0) + 1} 段]"
            context_parts.append(f"{source_info}\n{doc['content']}\n")
        
        return "\n".join(context_parts)
    
    def _extract_sources(self, context_docs: List[Dict]) -> List[Dict]:
        """提取来源信息"""
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
        """检查文档是否与问题相关"""
        if not context_docs:
            return False
        
        # 改进的相关性检查：降低阈值，提高匹配率
        max_similarity = max(doc.get('similarity', 0) for doc in context_docs)
        # 降低阈值到0.4，让更多文档被认为相关
        return max_similarity >= 0.4

