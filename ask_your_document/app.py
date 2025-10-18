import streamlit as st
import os
from dotenv import load_dotenv
from rag_pipeline import RAGPipeline

load_dotenv()

st.set_page_config(
    page_title="Ask Your Document",
    page_icon="📄",
    layout="wide"
)

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "rag_pipeline" not in st.session_state:
        st.session_state.rag_pipeline = None
    if "document_processed" not in st.session_state:
        st.session_state.document_processed = False
    if "last_query_data" not in st.session_state:
        st.session_state.last_query_data = None

def setup_rag_pipeline():
    """Initialize RAG pipeline with OpenAI API key."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        st.error("Please set your OPENAI_API_KEY in the .env file")
        st.stop()
    
    if st.session_state.rag_pipeline is None:
        st.session_state.rag_pipeline = RAGPipeline(openai_api_key)

def process_uploaded_file(uploaded_file):
    """Process uploaded text file and add to vector database."""
    if uploaded_file is not None:
        try:
            text = str(uploaded_file.read(), "utf-8")
            document_name = uploaded_file.name
            
            with st.spinner("Processing document..."):
                st.session_state.rag_pipeline.add_document(text, document_name)
                st.session_state.document_processed = True
                st.success(f"Document '{document_name}' processed successfully!")
                
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")

def display_chat_interface():
    """Display the chat interface."""
    st.subheader("💬 Chat with your document")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask a question about your document..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer, relevant_chunks = st.session_state.rag_pipeline.process_query(prompt)
                st.session_state.last_query_data = {
                    "query": prompt,
                    "answer": answer,
                    "chunks": relevant_chunks
                }
                st.markdown(answer)
        
        st.session_state.messages.append({"role": "assistant", "content": answer})

def display_validation_interface():
    """Display the validation interface."""
    st.subheader("🔍 Validation & Source Verification")
    
    if st.session_state.last_query_data is None:
        st.info("Ask a question in the Chat tab to see validation details here.")
        return
    
    query_data = st.session_state.last_query_data
    
    st.markdown("### Your Question")
    st.markdown(f"**{query_data['query']}**")
    
    st.markdown("### AI Answer")
    st.markdown(query_data['answer'])
    
    st.markdown("### Source Chunks Used")
    
    for i, chunk in enumerate(query_data['chunks'], 1):
        with st.expander(f"Chunk {i} (Similarity: {chunk['similarity_score']:.3f})"):
            st.markdown(f"**Document:** {chunk['metadata']['document_name']}")
            st.markdown(f"**Chunk Index:** {chunk['metadata']['chunk_index']}")
            st.markdown(f"**Similarity Score:** {chunk['similarity_score']:.3f}")
            st.markdown("**Content:**")
            st.markdown(chunk['text'])
    
    st.markdown("### Validation Instructions")
    st.info("""
    **How to validate the answer:**
    1. Check if the AI's answer is supported by the source chunks above
    2. Look for any information in the answer that doesn't appear in the chunks
    3. Verify that the answer doesn't contradict the source material
    4. If you find discrepancies, the answer may contain hallucinations
    """)

def main():
    """Main application function."""
    st.title("📄 Ask Your Document")
    st.markdown("Upload a text document and ask questions about its content with hallucination validation.")
    
    initialize_session_state()
    setup_rag_pipeline()
    
    tab1, tab2 = st.tabs(["💬 Chat", "🔍 Validation"])
    
    with tab1:
        st.markdown("### Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a text file (.txt)",
            type=['txt'],
            help="Upload a .txt file to start asking questions"
        )
        
        if uploaded_file is not None:
            process_uploaded_file(uploaded_file)
        
        if st.session_state.document_processed:
            display_chat_interface()
        else:
            st.info("Please upload a document first to start chatting.")
    
    with tab2:
        display_validation_interface()

if __name__ == "__main__":
    main()
