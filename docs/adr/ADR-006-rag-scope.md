# ADR-006: RAG Scope

**Status:** Accepted
**Date:** 2026-08-18

## Context

RAG (Retrieval-Augmented Generation) is mentioned as a key technology in the project. It is a powerful technique for grounding language model outputs in retrieved evidence. However, its applicability varies depending on the task. The system has multiple distinct capabilities: extraction from provided documents, validation, conflict resolution, and enrichment of missing data. Each capability has different requirements.

## Problem

Should RAG be the primary architecture for the entire system, or a targeted capability for specific tasks?

## Decision

RAG is a **targeted capability for enrichment only**. It is NOT the primary architecture.

**RAG is used for:**
- Filling missing attributes when input data is minimal (e.g., a product name with no specifications)
- Retrieving relevant technical standards or specifications from indexed reference sources
- Providing supplementary information during enrichment

**RAG is NOT used for:**
- Primary extraction from provided documents (requires document parsing, not retrieval)
- Validation (requires deterministic rules, not similarity search)
- Conflict resolution (requires evidence comparison, not retrieval)
- Schema enforcement (requires structural validation, not semantic retrieval)

## Rationale

RAG excels at retrieving relevant information from indexed sources and grounding generation in evidence. This is genuinely useful for enrichment: when a product has minimal input data, retrieving similar products or technical specifications from an indexed knowledge base can fill gaps.

However, RAG is a poor fit for the other core capabilities:
- **Extraction from provided documents** requires parsing structured or semi-structured documents (PDFs, datasheets, spec sheets). This is a document understanding problem, not a retrieval problem.
- **Validation** requires deterministic rule evaluation (schema checks, type checks, range checks, cross-field consistency). Similarity search does not produce deterministic validation outcomes.
- **Conflict resolution** requires comparing evidence from multiple sources, assessing provenance, and determining which values are supported. This is an evidence evaluation problem.

Using RAG as the primary architecture would mean forcing every capability through a retrieval-then-generate pattern, which would be a misuse of the technology and would produce worse outcomes than purpose-built approaches for each capability.

## Consequences

**Positive:**
- RAG is used where it genuinely provides value (enrichment of sparse data)
- Clear scope prevents misuse of RAG for tasks it cannot handle well
- Each capability can use the most appropriate technology
- Extraction pipeline, validation engine, and enrichment agent remain independent and testable

**Negative:**
- Requires a separate extraction pipeline (not just RAG) — more components to build
- More architectural complexity than a single-approach system
- RAG index must be maintained and kept current
- Enrichment quality depends on index coverage and retrieval quality

## Rejected Alternatives

- **RAG as primary architecture:** Rejected because extraction, validation, and conflict resolution are not retrieval problems. Forcing RAG into these roles would degrade quality.
- **No RAG at all:** Rejected because enrichment genuinely benefits from retrieval. When input data is sparse, retrieval from indexed sources provides valuable grounding.
