# Chess Player Search Chat

This project is a Retrieval-Augmented Generation (RAG) system that allows users to ask questions about chess players based on custom PDF documents. The system retrieves relevant context from a vector database (Chroma) and uses a Large Language Model (Gemini) to generate answers.

---

## Features:
- Text extraction from pdf
- Text chunking using LangChain
- Embedding generation using Gemini Embeddings
- Saving vectors to ChromaDB
- Embedding of user queries
- Semantic search in ChromaDB
- Question answering using Gemini LLM
- Unit testing with pytest and pytest-mock

---

## Tech Stack:
- Python
- chromadb
- fastapi
- uvicorn
- google-genai
- langchain-text-splitters
- pydantic
- PyMuPDF
- python-dotenv
- requests
- streamlit
- pytest
- pytest-mock

---

## Architecture

User Question -> Embedding -> ChromaDB Search -> Context -> Gemini -> Answer

## Project Structure

```
Chess-Player-Search-AI
|
|- main.py | Getting data about chess players from chess.com API; Streamlit interface
|- rag.py | RAG pipeline (Text processing + ChromaDB)
|- streamlit_app.py | RAG Streamlit UI
|- pdf_reader.py | Extract text from pdf
|- api.py | Endpoints and Swagger UI
|- players_info.pdf | Input for pdf_reader.py
|- requirements.txt | All dependencies for project
|- conftest.py
|- tests/
    |- test_api.py
    |- test_main.py
    |- test_rag.py
```

---

## Running the application
1. Clone repository
```
git clone https://github.com/panutka1/Chess-Player-Search-AI
cd Chess-Player-Search-AI
```

2. Create virtual environment
```
python -m venv venv
source venv/bin/activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Create .env file with GEMINI_API_KEY
```
GEMINI_API_KEY=your_api_key
```

5. Run tests
```
pytest tests/ -v
```

6. Run FastAPI
```
uvicorn api:app --reload

Swagger UI runs on:
http://127.0.0.1:8000/docs
```

6. Run Streamlit
```
streamlit run {path_to_your_main.py} - Chess.com API interface
streamlit run {path_to_your_streamlit_app.py} - RAG interface
```
---

## Future improvements
1. Replace static PDF with dynamic data source (live database or API)
2. Deploy application to cloud

