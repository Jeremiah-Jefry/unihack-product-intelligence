# Module 3 — System Architecture: Completion Report

**Status:** COMPLETE
**Date:** 2026-08-18

---

## 1. Executive Architecture Summary

The system uses a hybrid pipeline architecture with a deterministic core and AI at decision points. Key architectural properties:

- **Provenance-first design:** every value traces to source evidence
- **Four-layer validation:** deterministic → evidence-based → AI-assisted → human
- **Confidence-based routing** minimizes human review burden
- **Multi-candidate values** with explicit conflict tracking

---

## 2. Recommended Architecture

**Architecture D — Hybrid Pipeline with Selective AI** (from alternatives analysis)

| Concern | Implementation |
|---|---|
| Ingestion, normalization, validation, quality scoring | Deterministic (Python) |
| Extraction, classification, enrichment, conflict analysis | AI components (LLM/VLM) |
| Enrichment | One optional agent |
| Knowledge graph | Structured relationships only (no KG for MVP) |

---

## 3. Key Architectural Decisions (ADRs)

| ADR | Decision | Rationale |
|---|---|---|
| ADR-001 | Hybrid pipeline architecture | Best balance of determinism and AI flexibility |
| ADR-002 | Embedded AI with one enrichment agent | Avoids multi-agent complexity for MVP |
| ADR-003 | Provenance-first data flow | Ensures traceability and trust |
| ADR-004 | Four-layer validation | Reduces error propagation |
| ADR-005 | Confidence-based human review routing | Minimizes human review bottleneck |
| ADR-006 | RAG for enrichment only | Grounds enrichment in supplier/catalog evidence |
| ADR-007 | No knowledge graph for MVP | Structured relationships are sufficient |
| ADR-008 | One enrichment agent, no multi-agent | Keeps orchestration simple |

---

## 4. Technology Recommendations

Recommended MVP stack (from `docs/technology-evaluation.md`):

| Layer | Technology | Purpose |
|---|---|---|
| LLM (extraction) | GPT-4o-mini | Attribute extraction from text |
| LLM (reasoning) | GPT-4o | Complex reasoning, conflict analysis |
| VLM | GPT-4o (vision) | Image/label understanding |
| Embeddings | OpenAI text-embedding-3-small | RAG retrieval |
| Document Parsing | PyMuPDF + pdfplumber | PDF text and table extraction |
| OCR | Tesseract (local) + GPT-4o vision (fallback) | Scanned document handling |
| Vector DB | ChromaDB (local) | Evidence and document storage |
| Backend | Python + FastAPI | API and pipeline orchestration |
| Frontend | Streamlit (demo) | Human review interface |
| Storage | Local filesystem (MVP) | Product records and evidence |
| Orchestration | Python (direct) for MVP | Pipeline execution |

---

## 5. AI Component Decisions

| AI Technology | Role in System | Decision |
|---|---|---|
| LLM | Extraction, classification, enrichment, conflict analysis | CORE |
| VLM | Image and label understanding | IMPORTANT |
| RAG | Enrichment (grounded retrieval from supplier catalogs) | IMPORTANT |
| Knowledge Graph | Entity relationship modeling | NOT REQUIRED (MVP) |
| AI Agents | Enrichment orchestration (optional) | OPTIONAL |
| Human-in-the-Loop | Review interface, approval, corrections | CORE |
| Document Intelligence | PDF parsing, table extraction, OCR | CORE |

---

## 6. MVP Boundary

| Stage | Scope |
|---|---|
| Input | PDF datasheets, CSV supplier feeds |
| Extraction | LLM-based attribute extraction |
| Classification | LLM-based product classification |
| Normalization | Deterministic unit conversion |
| Evidence | Full provenance chain |
| Validation | Deterministic (schema, type, range, cross-field) |
| Conflict detection | Cross-source comparison |
| Human review | Evidence-based review interface |
| Output | JSON product records with provenance and quality metrics |
| Evaluation | 20+ products across 3 categories |

---

## 7. Scaling Path

| Phase | Volume | Processing Model |
|---|---|---|
| MVP | 1–10 products | Sequential |
| Demo | 10–100 products | Batch processing |
| Production | 100–1,000 products | Worker pools |
| Scale | 1,000–100K+ products | Distributed |

---

## 8. Critical Risks

1. LLM extraction accuracy may be insufficient for complex tables
2. Human review bottleneck at scale
3. Cost of LLM API calls for large catalogs
4. Confidence scoring calibration
5. Multi-product document handling complexity

---

## 9. Open Questions

1. Optimal prompt strategies for industrial document extraction
2. Confidence scoring calibration against ground truth
3. Optimal batch size for parallel processing
4. Cost optimization strategies for large catalogs

---

## 10. Files Created

### Core Architecture
- `docs/module-03-architecture.md`
- `docs/system-context.md`
- `docs/container-architecture.md`

### Pipeline and AI
- `docs/ai-pipeline.md`
- `docs/rag-strategy.md`
- `docs/agent-strategy.md`
- `docs/knowledge-graph-strategy.md`

### Quality and Operations
- `docs/validation-architecture.md`
- `docs/human-in-the-loop.md`
- `docs/scalability.md`
- `docs/security-and-trust.md`
- `docs/observability.md`

### Technology
- `docs/technology-evaluation.md`

### Architecture Decision Records
- `docs/adr/ADR-001-architecture-style.md`
- `docs/adr/ADR-002-ai-orchestration-strategy.md`
- `docs/adr/ADR-003-provenance-first-data-flow.md`
- `docs/adr/ADR-004-validation-strategy.md`
- `docs/adr/ADR-005-human-review-boundaries.md`
- `docs/adr/ADR-006-rag-scope.md`
- `docs/adr/ADR-007-knowledge-graph-decision.md`
- `docs/adr/ADR-008-agent-decision.md`

**Total: 21 files**

---

## 11. Module 4 Readiness

- Architecture is complete and consistent with Module 1 requirements and Module 2 domain model
- Technology recommendations are made but not finalized (implementation preference, not architectural decision)
- All P0 requirements map to architectural capabilities
- All Module 2 concepts have a place in the architecture
- Ready for Module 4 (Implementation)
