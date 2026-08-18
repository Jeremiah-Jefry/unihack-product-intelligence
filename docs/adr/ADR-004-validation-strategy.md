# ADR-004: Validation Strategy

**Status:** Accepted
**Date:** 2026-08-18
**Deciders:** Project Owner

---

## Context

The system must validate product data at multiple levels: structural correctness, type safety, unit normalization, cross-field consistency, source quality, semantic plausibility, and business risk. Different error classes require different detection methods.

---

## Problem

How to design validation that catches different classes of errors without being too restrictive or too lenient?

---

## Alternatives

- **A) Single validation pass** — One comprehensive validation step that checks all error classes at once.
- **B) Deterministic-only validation** — Only run schema, type, and rule-based validation. Flag issues for human review.
- **C) Four-layer validation** — Deterministic (blocking), Evidence-based (warning), AI-assisted (warning), Human (decision). Layers execute in order; each layer can only escalate, not de-escalate.
- **D) AI-first validation** — Use LLMs as the primary validation mechanism, with deterministic checks as a safety net.

---

## Decision

**C) Four-layer validation** — Deterministic (blocking), Evidence-based (warning), AI-assisted (warning), Human (decision). Layers execute in order; each layer can only escalate, not de-escalate.

---

## Rationale

Different error classes require different detection methods:

1. **Deterministic (blocking):** Schema validation, type checking, unit normalization, required-field presence. Catches obvious errors cheaply and reproducibly.
2. **Evidence-based (warning):** Verifies source quality, freshness, contradiction detection, confidence thresholds. Flags values that lack sufficient evidence.
3. **AI-assisted (warning):** Catches semantic issues — implausible values, cross-field inconsistencies, hallucinated attributes. Uses LLM judgment as a signal, not a verdict.
4. **Human (decision):** High-risk decisions that require domain expertise — contradictory sources, unverifiable claims, values with meaningful business impact.

The escalation-only rule ensures that a lower layer cannot override a higher layer's concern. A deterministic error cannot be silenced by a later AI check passing.

---

## Consequences

**Positive:**
- Comprehensive error detection across multiple error classes.
- Clear separation of concerns — each layer has a defined responsibility.
- Most validation is automated; human review is reserved for high-risk cases.
- Deterministic checks are fast and reproducible.

**Negative:**
- Four layers add complexity to the pipeline.
- Requires well-defined rules per layer.
- AI-assisted validation introduces non-determinism in warning generation.
- Human layer requires a review interface and workflow.
