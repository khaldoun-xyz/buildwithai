from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Tuple
import uvicorn
from rag_pipeline import RAGPipeline

app = FastAPI(title="Ask Your Document API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global RAG pipeline instance
rag_pipeline = RAGPipeline()

class QuestionRequest(BaseModel):
    """Request model for asking questions."""
    question: str

class QuestionResponse(BaseModel):
    """Response model for questions."""
    answer: str
    sources: List[dict]

class UploadResponse(BaseModel):
    """Response model for file uploads."""
    message: str
    chunks_count: int

@app.get("/health")
async def health_check():
    """Health check endpoint.
    
    Returns:
        Status of the API.
    """
    return {"status": "healthy", "message": "API is running"}

@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a text document.
    
    Args:
        file: The uploaded text file.
        
    Returns:
        Upload confirmation with chunk count.
        
    Raises:
        HTTPException: If file is not a text file or processing fails.
    """
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")
    
    try:
        content = await file.read()
        text = content.decode('utf-8')
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="File is empty")
        
        # Add document to RAG pipeline
        initial_chunks_count = len(rag_pipeline.chunks)
        rag_pipeline.add_document(text)
        new_chunks_count = len(rag_pipeline.chunks) - initial_chunks_count
        
        return UploadResponse(
            message=f"Document uploaded successfully: {file.filename}",
            chunks_count=new_chunks_count
        )
        
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be valid UTF-8 text")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """Ask a question about the uploaded document.
    
    Args:
        request: The question request.
        
    Returns:
        Answer with source information.
        
    Raises:
        HTTPException: If no document is uploaded or question processing fails.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        answer, sources = rag_pipeline.ask_question(request.question.strip())
        
        # Format sources for response
        formatted_sources = [
            {
                "chunk": chunk,
                "similarity_score": float(score)
            }
            for chunk, score in sources
        ]
        
        return QuestionResponse(
            answer=answer,
            sources=formatted_sources
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/status")
async def get_status():
    """Get the current status of the RAG pipeline.
    
    Returns:
        Current pipeline status including chunk count.
    """
    return {
        "chunks_count": len(rag_pipeline.chunks),
        "has_documents": len(rag_pipeline.chunks) > 0
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
