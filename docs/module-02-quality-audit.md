# Module 2 — Quality Gate Audit

**Date:** August 17, 2026  
**Auditor:** Agent (Skeptical Review)  
**Scope:** All Module 2 deliverables (8 documents)  
**Verdict:** PASS WITH CORRECTIONS (2 required fixes, 4 major items, 3 minor items)

---

## Executive Summary

Module 2 delivers a well-structured canonical product intelligence model that addresses all three mandatory inputs from the Module 1 quality audit (information category on provenance, source freshness, contradiction detection). The attribute-centric design is the right architectural choice for heterogeneous industrial products. The multi-candidate value model with explicit conflict tracking is a genuine strength.

However, the audit identified **2 critical inconsistencies** between the domain model prose and the JSON schema, **4 major gaps** in documentation and specification, and **3 minor items**. None block Module 3 from beginning, but the critical items should be corrected before implementation to prevent schema drift.

**Key strengths:**
- Attribute-centric model correctly handles heterogeneous product categories
- Multi-candidate values with explicit conflict representation — silent overwriting prohibited
- Information category on provenance enables evidence weighting by type
- Source freshness as first-class citizen with propagation rules
- Lifecycle states provide clear state machine for attribute processing
- 3 realistic product examples demonstrate model viability across bearing, valve, and sensor categories
- JSON schema is machine-readable with proper `$ref` structure and constraints
- Domain invariants explicitly stated (8 rules)

---

## 1. Core Model Review

**Entities defined:** 16 (Product, ProductRecord, Attribute, CandidateValue, SourceDocument, SourceLocation, BoundingBox, Transformation, FreshnessInfo, Resolution, Conflict, QualityMetrics, Category, AttributeSchema, AttributeDefinition, ProductRelationship)

**JSON Schema `$defs`:** 12 (ProductRecord, Attribute, CandidateValue, SourceDocument, SourceLocation, BoundingBox, Transformation, FreshnessInfo, Resolution, Conflict, QualityMetrics, ProductRelationship)

**Missing from JSON schema:** Category, AttributeSchema, AttributeDefinition — these are taxonomy infrastructure, not product record content. Acceptable omission if documented.

### Finding C-1: Product-level quality fields missing from JSON schema [CRITICAL]

The domain model (`canonical-product-model.md` Section 2.1) defines these fields on Product:

| Field | In Domain Model | In JSON Schema |
|-------|----------------|----------------|
| `completeness_score` | Yes | No (inside QualityMetrics only) |
| `confidence` | Yes | **Missing** |
| `validation_status` | Yes | **Missing** |
| `review_status` | Yes | **Missing** |
| `last_verified_at` | Yes | **Missing** |

The JSON schema has `quality_metrics` nested inside `ProductRecord`, but the domain model puts summary quality fields directly on Product. An engineer reading both documents would not know whether to implement quality fields at the Product level or only inside ProductRecord.

**Recommendation:** Either add `completeness_score`, `confidence`, `validation_status`, `review_status`, and `last_verified_at` to the top-level JSON schema Product object, or explicitly state in the domain model that these are derived/computed fields not stored in the canonical record.

### Finding C-2: Resolution placement inconsistency [CRITICAL]

The domain model (`canonical-product-model.md` Section 2.3) places `resolution` directly on Attribute:

```
Attribute → resolution: Resolution (Optional)
```

The JSON schema places `conflict` on Attribute and tracks resolution via Conflict:

```
Attribute → conflict: $ref Conflict
Conflict → resolution_id: UUID → Resolution
```

These are two different structural designs. An engineer cannot implement both.

**Recommendation:** Choose one pattern and update the other document. The JSON schema approach (Resolution accessed through Conflict via resolution_id) is cleaner because it avoids duplication — the same Resolution entity serves both Attribute and Conflict.

---

## 2. Value Model Review

The multi-candidate value model is well-designed:

- `Attribute.candidates[]` holds all candidate values from different sources
- `Attribute.selected_candidate_id` tracks the currently winning candidate
- `Attribute.conflict_status` tracks whether the attribute is in conflict
- Each `CandidateValue` has full provenance (source, location, extraction method, confidence, freshness)

**Verdict:** No issues. This is the strongest part of the model.

---

## 3. Normalization Review

Normalization is well-specified:

- Canonical unit system (SI) defined with conversion table
- Original values preserved alongside normalized values
- Transformations recorded with input/output, method, timestamp, and agent
- Ambiguous units flagged for human review

