# Validation and Lifecycle Model

> **Status:** Complete  
> **Module:** 2 — Canonical Product Intelligence Model & Data Contract  
> **Purpose:** Define attribute lifecycle, validation states, conflicts, resolution, and approval.  
> **Depends on:** `canonical-product-model.md`, `provenance-and-evidence-model.md`

---

## 1. Overview

This document defines how product attributes move through the system, how they are validated, how conflicts are handled, and how human review is represented.

---

## 2. Attribute Lifecycle

### 2.1 Lifecycle States

An attribute moves through these states:

```
DISCOVERED
    │
    ▼
EXTRACTED
    │
    ▼
NORMALIZED ──▶ ENRICHED
    │              │
    ▼              ▼
VALIDATED ◀──────┘
    │
    ▼
REVIEWED (if needed)
    │
    ▼
APPROVED
```

### 2.2 State Definitions

| State | Description | Entry conditions |
|-------|-------------|-----------------|
| `discovered` | Attribute identified in source but not yet extracted | Source document identified, attribute location known |
| `extracted` | Value extracted from source with confidence score | Extraction method applied, confidence calculated |
| `normalized` | Value converted to canonical representation | Unit conversion or terminology mapping applied |
| `enriched` | Value obtained from additional external source | External source consulted, value retrieved |
| `validated` | Value passed automated validation checks | Schema, type, range, cross-field checks passed |
| `reviewed` | Value reviewed by human reviewer | Human reviewer examined evidence and made decision |
| `approved` | Value approved for use in commerce | Human approved or auto-approved (high confidence + validation pass) |
| `rejected` | Value rejected as incorrect | Human rejected or auto-rejected (low confidence + validation fail) |

### 2.3 State Transitions

| From | To | Trigger | Required evidence |
|------|-----|---------|-------------------|
| discovered → extracted | Extraction applied | Source location, extraction method, confidence |
| extracted → normalized | Normalization applied | Original value, transformation record |
| extracted → enriched | External enrichment | External source, enrichment method |
| normalized → validated | Validation checks pass | Validation results |
| enriched → validated | Validation checks pass | Validation results |
| validated → reviewed | Human review required | Review reason, reviewer assignment |
| reviewed → approved | Human approves | Reviewer decision, review notes |
| reviewed → rejected | Human rejects | Reviewer decision, rejection reason |
| validated → approved | Auto-approval criteria met | High confidence + all validation passes |
| any → rejected | Critical failure | Failure reason, evidence |

### 2.4 State Invariants

1. **No skipping.** An attribute cannot jump from `discovered` to `approved` without passing through extraction and validation.
2. **Regression requires reason.** Moving from `approved` back to `reviewed` or `rejected` requires explicit reason and audit trail.
3. **Rejected is terminal.** Once rejected, an attribute cannot be re-approved without a new extraction or correction.
4. **Review is mandatory for low confidence.** Attributes with confidence < 0.7 must go through human review.
5. **Missing attributes use `discovered` state.** When an attribute has a `missing_status` (NOT_PROVIDED, NOT_APPLICABLE, NOT_DISCOVERED, etc.), its `lifecycle_state` is `discovered`. This indicates the system has acknowledged the attribute's absence but has not extracted a value. Missing attributes do not advance through the lifecycle until a value is provided.

---

## 3. Validation Model

### 3.1 Validation Layers

| Layer | What it checks | Automation | Blocking? |
|-------|---------------|------------|-----------|
| **Schema validation** | Are all required fields present? | Fully automated | Yes |
| **Type validation** | Is the value the correct data type? | Fully automated | Yes |
| **Unit validation** | Does the value have correct units? | Fully automated | Yes |
| **Range validation** | Is the value within physically possible bounds? | Automated | Yes (for clear violations) |
| **Cross-field consistency** | Do related fields agree? | Automated | Warning (may block) |
| **Cross-source agreement** | Do multiple sources agree? | Automated detection | Warning |
| **Contradiction detection** | Do sources give conflicting values? | Automated detection | Warning (blocks publication) |
| **Source verification** | Does the source exist and is accessible? | Automated | Yes |
| **Freshness check** | Is the source recent enough? | Automated | Warning (may block) |
| **Provenance check** | Does the value have traceable source? | Automated | Yes (for critical attributes) |
| **Category-specific rules** | Does this product type have required attributes? | Automated if schema defined | Yes |
| **Channel-specific rules** | Does the record meet channel requirements? | Automated if rules defined | Yes |

### 3.2 Validation Results

Each validation check produces:

