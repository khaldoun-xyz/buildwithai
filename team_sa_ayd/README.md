# Ask Your Document

A RAG-based document question-answering application that allows you to upload text documents and ask questions about their content using AI.

## Features

- **Document Upload**: Upload text files (.txt) for processing
- **Chat Interface**: Interactive chat interface for asking questions
- **RAG Pipeline**: Retrieval-Augmented Generation using TF-IDF embeddings and Groq's Llama 3.1 8B Instant
- **Source Citations**: View which parts of the document were used to answer your questions
- **Docker Deployment**: Easy deployment with Docker Compose

## Architecture

- **Frontend**: Streamlit (Python-based UI)
- **Backend**: FastAPI (REST API with RAG pipeline)
- **AI Models**: Groq API (Llama 3.1 8B Instant for chat completion)
- **Vector Storage**: In-memory (TF-IDF with scikit-learn for similarity search)

## Groq Integration

This application uses **Groq's Llama 3.1 8B Instant model** for fast inference and high-quality responses. Key features:

- **Fast Inference**: Groq provides ultra-fast inference speeds
- **Cost-Effective**: Competitive pricing compared to other AI providers
- **High Quality**: Llama 3.1 8B Instant delivers excellent performance for document Q&A
- **TF-IDF Embeddings**: Uses scikit-learn's TF-IDF vectorization for document similarity (since Groq doesn't provide embeddings)

### Getting a Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for an account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and use it in your environment variables

## Prerequisites

- Docker and Docker Compose
- Groq API key

## Setup Instructions

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd buildwithai
   ```

2. **Set up environment variables**:
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your_actual_groq_api_key_here
   BACKEND_URL=http://backend:8000
   ```

3. **Build and run with Docker Compose**:
   ```bash
   # Set the Groq API key as an environment variable
   export GROQ_API_KEY="your_actual_groq_api_key_here"
   
   # Build and run the application
   docker-compose up --build
   ```

4. **Access the application**:
   - Frontend (Streamlit UI): http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Usage

1. **Upload a document**:
   - Open the Streamlit app at http://localhost:8501
   - Use the sidebar to upload a `.txt` file
   - Wait for the document to be processed

2. **Ask questions**:
   - Type your questions in the chat interface
   - The AI will answer based on the uploaded document content
   - View source citations to see which parts of the document were used

## API Endpoints

### Backend API (FastAPI)

- `GET /health` - Health check
- `POST /upload` - Upload a text document
- `POST /ask` - Ask a question about the document
- `GET /status` - Get current pipeline status

### Example API Usage

```bash
# Upload a document
curl -X POST "http://localhost:8000/upload" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_document.txt"

# Ask a question
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is the main topic of this document?"}'
```

## Development

### Running locally (without Docker)

1. **Backend**:
   ```bash
   cd app/backend
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```

2. **Frontend**:
   ```bash
   cd app/frontend
   pip install -r requirements.txt
   streamlit run streamlit_app.py --server.port 8501
   ```

### Project Structure

```
/app
  /backend
    main.py          # FastAPI application
    rag_pipeline.py  # RAG pipeline implementation
    requirements.txt # Backend dependencies
  /frontend
    streamlit_app.py # Streamlit UI
    requirements.txt # Frontend dependencies
docker-compose.yml   # Docker Compose configuration
Dockerfile.backend   # Backend Docker image
Dockerfile.frontend  # Frontend Docker image
env.example         # Environment variables template
README.md           # This file
```

## Configuration

### Environment Variables

- `GROQ_API_KEY`: Your Groq API key (required)
- `BACKEND_URL`: Backend service URL (default: http://backend:8000)

### RAG Pipeline Settings

The RAG pipeline uses the following default settings:
- **Chunk size**: 800 characters
- **Overlap**: 100 characters
- **Embedding method**: TF-IDF vectorization (1000 max features)
- **Chat model**: llama-3.1-8b-instant
- **Top-k retrieval**: 5 most similar chunks

## Troubleshooting

### Common Issues

1. **Backend not responding**:
   - Check if the Groq API key is correctly set
   - Verify Docker containers are running: `docker-compose ps`
   - Check logs: `docker-compose logs backend`

2. **Frontend connection issues**:
   - Ensure backend is running and accessible
   - Check the BACKEND_URL environment variable
   - Verify Docker networking: `docker network ls`

3. **File upload errors**:
   - Only `.txt` files are supported
   - Ensure files are valid UTF-8 text
   - Check file size (large files may take time to process)

### Logs

View application logs:
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
```

## License

This project is part of the BuildWithAI initiative.