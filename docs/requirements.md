# Requirements

> **Status:** Complete  
> **Module:** 1 — Problem & Domain Understanding  
> **Purpose:** Define what the system must do, organized by priority and validated against the problem definition.  
> **Depends on:** `module-01-problem-definition.md`, `domain-model.md`

---

## 1. Priority Definitions

| Priority | Meaning |
|----------|---------|
| **P0** | Absolutely required. The system cannot function without this. |
| **P1** | Important. Significantly impacts quality or usability. |
| **P2** | Enhancement. Valuable but not critical for initial functionality. |

---

## 2. Requirements Matrix

### 2.1 Ingestion & Extraction

| # | Requirement | Why it matters | Input | Expected behavior | Failure risk | Validation need | Priority |
|---|------------|---------------|-------|-------------------|--------------|-----------------|----------|
| R-01 | Accept PDF documents as input | PDFs are the most common format for industrial product data (datasheets, catalogs, spec sheets) | PDF file | Parse PDF, extract text and tables; handle multi-page documents | Table structure lost; text garbled; multi-product pages cause mis-association | Verify extraction completeness; compare extracted count to expected | P0 |
| R-02 | Accept CSV/Excel supplier feeds as input | Suppliers deliver data in tabular formats | CSV/Excel file | Parse rows and columns; map to internal schema; detect header variations | Column name mismatches; data type errors; encoding issues | Schema mapping validation; data type checks | P0 |
| R-03 | Accept web pages as input | Manufacturer websites are a key enrichment source | URL or HTML | Fetch and parse page content; extract product information | Page structure varies; JavaScript-rendered content; anti-scraping measures | Content availability check; structured data extraction verification | P1 |
| R-04 | Accept images as input | Product images, labels, diagrams contain visual information | Image file | Extract text (OCR), identify product features; extract from labels/diagrams | OCR errors; ambiguous visual content; low-resolution images | OCR confidence scoring; cross-reference with other sources | P1 |
| R-05 | Handle scanned PDFs | Legacy documents often have no text layer | Scanned PDF | Apply OCR; preserve layout information; extract tables | OCR errors compound; table structure lost; layout misinterpreted | OCR confidence scoring; manual review flagging | P1 |
| R-06 | Extract structured attributes from unstructured text | Product specs often appear in prose, not structured fields | Parsed text | Identify attribute names, values, and units; associate with correct product | Attribute-value mismatch; wrong product association; unit ambiguity | Cross-field consistency checks; provenance tracking | P0 |
| R-07 | Extract data from tables in PDFs | Industrial catalogs present specs in tabular format | Parsed PDF tables | Preserve table structure; map rows to products; map columns to attributes | Row-column misalignment; merged cell errors; header row misidentification | Structural validation; cross-reference with text extraction | P0 |
| R-08 | Handle multi-product documents | A single PDF may contain 20-30 products per page | Parsed document | Isolate individual products; prevent cross-product contamination | Product A's specs assigned to Product B; attributes mixed across products | Product boundary detection; attribute-to-product association validation | P0 |

### 2.2 Identity & Deduplication

| # | Requirement | Why it matters | Input | Expected behavior | Failure risk | Validation need | Priority |
|---|------------|---------------|-------|-------------------|--------------|-----------------|----------|
| R-09 | Resolve product identity from MPN + brand | Minimal input scenario requires identity resolution | MPN and brand name | Look up product in known databases; retrieve available information | Wrong product matched; no match found; ambiguous matches | Match confidence scoring; multiple candidate handling | P0 |
| R-10 | Detect duplicate products across sources | Same product from different suppliers must be unified | Multiple source records | Match by MPN, GTIN, brand, and fuzzy matching; create canonical record | False positives (different products matched); false negatives (same product not matched) | Match validation; human review for ambiguous matches | P0 |
| R-11 | Handle variant relationships | Products come in sizes, materials, configurations | Product records with variants | Identify parent-variant relationships; group related products | Wrong variant grouping; missing variant links | Relationship validation; human review | P1 |

### 2.3 Classification

| # | Requirement | Why it matters | Input | Expected behavior | Failure risk | Validation need | Priority |
|---|------------|---------------|-------|-------------------|--------------|-----------------|----------|
| R-12 | Classify products into categories | Classification determines required attributes and channel eligibility | Product attributes | Assign category with confidence score; support multiple taxonomies | Wrong classification; low-confidence classification accepted as certain | Classification confidence threshold; human review for low confidence | P0 |
| R-13 | Support category-specific attribute schemas | Different product types require different attributes | Category assignment | Apply the correct attribute schema; identify required vs. optional fields | Wrong schema applied; required attributes not identified | Schema applicability check | P0 |
| R-14 | Map to industry taxonomies | Distributors and marketplaces require specific taxonomy codes | Product + taxonomy | Map to at least 3 of: ETIM, UNSPSC, eCl@ss, GS1 GPC codes | Wrong code assignment; stale code version; fewer than 3 standards supported | Code validation against current taxonomy version | P0 |

