# UniHack — AI-Powered Product Intelligence for Industrial Commerce

> AI-powered system for creating, enriching, validating, and preparing industrial product information for commerce from fragmented and potentially incomplete source material.

**Repository:** `unihack-product-intelligence`

**Challenge:** [Hack2Skill UniHack](https://hack2skill.com)

---

## Table of Contents

- [Overview](#overview)
- [Current Status](#current-status)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Database Migrations](#database-migrations)
- [Environment Variables](#environment-variables)
- [Running Tests](#running-tests)
- [Running Linters](#running-linters)
- [Architecture](#architecture)
- [Module Progress](#module-progress)
- [License](#license)

---

## Overview

Industrial product information often exists in fragmented, inconsistent, and incomplete forms — PDFs, spreadsheets, scanned documents, and web pages. This project builds an AI-powered system capable of:

- **Extracting** structured product data from heterogeneous sources
- **Enriching** incomplete product information using AI assistance
- **Validating** product data for correctness, consistency, and completeness
- **Tracking** data provenance and confidence for every attribute
- **Supporting** human review where automation has meaningful uncertainty

The system follows a **provenance-first** architecture: every piece of product information traces back to its source, with explicit confidence and validation status.

---

## Current Status

**Module 4 — Foundation & Validation Infrastructure: COMPLETE**

The system foundation is operational with:

- FastAPI backend with health/readiness endpoints and structured error handling
- SQLAlchemy ORM with Alembic migration infrastructure
- Domain model with comprehensive enums and dataclasses
- Streamlit frontend with backend connection indicator
- 61 passing tests (health, readiness, config, errors, database, domain)
- Ruff linting (0 errors) and format compliance

**Next:** Module 5 — Document Intelligence & Ingestion Pipeline

---

## Project Structure

```
unihack-product-intelligence/
├── README.md                          # This file
├── .env.example                       # Environment variable template
├── .gitignore                         # Git ignore rules
│
├── backend/
│   ├── pyproject.toml                 # Python project config & dependencies
│   ├── alembic.ini                    # Alembic configuration
│   ├── alembic/
│   │   ├── env.py                     # Alembic environment (reads DATABASE_URL)
│   │   ├── script.py.mako             # Migration template
│   │   └── versions/
│   │       └── 001_initial_migration.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI entry point
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── router.py          # API v1 router
│   │   │       └── health.py          # Health & readiness endpoints
│   │   ├── core/
│   │   │   ├── config.py              # Settings (pydantic-settings)
│   │   │   ├── database.py            # SQLAlchemy engine, session, Base
│   │   │   ├── exceptions.py          # Custom exception hierarchy
│   │   │   └── logging.py             # Structured logging setup
│   │   ├── domain/
│   │   │   └── models.py              # Domain enums & dataclasses
│   │   ├── models/
│   │   │   └── health_check.py        # HealthCheck ORM model
│   │   └── schemas/
│   │       └── health.py              # Pydantic response schemas
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py                # Shared fixtures
│       ├── test_config.py             # Configuration tests
│       ├── test_database.py           # Database integration tests
│       ├── test_domain.py             # Domain model tests
│       ├── test_errors.py             # Error handling tests
│       ├── test_health.py             # Health endpoint tests
│       └── test_ready.py              # Readiness endpoint tests
│
├── frontend/
│   ├── app.py                         # Streamlit application
│   └── requirements.txt               # Frontend dependencies
│
├── docs/                              # Project documentation
│   ├── module-01-problem-definition.md
│   ├── domain-model.md
│   ├── requirements.md
│   ├── risks-and-failure-modes.md
│   ├── evaluation-framework.md
│   ├── research-sources.md
│   ├── module-02-product-intelligence-specification.md
│   ├── canonical-product-model.md
│   ├── attribute-taxonomy.md
│   ├── provenance-and-evidence-model.md
│   ├── validation-and-lifecycle-model.md
│   ├── product-examples.md
│   ├── product-intelligence-schema.json
│   ├── module-03-architecture.md
│   ├── system-context.md
│   ├── container-architecture.md
│   ├── ai-pipeline.md
│   ├── rag-strategy.md
│   ├── agent-strategy.md
│   ├── knowledge-graph-strategy.md
│   ├── validation-architecture.md
│   ├── human-in-the-loop.md
│   ├── scalability.md
│   ├── security-and-trust.md
│   ├── observability.md
│   ├── technology-evaluation.md
│   ├── module-04-quality-audit.md
│   └── adr/
│       ├── ADR-001-architecture-style.md
│       ├── ADR-002-ai-orchestration-strategy.md
│       ├── ADR-003-provenance-first-data-flow.md
│       ├── ADR-004-validation-strategy.md
│       ├── ADR-005-human-review-boundaries.md
│       ├── ADR-006-rag-scope.md
│       ├── ADR-007-knowledge-graph.md
│       └── ADR-008-agent-decision.md
│
├── infrastructure/                    # (Planned) deployment configs
└── scripts/                           # (Planned) utility scripts
```

---

## Prerequisites

- **Python** 3.11 or higher
- **pip** (latest)
- **Git**

Optional (for development):
- Docker & Docker Compose
- An OpenAI API key (required for AI features in later modules)

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/unihack-product-intelligence.git
cd unihack-product-intelligence
```

### 2. Create and activate a virtual environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install backend dependencies

```bash
pip install -e .
```

### 4. Set up environment variables

```bash
cp ../.env.example .env
# Edit .env with your settings (defaults work for local development)
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the backend server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API is now running at `http://localhost:8000`. Verify with:

```bash
curl http://localhost:8000/api/v1/health
# {"status":"ok","service":"product-intelligence-api","version":"0.1.0","timestamp":"..."}
```

### 7. Start the frontend (optional)

In a new terminal:

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

The frontend is now running at `http://localhost:8501`.

---

## Backend Setup

### Development server with auto-reload

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API documentation (development mode only)

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Available endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/v1/health` | GET | Liveness check — always returns 200 if server is running |
| `/api/v1/ready` | GET | Readiness check — returns 200 if DB is accessible, 503 otherwise |

---

## Frontend Setup

The frontend is a **Streamlit** application that provides:

- Dashboard with backend connection indicator
- System status page showing service health
- Navigation sidebar

### Running the frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### Configuration

The frontend connects to the backend at `http://localhost:8000` by default. To change this:

```bash
export BACKEND_URL=http://your-backend-host:port
streamlit run app.py
```

---

## Database Migrations

This project uses **Alembic** for database schema management.

### Commands

```bash
cd backend

# Apply all migrations (create/update schema)
alembic upgrade head

# Roll back one migration
alembic downgrade -1

# Roll back to the initial state
alembic downgrade base

# View migration history
alembic history

# Show current migration state
alembic current
```

### Creating new migrations

After adding or modifying ORM models:

```bash
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

---

## Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Default | Description |
|---|---|---|
| `APP_ENV` | `development` | Application environment (`development`, `production`, `testing`) |
| `DATABASE_URL` | `sqlite:///./data/storage/product_intelligence.db` | Database connection URL |
| `APP_HOST` | `0.0.0.0` | API server host |
| `APP_PORT` | `8000` | API server port |
| `APP_DEBUG` | `false` | Enable debug mode |
| `LOG_LEVEL` | `INFO` | Logging level |
| `FRONTEND_URL` | `http://localhost:8501` | Frontend URL for CORS |
| `OPENAI_API_KEY` | *(empty)* | OpenAI API key (required for AI features) |
| `UPLOAD_DIR` | `data/uploads` | File upload directory |
| `STORAGE_DIR` | `data/storage` | Data storage directory |

---

## Running Tests

```bash
cd backend
pytest -v
```

### Running specific test files

```bash
pytest tests/test_health.py -v
pytest tests/test_ready.py -v
pytest tests/test_config.py -v
pytest tests/test_errors.py -v
pytest tests/test_database.py -v
pytest tests/test_domain.py -v
```

### Running with coverage

```bash
pytest --cov=app --cov-report=term-missing
```

---

## Running Linters

```bash
cd backend

# Lint check
ruff check .

# Auto-fix lint issues
ruff check --fix .

# Format check
ruff format --check .

# Auto-format
ruff format .

# Type check
mypy .
```

---

## Architecture

The system follows a **Hybrid Pipeline with Selective AI** architecture:

- **Backend:** FastAPI (Python 3.11+) with SQLAlchemy ORM
- **Frontend:** Streamlit for rapid prototyping
- **Database:** SQLite (development) → PostgreSQL (production)
- **Migrations:** Alembic
- **AI Strategy:** LLMs for extraction/enrichment, VLMs for image understanding, RAG for grounded retrieval
- **Validation:** Multi-layer (schema, type, unit, range, cross-field, provenance)
- **Human Review:** Selective HITL for high-uncertainty attributes

See `docs/module-03-architecture.md` for the full architecture document and `docs/adr/` for individual Architecture Decision Records.

---

## Module Progress

| Module | Status | Description |
|---|---|---|
| 1 — Problem & Domain Understanding | Complete | Problem definition, domain model, requirements, risks |
| 2 — Canonical Product Model | Complete | Data contract, attribute taxonomy, provenance model, JSON schema |
| 3 — System Architecture & AI Strategy | Complete | Architecture design, AI placements, 8 ADRs |
| 4 — Foundation & Validation Infrastructure | Complete | Backend server, DB migrations, tests, frontend shell |
| 5 — Document Intelligence & Ingestion | Pending | PDF parsing, OCR, multi-format ingestion |
| 6 — AI Extraction & Enrichment | Pending | LLM extraction, attribute normalization, conflict resolution |
| 7 — Validation & Human Review | Pending | Validation pipeline, HITL workflow |
| 8 — Integration & Polish | Pending | End-to-end flow, UI polish, performance |

---

## License

This project was developed for the Hack2Skill UniHack challenge.

---

**Built with care for trustworthy product intelligence.**
