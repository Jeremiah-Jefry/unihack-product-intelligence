# Technology Evaluation — Module 3: Architecture

**Project:** UniHack — AI-Powered Product Intelligence for Industrial Commerce  
**Document Type:** Technology Evaluation (not final selection)  
**Status:** Evaluation & Recommendations  

---

## Purpose

This document evaluates candidate technologies for each major system category. It distinguishes between:

- **Architectural decisions** — required capabilities the system must have (tool-agnostic)
- **Implementation preferences** — specific tools/libraries selected to meet those capabilities

Recommendations are made with hackathon constraints in mind: ~6 days remaining, single developer, minimal cost, local development capability, and convincing demo quality.

---

## Evaluation Criteria

Each candidate is evaluated across dimensions relevant to this project:

| Dimension | Description |
|---|---|
| **Quality** | Output quality for product intelligence tasks |
| **Reliability** | Stability, error handling, consistency |
| **Cost** | Free tier, pay-per-use, or open-source |
| **Local Dev** | Can it run locally during development? |
| **API Availability** | API access, rate limits, quotas |
| **Hackathon Fit** | Speed of integration, learning curve, demo value |
| **Deployment** | Ease of deployment to production/demo |
| **Ecosystem** | Community, docs, integrations |

---

## 1. LLM (Large Language Model)

### Architectural Requirement

The system needs an LLM capable of:
- Structured extraction from semi-structured industrial text
- Schema-constrained JSON generation
- Reasoning over technical product specifications
- Consistent, repeatable output
- Function/tool calling for agent workflows

### Candidates

| Dimension | GPT-4o | GPT-4o-mini | Claude 3.5 Sonnet | Gemini 1.5 Pro | Llama 3.1 70B |
|---|---|---|---|---|---|
| **Quality** | Excellent | Good | Excellent | Excellent | Good-Very Good |
| **Structured Output** | Strong (JSON mode, tool use) | Good | Strong (tool use) | Good | Moderate (prompt-dependent) |
| **Reasoning** | Strong | Moderate | Strong | Strong | Good |
| **Cost (per 1M tokens)** | ~$2.50 in / $10 out | ~$0.15 in / $0.60 out | ~$3 in / $15 out | ~$1.25 in / $5 out | Free (self-hosted) |
| **Rate Limits** | Generous free tier | Generous free tier | Free tier available | Free tier available | Unlimited (local) |
| **Local Dev** | No (API only) | No (API only) | No (API only) | No (API only) | Yes (GPU required) |
| **API Quality** | Excellent | Excellent | Excellent | Good | N/A |
| **Hackathon Fit** | High | High | High | Moderate | Low (infra overhead) |
| **JSON Reliability** | High | Moderate-High | High | Moderate-High | Variable |

### Recommendation

**Primary: GPT-4o-mini** — Best cost/quality ratio for hackathon. Structured JSON output is reliable enough. Free tier covers demo usage. Falls back gracefully.

**Fallback: GPT-4o** — For complex extraction tasks where mini produces lower quality. Budget allocation for critical paths only.

**Rationale:** GPT-4o-mini provides 90% of GPT-4o quality at ~10% of the cost. For a hackathon demo with limited budget, this is the right trade-off. Claude 3.5 Sonnet is excellent but pricing is less favorable. Llama 3.1 70B is eliminated due to GPU infrastructure requirements that exceed hackathon scope.

> **Decision type:** Implementation preference (GPT-4o-mini).  
> **Architectural decision:** System must support pluggable LLM backends to allow swapping models.

---

## 2. VLM (Vision-Language Model)

### Architectural Requirement

Process visual product information:
- Product images → extract visible attributes (color, shape, markings)
- Labels/packaging → OCR + semantic understanding
- Technical drawings → dimension/feature extraction
- Certifications/markings → identification and normalization

### Candidates

