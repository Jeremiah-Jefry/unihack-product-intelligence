# Risks and Failure Modes

> **Status:** Complete  
> **Module:** 1 — Problem & Domain Understanding  
> **Purpose:** Catalog everything that can go wrong, why it matters, and how to mitigate it.  
> **Depends on:** `module-01-problem-definition.md`, `requirements.md`

---

## 1. Failure Taxonomy

This document provides a comprehensive taxonomy of failure modes organized by the stage at which they occur. For each failure mode, we explain:

- **What it is**
- **Why it happens**
- **What the consequence is**
- **How to detect it**
- **How to mitigate it**

---

## 2. Extraction Failures

### 2.1 Hallucination

**What:** The system generates a plausible but fabricated value that has no basis in any source document.

**Why it happens:** Language models generate text based on patterns, not truth. Given a partial product record, an LLM may "complete" it with values that sound correct but are wrong. Example: given a bearing MPN, the LLM might invent a load rating that doesn't match any real specification.

**Consequence:** The most dangerous failure mode. A hallucinated specification (wrong bore diameter, wrong voltage rating, wrong material) can cause: wrong part ordered → equipment failure → safety incident → legal liability.

**Detection:**
- Provenance check: if a value has no source reference, it may be hallucinated
- Confidence scoring: hallucinated values should have low confidence
- Cross-reference: compare against manufacturer databases
- Human review: domain experts can spot implausible values

**Mitigation:**
- Never generate values without source evidence
- Tag all LLM-generated values as "inferred" or "requires verification"
- Auto-reject values that cannot be traced to a source
- Route all high-risk fields (specs, certifications) to human review

### 2.2 Incorrect Extraction

**What:** The system reads a value from a source document but extracts it incorrectly.

**Why it happens:** Text parsing errors, ambiguous formatting, OCR errors, or LLM misinterpretation. Example: "3/8 in" extracted as "3/8 mm"; "15.9 kN" extracted as "159 kN".

**Consequence:** Wrong value enters the catalog. May not be caught if it falls within a plausible range.

**Detection:**
- Unit consistency checks (a bearing bore of 3/8 mm is implausible)
- Range validation (a load rating of 159 kN for a small bearing is implausible)
- Cross-reference with other sources
- Human review of extracted values

**Mitigation:**
- Preserve original extracted text alongside normalized values
- Apply domain-specific range checks
- Use multiple extraction methods and compare results
- Flag values that differ from source by more than a threshold

### 2.3 Table-Reading Error

**What:** The system reads data from a table but assigns values to the wrong row (product) or column (attribute).

**Why it happens:** Complex table layouts, merged cells, multi-level headers, spanning rows, or non-standard formatting. Industrial PDFs frequently have dense tables with 20-30 products per page.

**Consequence:** Product A's specs are assigned to Product B. This is a wrong-product-association error, which is high-severity.

**Detection:**
- Structural validation (e.g., if a bearing has both a bore of 1-3/16 in and a bore of 2-1/8 in, something is wrong)
- Cross-reference with other sources for the same product
- Human review of table extraction results

**Mitigation:**
- Preserve table structure during parsing
- Use table-aware extraction models
- Validate extracted values against product identity (does this spec make sense for this product?)
- Provide table preview to reviewers for verification

### 2.4 OCR Error

**What:** Optical character recognition misreads characters in scanned documents.

**Why it happens:** Poor scan quality, faded text, unusual fonts, handwritten annotations, or low resolution. Common OCR errors: `5` → `S`, `0` → `O`, `1` → `l`, `8` → `B`.

**Consequence:** Corrupted specifications. An OCR error in a part number can cause wrong-product matching. An error in a numeric value can cause wrong specs.

**Detection:**
- Character-level confidence scores from OCR engine
- Cross-reference with known product data
- Pattern matching (part numbers have expected formats)
- Human review of low-confidence OCR results

**Mitigation:**
- Use high-quality OCR engines with confidence scoring
- Apply post-OCR correction using product-specific patterns
- Flag low-confidence OCR results for human review
- Prefer text-based PDFs over scanned documents when available

### 2.5 Unit Conversion Error

**What:** Mathematical error when converting between unit systems.

**Why it happens:** Incorrect conversion factors, ambiguous unit notation, or rounding errors. Example: converting "1-3/16 in" to mm requires interpreting the fraction, then multiplying by 25.4.

**Consequence:** Wrong dimensions. A part specified as 30.163 mm but stored as 301.63 mm (decimal point error) would be completely wrong.