**Minor gap:** The 4-significant-figure precision rule (`attribute-taxonomy.md` Section 4.3) is a documentation-level guideline not enforced by the schema. This is acceptable for a domain contract.

---

## 4. Provenance Review

Evidence chain is comprehensive: SourceDocument → SourceLocation → ExtractionMethod → ExtractionConfidence → Transformations → AttributeValue.

SourceDocument includes `content_hash` for change detection — a good production-quality detail.

SourceLocation covers text (page, section, text_span), table (table_id, row, column), image (BoundingBox), and web (url_fragment) modalities.

### Finding P-1: SourceDocument freshness gap [MAJOR]

The provenance model prose (`provenance-and-evidence-model.md` Section 6.1) states:

> "Every source document has a freshness assessment."

But the JSON schema's `SourceDocument` definition has no `freshness` field. Freshness is only on `CandidateValue.freshness`.

This creates ambiguity: is freshness a property of the source document or of each individual extraction from that source? The schema says per-extraction; the prose says per-source.

**Recommendation:** Add a `freshness` field to `SourceDocument` in the JSON schema, or clarify in the provenance model that freshness is computed per-candidate from SourceDocument timestamps (`published_at`, `acquired_at`) rather than stored explicitly on SourceDocument.

---

## 5. Information Category Review

10 information categories defined: identity, specification, classification, certification, safety, commercial, physical, compatibility, description, media.

These are distinct from the 13 attribute domains (which include performance, electrical, mechanical, environmental — all mapped to "specification" category).

### Finding IC-1: Category-domain mapping undocumented [MAJOR]

There is no explicit mapping between the 13 attribute domains and the 10 information categories. The product examples show the implicit mapping:

| Domain | Maps to Information Category |
|--------|------------------------------|
| identity | identity |
| classification | classification |
| specification | specification |
| physical | physical OR specification (ambiguous) |
| performance | specification |
| electrical | specification |
| mechanical | specification |
| environmental | specification |
| certification | certification |
| commercial | commercial |
| compatibility | compatibility |
| description | description |
| media | media |

**Problem:** Physical domain maps to either "physical" or "specification" depending on the attribute. In the examples:
- `material` → information_category = "physical"
- `bolt_pattern` → information_category = "specification"

Both have `domain = physical` but different information categories. Without an explicit mapping rule, implementers will make inconsistent choices.

**Recommendation:** Add a domain-to-category mapping table to `canonical-product-model.md` Section 5 or `attribute-taxonomy.md`, with clear rules for ambiguous cases.

### Finding IC-2: Information category overlap in examples [MINOR]

The "physical" and "specification" categories both list "Dimensions" as an example in `canonical-product-model.md` Section 5. This creates ambiguity for dimensional attributes.

---

## 6. Source Freshness Review

Freshness is modeled as first-class with:
- `FreshnessInfo` entity (source_published_at, source_version, source_last_verified_at, freshness_status, freshness_reason)
- Freshness thresholds per source type (datasheet: 2 years, website: 1 year, etc.)
- Freshness propagation rules (outdated source → flag all derived attributes)
- `FreshnessInfo` embedded in each `CandidateValue`

**Verdict:** Strong implementation. The propagation rules in `provenance-and-evidence-model.md` Section 6.3 are well-thought-out.

---

## 7. Conflict Review

Conflict model is well-designed:

- `Conflict` entity with candidate_ids (minItems: 2), conflict_type, status, resolution_id
- 4 conflict types: value_mismatch, unit_mismatch, source_contradiction, stale_vs_current
- 5 resolution methods: source_priority, confidence_based, human_decision, rule_based, newest_wins
- `permanently_conflicting` state for unresolvable conflicts
- All candidates preserved during conflict — no silent overwriting

**Verdict:** No issues. The conflict model correctly implements the "contradictions are data" principle.

---

## 8. Fact Classification Review

The system distinguishes fact types through:
- `extraction_method` on CandidateValue (text_extraction = source fact, inference = inference)
- `transformations` on CandidateValue (presence = normalized fact)
- `lifecycle_state` on Attribute (enriched = enriched value)
- `confidence` score (lower for inferences)

### Finding FC-1: Fact type classification not explicitly documented [MAJOR]

The Module 1 audit defined 5 information categories: fact, normalized fact, derived value, enriched value, inference. The Module 2 model represents these implicitly through model fields, but there is no explicit mapping document that says:

> "A value is classified as X when extraction_method = Y and transformations = Z and lifecycle_state = W."

