"""
系统测试脚本
验证各个组件是否正常工作
"""
import os
import sys
from pathlib import Path

def test_imports():
    """测试依赖导入"""
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
    """测试PDF文件"""
    print("\n📚 检查PDF文件...")
    
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf')]
    
    if not pdf_files:
        print("❌ 没有找到PDF文件")
        return False
    
    print(f"✅ 找到 {len(pdf_files)} 个PDF文件")
    
    # 显示前5个文件作为示例
    for i, file in enumerate(pdf_files[:5]):
        print(f"  • {file}")
    
    if len(pdf_files) > 5:
        print(f"  ... 还有 {len(pdf_files) - 5} 个文件")
    
    return True

def test_config():
    """测试配置文件"""
    print("\n⚙️ 检查配置文件...")
    
    if not os.path.exists('.env'):
        print("⚠️ 未找到 .env 文件，将使用默认配置")
        print("💡 建议创建 .env 文件并配置LLM API密钥")
        return True
    
    print("✅ 找到 .env 配置文件")
    return True

def test_system_components():
    """测试系统组件"""
    print("\n🔧 测试系统组件...")
    
    try:
        from pdf_processor import PDFProcessor
        print("✅ PDF处理器导入成功")
    except Exception as e:
        print(f"❌ PDF处理器导入失败: {e}")
        return False
    
    try:
        from text_chunker import TextChunker
        print("✅ 文本分块器导入成功")
    except Exception as e:
        print(f"❌ 文本分块器导入失败: {e}")
        return False
    
    try:
        from vector_store import VectorStore
        print("✅ 向量数据库导入成功")
    except Exception as e:
        print(f"❌ 向量数据库导入失败: {e}")
        return False
    
    try:
        from llm_client import LLMClient
        print("✅ LLM客户端导入成功")
    except Exception as e:
        print(f"❌ LLM客户端导入失败: {e}")
        return False
    
    try:
        from rag_system import RAGSystem
        print("✅ RAG系统导入成功")
    except Exception as e:
        print(f"❌ RAG系统导入失败: {e}")
        return False
    
    return True

def main():
    """主测试函数"""
    print("🚀 开始系统测试...\n")
    
    tests = [
        ("依赖导入", test_imports),
        ("PDF文件", test_pdf_files),
        ("配置文件", test_config),
        ("系统组件", test_system_components)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"测试: {test_name}")
        print('='*50)
        
        try:
            if test_func():
                print(f"✅ {test_name} 测试通过")
                passed += 1
            else:
                print(f"❌ {test_name} 测试失败")
        except Exception as e:
            print(f"❌ {test_name} 测试出错: {e}")
    
    print(f"\n{'='*50}")
    print(f"测试结果: {passed}/{total} 通过")
    print('='*50)
    
    if passed == total:
        print("🎉 所有测试通过！系统准备就绪")
        print("\n💡 下一步:")
        print("1. 配置 .env 文件（如果需要LLM功能）")
        print("2. 运行: python chatbot.py")
    else:
        print("⚠️ 部分测试失败，请检查错误信息")
    
    return passed == total

if __name__ == "__main__":
    main()