| Dimension | GPT-4o (Vision) | Claude 3.5 Sonnet (Vision) | Gemini 1.5 Pro (Vision) |
|---|---|---|---|
| **Image Understanding** | Excellent | Excellent | Excellent |
| **Technical Image Quality** | Strong | Strong | Strong |
| **OCR Capability** | Very Good | Very Good | Good |
| **Multi-image Processing** | Yes (native) | Yes (native) | Yes (native, large context) |
| **Cost** | Moderate | Higher | Moderate |
| **API Quality** | Excellent | Excellent | Good |
| **Hackathon Fit** | High | High | Moderate |

### Recommendation

**Primary: GPT-4o (Vision)** — Already selected as LLM fallback. Dual-use as VLM minimizes integration surface. Strong on technical image understanding.

**Rationale:** Using the same provider for LLM and VLM reduces API key management, error handling patterns, and SDK dependencies. GPT-4o vision is well-documented with extensive examples for structured extraction from images.

> **Decision type:** Implementation preference (GPT-4o).  
> **Architectural decision:** VLM processing must be abstracted behind a common interface so vision models can be swapped independently.

---

## 3. Embeddings

### Architectural Requirement

Generate vector representations for:
- Product descriptions (multi-lingual industrial terms)
- Technical specifications
- Category hierarchies
- Search queries (user intent matching)

### Candidates

| Dimension | OpenAI text-embedding-3-small | Cohere embed-v3 | BGE-M3 |
|---|---|---|---|
| **Quality** | Very Good | Excellent | Excellent |
| **Dimension** | 1536 | 1024 | 1024 |
| **Multi-lingual** | Moderate | Strong | Strong |
| **Cost** | $0.02/1M tokens | $0.1/1M tokens | Free (self-hosted) |
| **Local Dev** | No (API) | No (API) | Yes (requires ~2GB RAM) |
| **API Quality** | Excellent | Excellent | N/A |
| **Hackathon Fit** | High | Moderate | Low-Moderate |
| **Batch Support** | Yes | Yes | N/A (local) |

### Recommendation

**Primary: OpenAI text-embedding-3-small** — Already using OpenAI ecosystem. Cost is negligible. Quality is sufficient for product search and RAG.

**Future consideration: BGE-M3** — For production deployment where vendor lock-in and cost at scale matter. Not worth the infrastructure setup for hackathon.

**Rationale:** At hackathon scale (hundreds to low thousands of products), embedding cost is near-zero with OpenAI. Consolidating on one provider reduces complexity. Cohere is excellent but adds another vendor dependency.

> **Decision type:** Implementation preference (text-embedding-3-small).  
> **Architectural decision:** Embedding generation must be abstracted. Vector store must support configurable embedding dimensions.

---

## 4. Document Parsing

### Architectural Requirement

Extract structured content from industrial documents:
- PDFs (technical datasheets, catalogs, certificates)
- Preserving table structure (product specs are tabular)
- Handling multi-column layouts
- Extracting images alongside text
- Supporting scanned PDFs (OCR fallback)

### Candidates

| Dimension | PyMuPDF (fitz) | pdfplumber | LlamaParse | Unstructured.io | Docling (IBM) |
|---|---|---|---|---|---|
| **Text Extraction** | Excellent | Very Good | Excellent | Good | Very Good |
| **Table Extraction** | Good (basic) | Excellent | Very Good | Good | Excellent |
| **Layout Preservation** | Moderate | Good | Very Good | Good | Excellent |
| **Scanned PDF (OCR)** | Via integration | No (text only) | Yes (built-in) | Yes (built-in) | Yes (built-in) |
| **Speed** | Fast | Moderate | Slow (API) | Moderate | Moderate |
| **Cost** | Free | Free | Free tier + paid | Free (open source) | Free (open source) |
| **Local Dev** | Yes | Yes | Yes (with API) | Yes | Yes |
| **Image Extraction** | Yes | Limited | Yes | Yes | Yes |
| **Hackathon Fit** | High | High | Moderate | Moderate | Low |
| **Python Integration** | Excellent | Excellent | Good | Good | Good |

