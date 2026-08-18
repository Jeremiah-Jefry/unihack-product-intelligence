# Canonical Product Model

> **Status:** Complete  
> **Module:** 2 — Canonical Product Intelligence Model & Data Contract  
> **Purpose:** Detailed domain model defining the structure, relationships, and invariants of a product intelligence record.  
> **Depends on:** `module-02-product-intelligence-specification.md`, Module 1 documents

---

## 1. Overview

This document defines the canonical product intelligence model — the conceptual structure that represents a product within our system. It is a **domain contract**, not a database schema or API model.

The model must support:
- incomplete products
- partially known products
- multimodal evidence
- conflicting sources
- normalized values
- derived values
- enriched values
- uncertain information
- human review
- provenance tracking
- validation
- category-specific attributes
- catalog-scale processing

---

## 2. Core Entities

### 2.1 Product

**What it is:** The central entity — a distinct, purchasable industrial item.

**Core identity fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID | Yes | System-generated unique identifier |
| `mpn` | string | Yes | Manufacturer Part Number — the primary external identifier |
| `brand` | string | Yes | Manufacturer or brand name |
| `name` | string | Conditional | Descriptive product name (required when available) |
| `model` | string | Optional | Model or series reference |
| `lifecycle_status` | enum | Yes | active, discontinued, obsolete, unknown |

**Classification fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `primary_category` | string | Yes | Internal category path (e.g., "Mounted Bearings > Pillow Block") |
| `category_confidence` | float 0.0-1.0 | Yes | Confidence in category assignment |
| `taxonomy_codes` | map<string, string> | Optional | External taxonomy codes (ETIM, UNSPSC, eCl@ss, GS1 GPC) |

**Manufacturer fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `manufacturer_name` | string | Yes | Official manufacturer name |
| `manufacturer_id` | string | Optional | Internal manufacturer identifier |

**Description fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `short_description` | string | Optional | Brief product description (1-2 sentences) |
| `long_description` | string | Optional | Detailed product description |

**Quality fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `completeness_score` | float 0.0-1.0 | Yes | Weighted completeness against category schema |
| `confidence` | float 0.0-1.0 | Yes | Overall confidence in the record |
| `validation_status` | enum | Yes | pending, validated, partially_validated, rejected |
| `review_status` | enum | Yes | not_required, pending_review, under_review, approved, rejected |
| `last_verified_at` | timestamp | Optional | When the record was last human-verified |

**Relationships:**

```
Product ──has──▶ ProductRecord
Product ──manufactured_by──▶ Manufacturer
Product ──belongs_to──▶ Category
Product ──related_to──▶ Product (multiple relationship types)
Product ──published_to──▶ Channel
Product ──sourced_from──▶ SourceDocument (many-to-many)
```

### 2.2 ProductRecord

**What it is:** The collection of all known attributes for a product, organized by domain.

