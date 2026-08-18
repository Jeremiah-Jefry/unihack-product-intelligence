# Provenance and Evidence Model

> **Status:** Complete  
> **Module:** 2 — Canonical Product Intelligence Model & Data Contract  
> **Purpose:** Define the source, evidence, location, extraction, transformation, confidence, freshness, and traceability chain.  
> **Depends on:** `canonical-product-model.md`

---

## 1. Overview

Provenance is the chain of evidence connecting a product attribute value to its source. Without provenance, a value is unverifiable. This document defines how provenance is represented, tracked, and used.

---

## 2. Core Concepts

### 2.1 Source Document

Any input that contains product information. Sources are the foundation of the evidence chain.

**Source types:**

| Type | Description | Typical trust level |
|------|-------------|---------------------|
| `pdf` | PDF document (datasheet, catalog, spec sheet) | manufacturer_official to third_party_unverified |
| `csv` | CSV file (supplier feed) | manufacturer_official to third_party_unverified |
| `excel` | Excel file (supplier feed) | manufacturer_official to third_party_unverified |
| `web_page` | HTML page (manufacturer website) | manufacturer_official to third_party_unverified |
| `image` | Image file (product photo, label) | manufacturer_official to third_party_unverified |
| `scanned_document` | Image-based PDF (no text layer) | manufacturer_official to third_party_unverified |
| `erp_export` | Export from ERP system | manufacturer_official |
| `api_response` | Data from an API | varies |

**Trust levels:**

| Level | Description | Example |
|-------|-------------|---------|
| `manufacturer_official` | Official manufacturer data | Manufacturer's own datasheet |
| `authorized_distributor` | Authorized distributor data | Distributor's catalog feed |
| `third_party_verified` | Third-party data that has been verified | Verified database entry |
| `third_party_unverified` | Third-party data not yet verified | Unverified web scrape |
| `unknown` | Trust level unknown | New source without reputation |

### 2.2 Evidence

The specific piece of information from a source that supports a value. Evidence includes:
- Where in the source the value was found
- What the source actually says
- How the value was obtained from the source
- How trustworthy the source is for this type of information

### 2.3 Source Location

The precise location within a source document where a value was found. This enables verification — a human reviewer can go to the exact location and check whether the system extracted the value correctly.

### 2.4 Fact Type Classification

Every attribute value can be classified into one of these fact types based on its provenance fields:

| Fact Type | Description | extraction_method | transformations | lifecycle_state | Example |
|-----------|-------------|-------------------|-----------------|-----------------|---------|
| **Source-supported fact** | Directly extracted from a source document | `text_extraction`, `ocr`, `table_parsing`, `web_scraping`, `api_lookup`, `manual_entry` | None | `extracted` → `validated` → `approved` | "Bore: 1-3/16 in" extracted from datasheet |
| **Normalized fact** | Source fact after unit conversion or terminology mapping | Any extraction method | At least one transformation present | `normalized` → `validated` → `approved` | 1-3/16 in → 30.163 mm |
| **Derived value** | Computed from other attribute values | `inference` | Derivation transformation | `enriched` → `validated` → `approved` | Bolt pattern derived from bore diameter + housing style |
| **Enriched value** | Obtained from an additional external source | `web_scraping`, `api_lookup` | Optional | `enriched` → `validated` → `approved` | Material sourced from manufacturer website |
| **Inference** | AI-generated without direct source evidence | `inference` | None | `extracted` → `reviewed` → `approved` | Material inferred from product name |
| **Unresolved** | Conflicting values pending resolution | Any | Any | Any (conflict_status ≠ none) | Source A: 1.2 kg, Source B: 1.35 kg |

**Classification rule:** A value's fact type is determined by the combination of its `extraction_method`, presence of `transformations`, and `lifecycle_state`. The `extraction_method: "inference"` does not automatically mean "inference" fact type — derived values also use inference but have derivation transformations and known input attributes.

---

## 3. Evidence Chain

Every attribute value traces through this chain:

```
Source Document
    │
    ▼
Source Location (page, section, table, row, text_span)
    │
    ▼
Extraction Method (text_extraction, ocr, table_parsing, etc.)
    │
    ▼
Extraction Confidence (0.0-1.0)
    │
    ▼
Transformations (unit conversion, normalization, etc.)
    │
    ▼
Attribute Value
```

---

## 4. Evidence Models by Extraction Method

### 4.1 PDF Text Extraction

```
Source: UCF209-datasheet.pdf (manufacturer_official)
Location: Page 2, "Technical Data" table, Row 1, Column "Bore"
Text span: "Bore: 1-3/16 in (30.163 mm)"
Extraction method: text_extraction
Extraction confidence: 0.95
Freshness: current (published 2024-03-15, verified 2026-08-01)
```

### 4.2 Table Parsing