This mapping exists implicitly across the model but is never stated explicitly. An engineer implementing the system would need to infer these rules.

**Recommendation:** Add a "Fact Classification Mapping" table to `canonical-product-model.md` or `provenance-and-evidence-model.md` that explicitly maps model fields to fact types.

---

## 9. Confidence Review

Confidence components defined with weights:
- Source trust score: 0.3
- Extraction confidence: 0.3
- Source corroboration: 0.2
- Validation status: 0.2

Ranges defined: 0.9-1.0 high, 0.7-0.89 medium, 0.5-0.69 low, 0.0-0.49 very low.

### Finding CONF-1: Confidence calculation formula not specified [MAJOR]

The weights are listed but the actual calculation formula is not given. Is it a weighted sum?

```
confidence = 0.3 * source_trust + 0.3 * extraction_confidence + 0.2 * corroboration + 0.2 * validation
```

Or is it more complex (e.g., geometric mean, minimum threshold, Bayesian update)?

Without the formula, different implementers will compute different confidence scores from the same inputs.

**Recommendation:** Specify the exact formula in `provenance-and-evidence-model.md` Section 5.2. A weighted sum is sufficient for the hackathon.

---

## 10. Missing Information Review

6 missing states defined: NOT_PROVIDED, NOT_APPLICABLE, NOT_DISCOVERED, CONFLICTING, PENDING_REVIEW, NOT_VERIFIABLE.

These are represented on `Attribute.missing_status` in the JSON schema.

### Finding MI-1: Lifecycle state for missing attributes semantically confusing [MINOR]

The product examples show missing attributes with `lifecycle_state: "discovered"`. But the lifecycle model defines "discovered" as "attribute identified in source but not yet extracted." For a missing attribute, nothing was identified in any source.

The lifecycle model doesn't define a state for "this attribute is known to be missing." A missing attribute is not in the lifecycle — it was never discovered.

**Recommendation:** Either:
(a) Add a `missing` lifecycle state, or
(b) Clarify in the lifecycle model that `lifecycle_state: "discovered"` with `missing_status: "NOT_DISCOVERED"` means "the system looked for this attribute and confirmed it is not available."

Option (b) is simpler and doesn't require schema changes.

---

## 11. Category Extensibility Review

Extensibility is well-designed:
- New attributes added to any domain without schema changes
- New domains created for new product categories
- Category schemas define required/optional attributes per category
- Custom attributes allowed but flagged
- Schema evolution rules defined (existing records not broken, new required attributes flagged as missing)

**Verdict:** No issues. The extensibility model is appropriate for a hackathon with clear growth path.

---

## 12. Relationship Review

ProductRelationship has: id, source_product_id, target_product_id, relationship_type, confidence, source_id, validated, notes.

8 relationship types: replaces, compatible_with, accessory_of, equivalent_to, variant_of, requires, used_with, supersedes.

**Minor observation:** `source_id` is a single UUID. A relationship derived from multiple sources cannot be represented with multiple source references. This is an acceptable simplification for the hackathon — the multi-candidate pattern is not applied to relationships.

---

## 13. JSON Schema Review

The JSON schema is well-structured:
- Uses `$defs` for entity definitions (correct for draft 2020-12)
- Proper `$ref` references between entities
- Required fields specified per entity
- Enum values match domain model definitions
- `minItems` constraints on arrays (e.g., candidates minItems: 1, conflict candidate_ids minItems: 2)
- `format: uuid` and `format: date-time` constraints
- `minimum`/`maximum` on numeric fields

### Finding JS-1: Polymorphic value fields have no type constraint [MINOR]

The `value` field on both `Attribute` and `CandidateValue` has no type constraint — it's described as "type depends on value_type." This is correct for JSON Schema (which cannot express conditional types natively), but it means the schema cannot validate the actual value structure.

For example, a `measurement` value should be `{ value: number, unit: string }`, but the schema accepts any JSON value.

**Recommendation:** This is a known JSON Schema limitation. For the hackathon, document the expected value structure per value_type in the attribute taxonomy. For production, consider using a JSON Schema discriminator or switching to a type system that supports discriminated unions.

---

## 14. Real-World Stress Test

### Scenario 1: Simple Product (single source, no conflicts)

A basic bolt from a single catalog page. One source, one candidate per attribute, no conflicts. All fields populated straightforwardly.

**Result:** Model handles this cleanly. No issues.

### Scenario 2: Complex Product (multi-source, partial data)

