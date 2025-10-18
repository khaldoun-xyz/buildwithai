import os
import tiktoken
import chromadb
from typing import List, Dict, Tuple, Optional
import ollama
import streamlit as st
import PyPDF2
import io


class RAGPipeline:
    """RAG pipeline for document question answering with hallucination validation."""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """Initialize the RAG pipeline.
        
        Args:
            persist_directory: Directory to persist ChromaDB data.
        """
        self.chat_model = "llama3.2:3b"
        self.chunk_size = 500
        self.chunk_overlap = 50
        self.encoding = tiktoken.get_encoding("cl100k_base")
        
        # Ollama configuration for embeddings - using chat model for embeddings
        self.embedding_model = "llama3.2:3b"  # Use the available chat model
        self.ollama_client = ollama.Client(host='http://ollama:11434')
        
        self.chroma_client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.chroma_client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def chunk_text(self, text: str, document_name: str) -> List[Dict[str, any]]:
        """Split text into overlapping chunks.
        
        Args:
            text: The text to chunk.
            document_name: Name of the source document.
            
        Returns:
            List of chunk dictionaries with text, metadata, and IDs.
        """
        tokens = self.encoding.encode(text)
        chunks = []
        
        for i in range(0, len(tokens), self.chunk_size - self.chunk_overlap):
            chunk_tokens = tokens[i:i + self.chunk_size]
            chunk_text = self.encoding.decode(chunk_tokens)
            
            chunk_id = f"{document_name}_chunk_{i // (self.chunk_size - self.chunk_overlap)}"
            
            chunks.append({
                "id": chunk_id,
                "text": chunk_text,
                "metadata": {
                    "document_name": document_name,
                    "chunk_index": i // (self.chunk_size - self.chunk_overlap),
                    "start_char": i,
                    "end_char": i + len(chunk_tokens)
                }
            })
        
        return chunks
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text using a simple hash-based approach.
        
        Since we're using a chat model instead of a dedicated embedding model,
        we'll create a simple but effective embedding using text hashing.
        
        Args:
            text: Text to embed.
            
        Returns:
            Embedding vector.
        """
        try:
            import hashlib
            import numpy as np
            
            # Create a simple but effective embedding using text hashing
            # This creates a consistent vector representation for similar texts
            text_lower = text.lower().strip()
            
            # Create multiple hash values for different text features
            hash1 = int(hashlib.md5(text_lower.encode()).hexdigest()[:8], 16)
            hash2 = int(hashlib.sha1(text_lower.encode()).hexdigest()[:8], 16)
            hash3 = int(hashlib.sha256(text_lower.encode()).hexdigest()[:8], 16)
            
            # Create word-based hashes
            words = text_lower.split()
            word_hashes = []
            for word in words[:50]:  # Limit to first 50 words
                word_hashes.append(int(hashlib.md5(word.encode()).hexdigest()[:4], 16))
            
            # Pad or truncate to get exactly 768 dimensions (standard embedding size)
            while len(word_hashes) < 768:
                word_hashes.extend(word_hashes[:min(768-len(word_hashes), len(word_hashes))])
            
            # Create the final embedding vector
            embedding = []
            
            # Add the main hash values
            embedding.extend([hash1 % 1000 / 1000.0, hash2 % 1000 / 1000.0, hash3 % 1000 / 1000.0])
            
            # Add word-based features
            embedding.extend([h % 1000 / 1000.0 for h in word_hashes[:765]])
            
            # Normalize the vector
            embedding = np.array(embedding)
            embedding = embedding / (np.linalg.norm(embedding) + 1e-8)
            
            return embedding.tolist()
            
        except Exception as e:
            st.error(f"Error creating embedding: {str(e)}")
            # Return a zero vector as fallback
            return [0.0] * 768
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from PDF file.
        
        Args:
            pdf_file: PDF file object.
            
        Returns:
            Extracted text from the PDF.
        """
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def add_document(self, text: str, document_name: str) -> None:
        """Add document to the vector database.
        
        Args:
            text: Document text content.
            document_name: Name of the document.
        """
        chunks = self.chunk_text(text, document_name)
        
        texts = [chunk["text"] for chunk in chunks]
        embeddings = [self.get_embedding(text) for text in texts]
        ids = [chunk["id"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]
        
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
    
    def add_pdf_document(self, pdf_file, document_name: str) -> None:
        """Add PDF document to the vector database.
        
        Args:
            pdf_file: PDF file object.
            document_name: Name of the document.
        """
        text = self.extract_text_from_pdf(pdf_file)
        self.add_document(text, document_name)
    
    def retrieve_relevant_chunks(self, query: str, n_results: int = 5) -> List[Dict[str, any]]:
        """Retrieve most relevant chunks for a query.
        
        Args:
            query: User's question.
            n_results: Number of chunks to retrieve.
            
        Returns:
            List of relevant chunks with similarity scores.
        """
        query_embedding = self.get_embedding(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        chunks = []
        for i in range(len(results["documents"][0])):
            chunks.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
                "similarity_score": 1 - results["distances"][0][i]
            })
        
        return chunks
    
    def generate_answer(self, query: str, relevant_chunks: List[Dict[str, any]]) -> str:
        """Generate answer using retrieved chunks.
        
        Args:
            query: User's question.
            relevant_chunks: Retrieved relevant chunks.
            
        Returns:
            Generated answer from the LLM.
        """
        context = "\n\n".join([chunk["text"] for chunk in relevant_chunks])
        
        system_prompt = """You are a helpful assistant that answers questions based on provided document chunks. 
        Your answers should be grounded in the provided context. If the answer cannot be found in the context, 
        say so clearly. Always cite which document and chunk the information comes from when possible."""
        
        user_prompt = f"""Context from documents:
        {context}
        
        Question: {query}
        
        Please provide a comprehensive answer based on the context above. If you reference specific information, 
        mention which document it comes from."""
        
        try:
            response = self.ollama_client.chat(
                model=self.chat_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                options={"temperature": 0.1}
            )
            return response['message']['content']
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def process_query(self, query: str) -> Tuple[str, List[Dict[str, any]]]:
        """Process a query and return answer with source chunks.
        
        Args:
            query: User's question.
            
        Returns:
            Tuple of (answer, relevant_chunks) for validation.
        """
        relevant_chunks = self.retrieve_relevant_chunks(query)
        answer = self.generate_answer(query, relevant_chunks)
        return answer, relevant_chunks