### 2.4 Enrichment

| # | Requirement | Why it matters | Input | Expected behavior | Failure risk | Validation need | Priority |
|---|------------|---------------|-------|-------------------|--------------|-----------------|----------|
| R-15 | Fill missing attributes from additional sources | Incomplete input must be enriched to be useful | Partial product record + sources | Retrieve missing values from web, databases, or other sources; attach provenance | Wrong source used; enriched value conflicts with original; unsupported enrichment | Source trustworthiness check; conflict detection; provenance attachment | P0 |
| R-16 | Cross-reference multiple sources | More sources = higher confidence; contradictions must be detected | Multiple source records for same product | Compare values across sources; detect agreements and conflicts | Conflicts silently resolved; wrong source preferred; conflicts not surfaced | Conflict detection; contradiction flagging | P0 |
| R-17 | Normalize units | Inconsistent units break comparison and search | Values with various unit formats | Convert to consistent unit system; preserve original value | Conversion errors; original value lost; ambiguous unit interpretation | Unit conversion validation; original preservation check | P0 |
| R-18 | Normalize terminology | Different suppliers use different names for the same concept | Free-text attribute values | Map to controlled vocabulary; preserve original term | Wrong mapping; loss of nuance; controlled vocabulary too rigid | Mapping validation; human review for ambiguous terms | P1 |

### 2.5 Validation & Quality

| # | Requirement | Why it matters | Input | Expected behavior | Failure risk | Validation need | Priority |
|---|------------|---------------|-------|-------------------|--------------|-----------------|----------|
| R-19 | Validate against schema rules | Ensures required fields are present and correctly typed | Product record + schema | Check all required fields; verify data types; flag missing values | Schema rules incomplete; wrong schema applied | Schema rule coverage audit | P0 |
| R-20 | Validate value ranges | Catches physically impossible values (negative weight, zero bore diameter) | Numeric attribute values | Check against defined ranges; flag outliers | Range rules too narrow (rejects valid values) or too wide (accepts errors) | Range rule calibration; outlier investigation | P1 |
| R-21 | Detect cross-field contradictions | Some errors only visible when comparing related fields | Complete product record | Check logical consistency between related attributes | Complex cross-field rules missed; false contradiction alerts | Cross-field rule validation | P1 |
| R-22 | Compute completeness scores | Users need to know how complete a record is | Product record + schema | Calculate weighted completeness (critical attributes weighted more) | Weighting wrong; completeness misleading | Completeness metric validation against known-good records | P0 |
| R-23 | Compute confidence scores | Enables smart routing and honest quality reporting | Extraction and validation results | Score based on source quality, extraction method, validation results | Confidence scores dishonest (too high for low-quality extractions) | Confidence calibration against ground truth | P0 |
| R-24 | Flag values needing human review | Not everything can or should be automated | Confidence scores + validation results | Route low-confidence and high-risk values to review queue | Too many items routed (review overload); too few (errors slip through) | Review routing threshold tuning | P0 |

### 2.6 Provenance & Traceability

| # | Requirement | Why it matters | Input | Expected behavior | Failure risk | Validation need | Priority |
|---|------------|---------------|-------|-------------------|--------------|-----------------|----------|
| R-25 | Attach source reference to every attribute | Traceability is a core requirement | Extracted value | Record source document, page, section, passage for each value | Provenance missing for some values; provenance incorrect | Provenance completeness audit | P0 |
| R-26 | Preserve original extracted text | Enables verification and audit | Extracted value | Store the exact text/passage that was extracted | Original text lost or truncated | Original text preservation check | P0 |
| R-27 | Record extraction metadata | Understanding how values were obtained enables quality improvement | Extraction process | Record extraction method, timestamp, model version | Metadata incomplete; metadata not retained | Metadata completeness check | P1 |
| R-28 | Track information category of each value | Users must know whether a value is a fact, inference, or enrichment | Attribute value | Classify as: fact, normalized fact, derived value, enriched value, or inference | Misclassification; all values treated as equal | Category assignment validation | P1 |

### 2.7 Human Review

