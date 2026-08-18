# ADR-002: AI Orchestration Strategy

**Status:** Accepted
**Date:** 2026-08-18
**Deciders:** Project Owner

---

## Context

The system uses AI in multiple pipeline stages: extraction from unstructured text, classification, enrichment, and validation. The pipeline must remain deterministic and auditable while leveraging AI where it provides genuine value.

---

## Problem

Should AI components be fully autonomous (agents) or embedded within a deterministic pipeline?

---

## Alternatives

- **A) Fully autonomous agents** — Each AI-powered stage is an independent agent with its own planning, execution, and evaluation loop.
- **B) Embedded AI components** — AI is called as a function within a deterministic pipeline. The pipeline controls sequencing, error handling, and validation.
- **C) Hybrid orchestration** — Mostly embedded AI with one specialized agent for a stage that genuinely requires autonomous multi-step reasoning.

---

## Decision

**C) Hybrid orchestration** — Embedded AI components within a deterministic pipeline, with one enrichment agent as an optional enhancement.

---

## Rationale

Deterministic orchestration provides predictable behavior, testability, and auditability. Most pipeline stages (extraction, normalization, validation) are best served by embedded AI that returns structured output for deterministic post-processing.

The enrichment agent is justified as an exception. Enrichment requires autonomous multi-step reasoning: searching external sources, evaluating relevance, resolving conflicts, and deciding what evidence is trustworthy. This is inherently an agentic task where rigid pipeline control would limit effectiveness.

---

## Consequences

**Positive:**
- Most pipeline stages are deterministic and testable.
- Agent behavior is isolated to one component, limiting non-determinism.
- Clear interfaces between deterministic and AI components.

**Negative:**
- Agent behavior is harder to test and requires dedicated evaluation.
- Requires well-defined handoff protocols between deterministic and agent components.
- Agent failures must not block the pipeline — graceful degradation is required.

---

## Rejected Alternatives

- **Fully autonomous agents** — Excessive non-determinism across the entire pipeline. Testing and auditing become prohibitively difficult. No clear benefit for stages that follow well-defined rules.
- **Embedded AI only (no agent)** — The enrichment stage genuinely requires autonomous reasoning over external sources. Embedding it as a single function call would limit its effectiveness.