```
Source: bearing-catalog-2024.pdf (manufacturer_official)
Location: Page 15, Table 3 (UCF Series), Row 4, Column "Dynamic Load"
Text span: "15.9"
Extraction method: table_parsing
Extraction confidence: 0.92
Freshness: current (catalog 2024 edition)
```

### 4.3 OCR from Scanned Document

```
Source: legacy-bearings-scan.pdf (third_party_verified)
Location: Page 7, paragraph 3
Text span: "Bore diameter 1-3/16 inch" (OCR confidence: 0.88)
Extraction method: ocr
Extraction confidence: 0.85 (lower due to OCR uncertainty)
Freshness: unknown (scan date unknown)
```

### 4.4 Web Scraping

```
Source: https://iptci.com/products/UCF209 (manufacturer_official)
Location: "Specifications" section
Text span: "Bore Diameter: 1-3/16 in"
Extraction method: web_scraping
Extraction confidence: 0.90
Freshness: current (page last updated 2026-06-01)
```

### 4.5 API Lookup

```
Source: etim-api-response.json (third_party_verified)
Location: feature "EC000123" → "Bore diameter"
Value: 30.163
Extraction method: api_lookup
Extraction confidence: 0.98
Freshness: current (API data updated daily)
```

### 4.6 Derived Value

```
Source: computed from bore_diameter + housing_style
Input attributes: [bore_diameter: 30.163mm, housing_style: pillow_block]
Derivation rule: standard_pillow_block_bolt_pattern
Extraction method: inference
Extraction confidence: 0.85
Freshness: current (derived from current values)
```

### 4.7 Enriched Value

```
Source: manufacturer-website-2026-08-10 (manufacturer_official)
Location: Product page for UCF209
Text span: "Material: Cast iron housing"
Extraction method: web_scraping
Extraction confidence: 0.90
Source trust score: 0.95 (manufacturer official)
Freshness: current
```

### 4.8 Inference

```
Source: AI inference from product name and specifications
Basis: "UCF209" is a standard pillow block bearing designation
Extraction method: inference
Extraction confidence: 0.60
Freshness: N/A (inference, not source-based)
```

---

## 5. Confidence Model

### 5.1 Confidence vs. Correctness

**Confidence** is how strongly the system believes the value is likely correct, based on:
- Source quality
- Extraction certainty
- Validation results
- Number of corroborating sources

**Correctness** is whether the value actually matches reality. Confidence does not guarantee correctness — a value can be extracted with high confidence from a source that is itself wrong.

### 5.2 Confidence Components

Confidence is calculated from multiple factors:

| Factor | Weight | Description |
|--------|--------|-------------|
| Source trust score | 0.3 | How trustworthy the source is |
| Extraction confidence | 0.3 | How certain the extraction was |
| Source corroboration | 0.2 | How many sources agree |
| Validation status | 0.2 | Whether the value passed validation |

**Formula:**

```
confidence = (0.3 × source_trust_score) + (0.3 × extraction_confidence) + (0.2 × corroboration_score) + (0.2 × validation_score)
```

Where:
- `source_trust_score` = `CandidateValue.source_trust_score` (0.0–1.0)
- `extraction_confidence` = `CandidateValue.extraction_confidence` (0.0–1.0)
- `corroboration_score` = min(1.0, number_of_agreeing_sources / 3) — capped at 1.0 when 3+ sources agree
- `validation_score` = 1.0 if `validation_status` is `auto_validated` or `human_validated`, 0.5 if `pending`, 0.0 if `rejected`

For attributes with a single candidate, `corroboration_score` = 0.33 (one source provides baseline corroboration).

### 5.3 Confidence Ranges

| Range | Interpretation | Typical action |
|-------|---------------|----------------|
| 0.9 - 1.0 | High confidence | Auto-approve (if validation passes) |
| 0.7 - 0.89 | Medium confidence | Auto-approve with flag |
| 0.5 - 0.69 | Low confidence | Route to human review |
| 0.0 - 0.49 | Very low confidence | Require human review before use |

---

## 6. Source Freshness

### 6.1 Freshness Assessment

Freshness is tracked per `CandidateValue`, not per `SourceDocument`. A single source document may produce multiple extractions at different times, each with its own freshness assessment. The `SourceDocument` entity provides the raw timestamps (`published_at`, `acquired_at`) from which freshness is computed.

Each `CandidateValue` has a `FreshnessInfo` object:

| Status | Description | Action |
|--------|-------------|--------|
| `current` | Source is recent and believed to be accurate | Use with full confidence |
| `outdated` | Newer version exists or source is known to be stale | Flag for re-verification |
| `unknown` | Cannot determine when source was published | Use with reduced confidence |
| `requires_reverification` | Source age exceeds freshness threshold | Schedule re-verification |

### 6.2 Freshness Thresholds