**Core fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product_id` | UUID | Yes | Reference to Product |
| `attributes` | list<Attribute> | Yes | All known attributes |
| `conflicts` | list<Conflict> | Yes | All unresolved conflicts |
| `quality_metrics` | QualityMetrics | Yes | Overall quality assessment |
| `created_at` | timestamp | Yes | When the record was created |
| `updated_at` | timestamp | Yes | When the record was last modified |
| `version` | integer | Yes | Record version (incremented on change) |

### 2.3 Attribute

**What it is:** An atomic piece of product information with full provenance and quality metadata.

This is the most important entity in the model. Every piece of product information flows through an Attribute.

**Identity fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID | Yes | System-generated unique identifier |
| `product_id` | UUID | Yes | Reference to Product |
| `name` | string | Yes | Canonical attribute name (e.g., "bore_diameter") |
| `domain` | enum | Yes | Which domain this attribute belongs to (see Section 3) |

**Value fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `value_type` | enum | Yes | The type of value (see Section 4) |
| `value` | Value | Yes | The current/selected value |
| `original_value` | Value | Optional | The original value before normalization (when different from current) |
| `unit` | string | Optional | Unit of measurement (when applicable) |
| `normalized_value` | Value | Optional | Canonical representation (when normalization was applied) |
| `normalized_unit` | string | Optional | Canonical unit (when normalization was applied) |

**Provenance fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `information_category` | enum | Yes | What type of information this represents (see Section 5) |
| `information_category_detail` | string | Optional | Specific subcategory (e.g., "electrical_safety" for a certification) |
| `candidates` | list<CandidateValue> | Yes | All candidate values from different sources |
| `selected_candidate_id` | UUID | Optional | Which candidate is currently selected (null if unresolved) |
| `conflict_status` | enum | Yes | none, pending_resolution, resolved, permanently_conflicting |
| `conflict` | Conflict | Optional | Conflict details (when conflict_status is not 'none'); resolution is accessed via `Conflict.resolution_id` → `Resolution` |

**Quality fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `confidence` | float 0.0-1.0 | Yes | How trustworthy this value is |
| `validation_status` | enum | Yes | pending, auto_validated, human_validated, rejected |
| `lifecycle_state` | enum | Yes | discovered, extracted, normalized, enriched, validated, reviewed, approved, rejected |
| `requires_review` | boolean | Yes | Whether this attribute needs human review |
| `review_reason` | string | Optional | Why review is needed |

**Timestamp fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `extracted_at` | timestamp | Yes | When the value was first extracted |
| `last_validated_at` | timestamp | Optional | When the value was last validated |
| `last_reviewed_at` | timestamp | Optional | When the value was last reviewed by a human |
| `expires_at` | timestamp | Optional | When this value needs re-verification |

### 2.4 CandidateValue

**What it is:** A single value from a specific source, part of the evidence chain for an Attribute.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID | Yes | System-generated unique identifier |
| `attribute_id` | UUID | Yes | Reference to Attribute |
| `value` | Value | Yes | The extracted/obtained value |
| `unit` | string | Optional | Unit of measurement |
| `source_id` | UUID | Yes | Reference to SourceDocument |
| `source_location` | SourceLocation | Yes | Where in the source this value was found |
| `extraction_method` | enum | Yes | text_extraction, ocr, table_parsing, web_scraping, api_lookup, manual_entry, inference |
| `extraction_confidence` | float 0.0-1.0 | Yes | How confident the extraction was |
| `source_trust_score` | float 0.0-1.0 | Yes | How trustworthy this source is for this type of information |
| `freshness` | FreshnessInfo | Yes | How current this evidence is |
| `extracted_at` | timestamp | Yes | When this value was captured |
| `transformations` | list<Transformation> | Optional | What processing was applied to this value |

### 2.5 SourceDocument

**What it is:** Any input that contains product information.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID | Yes | System-generated unique identifier |
| `name` | string | Yes | Human-readable name (filename or URL) |
| `type` | enum | Yes | pdf, csv, excel, web_page, image, scanned_document, erp_export, api_response |
| `location` | string | Yes | File path or URL |
| `content_hash` | string | Yes | Hash of the document content (for change detection) |
| `acquired_at` | timestamp | Yes | When the document was ingested |
| `published_at` | timestamp | Optional | When the document was originally published (if known) |
| `trust_level` | enum | Yes | manufacturer_official, authorized_distributor, third_party_verified, third_party_unverified, unknown |
| `product_references` | list<UUID> | Yes | Which products this document is about |
| `extraction_status` | enum | Yes | pending, extracted, partially_extracted, failed |
| `metadata` | map<string, string> | Optional | Additional document metadata |

### 2.6 SourceLocation

**What it is:** The precise location within a source document where a value was found.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `page` | integer | Optional | Page number (for PDFs) |
| `section` | string | Optional | Section heading or identifier |
| `table_id` | string | Optional | Table identifier |
| `row` | integer | Optional | Row number within a table |
| `column` | string | Optional | Column header or identifier |
| `text_span` | string | Optional | The exact text passage that was extracted |
| `image_region` | BoundingBox | Optional | Region of an image (for visual extraction) |
| `url_fragment` | string | Optional | URL anchor or selector (for web pages) |

### 2.7 BoundingBox

**What it is:** A rectangular region in an image.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `x` | integer | Yes | Top-left X coordinate (pixels) |
| `y` | integer | Yes | Top-left Y coordinate (pixels) |
| `width` | integer | Yes | Width (pixels) |
| `height` | integer | Yes | Height (pixels) |
| `image_id` | string | Yes | Identifier for the image |

### 2.8 Transformation

**What it is:** A record of what processing was applied to a value.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | enum | Yes | unit_conversion, terminology_mapping, format_standardization, value_correction, derivation |
| `description` | string | Yes | Human-readable description of the transformation |
| `input_value` | Value | Yes | Value before transformation |
| `output_value` | Value | Yes | Value after transformation |
| `applied_at` | timestamp | Yes | When the transformation was applied |
| `applied_by` | string | Yes | What applied it (system, model_name, human_reviewer) |

### 2.9 FreshnessInfo

**What it is:** Information about how current the evidence is.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source_published_at` | timestamp | Optional | When the source was originally published |
| `source_version` | string | Optional | Version of the source document (if versioned) |
| `source_last_verified_at` | timestamp | Optional | When the source was last verified to be current |
| `freshness_status` | enum | Yes | current, outdated, unknown, requires_reverification |
| `freshness_reason` | string | Optional | Explanation of the freshness assessment |