### Recommendation

**Primary: PyMuPDF + pdfplumber** — PyMuPDF for fast text/image extraction and general PDF handling. pdfplumber for table-heavy documents where structure matters.

**Fallback: Unstructured.io** — If document complexity exceeds what PyMuPDF/pdfplumber handle. Provides a higher-level API with partitioning strategies.

**Rationale:** PyMuPDF is fast, reliable, and handles most PDF operations. pdfplumber excels at table extraction which is critical for product specifications. Both are pure Python with no external dependencies. LlamaParse requires API calls (adds latency, cost, dependency). Docling is powerful but has heavier dependencies and longer setup — poor hackathon fit.

> **Decision type:** Implementation preference (PyMuPDF + pdfplumber).  
> **Architectural decision:** Document parser must be pluggable. System must support a fallback chain (structured extraction → table extraction → OCR).

---

## 5. OCR / Vision Processing

### Architectural Requirement

Extract text from:
- Scanned documents
- Product images with text (labels, engravings)
- Low-quality or degraded images
- Various fonts and technical notations

### Candidates

| Dimension | Tesseract | Azure Document Intelligence | Google Document AI | PaddleOCR |
|---|---|---|---|---|
| **Accuracy (printed)** | Good | Excellent | Excellent | Excellent |
| **Accuracy (handwriting)** | Poor | Good | Good | Good |
| **Table Recognition** | Poor | Excellent | Excellent | Good |
| **Speed** | Fast (local) | Moderate (API) | Moderate (API) | Fast (local) |
| **Cost** | Free | $1.50/1000 pages | $1.50/1000 pages | Free |
| **Local Dev** | Yes | No (API) | No (API) | Yes |
| **Setup Complexity** | Low | Moderate | Moderate | Moderate |
| **Hackathon Fit** | High | Moderate | Moderate | Low |
| **Docker Support** | Excellent | N/A | N/A | Good |

### Recommendation

**Primary: Tesseract** — For MVP. Fast local OCR, zero cost, sufficient accuracy for product labels and printed text. Easy Docker deployment.

**Fallback: GPT-4o Vision** — For complex layouts or when Tesseract fails. The VLM already selected can handle OCR as a secondary capability, avoiding a separate OCR pipeline for the demo.

**Rationale:** Tesseract covers 80% of OCR needs at zero cost with no API dependency. For the remaining 20% (complex layouts, degraded scans), GPT-4o Vision can handle it without introducing another service. Azure/Google Document AI are excellent for production but add cost and account setup overhead inappropriate for hackathon.

> **Decision type:** Implementation preference (Tesseract + GPT-4o Vision fallback).  
> **Architectural decision:** OCR must be a composable pipeline step, not a monolithic dependency. Confidence scoring required to trigger fallback.

---

## 6. Vector Database

### Architectural Requirement

Store and retrieve product embeddings for:
- Semantic search over product catalog
- RAG for product intelligence queries
- Similarity matching for product deduplication
- Metadata filtering (category, manufacturer, etc.)

### Candidates

| Dimension | ChromaDB | Qdrant | Pinecone | Weaviate |
|---|---|---|---|---|
| **Setup** | Trivial (pip install) | Easy (Docker or cloud) | Easy (cloud only) | Moderate (Docker) |
| **Local Dev** | Excellent | Good | Poor (cloud-dependent) | Good |
| **Performance** | Good (small scale) | Excellent | Excellent | Excellent |
| **Metadata Filtering** | Good | Excellent | Good | Excellent |
| **Cost** | Free | Free (self-hosted) | Free tier (limited) | Free (self-hosted) |
| **Persistence** | Yes | Yes | Yes (cloud) | Yes |
| **Scalability** | Limited | High | High | High |
| **Hackathon Fit** | Excellent | High | Moderate | Low |
| **Python Integration** | Excellent | Excellent | Good | Good |
| **Docker** | Optional | Easy | N/A | Moderate |

