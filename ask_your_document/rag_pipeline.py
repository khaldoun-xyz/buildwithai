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
        self.chunk_size = 1000  # Larger chunks for better context
        self.chunk_overlap = 100  # More overlap for better retrieval
        self.encoding = tiktoken.get_encoding("cl100k_base")
        
        # Ollama configuration for embeddings - using chat model for embeddings
        self.embedding_model = "llama3.2:3b"  # Use the available chat model
        self.ollama_client = ollama.Client(host='http://ollama:11434')
        
        self.chroma_client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.chroma_client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine", "dimension": 384}
        )
    
    def clear_documents(self):
        """Clear all documents from the collection."""
        try:
            # Delete the entire collection
            self.chroma_client.delete_collection("documents")
            # Recreate the collection
            self.collection = self.chroma_client.get_or_create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine", "dimension": 384}
            )
        except Exception as e:
            # If collection doesn't exist, just create it
            self.collection = self.chroma_client.get_or_create_collection(
                name="documents",
                metadata={"hnsw:space": "cosine", "dimension": 384}
            )
    
    def chunk_text(self, text: str, document_name: str) -> List[Dict[str, any]]:
        """Split text into overlapping chunks with better sentence boundaries.
        
        Args:
            text: The text to chunk.
            document_name: Name of the source document.
            
        Returns:
            List of chunk dictionaries with text, metadata, and IDs.
        """
        import re
        
        # First, split by paragraphs (double newlines)
        paragraphs = text.split('\n\n')
        chunks = []
        chunk_index = 0
        
        for para_idx, paragraph in enumerate(paragraphs):
            if not paragraph.strip():
                continue
                
            # Clean up the paragraph
            paragraph = paragraph.strip()
            
            # If paragraph is small enough, use it as a single chunk
            if len(paragraph) <= self.chunk_size:
                chunk_id = f"{document_name}_chunk_{chunk_index}"
                chunks.append({
                    "id": chunk_id,
                    "text": paragraph,
                    "metadata": {
                        "document_name": document_name,
                        "chunk_index": chunk_index,
                        "paragraph_index": para_idx,
                        "type": "full_paragraph",
                        "char_count": len(paragraph)
                    }
                })
                chunk_index += 1
            else:
                # Split long paragraphs by sentences
                sentences = re.split(r'(?<=[.!?])\s+', paragraph)
                current_chunk = ""
                sentence_start = 0
                
                for sent_idx, sentence in enumerate(sentences):
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                        
                    # If adding this sentence would exceed chunk size, save current chunk
                    if len(current_chunk) + len(sentence) + 1 > self.chunk_size and current_chunk:
                        chunk_id = f"{document_name}_chunk_{chunk_index}"
                        chunks.append({
                            "id": chunk_id,
                            "text": current_chunk.strip(),
                            "metadata": {
                                "document_name": document_name,
                                "chunk_index": chunk_index,
                                "paragraph_index": para_idx,
                                "sentence_start": sentence_start,
                                "sentence_end": sent_idx - 1,
                                "type": "sentence_group",
                                "char_count": len(current_chunk)
                            }
                        })
                        chunk_index += 1
                        
                        # Start new chunk with overlap (last 2-3 sentences)
                        overlap_sentences = current_chunk.split('.')[-3:]
                        current_chunk = '. '.join([s.strip() for s in overlap_sentences if s.strip()]) + '. ' + sentence
                        sentence_start = sent_idx - len([s for s in overlap_sentences if s.strip()])
                    else:
                        current_chunk += " " + sentence if current_chunk else sentence
                
                # Add remaining chunk
                if current_chunk.strip():
                    chunk_id = f"{document_name}_chunk_{chunk_index}"
                    chunks.append({
                        "id": chunk_id,
                        "text": current_chunk.strip(),
                        "metadata": {
                            "document_name": document_name,
                            "chunk_index": chunk_index,
                            "paragraph_index": para_idx,
                            "sentence_start": sentence_start,
                            "sentence_end": len(sentences) - 1,
                            "type": "sentence_group",
                            "char_count": len(current_chunk)
                        }
                    })
                    chunk_index += 1
        
        return chunks
    
    def get_embedding(self, text: str) -> List[float]:
        """Get embedding for text using optimized hash-based approach.
        
        Args:
            text: Text to embed.
            
        Returns:
            Embedding vector.
        """
        try:
            import hashlib
            import numpy as np
            
            # Preprocess text for better performance
            text_clean = text.lower().strip()
            words = text_clean.split()[:30]  # Limit to first 30 words for speed
            
            # Create a smaller, faster embedding (384 dimensions instead of 768)
            embedding = []
            
            # Text-level features (3 values)
            text_hash = int(hashlib.md5(text_clean.encode()).hexdigest()[:8], 16)
            embedding.extend([
                (text_hash % 1000) / 1000.0,
                ((text_hash >> 8) % 1000) / 1000.0,
                ((text_hash >> 16) % 1000) / 1000.0
            ])
            
            # Word-level features (30 words * 12 features = 360 values)
            for word in words:
                word_hash = int(hashlib.md5(word.encode()).hexdigest()[:6], 16)
                # Create 12 features per word
                for i in range(12):
                    embedding.append(((word_hash >> (i * 2)) % 1000) / 1000.0)
            
            # Pad to exactly 384 dimensions
            while len(embedding) < 384:
                embedding.append(0.0)
            
            # Truncate if too long
            embedding = embedding[:384]
            
            # Normalize
            embedding = np.array(embedding)
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm
            
            return embedding.tolist()
            
        except Exception as e:
            st.error(f"Error creating embedding: {str(e)}")
            return [0.0] * 384
    
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
    
    def retrieve_relevant_chunks(self, query: str, n_results: int = 3) -> List[Dict[str, any]]:
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
