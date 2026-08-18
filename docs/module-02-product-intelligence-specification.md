# Module 02 — Product Intelligence Specification

> **Status:** Complete  
> **Module:** 2 — Canonical Product Intelligence Model & Data Contract  
> **Purpose:** Define the implementation-independent contract that all later AI, backend, and API components must respect.  
> **Depends on:** All Module 1 documents

---

## 1. Purpose

This document defines the canonical representation of an industrial product that our system will create, enrich, validate, review, store, and expose.

It answers:

> "What exactly do we need to know about a product, how do we represent it, and how do we know where each piece of information came from?"

This is **not** a database schema. This is **not** an API design. This is the **domain contract** that all later implementation decisions must satisfy.

---

## 2. Scope

### In Scope

- Canonical product record structure
- Core vs. category-specific fields
- Attribute model with provenance, confidence, validation
- Value types (measurements, ranges, enumerations)
- Unit normalization contract
- Provenance and evidence model
- Contradiction representation
- Information category classification
- Attribute lifecycle states
- Quality scoring model
- Missing data representation

### Out of Scope

- Technology selection (databases, LLMs, frameworks)
- API endpoints or request/response formats
- UI/UX design
- Pipeline implementation
- Specific taxonomy mappings (ETIM, UNSPSC, eCl@ss) — the contract supports them; the mappings are implementation details

---

## 3. Design Principles

### 3.1 Evidence First

Every attribute value must be traceable to source evidence. The system must never produce a value without knowing where it came from and how it was obtained.

### 3.2 Honest Uncertainty

The system must distinguish between what it knows, what it has normalized, what it has derived, what it has enriched from external sources, what it has inferred, and what it does not know. These are fundamentally different epistemic states.

### 3.3 Contradictions Are Data

When two sources disagree, the conflict itself is information. The model must represent multiple candidate values simultaneously. Never silently overwrite one source with another.

### 3.4 Category-Aware but Not Category-Hardcoded

The model must support products with very different attribute sets (motors vs. valves vs. sensors) without requiring a new schema for each category. Category-specific attributes are handled through an extensible attribute system, not through schema changes.

### 3.5 Minimal Core, Extensible Periphery

A small set of core fields applies to almost all products. Everything else is category-specific and handled through the attribute system. The core is rigid; the periphery is flexible.

### 3.6 Traceable Information Categories

Provenance must not only track where a value came from, but also what type of information it represents (identity, specification, certification, safety, commercial, etc.). This enables downstream systems to make trust decisions based on information type.

### 3.7 Source Freshness Is Mandatory

The model must preserve enough information to determine whether evidence is current, outdated, unknown, or requires re-verification. Stale evidence is a first-class concern.

---

## 4. Core Concepts

### 4.1 Product

The central entity. A distinct, purchasable industrial item that can be identified, described, and transacted.

### 4.2 Product Intelligence Record

The structured, validated, provenance-tracked representation of a product within the system. This is the "golden record" that all extraction, enrichment, validation, and review processes produce.

### 4.3 Attribute

An atomic piece of product information. Every attribute has a name, a value (or set of candidate values), provenance data, confidence, validation state, and information category. Attributes are the units of quality measurement.

### 4.4 Evidence

The chain of provenance connecting an attribute value to its source. Evidence includes: where the value came from, how it was obtained, when it was captured, and how trustworthy the source is.

### 4.5 Source Document

Any input that contains product information — PDF, web page, CSV, image, scanned document, ERP export. Source documents are the evidence base.

### 4.6 Category

A node in a product taxonomy that determines which attributes are required. Classification is a prerequisite for completeness measurement.

### 4.7 Channel

A destination where product data is published — a marketplace, e-commerce site, distributor portal. Each channel has specific data requirements.

---

## 5. Key Decisions

### 5.1 Attribute-Centric Model

**Decision:** The product record is built around an attribute abstraction, not flat fields.

**Rationale:** Industrial products have wildly different attribute sets. A bearing needs bore diameter and load rating. A valve needs port size and pressure rating. A flat model with 500 fields would be unwieldy and mostly empty. An attribute-centric model is extensible by design.

**Trade-off:** More complex to query than flat fields. Requires attribute schema definitions to measure completeness. But this complexity is necessary for the problem domain.

### 5.2 Multi-Candidate Values

**Decision:** An attribute may have multiple candidate values from different sources, with conflict status tracked.

**Rationale:** Real-world data is contradictory. Source A says 12 kg, Source B says 13.5 kg. The model must represent both until a human or evidence-based rule resolves the conflict. Silent overwriting is prohibited.

**Trade-off:**增加了复杂性，但这是处理现实世界数据矛盾的唯一诚实方式。

### 5.3 Information Category on Provenance

**Decision:** Each provenance record includes an information category (identity, specification, certification, safety, commercial, classification, relationship, description, media).

**Rationale:** Not all evidence is equally trustworthy. A manufacturer's datasheet is authoritative for specifications but not for commercial attributes. Information category enables downstream systems to weight evidence by type.

### 5.4 Source Freshness as First-Class

**Decision:** Every source document has a timestamp, and every provenance record tracks source freshness.

**Rationale:** Stale data is a silent killer. A product's certification may have expired; a specification may have been revised. Without freshness tracking, the system cannot know when to re-verify.

### 5.5 Lifecycle States for Attributes

**Decision:** Attributes have explicit lifecycle states (discovered, extracted, normalized, validated, enriched, reviewed, approved, rejected).

**Rationale:** The system must know where each attribute is in its journey from raw extraction to trusted intelligence. This enables smart routing, audit trails, and quality measurement.

---

## 6. Open Questions

These are questions that cannot be fully resolved at the domain model level and will be addressed in Module 3 (Architecture):

1. **Storage:** How should attribute provenance be stored for efficient querying at scale?
2. **Conflict resolution:** What automated rules can resolve conflicts without human review?
3. **Schema evolution:** How should category schemas be updated without breaking existing records?
4. **Multi-tenancy:** Should the model support multiple organizations with isolated data?
5. **Versioning:** How should product records be versioned over time?

---

## 7. Acceptance Criteria

After reading all Module 2 documents, an engineer should be able to answer:

1. What is a product intelligence record?
2. What are its core fields?
3. How do category-specific fields work?
4. How are technical measurements represented?
5. How are units normalized?
6. How is provenance represented?
7. How are conflicting values represented?
8. How do confidence and validation differ?
9. How is human review represented?
10. How are facts, derivations, enrichment, and inference distinguished?
11. How are relationships represented?
12. How is missing information represented?
13. How can the model evolve as new product categories appear?
14. Can the model support multimodal evidence?
15. Can the model eventually support large-scale processing?

---

## 8. Document Map

| Document | Purpose |
|----------|---------|
| `canonical-product-model.md` | Detailed domain model with entities, relationships, and processes |
| `attribute-taxonomy.md` | Attribute system: categories, data types, value types, units, extensibility |
| `provenance-and-evidence-model.md` | Source, evidence, location, extraction, transformation, confidence, freshness |
| `validation-and-lifecycle-model.md` | Attribute lifecycle, validation states, conflicts, resolution, approval |
| `product-examples.md` | Realistic examples demonstrating the model works |
| `product-intelligence-schema.json` | Machine-readable representation of the canonical contract |

---

*This specification is the foundation for Module 03 (Architecture & Data Model). All implementation decisions must satisfy this contract.*