### Recommendation

**Primary: ChromaDB** — Trivial setup (`pip install chromadb`), zero infrastructure, sufficient for hackathon scale. Perfect for rapid prototyping.

**Production consideration: Qdrant** — If scale or performance becomes an issue. Easy migration path from ChromaDB with similar API patterns.

**Rationale:** ChromaDB requires zero configuration. It runs in-process during development and persists to disk. For a demo with hundreds to low-thousands of products, it performs well. Pinecone is eliminated for hackathon because it requires cloud account setup and adds network dependency during development. Weaviate is powerful but heavier than needed.

> **Decision type:** Implementation preference (ChromaDB).  
> **Architectural decision:** Vector store must support a standard interface (add, query, delete, filter) to enable migration.

---

## 7. Backend Framework

### Architectural Requirement

Serve product intelligence via:
- REST API for CRUD operations
- Streaming responses for AI generation
- Background task management
- File upload handling
- Authentication (minimal for demo)

### Candidates

| Dimension | Python (FastAPI) | Node.js (Express) |
|---|---|---|
| **AI/ML Integration** | Native (all ML libs are Python) | Requires bindings/child processes |
| **Performance** | Very Good (async, Starlette) | Good |
| **Streaming** | Excellent (SSE, WebSocket) | Good |
| **Type Safety** | Excellent (Pydantic) | Moderate (TypeScript helps) |
| **Async Support** | Excellent (async/await) | Excellent (native) |
| **Hackathon Fit** | Excellent | Moderate |
| **Ecosystem** | Excellent for AI/ML | Excellent for web |
| **Development Speed** | Fast (for this project) | Moderate |

### Recommendation

**Primary: Python (FastAPI)** — All AI/ML libraries (LLM clients, document parsers, embedding models, OCR) are Python-native. FastAPI provides excellent performance, automatic OpenAPI docs, Pydantic validation, and native async support. Zero impedance mismatch.

**Rationale:** This is fundamentally a Python project. The LLM clients, document parsers, embedding libraries, and ML tools are all Python. Using Node.js would require bridging layers for every AI component. FastAPI is the best Python web framework for this use case.

> **Decision type:** Implementation preference (FastAPI).  
> **Architectural decision:** Backend must expose a well-defined API contract (OpenAPI spec). Business logic must be decoupled from framework.

---

## 8. Frontend

### Architectural Requirement

Display and interact with product intelligence:
- Product data visualization
- AI enrichment status/results
- Search and browse interface
- Upload and processing UI (demo)

### Candidates

| Dimension | React | Next.js | Streamlit |
|---|---|---|---|
| **Development Speed** | Moderate | Moderate | Very Fast |
| **Customization** | Excellent | Excellent | Limited |
| **UI Quality** | Excellent | Excellent | Moderate |
| **Backend Integration** | Via API | Via API | Direct Python |
| **Hackathon Fit** | Moderate | Moderate | Excellent |
| **Deployment** | Separate | Separate | Bundled with backend |
| **Demo Impression** | High | High | Moderate |
| **Learning Curve** | Low-Moderate | Moderate | Very Low |

### Recommendation

**Primary (Demo): Streamlit** — Fastest path to a working demo. Direct Python integration with backend. Zero frontend build tooling. Ideal for data-centric applications.

**Production: React or Next.js** — For a real product. Not worth the time investment during hackathon unless a frontend developer is available.

**Rationale:** Streamlit allows building a functional demo UI in hours, not days. It integrates directly with Python data structures, supports real-time updates, and handles file uploads natively. The trade-off is limited customization, which is acceptable for a hackathon demo focused on backend intelligence.

> **Decision type:** Implementation preference (Streamlit for demo).  
> **Architectural decision:** Frontend must be decoupled from backend via API to allow future UI replacement.

---

## 9. Object Storage

### Architectural Requirement

Store:
- Uploaded source documents (PDFs, images)
- Processed/parsed document artifacts
- Generated product images (if applicable)
- System outputs and exports