### 2.10 Resolution

**What it is:** How a conflict between candidate values was resolved.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `method` | enum | Yes | source_priority, confidence_based, human_decision, rule_based, newest_wins |
| `selected_candidate_id` | UUID | Yes | Which candidate was selected |
| `reason` | string | Yes | Why this candidate was selected |
| `resolved_by` | string | Yes | Who/what resolved it (system, reviewer_id, rule_name) |
| `resolved_at` | timestamp | Yes | When the resolution was recorded |
| `rejection_candidates` | list<UUID> | Optional | Which candidates were rejected |

### 2.11 Conflict

**What it is:** A record of an unresolved or permanently conflicting set of candidate values.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID | Yes | System-generated unique identifier |
| `attribute_id` | UUID | Yes | Reference to Attribute |
| `candidate_ids` | list<UUID> | Yes | The conflicting candidate values |
| `conflict_type` | enum | Yes | value_mismatch, unit_mismatch, source_contradiction, stale_vs_current |
| `detected_at` | timestamp | Yes | When the conflict was detected |
| `status` | enum | Yes | open, investigating, resolved, permanently_conflicting |
| `resolution_id` | UUID | Optional | Reference to Resolution (when resolved) |

### 2.12 QualityMetrics

**What it is:** Overall quality assessment for a product record.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `completeness_score` | float 0.0-1.0 | Yes | Weighted completeness against category schema |
| `accuracy_score` | float 0.0-1.0 | Yes | Overall accuracy based on source quality and validation |
| `consistency_score` | float 0.0-1.0 | Yes | Cross-field and cross-source consistency |
| `freshness_score` | float 0.0-1.0 | Yes | How current the evidence is |
| `evidence_coverage` | float 0.0-1.0 | % of values with traceable provenance |
| `validation_coverage` | float 0.0-1.0 | % of values that have been validated |
| `conflict_count` | integer | Yes | Number of unresolved conflicts |
| `review_pending_count` | integer | Yes | Number of attributes awaiting human review |
| `commerce_readiness` | map<string, float> | Optional | Per-channel readiness scores |

### 2.13 Category

**What it is:** A node in a product taxonomy that determines which attributes are required.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID | Yes | System-generated unique identifier |
| `taxonomy` | string | Yes | Which taxonomy (internal, ETIM, UNSPSC, eCl@ss, GS1_GPC) |
| `code` | string | Yes | Category code within the taxonomy |
| `name` | string | Yes | Human-readable category name |
| `path` | list<string> | Yes | Hierarchical path (e.g., ["Industrial", "Bearings", "Mounted Bearings", "Pillow Block"]) |
| `parent_id` | UUID | Optional | Reference to parent category |
| `attribute_schema` | AttributeSchema | Yes | Which attributes are required/optional for this category |

### 2.14 AttributeSchema

**What it is:** The definition of which attributes are required, optional, and what values they can take for a given product category.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `category_id` | UUID | Yes | Reference to Category |
| `required_attributes` | list<AttributeDefinition> | Yes | Attributes that must be present |
| `optional_attributes` | list<AttributeDefinition> | Optional | Attributes that may be present |
| `controlled_vocabularies` | map<string, list<string>> | Optional | Allowed values for enum attributes |

### 2.15 AttributeDefinition

**What it is:** The definition of a single attribute within a schema.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Canonical attribute name |
| `domain` | enum | Yes | Which domain this attribute belongs to |
| `value_type` | enum | Yes | The type of value expected |
| `unit` | string | Optional | Expected unit (if measurement) |
| `required` | boolean | Yes | Whether this attribute is mandatory |
| `description` | string | Optional | Human-readable description |
| `validation_rules` | list<ValidationRule> | Optional | Rules for validating values of this attribute |

### 2.16 ProductRelationship

