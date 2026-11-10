# Autonomous DevOps Agent

Autonomous DevOps Agent is an enterprise-level backend and RAG platform for automated incident intake, diagnostics, and retrieval-augmented runbook intelligence.

---

## Project Structure

```text
AUTONOMOUS-DEVOPS-AGENT/
│
├── backend/
│   │
│   ├── fastapi_app/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── incidents.py
│   │   │   └── error_service.py
│   │   │
│   │   └── requirements.txt
│   │
│   └── rag_engine/
│       ├── document_loader.py
│       ├── chunking.py
│       ├── embeddings.py
│       ├── vector_store.py
│       ├── retriever.py
│       ├── rag_pipeline.py
│       └── requirements.txt
│
├── data/
│   ├── documents/
│   └── vector_db/
│
├── .env
├── .gitignore
└── README.md
```

---

## Component Overview

### 1. FastAPI Backend (`backend/fastapi_app/`)
- **`app/main.py`**: Initializes the FastAPI application, mounts API routes under `/api/v1`, and defines health check endpoints.
- **`app/config.py`**: Loads environment variables from `.env` using `python-dotenv`.
- **`app/database.py`**: Configures SQLAlchemy engine and session factory for Microsoft SQL Server using PyODBC.
- **`app/models.py`**: Defines SQLAlchemy ORM database models (`ErrorLog`).
- **`app/schemas.py`**: Defines Pydantic validation schemas (`ErrorLogCreate`, `ErrorLogResponse`).
- **`app/incidents.py`**: Exposes REST API endpoints for incident intake.
- **`app/error_service.py`**: Houses error creation, business logic, and database insertion routines.
- **`requirements.txt`**: Core dependencies for the FastAPI service.

### 2. RAG Engine (`backend/rag_engine/`)
- **`document_loader.py`**: Ingests and parses documents (PDFs, incident logs, runbooks).
- **`chunking.py`**: Splits documents into manageable text chunks.
- **`embeddings.py`**: Generates vector embeddings via Sentence Transformers.
- **`vector_store.py`**: Manages ChromaDB collections and persistent vector indexing.
- **`retriever.py`**: Performs similarity search to retrieve relevant context.
- **`rag_pipeline.py`**: Orchestrates the complete ingestion-to-retrieval workflow.
- **`requirements.txt`**: Dependencies for the RAG engine.

### 3. Data Directory (`data/`)
- **`documents/`**: Directory for raw runbooks, logs, and PDF files.
- **`vector_db/`**: Local storage directory for persistent ChromaDB vector databases.

---

## Getting Started

1. **Activate Virtual Environment:**
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

2. **Run FastAPI Application:**
   ```bash
   cd backend/fastapi_app
   uvicorn app.main:app --reload
   ```

3. **API Testing:**
   Test endpoints using Postman at `http://127.0.0.1:8000/api/v1/incidents/`.
