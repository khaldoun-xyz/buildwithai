# Ask Your Document

A RAG-based document question answering application with hallucination validation.

## Features

- Upload text documents (.txt files) and PDF files (.pdf)
- Ask questions about document content
- AI-powered answers using GPT-4
- Validation tab to check for hallucinations
- Source chunk verification
- Docker deployment ready

## Quick Start

1. **Clone and setup:**
   ```bash
   cd ask_your_document
   cp .env.example .env
   ```

2. **Install and setup Ollama:**
   ```bash
   # Install Ollama (if not already installed)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull the llama3.1:8b-instant model
   ollama pull llama3.1:8b-instant
   ```

3. **Run with Docker:**
   ```bash
   docker-compose up --build
   ```

4. **Access the application:**
   Open http://localhost:8501 in your browser

## Manual Setup (without Docker)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Ollama service:**
   ```bash
   ollama serve
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Upload a document:** Use the file uploader in the Chat tab to upload a .txt or .pdf file
2. **Ask questions:** Type your questions in the chat interface
3. **Validate answers:** Switch to the Validation tab to see source chunks and verify the AI's answers

## Architecture

- **Frontend:** Streamlit
- **Vector Database:** ChromaDB (persistent storage)
- **LLM:** Ollama llama3.1:8b-instant + sentence-transformers
- **Deployment:** Docker + docker-compose

## Validation Feature

The validation tab helps you:
- See which document chunks were used to generate each answer
- Check similarity scores for relevance
- Verify if the AI's answer is grounded in the source material
- Identify potential hallucinations

## Requirements

- Python 3.11+
- Ollama installed and running
- llama3.1:8b-instant model available in Ollama
- Docker (optional, for containerized deployment)
