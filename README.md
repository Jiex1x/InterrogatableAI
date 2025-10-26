# PDF Intelligent Q&A System

An intelligent PDF document Q&A system based on RAG (Retrieval-Augmented Generation) technology

## Features

- 📚 **PDF Document Processing**: Automatically parse PDF files and extract text content
- 🔍 **Intelligent Retrieval**: Document fragment retrieval based on semantic similarity
- 🤖 **Accurate Answers**: Generate precise answers based on retrieved document content
- 📖 **Source Citations**: Provide accurate document sources and paragraph references
- 🚫 **Rejection Mechanism**: Refuse to answer when no relevant information is available
- 💬 **Terminal Interface**: User-friendly command-line chat interface

## System Architecture

```
PDF Documents → Text Extraction → Chunking → Vectorization → Vector Database
                                                                    ↓
User Questions → Vector Retrieval → Relevant Document Fragments → LLM Generation → Precise Citations → Answers
```

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the environment variables configuration file:
```bash
cp env_example.txt .env
```

2. Edit the `.env` file to configure LLM API:
```env
OPENAI_API_KEY=your_openai_api_key_here
LLM_BASE_URL=https://api.openai.com/v1
```

## Usage

### Start the Chatbot

```bash
python chatbot.py
```

### Available Commands

- `/help` - Show help information
- `/info` - Display system information
- `/rebuild` - Rebuild the knowledge base
- `/quit` - Exit the program

### Direct Questioning

In the chat interface, simply input your questions. The system will:
1. Retrieve relevant document fragments
2. Generate answers based on retrieval results
3. Provide precise source citations

## System Components

### 1. PDF Processor (`pdf_processor.py`)
- Uses `pdfplumber` to extract PDF text
- Supports batch processing of multiple PDF files
- Text cleaning and preprocessing

### 2. Text Chunker (`text_chunker.py`)
- Intelligent text segmentation
- Configurable chunk size and overlap
- Maintains semantic integrity

### 3. Vector Database (`vector_store.py`)
- Uses ChromaDB for vector storage
- Supports semantic similarity search
- Persistent storage

### 4. LLM Client (`llm_client.py`)
- Supports multiple LLM APIs
- Intelligent context construction
- Precise source extraction

### 5. RAG System (`rag_system.py`)
- Integrates all components
- Provides complete Q&A workflow
- Intelligent relevance checking

## Configuration Options

In `config.py`, you can adjust:

- `CHUNK_SIZE`: Text chunk size (default: 512)
- `CHUNK_OVERLAP`: Chunk overlap (default: 50)
- `TOP_K_RESULTS`: Number of retrieval results (default: 5)
- `SIMILARITY_THRESHOLD`: Similarity threshold (default: 0.7)

## Tech Stack

- **PDF Processing**: PyPDF2, pdfplumber
- **Text Processing**: LangChain
- **Vectorization**: sentence-transformers
- **Vector Database**: ChromaDB
- **LLM Interface**: OpenAI API
- **Terminal Interface**: Rich

## Important Notes

1. Ensure PDF files are in the project root directory
2. The knowledge base will be built automatically on first run
3. A valid LLM API key is required
4. The system will automatically reject questions without relevant information

## Troubleshooting

### Common Issues

1. **PDF Extraction Failed**: Check if PDF files are corrupted
2. **LLM Call Failed**: Check API key and network connection
3. **Vector Database Error**: Delete the `vector_db` folder and rebuild

### Log Files

System operation logs are saved in the `chatbot.log` file, where you can view detailed error information.


