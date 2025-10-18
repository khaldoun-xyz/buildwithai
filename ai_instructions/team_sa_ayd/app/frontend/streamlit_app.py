import streamlit as st
import requests
import os
from typing import Dict, List

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def upload_document(file_content: bytes, filename: str) -> Dict:
    """Upload a document to the backend.
    
    Args:
        file_content: The file content as bytes.
        filename: The name of the file.
        
    Returns:
        Response from the backend API.
        
    Raises:
        requests.RequestException: If upload fails.
    """
    files = {"file": (filename, file_content, "text/plain")}
    response = requests.post(f"{BACKEND_URL}/upload", files=files)
    response.raise_for_status()
    return response.json()

def ask_question(question: str) -> Dict:
    """Send a question to the backend.
    
    Args:
        question: The question to ask.
        
    Returns:
        Response from the backend API.
        
    Raises:
        requests.RequestException: If request fails.
    """
    response = requests.post(
        f"{BACKEND_URL}/ask",
        json={"question": question}
    )
    response.raise_for_status()
    return response.json()

def get_backend_status() -> Dict:
    """Get the status of the backend.
    
    Returns:
        Status information from the backend.
        
    Raises:
        requests.RequestException: If request fails.
    """
    response = requests.get(f"{BACKEND_URL}/status")
    response.raise_for_status()
    return response.json()

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Ask Your Document",
        page_icon="📄",
        layout="wide"
    )
    
    st.title("📄 Ask Your Document")
    st.markdown("Upload a text document and ask questions about its content.")
    
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "document_uploaded" not in st.session_state:
        st.session_state.document_uploaded = False
    
    # Sidebar for document upload
    with st.sidebar:
        st.header("📁 Document Upload")
        
        uploaded_file = st.file_uploader(
            "Choose a text file",
            type=['txt'],
            help="Upload a .txt file to start asking questions"
        )
        
        if uploaded_file is not None:
            if st.button("Upload Document"):
                try:
                    with st.spinner("Uploading and processing document..."):
                        file_content = uploaded_file.read()
                        result = upload_document(file_content, uploaded_file.name)
                        
                        st.success(result["message"])
                        st.info(f"Document processed into {result['chunks_count']} chunks")
                        
                        # Clear previous messages when new document is uploaded
                        st.session_state.messages = []
                        st.session_state.document_uploaded = True
                        
                        # Refresh the page to show the new state
                        st.rerun()
                        
                except requests.RequestException as e:
                    st.error(f"Failed to upload document: {str(e)}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        
        # Show backend status
        try:
            status = get_backend_status()
            st.subheader("📊 Status")
            st.write(f"Chunks in memory: {status['chunks_count']}")
            st.write(f"Document loaded: {'Yes' if status['has_documents'] else 'No'}")
        except requests.RequestException:
            st.error("Backend is not available")
    
    # Main chat interface
    if not st.session_state.document_uploaded:
        st.info("👆 Please upload a document first using the sidebar.")
        
        # Check if backend has documents
        try:
            status = get_backend_status()
            if status['has_documents']:
                st.session_state.document_uploaded = True
                st.rerun()
        except requests.RequestException:
            pass
    else:
        st.subheader("💬 Chat with your document")
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show sources if available
                if message["role"] == "assistant" and "sources" in message:
                    with st.expander("📚 Sources"):
                        for i, source in enumerate(message["sources"], 1):
                            st.markdown(f"**Source {i}** (similarity: {source['similarity_score']:.3f})")
                            st.text(source["chunk"][:200] + "..." if len(source["chunk"]) > 200 else source["chunk"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your document..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get response from backend
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = ask_question(prompt)
                        answer = response["answer"]
                        sources = response["sources"]
                        
                        st.markdown(answer)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": answer,
                            "sources": sources
                        })
                        
                    except requests.RequestException as e:
                        error_msg = f"Failed to get answer: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": error_msg
                        })
                    except Exception as e:
                        error_msg = f"An error occurred: {str(e)}"
                        st.error(error_msg)
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": error_msg
                        })
    
    # Footer
    st.markdown("---")
    st.markdown("Built with Streamlit and FastAPI")

if __name__ == "__main__":
    main()