**Detection:**
- Round-trip conversion check (convert back to original; should match)
- Plausibility check (is this dimension physically reasonable for this product type?)
- Cross-reference with source value

**Mitigation:**
- Use well-tested unit conversion libraries
- Preserve original values alongside converted values
- Apply range checks specific to product category
- Never silently convert — always record the conversion in provenance

### 2.6 Wrong Product Association

**What:** Data from one product is assigned to a different product.

**Why it happens:** Identity resolution errors (matching wrong MPN), table-reading errors (wrong row), or multi-product document parsing errors (wrong product isolated).

**Consequence:** High-severity. Buyer receives wrong specifications for a product they intend to purchase. Can cause equipment failure, safety incidents, or financial loss.

**Detection:**
- Cross-reference extracted specs against known data for the product
- Validate that specs are physically plausible for the product type
- Human review of products with conflicting data from multiple sources

**Mitigation:**
- Robust identity resolution with multiple matching criteria
- Validate extracted values against product category expectations
- Flag products where data from multiple sources conflicts
- Never auto-publish products with unresolved identity conflicts

---

## 3. Data Quality Failures

### 3.1 Missing Fields

**What:** Required attributes are left blank or marked as unknown.

**Why it happens:** The source documents don't contain the information; extraction failed; or the field wasn't recognized as applicable.

**Consequence:** Product is invisible in filtered search; incomplete product page; buyer must call for information; channel listing may be rejected.

**Detection:**
- Completeness scoring against attribute schema
- Channel-specific completeness checks
- Missing field reporting

**Mitigation:**
- Attempt enrichment from additional sources before accepting a field as missing
- Clearly mark missing fields (not as empty strings, but as "unknown" or "not found in sources")
- Prioritize enrichment of critical (filter-driving) attributes
- Set minimum completeness thresholds for channel publishing

### 3.2 Conflicting Sources

**What:** Two or more source documents give different values for the same attribute.

**Why it happens:** Products are updated over time but old documents persist; different regions have different specs; errors in one or more sources; or different product variants are confused.

**Consequence:** If resolved silently, the wrong value may be published. If not resolved, the conflict remains and may confuse downstream consumers.

**Detection:**
- Cross-source comparison during enrichment
- Conflict detection rules (same attribute, different values from different sources)
- Version/freshness comparison