| Field | Type | Description |
|-------|------|-------------|
| `layer` | string | Which validation layer |
| `passed` | boolean | Did the check pass? |
| `severity` | enum | blocking, warning, info |
| `message` | string | Human-readable message |
| `attribute_id` | UUID | Which attribute was checked (if applicable) |
| `details` | map | Additional details |

### 3.3 Validation Status

| Status | Description |
|--------|-------------|
| `pending` | Not yet validated |
| `auto_validated` | Passed all automated checks |
| `human_validated` | Reviewed and approved by human |
| `rejected` | Failed critical validation checks |

---

## 4. Conflict Model

### 4.1 What Is a Conflict

A conflict exists when multiple candidate values for the same attribute cannot be automatically reconciled. The system must represent all candidates and track the conflict.

### 4.2 Conflict Types

| Type | Description | Example |
|------|-------------|---------|
| `value_mismatch` | Different values from different sources | Source A: 12 kg, Source B: 13.5 kg |
| `unit_mismatch` | Same value, different units (not convertible) | Source A: "3/8 in", Source B: "3/8 mm" |
| `source_contradiction` | Sources explicitly contradict each other | Source A: "CE marked", Source B: "No CE marking" |
| `stale_vs_current` | Old and new values conflict | 2023 datasheet vs 2025 datasheet |

### 4.3 Conflict Representation

When a conflict is detected:

1. All candidate values are preserved with their sources.
2. A Conflict record is created.
3. The attribute's `conflict_status` is set to `pending_resolution`.
4. No candidate is selected as the winner until resolution.
5. The conflict is flagged for human review (unless automated resolution rules apply).

### 4.4 Conflict Resolution Methods

| Method | Description | When to use |
|--------|-------------|-------------|
| `source_priority` | Prefer manufacturer over distributor over third-party | When source trust levels differ significantly |
| `confidence_based` | Select the candidate with highest extraction confidence | When extraction quality differs |
| `human_decision` | Human reviewer selects the correct value | When automated resolution is not safe |
| `rule_based` | Apply a defined rule (e.g., "newest wins") | When rules are established and safe |
| `newest_wins` | Prefer the most recent source | When source freshness is the primary factor |

### 4.5 Conflict Resolution Record

| Field | Type | Description |
|-------|------|-------------|
| `method` | enum | How the conflict was resolved |
| `selected_candidate_id` | UUID | Which candidate was selected |
| `reason` | string | Why this candidate was selected |
| `resolved_by` | string | Who/what resolved it |
| `resolved_at` | timestamp | When the resolution was recorded |
| `rejection_candidates` | list<UUID> | Which candidates were rejected |

### 4.6 Permanently Conflicting

Some conflicts cannot be resolved automatically and require human decision:
- Safety-critical attributes (always human review)
- Certifications (manufacturer claims vs. third-party verification)
- Conflicting manufacturer data (different product versions)

These are marked as `permanently_conflicting` until human intervention.

---

## 5. Human Review Model

### 5.1 Review Routing

Attributes are routed to human review when:

| Condition | Reason |
|-----------|--------|
| Confidence < 0.7 | Low extraction confidence |
| Conflict detected | Sources disagree |
| Safety-critical attribute | Safety information always needs review |
| Certification attribute | Certifications need verification |
| Derived value | Computed values need verification |
| Inference | AI-generated values need verification |
| Freshness concern | Source may be outdated |

### 5.2 Review Interface Data

When presenting an attribute for review, the system provides:

1. **The attribute name and domain**
2. **All candidate values** with their sources
3. **Source locations** (page, section, text span)
4. **Extraction confidence** for each candidate
5. **Source trust scores** for each source
6. **Freshness status** for each source
7. **Information category** (what type of information this is)
8. **Related attributes** (for context)
9. **Validation results** (what checks passed/failed)

### 5.3 Review Actions

| Action | Description | Effect |
|--------|-------------|--------|
| `approve` | Approve the selected value | Attribute moves to `approved` |
| `reject` | Reject the value | Attribute moves to `rejected` |
| `correct` | Provide a corrected value | New candidate added, marked as human-corrected |
| `defer` | Defer decision | Attribute stays in `reviewed` state |
| `merge` | Combine values from multiple sources | New candidate created from merged values |

### 5.4 Review Audit Trail

Every review action is recorded:

