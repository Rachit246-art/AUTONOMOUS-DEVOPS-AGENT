# Autonomous DevOps Agent

An enterprise-grade, modular backend platform designed for intelligent autonomous DevOps operations, incident remediation, and retrieval-augmented runbook diagnostics.

---

## 1. System Architecture

The project is structured around clean separation of concerns, isolating the core web API service, retrieval-augmented generation (RAG) engine, data repositories, and future AI/DevOps orchestration integrations into decoupled modules.

```text
AUTONOMOUS-DEVOPS-AGENT/
│
├── backend/
│   │
│   ├── fastapi_app/               # Primary REST API Service
│   │   ├── app/
│   │   │   ├── main.py            # FastAPI Application Entrypoint
│   │   │   ├── api/               # API Routing Layer
│   │   │   │   └── v1/
│   │   │   │       ├── router.py  # Central v1 Router Aggregator
│   │   │   │       └── endpoints/ # Domain-Specific Route Handlers
│   │   │   │           ├── projects.py   # DevOps Project Management Endpoints
│   │   │   │           ├── incidents.py  # Incident Tracking & Diagnostics Endpoints
│   │   │   │           └── documents.py  # Document Intake & Metadata Endpoints
│   │   │   ├── core/              # Global Configuration & Security
│   │   │   │   ├── config.py      # Pydantic Settings & Environment Parsing
│   │   │   │   └── security.py    # Authentication, Authorization & Encryption
│   │   │   ├── database/          # Database Connectivity
│   │   │   │   ├── connection.py  # SQLAlchemy Engine & SQL Server Dialect Setup
│   │   │   │   └── session.py     # Scoped Session Management & Dependency Injection
│   │   │   ├── models/            # SQLAlchemy ORM Database Entities
│   │   │   ├── schemas/           # Pydantic Request/Response DTO Schemas
│   │   │   ├── services/          # Business Logic & Workflow Services
│   │   │   └── repositories/      # Data Access Layer (Repository Pattern)
│   │   ├── tests/                 # Unit & Integration Tests for API Service
│   │   └── requirements.txt       # Backend Core Dependencies
│   │
│   ├── rag_engine/                # Retrieval-Augmented Generation Engine
│   │   ├── ingestion/             # Document Ingestion (PyPDF, Markdown, Text)
│   │   ├── chunking/              # Document Splitting & Chunking Strategies
│   │   ├── embeddings/            # Sentence-Transformers Vector Embedding Models
│   │   ├── vector_store/          # ChromaDB Client & Vector Storage Manager
│   │   ├── retrieval/             # Similarity Search & Reranking Mechanisms
│   │   ├── pipeline/              # Coordinated Ingestion-to-Retrieval Pipeline
│   │   ├── tests/                 # RAG Unit & Retrieval Accuracy Tests
│   │   └── requirements.txt       # RAG Engine Dependencies
│   │
│   └── integrations/              # External Ecosystem Connectors (Future Extensibility)
│       ├── llm/                   # Direct LLM Providers (Groq, OpenAI, Ollama)
│       └── langchain/             # LangChain & LangGraph Orchestration Chains
│
├── data/                          # Local Storage & Persistent Volumes (Git Ignored)
│   ├── documents/                 # Raw Input Documents (PDFs, Logs, Runbooks)
│   └── vector_db/                 # Persistent ChromaDB Database Files
│
├── .env                           # Local Environment Secrets (Git Ignored)
├── .env.example                   # Environment Configuration Template
├── .gitignore                     # Git Exclusion Rules
├── README.md                      # Architecture & Setup Documentation
└── docker-compose.yml             # Local Infrastructure (SQL Server, etc.)
```

---

## 2. Component Responsibilities

