"""
PDF Document Processor
Responsible for extracting text content from PDF files
"""
import os
import re
from typing import List, Dict, Tuple
import pdfplumber
from PyPDF2 import PdfReader
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self, pdf_dir: str):
        self.pdf_dir = pdf_dir
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text
        except Exception as e:
            logger.error(f"Failed to extract PDF text {pdf_path}: {e}")
            return ""
    
    def get_pdf_files(self) -> List[str]:
        """Get all PDF file paths"""
        pdf_files = []
        for filename in os.listdir(self.pdf_dir):
            if filename.endswith('.pdf'):
                pdf_files.append(os.path.join(self.pdf_dir, filename))
        return sorted(pdf_files)
    
    def process_all_pdfs(self) -> List[Dict]:
        """Process all PDF files and return document information list"""
        documents = []
        pdf_files = self.get_pdf_files()
        
        logger.info(f"Found {len(pdf_files)} PDF files")
        
        for pdf_path in pdf_files:
            filename = os.path.basename(pdf_path)
            doc_id = filename.replace('.pdf', '')
            
            logger.info(f"Processing file: {filename}")
            
            text = self.extract_text_from_pdf(pdf_path)
            if text.strip():
                documents.append({
                    'id': doc_id,
                    'filename': filename,
                    'content': text,
                    'source': pdf_path
                })
                logger.info(f"Successfully extracted text, length: {len(text)} characters")
            else:
                logger.warning(f"File {filename} has no extracted text")
        
        return documents
    
    def clean_text(self, text: str) -> str:
        """Clean text content"""
        # Remove extra whitespace characters
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters
        text = re.sub(r'[^\w\s\u4e00-\u9fff.,!?;:()]', '', text)
        return text.strip()