**Mitigation:**
- Surface conflicts to human reviewers (never silently resolve)
- Prefer manufacturer-official sources over third-party sources
- Prefer more recent sources over older ones (but don't assume newer is always correct)
- Record both values with their sources in the conflict log
- Allow reviewers to select the correct value and record their rationale

### 3.3 Outdated Information

**What:** Published data is based on an old version of a product that has since been updated or discontinued.

**Why it happens:** Source documents are not refreshed; old datasheets circulate; product is discontinued but data remains in the catalog.

**Consequence:** Buyer receives information about a product that no longer exists or has been updated. May order wrong version.

**Detection:**
- Lifecycle status checks (is the product still active?)
- Source freshness monitoring (when was the source last updated?)
- Cross-reference with manufacturer's current catalog

**Mitigation:**
- Track source document timestamps
- Periodically re-check sources for updates
- Flag products with old sources for refresh
- Mark lifecycle status explicitly (active, discontinued, obsolete)

### 3.4 Duplicate Products

**What:** The same physical product appears multiple times in the catalog under different identifiers.

**Why it happens:** Different suppliers use different part numbers for the same product; internal teams create new records instead of finding existing ones; acquisitions add duplicate catalogs.

**Consequence:** Confused buyers (which one to order?); inflated catalog metrics; broken comparison tools; duplicate maintenance work.

**Detection:**
- Identity matching (MPN, GTIN, brand + model)
- Fuzzy matching on product names and specs
- Cross-reference databases

**Mitigation:**
- Canonical record creation (one record per real product)
- Duplicate detection as a mandatory step before publishing
- Supplier cross-reference mapping
- Human review for ambiguous matches

### 3.5 Incorrect Categorization

**What:** A product is assigned to the wrong category in the taxonomy.

**Why it happens:** Ambiguous product descriptions; similar-looking products in different categories; AI misclassification; or taxonomy gaps (no perfect category exists).

**Consequence:** Wrong attribute schema applied (required fields are wrong); product not findable in correct filters; marketplace listing in wrong section.

**Detection:**
- Classification confidence scoring
- Cross-reference: do the product's specs match the category's expected attributes?
- Human review for low-confidence classifications

**Mitigation:**
- Use multiple classification signals (name, specs, manufacturer)
- Apply confidence thresholds (below threshold → human review)
- Validate that classified attributes match category expectations
- Support multi-label classification when a product fits multiple categories

### 3.6 Ambiguous Terminology

**What:** The same term means different things across contexts, or different terms mean the same thing.

**Why it happens:** Industry jargon varies by region, supplier, and discipline. Example: "pipe diameter" vs "nominal size" vs "NB" (nominal bore) — all refer to the same concept but in different contexts.

**Consequence:** Incorrect attribute mapping; confused search results; broken comparisons.

**Detection:**
- Terminology mapping validation
- Cross-supplier comparison
- Human review of ambiguous mappings

**Mitigation:**
- Build and maintain a controlled vocabulary with synonyms
- Map supplier-specific terms to canonical terms
- Preserve original terms alongside mapped terms
- Flag ambiguous mappings for human review

### 3.7 False Confidence

**What:** The system reports high confidence for a value that is actually wrong.

**Why it happens:** Confidence scoring is based on extraction certainty, not verification against ground truth. A value can be extracted with high confidence from a source that is itself wrong.

**Consequence:** Reviewers trust the system; wrong values slip through without human review; errors propagate.

**Detection:**
- Periodic accuracy audits (compare system output against ground truth)
- Track confidence distribution vs. actual accuracy
- Flag any value with confidence > 0.9 that is later found to be wrong

**Mitigation:**
- Ground confidence in evidence quality, not just extraction certainty
- Distinguish extraction confidence (how sure are we we read this correctly?) from source confidence (how sure are we this source is correct?)
- Never use confidence as a substitute for verification
- Maintain feedback loops from human review to calibrate confidence scoring

---

## 4. Enrichment Failures

### 4.1 Unsupported Enrichment

**What:** A value is added from an unverified or untrustworthy source.

**Why it happens:** The enrichment system retrieves data from a web page, a third-party database, or an AI-generated source without verifying its accuracy.

**Consequence:** Wrong data enters the catalog. If the enriched value conflicts with the manufacturer's specification, the buyer may be misled.

**Detection:**
- Source trustworthiness scoring
- Cross-reference with manufacturer-official sources
- Provenance tracking (is the source a manufacturer website or an unknown third party?)

**Mitigation:**
- Score source trustworthiness (manufacturer > authorized distributor > third-party > unknown)
- Prefer manufacturer sources for technical specifications
- Flag enriched values from unverified sources for human review
- Never auto-enrich high-risk fields (safety specs, certifications) without human review

### 4.2 Cross-Product Contamination

**What:** Specs from one product variant are mixed into another variant's record.

**Why it happens:** Variant resolution errors; multi-product extraction assigns values to wrong variant; similar-looking variants confused.

**Consequence:** Buyer selects wrong variant based on contaminated specs.

**Detection:**
- Variant-level validation (do specs match this specific variant?)
- Cross-reference with variant-specific source documents

**Mitigation:**
- Strict variant identity resolution
- Variant-specific extraction and validation
- Flag products where variant data seems inconsistent

### 4.3 Incorrect Relationships

**What:** Wrong cross-references, compatibility claims, or replacement relationships are established.

**Why it happens:** AI infers relationships from similarity rather than evidence; cross-reference databases are incomplete; product families have complex relationship webs.

**Consequence:** Buyer orders an incompatible accessory; replacement part doesn't fit; cross-reference leads to wrong product.

**Detection:**
- Relationship validation against manufacturer cross-reference data
- Physical compatibility checks (do dimensions match?)
- Human review of relationship claims

**Mitigation:**
- Only establish relationships with source evidence
- Cross-reference with manufacturer cross-reference data
- Flag inferred relationships for human review
- Validate physical compatibility for "replaces" and "compatible with" relationships

---

## 5. Systemic Failures

### 5.1 Schema Drift

**What:** Attribute definitions change over time without propagation to existing records.

**Why it happens:** New attributes are added to the schema; attribute names change; data types change; controlled vocabularies are updated.

**Consequence:** Existing records don't conform to current schema; completeness scores become inaccurate; channel validation fails.

**Detection:**
- Schema version tracking
- Periodic schema conformance audits
- Channel validation failures after schema changes

**Mitigation:**
- Version the schema
- When schema changes, identify affected records and re-validate
- Maintain backward compatibility where possible
- Document schema changes and their impact

### 5.2 Source Staleness

**What:** The system continues to use old source data after newer versions are available.

**Why it happens:** Sources are not re-checked; update mechanisms are not implemented; monitoring is absent.

**Consequence:** Published data is outdated; may not reflect product changes, price updates, or specification revisions.

**Detection:**
- Source freshness monitoring
- Periodic re-crawling of web sources
- Supplier feed change detection

**Mitigation:**
- Track source timestamps
- Implement source change detection
- Re-extract when sources are updated
- Mark data freshness explicitly in product records

### 5.3 Scale Degradation

**What:** Quality drops as catalog grows. Small catalogs are processed carefully; large catalogs have more errors.

**Why it happens:** Processing shortcuts at scale; review capacity doesn't grow with catalog size; validation rules become less effective with more diverse products.

**Consequence:** Large catalogs have lower quality than small ones. The system is less useful for the customers who need it most (those with large catalogs).

**Detection:**
- Quality metrics by catalog size
- Error rate trends as catalog grows
- Review bottleneck monitoring

**Mitigation:**
- Design for scale from the beginning
- Implement confidence-based routing to minimize human review
- Automate validation where possible
- Track quality metrics continuously

### 5.4 Non-Deterministic Output

**What:** The same input produces different output on different runs.

**Why it happens:** LLMs are inherently non-deterministic; extraction results may vary; random sampling in model inference.

**Consequence:** Difficult to debug; quality is inconsistent; reviewers see different results for the same product.

**Detection:**
- Run the same input multiple times and compare outputs
- Track output stability over time

**Mitigation:**
- Use temperature=0 or deterministic settings where possible
- Cache extraction results for the same input
- Version and pin model versions
- Focus on structural extraction (deterministic) over creative generation

---

## 6. Risk Severity Matrix

| Risk | Likelihood | Impact | Overall | Mitigation priority |
|------|-----------|--------|---------|-------------------|
| Hallucination | High | Critical | **Critical** | P0 — must be addressed |
| Wrong product association | Medium | Critical | **High** | P0 — must be addressed |
| Incorrect extraction | High | High | **High** | P0 — must be addressed |
| Table-reading error | High | High | **High** | P0 — must be addressed |
| Conflicting sources | High | Medium | **High** | P0 — must be addressed |
| Missing fields | High | Medium | **High** | P0 — must be addressed |
| OCR error | Medium | Medium | **Medium** | P1 — important |
| Unit conversion error | Low | High | **Medium** | P1 — important |
| Incorrect categorization | Medium | Medium | **Medium** | P1 — important |
| Duplicate products | Medium | Medium | **Medium** | P1 — important |
| Ambiguous terminology | High | Low | **Medium** | P1 — important |
| False confidence | Medium | High | **Medium** | P1 — important |
| Outdated information | Medium | Medium | **Medium** | P1 — important |
| Unsupported enrichment | Medium | High | **Medium** | P1 — important |
| Cross-product contamination | Low | High | **Medium** | P1 — important |
| Incorrect relationships | Low | Medium | **Low** | P2 — enhancement |
| Schema drift | Low | Medium | **Low** | P2 — enhancement |
| Source staleness | Medium | Low | **Low** | P2 — enhancement |
| Scale degradation | Medium | Medium | **Medium** | P1 — important |
| Non-deterministic output | Medium | Low | **Low** | P2 — enhancement |

---

## 7. Mitigation Strategies Summary

### 7.1 Prevention

- Every value must have provenance (CC-01)
- Unknown is better than wrong (CC-02)
- Confidence must be honest (CC-03)
- Batch processing with consistent rules (CC-04)
- Support incremental updates without full reprocessing (CC-05)
- Maintain audit trails for all changes (CC-06)
- Surface and resolve conflicting sources (CC-07)
- Validation before publication (CC-08)

### 7.2 Detection

- Multi-layer validation (schema, type, range, cross-field, cross-source)
- Conflict detection across sources
- Completeness and accuracy scoring
- Confidence calibration against ground truth
- Periodic quality audits

### 7.3 Correction

- Human review for low-confidence and high-risk values
- Audit trail for all changes
- Source freshness monitoring and re-extraction
- Feedback loops from human review to improve extraction

### 7.4 Containment

- Never auto-publish unreviewed high-risk values
- Flag and quarantine products with unresolved conflicts
- Version product records for rollback capability
- Monitor quality metrics continuously

---

*This risk document will be updated in later modules as the architecture introduces new components and the evaluation framework provides empirical data on actual failure rates.*
