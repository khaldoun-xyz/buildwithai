import os
import tiktoken
import chromadb
from typing import List, Dict, Tuple, Optional
from openai import OpenAI
import streamlit as st


class RAGPipeline:
    """RAG pipeline for document question answering with hallucination validation."""
    
    def __init__(self, openai_api_key: str, persist_directory: str = "./chroma_db"):
        """Initialize the RAG pipeline.
        
        Args:
            openai_api_key: OpenAI API key for embeddings and chat completion.
            persist_directory: Directory to persist ChromaDB data.
        """
        self.client = OpenAI(api_key=openai_api_key)
        self.embedding_model = "text-embedding-3-small"
        self.chat_model = "gpt-4"
        self.chunk_size = 500
        self.chunk_overlap = 50
        self.encoding = tiktoken.get_encoding("cl100k_base")
        
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
        """Get embedding for text using OpenAI.
        
        Args:
            text: Text to embed.
            
        Returns:
            Embedding vector.
        """
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
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
        
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1
        )
        
        return response.choices[0].message.content
    
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
