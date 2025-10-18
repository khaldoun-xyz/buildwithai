<!-- fa6d2135-1e14-4ac1-8ad0-734f7329bbf0 7f180384-16a0-4734-854c-ac9eee9e161c -->
# Ask Your Document - RAG Application

## Architecture

**Tech Stack:**

- Frontend: Streamlit (Python-based UI)
- Vector DB: ChromaDB (embedded, lightweight)
- LLM Provider: OpenAI (GPT-4 + text-embedding-3-small)
- Deployment: Docker + docker-compose

## Implementation Steps

### 1. Project Structure Setup

Create the following structure:

```
/Users/louis/buildwithai/ask_your_document/
├── app.py                 # Main Streamlit application
├── rag_pipeline.py        # RAG logic (chunking, embedding, retrieval)
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container setup
├── docker-compose.yml    # Orchestration
├── .env.example          # Environment variable template
└── README.md             # Setup instructions
```

### 2. Core RAG Pipeline (`rag_pipeline.py`)

Implement:

- **Text chunking**: Split documents into overlapping chunks (e.g., 500 tokens with 50 token overlap)
- **Embedding function**: Use OpenAI's `text-embedding-3-small` model
- **ChromaDB setup**: Initialize collection with persistent storage
- **Document ingestion**: Process uploaded .txt files, chunk, embed, and store in ChromaDB
- **Retrieval function**: Embed query and perform similarity search (top-k=3-5 chunks)
- **Answer synthesis**: Send query + retrieved chunks to GPT-4 with system prompt to minimize hallucinations

### 3. Streamlit UI (`app.py`)

Create two tabs:

- **Chat Tab**: 
  - File uploader for .txt files
  - Document processing status indicator
  - Chat interface with message history
  - Display AI responses with streaming support
- **Validation Tab**:
  - Show the user's question
  - Display retrieved chunks with similarity scores
  - Show the AI's answer
  - Highlight which chunks were used to generate the answer
  - Allow users to verify if the answer is grounded in the source material

### 4. Dependencies (`requirements.txt`)

Include:

- streamlit
- chromadb
- openai
- python-dotenv
- tiktoken (for token counting)

### 5. Docker Setup

- **Dockerfile**: Python 3.11 base, install dependencies, expose port 8501
- **docker-compose.yml**: Define service with volume mounts for data persistence and environment variables
- **.env.example**: Template for OPENAI_API_KEY

### 6. Key Implementation Details

- Store metadata with each chunk (document name, chunk index, character positions)
- Use session state in Streamlit to maintain chat history and document state
- Implement proper error handling for API calls and file uploads
- Add clear instructions in the UI for users
- Follow Google-style docstrings for all functions
- Minimize code comments (per ai_instructions.md)

## Validation Feature Design

The validation tab will:

1. Store retrieved chunks alongside each answer in session state
2. Display chunks with relevance scores
3. Show the final answer for side-by-side comparison
4. Help users identify potential hallucinations by checking if the answer content exists in the cited chunks

### To-dos

- [ ] Create project directory structure and initialize files
- [ ] Build RAG pipeline with chunking, embedding, ChromaDB integration, and retrieval logic
- [ ] Create Streamlit app with chat and validation tabs
- [ ] Create Dockerfile, docker-compose.yml, and .env.example
- [ ] Write README.md with setup and usage instructions