**What it is:** A relationship between two products.

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | UUID | Yes | System-generated unique identifier |
| `source_product_id` | UUID | Yes | The product that has the relationship |
| `target_product_id` | UUID | Yes | The related product |
| `relationship_type` | enum | Yes | replaces, compatible_with, accessory_of, equivalent_to, variant_of, requires, used_with, supersedes |
| `confidence` | float 0.0-1.0 | Yes | Confidence in the relationship |
| `source_id` | UUID | Optional | Reference to SourceDocument |
| `validated` | boolean | Yes | Whether this relationship has been validated |
| `notes` | string | Optional | Additional context about the relationship |

---

## 3. Attribute Domains

Attributes are organized into domains that correspond to the categories defined in the Module 1 problem definition.

| Domain | Description | Examples |
|--------|-------------|----------|
| `identity` | Product identifiers and names | mpn, brand, name, gtin, sku, model, series |
| `classification` | Category and taxonomy assignments | primary_category, etim_class, unspsc_code, eclass_class |
| `specification` | Technical specifications (category-specific) | bore_diameter, voltage_rating, flow_coefficient, pressure_rating |
| `physical` | Physical characteristics | dimensions, weight, color, finish, material |
| `performance` | Performance characteristics | load_rating, speed_rating, efficiency, power_output |
| `electrical` | Electrical characteristics | voltage, current, frequency, power_factor |
| `mechanical` | Mechanical characteristics | torque, pressure, flow_rate, stroke_length |
| `environmental` | Operating conditions | operating_temperature, operating_humidity, ip_rating, corrosion_resistance |
| `certification` | Certifications and compliance | ce_mark, ul_listed, rohs_compliant, Reach_compliance |
| `commercial` | Commercial information | unit_of_measure, moq, lead_time, warranty, country_of_origin |
| `compatibility` | Compatibility and relationships | compatible_shaft_size, replaces_part, cross_reference |
| `description` | Textual descriptions | short_description, long_description, features |
| `media` | Digital assets | product_image, datasheet, cad_file, installation_manual |

---

## 4. Value Types

See `attribute-taxonomy.md` for detailed definitions. Summary:

| Type | Description | Example |
|------|-------------|---------|
| `string` | Free text | "Cast iron housing" |
| `number` | Numeric value | 30.163 |
| `boolean` | True/false | true |
| `enum` | Controlled vocabulary | "IP65" |
| `range` | Min-max range | -20°C to +80°C |
| `measurement` | Number + unit | 15.9 kN |
| `dimension` | L × W × H | 152 × 42 × 48 mm |
| `percentage` | Percentage value | 85% |
| `date` | Date value | 2027-06-15 |
| `duration` | Time period | 2-3 weeks |
| `compound` | Structured object | { thread: "M10", pitch: "1.5", grade: "8.8" } |
| `list` | Multiple values | ["CE", "UL", "RoHS"] |

---

## 5. Information Categories

Every provenance record must classify what type of information the evidence supports. This enables downstream systems to weight evidence by trustworthiness for different information types.

| Category | Description | Examples | Typical Source Trust |
|----------|-------------|----------|---------------------|
| `identity` | Product identifiers and names | MPN, brand, GTIN, product name | manufacturer_official |
| `specification` | Technical specifications | Bore diameter, voltage rating, flow coefficient, performance | manufacturer_official |
| `classification` | Category and taxonomy | Category assignment, ETIM/UNSPSC codes | manufacturer_official, third_party_verified |
| `certification` | Certifications and compliance | CE, UL, RoHS, expiry dates | manufacturer_official |
| `safety` | Safety-critical information | Load limits, operating limits, warnings | manufacturer_official |
| `commercial` | Commercial information | Price, MOQ, lead time, warranty | manufacturer_official, authorized_distributor |
| `physical` | Physical characteristics | Length, width, height, weight, material, finish | manufacturer_official |
| `compatibility` | Compatibility and relationships | Cross-references, replacements, accessories | manufacturer_official, third_party_verified |
| `description` | Textual descriptions | Short description, long description | manufacturer_official, third_party_verified |
| `media` | Digital assets | Images, datasheets, CAD files | manufacturer_official |

### 5.1 Domain-to-Information-Category Mapping

Not all attribute domains map 1:1 to information categories. The following table defines the default mapping:

