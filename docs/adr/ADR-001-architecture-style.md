# ADR-001: Architecture Style

**Status:** Accepted
**Date:** 2026-08-18
**Deciders:** Project Owner

---

## Context

The system must transform fragmented industrial product information into structured, validated, provenance-tracked, commerce-ready product intelligence. The source material is unreliable, incomplete, and multimodal. The system must produce trustworthy output with traceability to original sources, not just plausible-looking results.

---

## Problem

What architectural style best serves the requirements of correctness, traceability, validation, and selective AI usage?

---

## Alternatives

- **A) Simple LLM pipeline** — A linear chain of LLM calls that extract, normalize, and enrich product data using prompt engineering alone.
- **B) RAG-centric pipeline** — A system built around retrieval-augmented generation where an LLM retrieves relevant context and generates structured output.
- **C) Fully agentic system** — An autonomous multi-agent system where agents plan, execute, and reason through the product intelligence workflow.
- **D) Hybrid pipeline with selective AI** — A deterministic core pipeline (ingestion, normalization, validation, quality scoring) with AI embedded at specific decision points where it genuinely adds value (extraction from unstructured text, classification, enrichment).

---

## Decision

**D) Hybrid pipeline with selective AI** — deterministic core with AI at decision points.

---

## Rationale

The core pipeline stages (ingestion, normalization, validation, quality scoring) must be deterministic for correctness and auditability. AI is deployed where it genuinely adds value: extracting structured attributes from unstructured text, classifying products into categories, and enriching incomplete records. Every AI output is validated before entering the canonical record.

This aligns with the project principle that AI output is not automatically truth. A deterministic core ensures the system is testable, reproducible, and auditable. AI at the edges is replaceable — if a better extraction model becomes available, only that component needs to change.

---

## Consequences

**Positive:**
- Deterministic core is testable and auditable.
- AI components are replaceable without rearchitecting the system.
- Each component has a single, clear responsibility.

**Negative:**
- More complex than a pure-LLM approach.
- Requires careful boundary definition between deterministic and AI components.
- Integration testing must cover both deterministic and AI paths.

---

## Rejected Alternatives

- **Simple LLM pipeline** — No provenance tracking, no validation layer, no auditability. Output quality is entirely dependent on prompt quality with no structural guarantees.
- **RAG-centric pipeline** — Insufficient for extraction from fragmented sources. RAG assumes information exists and can be retrieved; the core challenge here is extraction and synthesis, not retrieval.
- **Fully agentic system** — Non-deterministic behavior makes auditability and validation extremely difficult. Overkill for a pipeline where most stages follow well-defined rules.
