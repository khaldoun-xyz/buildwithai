import os
import re
from typing import List, Tuple
import numpy as np
from groq import Groq
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from dotenv import load_dotenv

load_dotenv()

class RAGPipeline:
    """RAG pipeline for document question answering."""
    
    def __init__(self):
        """Initialize the RAG pipeline with Groq client."""
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.chunks = []
        self.embeddings = []
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.chat_model = "llama-3.1-8b-instant"
    
    def chunk_text(self, text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
        """Split text into overlapping chunks.
        
        Args:
            text: The input text to chunk.
            chunk_size: Maximum size of each chunk in characters.
            overlap: Number of characters to overlap between chunks.
            
        Returns:
            List of text chunks.
        """
        if not text.strip():
            return []
        
        # Split by paragraphs first
        paragraphs = re.split(r'\n\s*\n', text.strip())
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
                
            # If adding this paragraph would exceed chunk size
            if len(current_chunk) + len(paragraph) + 1 > chunk_size:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    # Start new chunk with overlap
                    current_chunk = current_chunk[-overlap:] + " " + paragraph if overlap > 0 else paragraph
                else:
                    # Single paragraph is too long, split it
                    if len(paragraph) > chunk_size:
                        chunks.extend(self._split_long_text(paragraph, chunk_size, overlap))
                    else:
                        current_chunk = paragraph
            else:
                current_chunk += " " + paragraph if current_chunk else paragraph
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _split_long_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Split a long text into smaller chunks.
        
        Args:
            text: The text to split.
            chunk_size: Maximum size of each chunk.
            overlap: Number of characters to overlap.
            
        Returns:
            List of text chunks.
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            if end >= len(text):
                chunks.append(text[start:])
                break
            
            # Try to break at sentence boundary
            sentence_end = text.rfind('.', start, end)
            if sentence_end > start:
                end = sentence_end + 1
            
            chunks.append(text[start:end])
            start = end - overlap if overlap > 0 else end
        
        return chunks
    
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for a list of texts using TF-IDF.
        
        Args:
            texts: List of texts to embed.
            
        Returns:
            List of embedding vectors.
        """
        if not texts:
            return []
        
        # Fit the vectorizer on all texts if it hasn't been fitted yet
        if not hasattr(self.vectorizer, 'vocabulary_') or not self.vectorizer.vocabulary_:
            self.vectorizer.fit(texts)
        
        # Transform texts to TF-IDF vectors
        tfidf_matrix = self.vectorizer.transform(texts)
        
        # Convert to dense arrays and return as list of lists
        return tfidf_matrix.toarray().tolist()
    
    def add_document(self, text: str) -> None:
        """Add a document to the vector store.
        
        Args:
            text: The document text to add.
        """
        chunks = self.chunk_text(text)
        if not chunks:
            return
        
        # Add new chunks to existing chunks
        self.chunks.extend(chunks)
        
        # Re-fit the vectorizer on all chunks and create embeddings
        if self.chunks:
            # Fit vectorizer on all chunks
            self.vectorizer.fit(self.chunks)
            # Create embeddings for all chunks
            self.embeddings = self.create_embeddings(self.chunks)
    
    def retrieve_relevant_chunks(self, question: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """Retrieve most relevant chunks for a question.
        
        Args:
            question: The question to find relevant chunks for.
            top_k: Number of top chunks to retrieve.
            
        Returns:
            List of (chunk, similarity_score) tuples.
        """
        if not self.chunks or not self.embeddings:
            return []
        
        # Create embedding for the question using the fitted vectorizer
        question_embedding = self.vectorizer.transform([question]).toarray()[0]
        
        similarities = cosine_similarity(
            [question_embedding], 
            self.embeddings
        )[0]
        
        # Get top_k most similar chunks
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        return [(self.chunks[i], similarities[i]) for i in top_indices]
    
    def generate_answer(self, question: str, context_chunks: List[str]) -> str:
        """Generate an answer using retrieved context.
        
        Args:
            question: The user's question.
            context_chunks: List of relevant text chunks.
            
        Returns:
            Generated answer.
        """
        context = "\n\n".join(context_chunks)
        
        prompt = f"""Answer the following question based on the provided context. If the answer is not in the context, say so clearly.

Context:
{context}

Question: {question}

Answer:"""
        
        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.1
        )
        
        return response.choices[0].message.content.strip()
    
    def ask_question(self, question: str) -> Tuple[str, List[Tuple[str, float]]]:
        """Ask a question and get an answer with sources.
        
        Args:
            question: The question to ask.
            
        Returns:
            Tuple of (answer, source_chunks_with_scores).
        """
        if not self.chunks:
            return "No documents have been uploaded yet. Please upload a document first.", []
        
        relevant_chunks = self.retrieve_relevant_chunks(question)
        context_chunks = [chunk for chunk, _ in relevant_chunks]
        
        if not context_chunks:
            return "I couldn't find relevant information in the uploaded document.", []
        
        answer = self.generate_answer(question, context_chunks)
        
        return answer, relevant_chunks
