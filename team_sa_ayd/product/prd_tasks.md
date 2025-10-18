# Ask Your Document - Implementation Plan

## Architecture Overview
- **Frontend**: Streamlit (Python-based UI)
- **Backend**: FastAPI (REST API with RAG pipeline)
- **AI Models**: OpenAI API (embeddings + chat completion)
- **Vector Storage**: In-memory (NumPy/scikit-learn for similarity search)
- **Deployment**: Docker Compose

## Implementation Steps

### 1. Project Structure Setup
Create the following structure:
```
/app
  /backend
    main.py          # FastAPI app
    rag_pipeline.py  # RAG logic (chunking, embedding, retrieval)
    requirements.txt
  /frontend
    streamlit_app.py # Streamlit UI
    requirements.txt
docker-compose.yml
Dockerfile.backend
Dockerfile.frontend
.env.example
README.md
```

### 2. Backend Implementation (`/app/backend`)

**`rag_pipeline.py`**: Core RAG functionality
- Text chunking function (split by paragraphs or fixed token size with overlap)
- Embedding function using OpenAI's `text-embedding-ada-002`
- In-memory vector store (store chunks + embeddings in lists)
- Similarity search using cosine similarity
- Answer generation using OpenAI's chat completion API with retrieved context

**`main.py`**: FastAPI endpoints
- `POST /upload`: Accept text file, chunk it, create embeddings, store in memory
- `POST /ask`: Receive question, embed it, retrieve top-k chunks, generate answer
- `GET /health`: Health check endpoint

### 3. Frontend Implementation (`/app/frontend`)

**`streamlit_app.py`**: Simple chat interface
- File uploader widget for `.txt` files
- Display upload confirmation
- Text input for questions
- Chat-style display of Q&A history
- Call backend API endpoints via `requests` library

### 4. Docker Configuration

**`Dockerfile.backend`**:
- Python 3.11 base image
- Install dependencies from `backend/requirements.txt`
- Expose port 8000
- Run FastAPI with uvicorn

**`Dockerfile.frontend`**:
- Python 3.11 base image
- Install dependencies from `frontend/requirements.txt`
- Expose port 8501
- Run Streamlit app

**`docker-compose.yml`**:
- Define `backend` service (port 8000)
- Define `frontend` service (port 8501)
- Pass OpenAI API key via environment variable
- Set up service networking

### 5. Dependencies

**Backend** (`backend/requirements.txt`):
- fastapi
- uvicorn
- openai
- python-multipart (for file uploads)
- numpy
- scikit-learn (for cosine similarity)
- python-dotenv

**Frontend** (`frontend/requirements.txt`):
- streamlit
- requests

### 6. Configuration Files

**`.env.example`**: Template for environment variables
- `OPENAI_API_KEY=your_api_key_here`
- `BACKEND_URL=http://backend:8000`

**`README.md`**: Usage instructions
- Setup steps (copy `.env.example` to `.env`, add API key)
- How to run with Docker Compose
- How to use the application

## Key Implementation Details

### Chunking Strategy
Split text into ~500-1000 character chunks with 100-character overlap to maintain context continuity.

### Retrieval
Retrieve top 3-5 most similar chunks based on cosine similarity between question embedding and chunk embeddings.

### Prompt Engineering
Format prompt as: "Answer the following question based on the provided context. If the answer is not in the context, say so. Context: {chunks} Question: {question}"

### Following AI Instructions
- All Python functions will include Google-style docstrings
- Code will be junior-developer friendly
- Minimal unnecessary comments
- Docker deployment ready

## Implementation Todos

1. **setup-structure**: Create project directory structure and configuration files
2. **backend-rag**: Implement RAG pipeline (chunking, embedding, retrieval, generation) [depends on: setup-structure]
3. **backend-api**: Implement FastAPI endpoints for upload and query [depends on: backend-rag]
4. **frontend-ui**: Build Streamlit interface with upload and chat features [depends on: backend-api]
5. **docker-setup**: Create Dockerfiles and docker-compose.yml for deployment [depends on: backend-api, frontend-ui]
6. **documentation**: Create README with setup and usage instructions [depends on: docker-setup]

