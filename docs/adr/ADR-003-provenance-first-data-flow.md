# ADR-003: Provenance-First Data Flow

**Status:** Accepted
**Date:** 2026-08-18
**Deciders:** Project Owner

---

## Context

Every product attribute must be traceable to its source. The system ingests fragmented, potentially contradictory information from multiple sources. Without provenance, any output value is unverifiable and therefore untrustworthy.

---

## Problem

How to ensure provenance is never lost or disconnected from the values it supports as data flows through the pipeline?

---

## Alternatives

- **A) Provenance at output** — Attach provenance only when generating the final product record, inferring source links from the pipeline history.
- **B) Provenance at extraction** — Attach provenance at the point of extraction and carry it through every pipeline stage. Every transformation preserves the original value.
- **C) Provenance as a side channel** — Store provenance separately and join it with values at query time using identifiers.

---

## Decision

**B) Provenance at extraction** — Provenance is attached at the point of extraction and carried through every pipeline stage. Every transformation preserves the original value. Evidence is co-located with attributes in storage.

---

## Rationale

Provenance is a core requirement (CC-01, R-25, R-26). Without provenance, values are unverifiable. Attaching provenance at extraction and preserving it through the pipeline is the only way to guarantee traceability.

Co-locating evidence with attributes in storage ensures that provenance is never orphaned. Every value in the canonical record is directly linkable to its source, extraction method, confidence, and any contradictions found.

---

## Consequences

**Positive:**
- Every value is traceable to its source.
- Reviewers can verify any value against its original evidence.
- Contradictions between sources are detectable and resolvable.
- The system can explain why a value was chosen over alternatives.

**Negative:**
- Storage overhead for provenance metadata.
- Pipeline must be careful not to lose provenance during transformations.
- Every pipeline stage must accept and propagate provenance alongside data.

---

## Rejected Alternatives

- **Provenance at output** — Inferring provenance from pipeline history after the fact is unreliable. Transformation steps may lose the link between a value and its source.
- **Provenance as a side channel** — Separating provenance from values creates a risk of orphaned records. Join operations at query time are error-prone and add latency.