| Field | Type | Description |
|-------|------|-------------|
| `attribute_id` | UUID | Which attribute was reviewed |
| `reviewer_id` | string | Who reviewed it |
| `action` | enum | approve, reject, correct, defer, merge |
| `previous_state` | enum | What state the attribute was in |
| `new_state` | enum | What state the attribute moved to |
| `notes` | string | Reviewer's notes |
| `timestamp` | timestamp | When the review occurred |

---

## 6. Quality Scoring

### 6.1 Product-Level Quality Metrics

| Metric | Calculation | Target |
|--------|-------------|--------|
| `completeness_score` | Weighted % of required attributes present | ≥ 85% |
| `accuracy_score` | Average confidence of all attributes | ≥ 0.85 |
| `consistency_score` | % of cross-field checks that pass | ≥ 95% |
| `freshness_score` | % of attributes with current sources | ≥ 80% |
| `evidence_coverage` | % of values with traceable provenance | ≥ 95% |
| `validation_coverage` | % of values that have been validated | ≥ 90% |

### 6.2 Completeness Calculation

Completeness is measured against the category's attribute schema:

```
completeness = sum(weight_i * present_i) / sum(weight_i)
```

Where:
- `weight_i` = weight of attribute i (critical attributes weighted more)
- `present_i` = 1 if attribute i is present, 0 if missing

### 6.3 Attribute-Level Quality

Each attribute has:
- **Confidence:** How trustworthy the value is
- **Validation status:** Whether it passed automated checks
- **Review status:** Whether it has been human-reviewed
- **Freshness:** Whether the evidence is current

---

## 7. Missing Data Representation

### 7.1 Missing Data States

| State | Description | When to use |
|-------|-------------|-------------|
| `NOT_PROVIDED` | Value was not provided in input | Input did not include this attribute |
| `NOT_APPLICABLE` | Attribute does not apply to this product | e.g., "roof_rack" for a sedan |
| `NOT_DISCOVERED` | System searched but could not find the value | Enrichment attempted, nothing found |
| `CONFLICTING` | Multiple values found but cannot be resolved | Sources disagree, pending resolution |
| `PENDING_REVIEW` | Value found but awaiting human verification | Low confidence, awaiting review |
| `NOT_VERIFIABLE` | Value exists but cannot be verified | Source exists but is not trustworthy enough |

### 7.2 Why Distinct States Matter

- `NOT_PROVIDED` vs `NOT_DISCOVERED`: The system knows whether it looked for a value and couldn't find it, vs. the value was never in the input.
- `NOT_APPLICABLE` vs `NOT_PROVIDED`: A value that doesn't apply should not reduce completeness scores.
- `CONFLICTING` vs `NOT_PROVIDED`: A conflict is a different problem than missing data.
- `PENDING_REVIEW` vs `APPROVED`: The system knows whether a value has been verified.

---

## 8. Product-Level Lifecycle

### 8.1 Product States

| State | Description |
|-------|-------------|
| `created` | Product record created, no attributes extracted yet |
| `extracting` | Attributes being extracted from sources |
| `enriching` | Missing attributes being filled from external sources |
| `validating` | Validation checks running |
| `reviewing` | Awaiting human review |
| `ready` | All required attributes present, validated, and approved |
| `published` | Product data published to one or more channels |
| `updating` | Product data being updated from new sources |
| `discontinued` | Product is no longer active |

### 8.2 State Transitions

```
created → extracting → enriching → validating → reviewing → ready → published
                ↑           ↑           ↑           ↑
                └───────────┴───────────┴───────────┘
                    (re-extraction on new sources or corrections)
```

---

## 9. Audit Trail

### 9.1 What Is Tracked

Every change to a product record is tracked:

| Event | What is recorded |
|-------|-----------------|
| Attribute extracted | Source, method, confidence, timestamp |
| Attribute normalized | Transformation applied, input/output values |
| Attribute enriched | External source, method, confidence |
| Attribute validated | Validation results, pass/fail per layer |
| Conflict detected | Conflicting candidates, conflict type |
| Conflict resolved | Resolution method, selected candidate, reason |
| Attribute reviewed | Reviewer, action, notes, timestamp |
| Attribute approved | Approval timestamp |
| Attribute rejected | Rejection reason, timestamp |
| Product published | Channel, timestamp, version |

### 9.2 Audit Trail Purpose

1. **Debugging** — trace back errors to their source
2. **Compliance** — demonstrate due diligence in data quality
3. **Improvement** — identify where errors originate
4. **Accountability** — know who approved what and when

---

*This validation and lifecycle model ensures that product attributes move through a controlled, auditable process from extraction to approval. See `product-examples.md` for concrete examples of how this model works in practice.*