### Candidates

| Dimension | Local Filesystem | S3 | MinIO |
|---|---|---|---|
| **Setup** | Trivial | Moderate (AWS account) | Easy (Docker) |
| **Cost** | Free | Pay-per-use | Free (self-hosted) |
| **Reliability** | Low (single disk) | Excellent | Good |
| **Scalability** | Poor | Excellent | Good |
| **Hackathon Fit** | Excellent | Low | Moderate |
| **Local Dev** | Excellent | Poor (requires cloud) | Good |
| **S3 Compatibility** | No | Native | Yes (S3-compatible) |

### Recommendation

**Primary (MVP): Local filesystem** — Simple, zero-cost, immediate. Organized directory structure under a project `data/` directory.

**Production: MinIO** — S3-compatible, runs locally via Docker, easy migration from local filesystem. Preserves the S3 API interface for eventual cloud deployment.

**Rationale:** For a hackathon demo, local filesystem is sufficient. The number of documents is small. MinIO provides a clean upgrade path without changing application code (S3-compatible API).

> **Decision type:** Implementation preference (local filesystem for MVP).  
> **Architectural decision:** Storage must be accessed through an abstraction layer (interface) to enable backend swapping.

---

## 10. Orchestration

### Architectural Requirement

Coordinate multi-step product intelligence workflows:
- Document parsing → extraction → validation → storage
- Parallel processing of multiple documents
- Error recovery and retry
- State management for long-running tasks
- Visibility into pipeline progress

### Candidates

| Dimension | Python (direct) | Celery | Temporal |
|---|---|---|---|
| **Complexity** | Very Low | Moderate | High |
| **Reliability** | Low (manual) | Good | Excellent |
| **Error Handling** | Manual | Built-in (retries) | Built-in (replay) |
| **State Management** | Manual | Limited | Excellent |
| **Local Dev** | Trivial | Moderate (requires Redis) | Complex |
| **Hackathon Fit** | Excellent | Moderate | Poor |
| **Learning Curve** | None | Low-Moderate | High |
| **Deployment** | Trivial | Moderate | Complex |

### Recommendation

**Primary (Hackathon): Python direct** — Simple sequential/async pipeline orchestration. Use Python's `asyncio` for concurrent operations. Manual state management via database status fields.

**Production: Temporal** — For production reliability, observability, and error recovery. Not worth the setup time during hackathon.

**Rationale:** For a single-developer hackathon, the overhead of setting up Celery (requires Redis/RabbitMQ) or Temporal (requires server) is not justified. A well-structured Python pipeline with clear state transitions (status fields in DB) is sufficient and more debuggable under time pressure.

> **Decision type:** Implementation preference (Python direct for hackathon).  
> **Architectural decision:** Pipeline must be designed as composable steps with clear input/output contracts to enable future orchestration framework adoption.

---

## 11. Queue / Background Processing

### Architectural Requirement

Handle:
- Document processing jobs (can be slow)
- Non-blocking API responses
- Progress updates to frontend
- Job status tracking

### Candidates

| Dimension | Redis Queue (rq) | Celery | BullMQ | In-process (asyncio) |
|---|---|---|---|---|
| **Setup** | Easy (pip + Redis) | Moderate (Redis/RabbitMQ) | Moderate (Node.js + Redis) | Trivial |
| **Reliability** | Good | Excellent | Good | Low |
| **Concurrency** | Good | Excellent | Excellent | Limited |
| **Local Dev** | Easy (Redis required) | Moderate | Moderate (Node.js) | Trivial |
| **Hackathon Fit** | Moderate | Low | Low | Excellent |
| **Monitoring** | Basic (Flower for Celery) | Excellent (Flower) | Good | Manual |

### Recommendation

**Primary (Hackathon): In-process asyncio** — Background tasks via `asyncio.create_task` or `concurrent.futures`. Job status tracked in database. Sufficient for demo with low concurrent load.