A motor with manufacturer datasheet, distributor listing, and web scrape. Some attributes from manufacturer only (specifications), some from distributor only (pricing), some missing (certifications).

**Result:** Model handles this through multi-candidate values and missing_status. The `NOT_PROVIDED` vs `NOT_DISCOVERED` distinction is useful here — pricing was NOT_PROVIDED (not in manufacturer datasheet) while certifications were NOT_DISCOVERED (searched but not found).

### Scenario 3: Conflicting Sources

Product A from manufacturer says "IP65", distributor says "IP67". Both sources are trustworthy.

**Result:** Conflict detected with type `value_mismatch`. Both candidates preserved. `conflict_status: "pending_resolution"`. Requires human review or source_priority resolution. Model handles this correctly.

### Scenario 4: Stale Data

Old catalog (2020) vs new website (2026) for same product. Different values for operating temperature.

**Result:** FreshnessInfo flags old catalog as `outdated`. Conflict type is `stale_vs_current`. Resolution method `newest_wins` or `source_priority` (manufacturer website > old catalog). Model handles this through the freshness + conflict combination.

### Scenario 5: Derived + Inferred Values

Bolt pattern derived from bore diameter + housing style. Material inferred from product name ("stainless steel" in name → material = stainless steel).

**Result:** Both use `extraction_method: "inference"`. Bolt pattern has higher confidence (0.85, derived from known values) than material (0.60, inferred from name alone). Both have provenance through the inference chain. Model handles this correctly.

**Stress Test Verdict:** All 5 scenarios are handled by the model without structural gaps.

---

## 15. Anti-Hallucination Review

The model supports anti-hallucination through:
- Domain invariant: "Every candidate has a source. No value exists without provenance."
- Missing data explicitly represented (NOT_PROVIDED, NOT_DISCOVERED, etc.) rather than fabricated
- Confidence scoring grounded in source quality
- Human review for low-confidence values (< 0.7)
- Extraction method distinguishes source facts from inferences

**Acceptable gap:** The model does not detect fabricated sources at the schema level. If an LLM hallucinates a source document, the model would accept it. This is an implementation-level concern (source verification, cross-referencing), not a domain model concern.

---

## 16. Over-Engineering Review

For a 1-person hackathon team with ~6 days remaining:

**Appropriately scoped:**
- Core entities (Product, Attribute, CandidateValue, SourceDocument) — essential
- Supporting entities (FreshnessInfo, Transformation, Conflict, Resolution) — necessary for requirements
- Quality metrics — necessary for evaluation

**Acknowledged deferrals (from completion report):**
- Category-specific schemas — defer to implementation
- Advanced conflict resolution — start with simple detection
- Multi-tenancy — not needed for demo
- Performance optimization — not needed for demo

**Potential concern:** 16 entities is ambitious for a hackathon. However, the team has explicitly identified what to defer. The model is comprehensive but the implementation can be incremental.

---

## 17. Judge Perspective

For a Hack2Skill/Unilog judge:

| Criterion | Assessment |
|-----------|------------|
| Domain understanding | Excellent — attribute-centric model shows deep B2B data knowledge |
| Technical depth | Strong — provenance, conflict, freshness models are more sophisticated than typical submissions |
| Innovation | Good — information category on provenance is a genuine differentiator |
| Completeness | Strong — 8 documents, ~3000 lines total |
| Feasibility | Moderate concern — model promises a lot; demo must deliver |
| Unilog alignment | Strong — the model directly addresses Unilog's product data challenges |

**Risk:** If the implementation doesn't deliver on the model's promise, the gap between design sophistication and demo simplicity could hurt. The product examples help bridge this gap — they show the model working with realistic data.

---

## 18. Module 3 Readiness

The model provides a solid foundation for Module 3 (Architecture). Open questions are properly identified:
- Schema storage
- Conflict resolution rules
- Multi-tenancy
- Versioning
- Performance

The domain model provides clear constraints for technology selection: the system must support polymorphic attributes, multi-candidate values, provenance tracking, and conflict management.

**Status:** READY for Module 3 with corrections applied.

---

## Required Corrections

| # | Document | Issue | Severity | Fix | Status |
|---|----------|-------|----------|-----|--------|
| 1 | `product-intelligence-schema.json` | Product-level quality fields (confidence, validation_status, review_status, last_verified_at) missing from top-level Product object — domain model has them | CRITICAL | Added fields to JSON schema | ✅ FIXED |
| 2 | `canonical-product-model.md` / `product-intelligence-schema.json` | Resolution placement: domain model puts `resolution` on Attribute; JSON schema puts `conflict` on Attribute with resolution via Conflict.resolution_id | CRITICAL | Updated domain model to match JSON schema pattern (resolution accessed through Conflict) | ✅ FIXED |

