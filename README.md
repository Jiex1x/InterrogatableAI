# PDF智能问答系统

基于RAG（Retrieval-Augmented Generation）技术的PDF文档智能问答系统

## 功能特点

- 📚 **PDF文档处理**: 自动解析PDF文件，提取文本内容
- 🔍 **智能检索**: 基于语义相似度的文档片段检索
- 🤖 **精确回答**: 基于检索到的文档内容生成准确回答
- 📖 **来源引用**: 提供精确的文档来源和段落引用
- 🚫 **拒绝机制**: 当没有相关信息时拒绝回答
- 💬 **终端交互**: 友好的命令行聊天界面

## 系统架构

```
PDF文档 → 文本提取 → 分块处理 → 向量化 → 向量数据库
                                    ↓
用户问题 → 向量检索 → 相关文档片段 → LLM生成 → 精确引用 → 回答
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

1. 复制环境变量配置文件：
```bash
cp env_example.txt .env
```

2. 编辑 `.env` 文件，配置LLM API：
```env
OPENAI_API_KEY=your_openai_api_key_here
LLM_BASE_URL=https://api.openai.com/v1
```

## 使用方法

### 启动聊天机器人

```bash
python chatbot.py
```

### 可用命令

- `/help` - 显示帮助信息
- `/info` - 显示系统信息
- `/rebuild` - 重建知识库
- `/quit` - 退出程序

### 直接提问

在聊天界面中直接输入问题，系统会：
1. 检索相关文档片段
2. 基于检索结果生成回答
3. 提供精确的来源引用

## 系统组件

### 1. PDF处理器 (`pdf_processor.py`)
- 使用 `pdfplumber` 提取PDF文本
- 支持批量处理多个PDF文件
- 文本清理和预处理

### 2. 文本分块器 (`text_chunker.py`)
- 智能文本分割
- 可配置的分块大小和重叠
- 保持语义完整性

### 3. 向量数据库 (`vector_store.py`)
- 使用 ChromaDB 存储向量
- 支持语义相似度搜索
- 持久化存储

### 4. LLM客户端 (`llm_client.py`)
- 支持多种LLM API
- 智能上下文构建
- 精确来源提取

### 5. RAG系统 (`rag_system.py`)
- 整合所有组件
- 提供完整的问答流程
- 智能相关性检查

## 配置选项

在 `config.py` 中可以调整：

- `CHUNK_SIZE`: 文本分块大小 (默认: 512)
- `CHUNK_OVERLAP`: 分块重叠 (默认: 50)
- `TOP_K_RESULTS`: 检索结果数量 (默认: 5)
- `SIMILARITY_THRESHOLD`: 相似度阈值 (默认: 0.7)

## 技术栈

- **PDF处理**: PyPDF2, pdfplumber
- **文本处理**: LangChain
- **向量化**: sentence-transformers
- **向量数据库**: ChromaDB
- **LLM接口**: OpenAI API
- **终端界面**: Rich

## 注意事项

1. 确保PDF文件在项目根目录
2. 首次运行会自动构建知识库
3. 需要配置有效的LLM API密钥
4. 系统会自动拒绝没有相关信息的提问

## 故障排除

### 常见问题

1. **PDF提取失败**: 检查PDF文件是否损坏
2. **LLM调用失败**: 检查API密钥和网络连接
3. **向量数据库错误**: 删除 `vector_db` 文件夹重新构建

### 日志文件

系统运行日志保存在 `chatbot.log` 文件中，可以查看详细错误信息。