| Source type | Freshness threshold | Reasoning |
|-------------|---------------------|-----------|
| Manufacturer datasheet | 2 years | Specs change slowly but standards evolve |
| Manufacturer website | 1 year | Websites are updated more frequently |
| Supplier feed | 6 months | Supplier data should be current |
| Third-party database | 1 year | Varies by database |
| Certification data | 1 year | Certifications expire |

### 6.3 Freshness Propagation

When a source is assessed as outdated:
1. All attributes derived from that source are flagged as "requires_reverification"
2. The freshness score for the product is reduced
3. The system may attempt to find a newer source
4. Human review may be triggered

---

## 7. Information Category on Provenance

### 7.1 Why It Matters

Not all evidence is equally trustworthy for all purposes. A manufacturer's datasheet is authoritative for technical specifications but may not be current for commercial attributes. Information category enables downstream systems to weight evidence by type.

### 7.2 Categories

| Category | Description | Typical source trust requirement |
|----------|-------------|----------------------------------|
| `identity` | Product identifiers and names | manufacturer_official |
| `specification` | Technical specifications | manufacturer_official |
| `classification` | Category and taxonomy | manufacturer_official, third_party_verified |
| `certification` | Certifications and compliance | manufacturer_official |
| `safety` | Safety-critical information | manufacturer_official |
| `commercial` | Commercial information | manufacturer_official, authorized_distributor |
| `physical` | Physical characteristics | manufacturer_official |
| `compatibility` | Compatibility and relationships | manufacturer_official, third_party_verified |
| `description` | Textual descriptions | manufacturer_official, third_party_verified |
| `media` | Digital assets | manufacturer_official |

### 7.3 Usage

Information category is used for:
1. **Evidence weighting** — manufacturer specs weighted higher than third-party descriptions
2. **Review routing** — safety information always requires human review
3. **Freshness requirements** — certification data has stricter freshness requirements
4. **Conflict resolution** — manufacturer data preferred over third-party for specifications

---

## 8. Transformation Tracking

### 8.1 What Is Tracked

Every transformation applied to a value is recorded:

1. **What type of transformation** (unit conversion, terminology mapping, format standardization)
2. **What the input was** (original value and unit)
3. **What the output is** (normalized value and unit)
4. **When it was applied** (timestamp)
5. **What applied it** (system, model name, human reviewer)

### 8.2 Transformation Types

| Type | Description | Example |
|------|-------------|---------|
| `unit_conversion` | Converting between unit systems | 1-3/16 in → 30.163 mm |
| `terminology_mapping` | Mapping to controlled vocabulary | "SS304" → "stainless steel 304" |
| `format_standardization` | Standardizing format | "2027/06/15" → "2027-06-15" |
| `value_correction` | Correcting an extracted value | "3/8 mm" → "3/8 in" (unit correction) |
| `derivation` | Computing from other values | Bolt pattern derived from bore diameter |

### 8.3 Why It Matters

1. **Verification** — a reviewer can see exactly what transformation was applied
2. **Audit trail** — every change is traceable
3. **Debugging** — if a normalized value is wrong, the transformation can be examined
4. **Reversibility** — original values are preserved, so transformations can be undone

---

## 9. Traceability Requirements

### 9.1 Minimum Traceability

For every attribute value, the system must be able to answer:
1. **Where** did this value come from? (Source document)
2. **How** was it obtained? (Extraction method)
3. **When** was it captured? (Timestamp)
4. **How certain** is the system? (Confidence score)
5. **What type** of information is this? (Information category)

### 9.2 Full Traceability

For complete traceability, the system must also answer:
6. **Where exactly** in the source? (Page, section, table, row, text span)
7. **What processing** was applied? (Transformations)
8. **How current** is the source? (Freshness)
9. **How trustworthy** is the source? (Trust level)
10. **Has it been validated?** (Validation status)

### 9.3 Traceability Coverage

The system tracks traceability coverage:
- **Provenance coverage:** % of values with at least one source reference
- **Provenance depth:** % of values with full provenance (source + location + confidence)
- **Source diversity:** % of products with data from multiple sources

---

## 10. Multimodal Evidence

### 10.1 Supported Modalities

| Modality | Evidence representation | Example |
|----------|------------------------|---------|
| Text | Text span from document | "Bore: 1-3/16 in" |
| Table | Table ID + row + column | Table 3, Row 4, Column "Bore" |
| Image | Bounding box in image | Product label region |
| Diagram | Bounding box in diagram | Technical drawing annotation |
| Web | URL + CSS selector | Product page specifications section |

### 10.2 Image Evidence

For visual extraction (OCR, VLM), evidence includes:
- Image file reference
- Bounding box coordinates (x, y, width, height)
- What the image shows (text, diagram, label)
- Extraction confidence (OCR confidence or VLM confidence)

---

*This provenance model ensures every value in the system is traceable, verifiable, and trustworthy. See `validation-and-lifecycle-model.md` for how provenance feeds into validation and lifecycle management.*
