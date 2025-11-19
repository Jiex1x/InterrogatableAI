import streamlit as st
from rag_system import RAGSystem

st.set_page_config(
    page_title="PDF Intelligent Q&A System",
    page_icon="📚",
    layout="wide"
)

if "rag_system" not in st.session_state:
    st.session_state.rag_system = RAGSystem()
    with st.spinner("Initializing system..."):
        st.session_state.rag_system.build_knowledge_base()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("📚 PDF Intelligent Q&A System")
st.caption("Academic Document Q&A Assistant based on RAG Technology")

with st.sidebar:
    st.header("System Information")
    info = st.session_state.rag_system.get_system_info()
    st.metric("Document Count", info['vector_db']['document_count'])
    st.metric("LLM Configuration", "Configured" if info['llm_configured'] else "Not Configured")
    
    if st.button("Rebuild Knowledge Base"):
        with st.spinner("Rebuilding knowledge base..."):
            st.session_state.rag_system.build_knowledge_base(force_rebuild=True)
        st.success("Knowledge base rebuild completed!")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        if message["role"] == "assistant" and "sources" in message and message["sources"]:
            with st.expander("Reference Sources"):
                for source in message["sources"]:
                    st.write(f"**{source['filename']}** - Segment {source['chunk_index'] + 1}")
                    st.caption(f"Similarity: {source['similarity']:.3f}")
                    st.text(source['content_preview'])

if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.rag_system.ask_question(prompt)
            
            if response['success']:
                st.markdown(response['answer'])
                
                if response['sources']:
                    with st.expander("Reference Sources"):
                        for source in response['sources']:
                            st.write(f"**{source['filename']}** - Segment {source['chunk_index'] + 1}")
                            st.caption(f"Similarity: {source['similarity']:.3f}")
                            st.text(source['content_preview'])
                
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response['answer'],
                    "sources": response['sources']
                })
            else:
                error_msg = f"Error: {response['answer']}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })