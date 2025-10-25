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
        system_prompt = """你是一个专业的学术助手，基于提供的文档内容回答问题。
        
规则：
1. 只能基于提供的文档内容回答问题
2. 如果文档中没有相关信息，请明确说明"根据提供的文档，我无法找到相关信息来回答这个问题"
3. 回答时要准确引用来源，格式：根据[文档名]第X段的内容...
4. 保持回答的准确性和客观性
5. 如果信息不完整，请说明限制"""

        user_prompt = f"""基于以下文档内容回答问题：

文档内容：
{context_text}

问题：{query}

请基于上述文档内容回答问题，并准确引用来源。如果文档中没有相关信息，请明确说明。"""

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
        
        # 简单的相关性检查：如果最高相似度低于阈值，认为不相关
        max_similarity = max(doc.get('similarity', 0) for doc in context_docs)
        return max_similarity >= 0.6