**Production: Redis Queue (rq)** — If background processing needs exceed asyncio capabilities. Simple, Python-native, minimal setup.

**Rationale:** For a hackathon demo, the system will process documents sequentially or in small batches. asyncio provides sufficient concurrency without infrastructure overhead. Redis Queue is the natural upgrade path if needed.

> **Decision type:** Implementation preference (asyncio for hackathon).  
> **Architectural decision:** Background processing must be abstracted behind a task interface to enable queue system adoption later.

---

## Consolidated Technology Stack

### Hackathon MVP Stack

| Layer | Technology | Justification |
|---|---|---|
| **LLM** | GPT-4o-mini (primary), GPT-4o (fallback) | Cost-effective, reliable structured output |
| **VLM** | GPT-4o (Vision) | Dual-use with LLM, strong visual understanding |
| **Embeddings** | OpenAI text-embedding-3-small | Ecosystem consolidation, negligible cost |
| **Document Parsing** | PyMuPDF + pdfplumber | Fast, free, local, excellent table extraction |
| **OCR** | Tesseract + GPT-4o Vision fallback | Free local OCR + AI fallback for complex cases |
| **Vector DB** | ChromaDB | Zero-config, local, sufficient for demo scale |
| **Backend** | Python + FastAPI | Native AI/ML integration, excellent async |
| **Frontend** | Streamlit | Fastest demo development, Python-native |
| **Storage** | Local filesystem | Zero setup, sufficient for demo |
| **Orchestration** | Python (asyncio) | No infrastructure overhead |
| **Background Tasks** | In-process asyncio | Sufficient for demo load |

### External Dependencies (API Keys Required)

| Service | Purpose | Free Tier |
|---|---|---|
| OpenAI API | LLM, VLM, Embeddings | $5 credit for new accounts |
| — | No other API keys required for MVP | — |

### Infrastructure Requirements

| Component | Requirement |
|---|---|
| Python | 3.11+ |
| Tesseract OCR | System-level install |
| Redis | Not required for MVP |
| Docker | Optional (for consistent env) |
| GPU | Not required |

---

## Key Architectural Decisions (Tool-Agnostic)

These decisions hold regardless of specific tool choices:

1. **Pluggable LLM backend** — Model provider must be swappable without code changes
2. **Composable document parsing pipeline** — Parser must be a step in a chain, not a monolith
3. **Standard vector store interface** — CRUD + search operations must follow a common contract
4. **Storage abstraction** — File storage behind an interface for backend swapping
5. **API-first design** — Backend exposes OpenAPI contract; frontend is replaceable
6. **Pipeline step contracts** — Each processing step has defined input/output schemas
7. **Confidence-aware fallback** — OCR/extraction failures trigger higher-capability fallbacks

---

## Risk Register (Technology-Specific)

| Risk | Impact | Mitigation |
|---|---|---|
| OpenAI rate limits during demo | High | Implement retry with backoff; cache results |
| Tesseract accuracy insufficient | Medium | GPT-4o Vision as fallback |
| ChromaDB memory usage at scale | Low | Sufficient for hackathon; migrate to Qdrant if needed |
| Streamlit limitations for complex UI | Medium | Accept demo-quality UI; document future React path |
| OpenAI free tier exhaustion | High | Budget monitoring; use mini model aggressively |
| Document parsing edge cases | Medium | Fallback chain: PyMuPDF → pdfplumber → Unstructured |

---

## Open Questions

1. **Multi-tenancy** — Is the demo single-tenant? (Assumed yes for hackathon)
2. **Authentication** — Is any auth required for demo? (Assumed minimal/no for hackathon)
3. **Deployment target** — Where will the demo be deployed? (Affects storage and orchestration choices)
4. **Concurrent users** — How many simultaneous users expected? (Affects queue/orchestration needs)

---

*This document is an evaluation, not a final commitment. Specific versions and configurations will be locked during implementation. All architectural decisions (tool-agnostic) are stable; implementation preferences may change based on integration experience.*
