# Product sheet: Ask your document

Chat with your document.

Upload a text-based document and ask questions
about its content. Make sure to minimise hallucinations.

## Required features

- **Document upload**: A user can upload a text file (.txt).
- **Chat interface**: The user can ask a question.
- **Backend RAG pipeline**:
  - Receive and chunk the text from the uploaded document.
  - Use an embedding model to turn the text chunks into vectors.
  - When a question comes in, embed it and perform a vector
    search to find the most relevant chunks.
  - Send the question and the retrieved chunks to a generative AI
    model to synthesize the final answer.
- **Display the answer**: Show the AI-generated answer in
  the chat window.

## Optional features

- Cite on which page or in which segment the source text was found.
- Allow an upload of other file formats (e.g. .pdf or .png).
