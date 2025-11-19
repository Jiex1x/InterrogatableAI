"""
System Test Script
Verify that all components are working properly
"""
import os
import sys
from pathlib import Path

def test_imports():
    """Test dependency imports"""
    print("🔍 Testing dependency imports...")
    
    try:
        import PyPDF2
        print("✅ PyPDF2 import successful")
    except ImportError as e:
        print(f"❌ PyPDF2 import failed: {e}")
        return False
    
    try:
        import pdfplumber
        print("✅ pdfplumber import successful")
    except ImportError as e:
        print(f"❌ pdfplumber import failed: {e}")
        return False
    
    try:
        import langchain
        print("✅ langchain import successful")
    except ImportError as e:
        print(f"❌ langchain import failed: {e}")
        return False
    
    try:
        import chromadb
        print("✅ chromadb import successful")
    except ImportError as e:
        print(f"❌ chromadb import failed: {e}")
        return False
    
    try:
        import sentence_transformers
        print("✅ sentence-transformers import successful")
    except ImportError as e:
        print(f"❌ sentence-transformers import failed: {e}")
        return False
    
    try:
        import openai
        print("✅ openai import successful")
    except ImportError as e:
        print(f"❌ openai import failed: {e}")
        return False
    
    try:
        import rich
        print("✅ rich import successful")
    except ImportError as e:
        print(f"❌ rich import failed: {e}")
        return False
    
    return True

def test_pdf_files():
    """Test PDF files"""
    print("\n📚 Checking PDF files...")
    
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    
    if not pdf_files:
        print("❌ No PDF files found")
        return False
    
    print(f"✅ Found {len(pdf_files)} PDF files")
    
    # Display first 5 files as examples
    for i, file in enumerate(pdf_files[:5]):
        print(f"  • {file}")
    
    if len(pdf_files) > 5:
        print(f"  ... and {len(pdf_files) - 5} more files")
    
    return True

def test_config():
    """Test configuration file"""
    print("\n⚙️ Checking configuration file...")
    
    if not os.path.exists('.env'):
        print("⚠️ .env file not found, will use default configuration")
        print("💡 It is recommended to create .env file and configure LLM API key")
        return True
    
    print("✅ Found .env configuration file")
    return True

def test_system_components():
    """Test system components"""
    print("\n🔧 Testing system components...")
    
    try:
        from pdf_processor import PDFProcessor
        print("✅ PDF processor import successful")
    except Exception as e:
        print(f"❌ PDF processor import failed: {e}")
        return False
    
    try:
        from text_chunker import TextChunker
        print("✅ Text chunker import successful")
    except Exception as e:
        print(f"❌ Text chunker import failed: {e}")
        return False
    
    try:
        from vector_store import VectorStore
        print("✅ Vector database import successful")
    except Exception as e:
        print(f"❌ Vector database import failed: {e}")
        return False
    
    try:
        from llm_client import LLMClient
        print("✅ LLM client import successful")
    except Exception as e:
        print(f"❌ LLM client import failed: {e}")
        return False
    
    try:
        from rag_system import RAGSystem
        print("✅ RAG system import successful")
    except Exception as e:
        print(f"❌ RAG system import failed: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🚀 Starting system tests...\n")
    
    tests = [
        ("Dependency Imports", test_imports),
        ("PDF Files", test_pdf_files),
        ("Configuration File", test_config),
        ("System Components", test_system_components)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Test: {test_name}")
        print('='*50)
        
        try:
            if test_func():
                print(f"✅ {test_name} test passed")
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test error: {e}")
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} passed")
    print('='*50)
    
    if passed == total:
        print("🎉 All tests passed! System is ready")
        print("\n💡 Next steps:")
        print("1. Configure .env file (if LLM functionality is needed)")
        print("2. Run: python chatbot.py")
    else:
        print("⚠️ Some tests failed, please check error messages")
    
    return passed == total

if __name__ == "__main__":
    main()