## Major Items (should fix before Module 3)

| # | Document | Issue | Severity | Fix | Status |
|---|----------|-------|----------|-----|--------|
| 3 | `canonical-product-model.md` | Domain-to-information-category mapping undocumented; physical domain maps to either "physical" or "specification" depending on attribute | MAJOR | Added explicit mapping table in Section 5.1 | ✅ FIXED |
| 4 | `provenance-and-evidence-model.md` | SourceDocument has no freshness field in schema, but prose says "every source document has a freshness assessment" | MAJOR | Clarified freshness is per-candidate, computed from SourceDocument timestamps | ✅ FIXED |
| 5 | `canonical-product-model.md` | Fact type classification (fact vs normalized vs derived vs enriched vs inference) is implicit in model fields, never explicitly mapped | MAJOR | Added fact classification mapping table in provenance model Section 2.4 | ✅ FIXED |
| 6 | `provenance-and-evidence-model.md` | Confidence calculation formula not specified — weights given (0.3, 0.3, 0.2, 0.2) but actual formula omitted | MAJOR | Added explicit formula with corroboration and validation score definitions | ✅ FIXED |

## Minor Items (nice to fix)

| # | Document | Issue | Severity | Fix | Status |
|---|----------|-------|----------|-----|--------|
| 7 | `canonical-product-model.md` | Information categories "physical" and "specification" both list "Dimensions" as example — ambiguous | MINOR | Disambiguated: specification → "Bore diameter, voltage rating, flow coefficient"; physical → "Length, width, height, weight, material, finish" | ✅ FIXED |
| 8 | `validation-and-lifecycle-model.md` | Lifecycle state "discovered" used for missing attributes, but "discovered" means "identified in source" — semantically confusing | MINOR | Added invariant #5: missing attributes use `discovered` state to indicate acknowledged absence | ✅ FIXED |
| 9 | `product-intelligence-schema.json` | Polymorphic `value` fields have no type constraint — JSON Schema limitation | MINOR | Added value structure reference table in attribute-taxonomy.md Section 3.5 | ✅ FIXED |

---

## Strengths

1. **Attribute-centric model** — correct architectural choice for heterogeneous industrial products
2. **Multi-candidate values** — silent overwriting prohibited; conflicts are data, not errors
3. **Information category on provenance** — enables evidence weighting by type; rare in hackathon submissions
4. **Source freshness as first-class** — propagation rules ensure stale data is never silently used
5. **Domain invariants** — 8 explicit rules that constrain the model (Section 6 of canonical model)
6. **Product examples** — 3 realistic products (bearing, valve, sensor) demonstrate model viability
7. **JSON schema** — machine-readable with proper constraints, refs, and enums
8. **Missing data representation** — 6 distinct states distinguish "not provided" from "not found" from "not applicable"
9. **Conflict resolution methods** — 5 methods from automated (newest_wins) to human (human_decision)
10. **Transformation tracking** — every normalization recorded with input/output/agent/timestamp

---

## Appendix: Audit Dimensions Summary

| Dimension | Verdict |
|-----------|---------|
| Core model review | ⚠️ PASS WITH CRITICAL (2 inconsistencies between domain model and schema) |
| Value model review | ✅ PASS |
| Normalization review | ✅ PASS |
| Provenance review | ⚠️ PASS WITH MAJOR (freshness on SourceDocument gap) |
| Information category review | ⚠️ PASS WITH MAJOR (domain-category mapping undocumented) |
| Source freshness review | ✅ PASS |
| Conflict review | ✅ PASS |
| Fact classification review | ⚠️ PASS WITH MAJOR (classification mapping implicit) |
| Confidence review | ⚠️ PASS WITH MAJOR (formula not specified) |
| Missing information review | ✅ PASS |
| Category extensibility review | ✅ PASS |
| relationship review | ✅ PASS |
| JSON schema review | ✅ PASS |
| Real-world stress test | ✅ PASS (all 5 scenarios handled) |
| Anti-hallucination review | ✅ PASS |
| Over-engineering review | ✅ PASS (acknowledged deferrals) |
| Judge perspective | ✅ PASS (strong differentiation) |
| Module 3 readiness | ✅ PASS (with corrections) |

**Overall:** PASS WITH CORRECTIONS