| Directory / File | Responsibility |
| :--- | :--- |
| `backend/fastapi_app/app/main.py` | FastAPI application initialization, CORS middleware, lifespan events, and router registration. |
| `backend/fastapi_app/app/api/v1/` | Versioned RESTful API routes, structured by business domain (`projects`, `incidents`, `documents`). |
| `backend/fastapi_app/app/core/` | Centralized settings management (`config.py`) using Pydantic Settings, JWT/API keys security (`security.py`). |
| `backend/fastapi_app/app/database/` | SQL Server connectivity (`connection.py`) via `pyodbc` and `sqlalchemy`, with session lifecycle management (`session.py`). |
| `backend/fastapi_app/app/models/` | SQLAlchemy ORM database models representing relational tables. |
| `backend/fastapi_app/app/schemas/` | Pydantic DTO models for strict request validation and response serialization. |
| `backend/fastapi_app/app/services/` | Pure business logic layer decoupled from transport protocols (HTTP/REST). |
| `backend/fastapi_app/app/repositories/` | Data access layer isolating raw database queries from business rules. |
| `backend/rag_engine/` | Independent knowledge engine responsible for parsing documents, generating embeddings, and executing semantic searches. |
| `backend/rag_engine/ingestion/` | Multi-format document intake parsers (PDF, TXT, MD, YAML/JSON). |
| `backend/rag_engine/chunking/` | Recursive character, token-based, and semantic text chunking implementations. |
| `backend/rag_engine/embeddings/` | Hugging Face Sentence Transformers interface for local text vectorization. |
| `backend/rag_engine/vector_store/` | ChromaDB collection initialization, persistence management, and indexing. |
| `backend/rag_engine/retrieval/` | Top-K similarity search, MMR (Maximal Marginal Relevance), and metadata filtering. |
| `backend/rag_engine/pipeline/` | Orchestrates the end-to-end flow from document loading to contextual knowledge retrieval. |
| `backend/integrations/` | Extensible adapter layer for future agentic orchestration and LLM integrations (LangChain, Groq, OpenAI). |
| `data/` | Isolated directory for raw input files and persistent vector index files; contents excluded from version control. |

---

## 3. Technology Stack

### Backend API
- **Language:** Python 3.11
- **Web Framework:** FastAPI
- **ASGI Server:** Uvicorn
- **ORM & Database Toolkit:** SQLAlchemy 2.0
- **Database Driver:** PyODBC
- **Target RDBMS:** Microsoft SQL Server
- **Data Validation & Settings:** Pydantic v2 & Pydantic-Settings

### RAG Engine
- **Document Parsing:** PyPDF
- **Embeddings:** Sentence-Transformers (`all-MiniLM-L6-v2` or similar)
- **Vector Storage:** ChromaDB (embedded/persistent)
- **Math & Tensors:** NumPy & PyTorch

### Testing & Tooling
- **Test Framework:** Pytest & HTTPX
- **API Testing:** Postman (Collections to be maintained for all v1 endpoints)
- **Containerization:** Docker Compose (local SQL Server container)

---

## 4. Architectural Principles

1. **Separation of Concerns:** 
   The REST API (`fastapi_app`) and the knowledge engine (`rag_engine`) remain independent Python packages. The API can import and leverage the RAG engine as a service without tight coupling.
2. **Repository & Service Pattern:**
   FastAPI endpoints delegate to the service layer for business workflows. The service layer accesses relational data exclusively through repository classes, ensuring testability and database neutrality.
3. **API-First & No Frontend:**
   The architecture is purely backend-oriented, designed for automated agent integration and verified using Postman API collections. No frontend frameworks (React, Vue, etc.) are present or required.
4. **Extensibility for Future Orchestration:**
   The `integrations/` package is structured to introduce LangChain, agent supervisors, Groq/OpenAI LLM inference, and CI/CD connectors (Jenkins, Docker, GitHub Actions) without modifying core business models.

---

## 5. Getting Started

### Prerequisites
- Python 3.11+
- ODBC Driver 18 for SQL Server (or Microsoft SQL Server Docker container)

### Setup Instructions
1. **Clone the repository and enter workspace:**
   ```bash
   cd AUTONOMOUS-DEVOPS-AGENT
   ```

2. **Configure Environment Variables:**
   ```bash
   copy .env.example .env
   ```
   Update `.env` with your SQL Server credentials and file storage paths.

3. **Install Dependencies:**
   ```bash
   # Install backend dependencies
   pip install -r backend/fastapi_app/requirements.txt

   # Install RAG dependencies
   pip install -r backend/rag_engine/requirements.txt
   ```

4. **Start Supporting Infrastructure (Optional SQL Server):**
   ```bash
   docker compose up -d sqlserver
   ```