| Domain | Default Information Category | Notes |
|--------|------------------------------|-------|
| `identity` | `identity` | Always identity |
| `classification` | `classification` | Always classification |
| `specification` | `specification` | Always specification |
| `physical` | `physical` | For intrinsic physical properties: material, weight, color, finish |
| `physical` (dimensional) | `specification` | For dimensional/structural specs derived from engineering requirements (e.g., bolt_pattern) |
| `performance` | `specification` | Performance ratings are technical specifications |
| `electrical` | `specification` | Electrical ratings are technical specifications |
| `mechanical` | `specification` | Mechanical ratings are technical specifications |
| `environmental` | `specification` | Environmental ratings are technical specifications |
| `certification` | `certification` | Always certification |
| `commercial` | `commercial` | Always commercial |
| `compatibility` | `compatibility` | Always compatibility |
| `description` | `description` | Always description |
| `media` | `media` | Always media |

**Rule:** When an attribute belongs to a domain that maps to `specification`, the information category is `specification`. When an attribute belongs to `physical` domain, use `physical` for intrinsic physical properties (material, weight, color) and `specification` for dimensional/structural specs derived from engineering requirements.

---

## 6. Domain Invariants

These rules must always hold:

1. **Every attribute has at least one candidate value.** An attribute with no candidates should not exist — the information is simply missing.

2. **Every candidate has a source.** No value exists without provenance. If the source is unknown, the value is an inference with no source evidence.

3. **Conflicts are never silently resolved.** When sources disagree, the conflict is recorded. Resolution requires either evidence-based rules or human decision.

4. **Original values are preserved.** When normalization or transformation is applied, the original value is always preserved alongside the normalized value.

5. **Information category is mandatory on provenance.** Every piece of evidence must be classified by what type of information it supports.

6. **Freshness is tracked.** Every source has a freshness assessment. Stale evidence is flagged, not silently used.

7. **Lifecycle state is monotonically advancing (mostly).** Attributes generally move forward through states. Regression (e.g., from "approved" back to "extracted") requires explicit reason and audit trail.

8. **Quality metrics reflect evidence.** Scores are grounded in source quality, validation results, and completeness — not arbitrary numbers.

---

## 7. Conceptual Relationships Diagram

```
                          ┌─────────────────┐
                          │   Product        │
                          │─────────────────│
                          │ id              │
                          │ mpn             │
                          │ brand           │
                          │ name            │
                          │ lifecycle_status│
                          └────────┬────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
          ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
          │ Category    │ │ Manufacturer│ │ Channel     │
          │─────────────│ │─────────────│ │─────────────│
          │ taxonomy    │ │ name        │ │ name        │
          │ code        │ │ trust_level │ │ requirements│
          │ attribute_  │ └─────────────┘ └─────────────┘
          │   schema    │
          └─────────────┘
                    │
                    ▼
          ┌─────────────────────────────────┐
          │   ProductRecord                 │
          │─────────────────────────────────│
          │ attributes: list<Attribute>     │
          │ conflicts: list<Conflict>       │
          │ quality_metrics: QualityMetrics │
          └────────────────┬────────────────┘
                           │
                           ▼
          ┌─────────────────────────────────┐
          │   Attribute                     │
          │─────────────────────────────────│
          │ name: string                    │
          │ domain: enum                    │
          │ information_category: enum      │
          │ value: Value                    │
          │ candidates: list<CandidateValue>│
          │ confidence: float               │
          │ validation_status: enum         │
          │ lifecycle_state: enum           │
          │ conflict_status: enum           │
          └────────────────┬────────────────┘
                           │
                           ▼
          ┌─────────────────────────────────┐
          │   CandidateValue                │
          │─────────────────────────────────│
          │ value: Value                    │
          │ source: SourceDocument          │
          │ location: SourceLocation        │
          │ extraction_method: enum         │
          │ extraction_confidence: float    │
          │ source_trust_score: float       │
          │ freshness: FreshnessInfo        │
          │ transformations: list<...>      │
          └────────────────┬────────────────┘
                           │
                           ▼
          ┌─────────────────────────────────┐
          │   SourceDocument                │
          │─────────────────────────────────│
          │ type: enum                      │
          │ location: string                │
          │ trust_level: enum               │
          │ published_at: timestamp         │
          │ content_hash: string            │
          └─────────────────────────────────┘
```

---

*This canonical model is the foundation for all Module 2 deliverables. See `attribute-taxonomy.md` for value type details, `provenance-and-evidence-model.md` for evidence details, and `validation-and-lifecycle-model.md` for lifecycle details.*