| # | Requirement | Why it matters | Input | Expected behavior | Failure risk | Validation need | Priority |
|---|------------|---------------|-------|-------------------|--------------|-----------------|----------|
| R-29 | Present evidence for review decisions | Reviewers need to see source data to make informed decisions | Flagged attribute + provenance | Show value, source, confidence, and extracted passage side by side | Evidence incomplete; reviewer cannot make informed decision | Evidence presentation completeness | P0 |
| R-30 | Support approve/reject/correct actions | Reviewers must be able to act on each flagged value | Review interface | Allow approve, reject, or correct with audit trail | Actions not recorded; corrections don't update the record | Action recording verification | P0 |
| R-31 | Support batch review | Reviewing one product at a time doesn't scale | Queue of flagged values | Group related reviews; allow bulk actions with per-item override | Batch action overrides individual judgment; bulk approve skips critical items | Batch action audit trail | P1 |

### 2.8 Output & Publishing

| # | Requirement | Why it matters | Input | Expected behavior | Failure risk | Validation need | Priority |
|---|------------|---------------|-------|-------------------|--------------|-----------------|----------|
| R-32 | Produce machine-readable structured output | Downstream systems need structured data, not prose | Complete product record | Output in a defined format (JSON, CSV, or equivalent) with all attributes, provenance, and quality scores | Output format inconsistent; fields missing; provenance not included | Output schema validation | P0 |
| R-33 | Produce human-readable product view | Reviewers and users need to see the data clearly | Complete product record | Display all fields with values, sources, confidence, and validation state | Display confusing; important information buried | User experience review | P1 |
| R-34 | Measure commerce-readiness per channel | Different channels have different requirements | Product record + channel requirements | Score completeness against channel-specific requirements | Channel requirements not defined; scoring inaccurate | Channel requirement validation | P1 |
| R-35 | Support channel-specific formatting | Different channels require different data formats | Product record + channel | Transform attributes to channel-specific format (Amazon, Google, B2B portal) | Format errors; channel-specific rules violated | Channel format validation | P2 |

---

## 3. Requirements Summary by Priority

### P0 — Absolutely Required (22 requirements)

| # | Requirement |
|---|------------|
| R-01 | Accept PDF documents as input |
| R-02 | Accept CSV/Excel supplier feeds as input |
| R-06 | Extract structured attributes from unstructured text |
| R-07 | Extract data from tables in PDFs |
| R-08 | Handle multi-product documents |
| R-09 | Resolve product identity from MPN + brand |
| R-10 | Detect duplicate products across sources |
| R-12 | Classify products into categories |
| R-13 | Support category-specific attribute schemas |
| R-14 | Map to industry taxonomies |
| R-15 | Fill missing attributes from additional sources |
| R-16 | Cross-reference multiple sources |
| R-17 | Normalize units |
| R-19 | Validate against schema rules |
| R-22 | Compute completeness scores |
| R-23 | Compute confidence scores |
| R-24 | Flag values needing human review |
| R-25 | Attach source reference to every attribute |
| R-26 | Preserve original extracted text |
| R-29 | Present evidence for review decisions |
| R-30 | Support approve/reject/correct actions |
| R-32 | Produce machine-readable structured output |

### P1 — Important (12 requirements)

| # | Requirement |
|---|------------|
| R-03 | Accept web pages as input |
| R-04 | Accept images as input |
| R-05 | Handle scanned PDFs |
| R-11 | Handle variant relationships |
| R-18 | Normalize terminology |
| R-20 | Validate value ranges |
| R-21 | Detect cross-field contradictions |
| R-27 | Record extraction metadata |
| R-28 | Track information category of each value |
| R-31 | Support batch review |
| R-33 | Produce human-readable product view |
| R-34 | Measure commerce-readiness per channel |

### P2 — Enhancement (1 requirement)

| # | Requirement |
|---|------------|
| R-35 | Support channel-specific formatting |

---

## 4. Cross-Cutting Requirements

These apply across all functional requirements:

| # | Requirement | Why it matters | Priority |
|---|------------|---------------|----------|
| CC-01 | Every extracted value must have provenance | Traceability is non-negotiable for trustworthy output | P0 |
| CC-02 | Unknown/missing must be represented, not fabricated | False data is worse than no data | P0 |
| CC-03 | Confidence scores must be honest and grounded | Misleading confidence defeats the purpose of scoring | P0 |
| CC-04 | System must support batch processing | Processing one product at a time doesn't scale | P0 |
| CC-05 | System must support incremental updates | Products change; sources update; reprocessing must be efficient | P1 |
| CC-06 | System must have audit trails | Every change must be traceable for compliance and debugging | P1 |
| CC-07 | System must handle conflicting sources | Real-world data is contradictory; the system must surface conflicts | P0 |
| CC-08 | System must not auto-publish unreviewed high-risk values | Safety and correctness over speed | P0 |

---

*This requirements document will be refined in Module 02 (Architecture) where implementation feasibility and technical constraints are assessed.*
