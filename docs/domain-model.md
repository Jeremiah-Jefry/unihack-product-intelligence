# Domain Model

> **Status:** Complete  
> **Module:** 1 — Problem & Domain Understanding  
> **Purpose:** Define the core entities, relationships, and processes in the industrial product intelligence domain.  
> **Depends on:** `module-01-problem-definition.md`

---

## 1. Overview

This document defines the domain model — the key concepts, their relationships, and the processes that operate on them. This is a **conceptual** model, not a data model or schema. It describes the problem domain in technology-independent terms.

---

## 2. Core Entities

### 2.1 Product

**What it is:** A distinct, purchasable industrial item that can be identified, described, and transacted.

**Key characteristics:**
- Has a unique identity (MPN, brand, optionally GTIN)
- Belongs to one or more categories
- Has technical specifications that define its capabilities
- Has physical attributes (dimensions, weight, material)
- Has commercial attributes (UOM, lead time, warranty)
- May have relationships to other products (replacements, accessories, equivalents)
- Has associated media (images, datasheets, drawings)
- Has provenance data linking every important value to its source

**Why it matters:** The product is the central entity. Everything else exists to describe, classify, validate, or serve the product.

### 2.2 Product Record

**What it is:** The structured representation of a product within the system — the "golden record" that aggregations, enrichments, and validations produce.

**Key characteristics:**
- Contains all known attributes for a product
- Each attribute has a value, a source, a confidence score, and a validation state
- May be incomplete (some fields marked as "unknown" or "requires verification")
- Has overall quality metrics (completeness, accuracy, consistency)
- Has a review/approval status
- Can be versioned (changes tracked over time)

**Relationship to Product:** A Product has one canonical Product Record. Multiple source documents contribute to this record.

### 2.3 Source Document

**What it is:** Any input that contains product information — a PDF datasheet, a web page, a CSV file, an image, a scanned document, an ERP export, or any other artifact.

**Key characteristics:**
- Has a type (pdf, web-page, csv, image, scanned-document, erp-export, etc.)
- Has a location (file path, URL)
- May contain information about multiple products
- May contain conflicting information with other sources
- Has a timestamp (when acquired, when published)
- Has a trustworthiness level (manufacturer-official, third-party, unverified)
- Contains extractable content (text, tables, images, diagrams)

**Why it matters:** Source documents are the evidence base. Without them, there is no provenance.

### 2.4 Attribute

**What it is:** A specific piece of information about a product — a field with a name, a value, a unit, and metadata.

**Key characteristics:**
- Has a name (e.g., "bore diameter", "brand", "weight")
- Has a value (e.g., "1-3/16 in", "IPTCI", "1.2 kg")
- Has a data type (numeric, text, date, enumeration, boolean)
- Has optional units (mm, kg, °C, etc.)
- Has provenance (source document, page, passage, confidence)
- Has a validation state (pending, validated, rejected, human-approved)
- Has an information category (fact, normalized fact, derived value, enriched value, inference)

**Why it matters:** Attributes are the atomic units of product intelligence. Quality and trustworthiness are measured at the attribute level.

### 2.5 Category / Classification

**What it is:** A node in a product taxonomy that describes what type of product something is.

**Key characteristics:**
- Belongs to a specific taxonomy (ETIM, UNSPSC, eCl@ss, GS1 GPC, or custom)
- Has a hierarchical path (Segment > Family > Class > Commodity)
- Defines which attributes are required for products in this category
- May have synonyms (alternative names for the same category)
- Has a version (taxonomies are updated periodically)

**Why it matters:** Classification determines the attribute schema. A product in the "Pillow Block Bearing" category requires bore diameter, load rating, and housing type. A product in the "Pipe Fitting" category requires nominal size, material, and pressure rating. Wrong classification → wrong attributes shown.

### 2.6 Attribute Schema

**What it is:** The set of attributes required (and optional) for a given product category.

**Key characteristics:**
- Defined per category
- Specifies required attributes, optional attributes, and controlled vocabularies
- Defines data types, units, and allowed values for each attribute
- May differ between taxonomies (ETIM features vs. eCl@ss properties)
- May differ between channels (marketplace requirements vs. internal requirements)

**Why it matters:** The attribute schema is the contract between the system and its output. Without it, completeness cannot be measured.

### 2.7 Manufacturer

**What it is:** The company that produces a product.

**Key characteristics:**
- Has a name and identifiers
- May have multiple brand names
- Has a relationship to its products (manufactured-by)
- May have its own data standards and formats
- Has a trustworthiness level as a source (official manufacturer data is higher trust than third-party)

**Why it matters:** Manufacturer identity is key to product identity and source trustworthiness.

### 2.8 Channel

**What it is:** A destination where product data is published or consumed — a marketplace, an e-commerce site, a distributor portal, a procurement system.

**Key characteristics:**
- Has specific data requirements (required fields, formats, taxonomies)
- Has validation rules specific to that channel
- Has acceptance criteria (what makes a listing "ready" for this channel)
- May require specific classification codes (e.g., Amazon requires GTIN; Google Shopping requires GPC)

**Why it matters:** Commerce-readiness is per-channel. A product may be ready for one channel but not another.

---

## 3. Core Relationships

```
Manufacturer ──produces──▶ Product
Product ──has──▶ Product Record
Product ──belongs to──▶ Category (in Taxonomy)
Category ──defines──▶ Attribute Schema
Product Record ──contains──▶ Attribute
Attribute ──sourced from──▶ Source Document
Attribute ──has──▶ Provenance
Product ──related to──▶ Product (replaces, compatible-with, accessory-of)
Product ──published to──▶ Channel
Channel ──requires──▶ Attribute Schema
Source Document ──about──▶ Product (one or many)
```

### 3.1 Product ↔ Source Document (Many-to-Many)

One source document may contain information about many products (e.g., a catalog PDF). One product may have many source documents (datasheet, website, ERP record, image).

The system must resolve which parts of which source document apply to which product.

### 3.2 Product ↔ Category (Many-to-Many, with Confidence)

A product may be classified into one or more categories. Classification has a confidence score. Wrong classification is a high-impact error because it determines which attributes are required.

### 3.3 Attribute ↔ Source Document (Many-to-One, with Location)

Each attribute value traces back to a specific location in a specific source document. This is the provenance chain.

### 3.4 Product ↔ Product (Multiple Relationship Types)

Products relate to each other through:
- **Replaces / Supersedes:** Product A replaces Product B
- **Compatible with:** Product A works with Product B
- **Accessory of:** Product A is an accessory for Product B
- **Equivalent / Cross-reference:** Product A is equivalent to Product B from another brand
- **Variant of:** Product A is a variant of Product B (different size, material, etc.)

---

## 4. Core Processes

### 4.1 Ingestion

**What happens:** Source documents are received by the system.

**Inputs:** PDFs, web pages, CSV files, images, ERP exports, manual uploads.

**Outputs:** Stored source documents with metadata (type, timestamp, trustworthiness).

**Key concerns:**
- Format detection and parsing
- Multi-product isolation (which products are in this document?)
- Text extraction (OCR for scanned documents; HTML parsing for web pages)
- Table structure preservation

### 4.2 Extraction

**What happens:** Product attributes are extracted from source documents.

**Inputs:** Parsed source documents.

**Outputs:** Candidate attributes with source references and confidence scores.

**Key concerns:**
- Accurate reading of tables, text, and images
- Correct association of extracted values to the right product
- Unit detection and normalization
- Handling of ambiguous or missing data
- Provenance tracking (where in the source did this value come from?)

### 4.3 Identity Resolution

**What happens:** The system determines which extracted values belong to the same real-world product.

**Inputs:** Extracted attributes from multiple sources.

**Outputs:** Canonical product records with matched/merged data.

**Key concerns:**
- Matching by MPN, GTIN, brand, and other identifiers
- Detecting duplicates across sources
- Resolving conflicts when sources disagree
- Handling variant relationships (same product, different size)

### 4.4 Classification

**What happens:** Products are assigned to categories in one or more taxonomies.

**Inputs:** Product attributes (especially identity and key specs).

**Outputs:** Category assignment with confidence score.

**Key concerns:**
- Accurate classification into the correct category
- Mapping to the right taxonomy (ETIM, UNSPSC, eCl@ss, custom)
- Determining which attribute schema applies
- Handling products that could belong to multiple categories

### 4.5 Enrichment

**What happens:** Missing attributes are filled from additional sources.

**Inputs:** Partial product records; additional source documents or external databases.

**Outputs:** More complete product records with enriched values and provenance.

**Key concerns:**
- Only enrich from trustworthy sources
- Every enriched value must have provenance
- Enriched values must be flagged as "enriched" (not original)
- Cross-source enrichment must detect conflicts
- Enrichment quality must be validated

### 4.6 Normalization

**What happens:** Values are converted to a consistent representation.

**Inputs:** Raw attribute values in various formats.

**Outputs:** Normalized values with original preserved.

**Key concerns:**
- Unit conversion (inches → mm, lbs → kg)
- Terminology mapping (free text → controlled vocabulary)
- Format standardization (dates, identifiers, numbers)
- Preserving original values alongside normalized ones

### 4.7 Validation

**What happens:** Product records are checked against rules for correctness and completeness.

**Inputs:** Product records; validation rules (schema, type, range, cross-field, channel-specific).

**Outputs:** Validation results (pass/fail per rule per field); overall quality scores.

**Key concerns:**
- Multiple validation layers (see Problem Definition, Section 8)
- Distinguishing blocking errors from warnings
- Routing failures to the appropriate handler
- Measuring validation pass rates over time

### 4.8 Quality Scoring

**What happens:** Product records are assessed for overall quality.

**Inputs:** Product records; validation results; provenance data.

**Outputs:** Quality metrics (completeness score, accuracy confidence, consistency flags).

**Key concerns:**
- Weighted completeness (critical attributes weighted more than optional ones)
- Accuracy confidence based on source quality and validation results
- Consistency measurement across fields and across sources
- Freshness of data

### 4.9 Review and Approval

**What happens:** Human reviewers evaluate low-confidence or high-risk values.

**Inputs:** Product records with flagged fields; evidence (source documents, confidence scores).

**Outputs:** Approved, rejected, or corrected values; audit trail.

**Key concerns:**
- Efficient routing (only show what needs review)
- Evidence presentation (source document, extracted passage, confidence)
- Batch review capabilities
- Audit trail for compliance

### 4.10 Publishing / Syndication

**What happens:** Approved product records are formatted and delivered to target channels.

**Inputs:** Approved product records; channel-specific requirements.

**Outputs:** Channel-ready data feeds.

**Key concerns:**
- Mapping internal attributes to channel-specific formats
- Meeting channel-specific validation rules
- Handling channel-specific taxonomies
- Tracking publication status per channel

---

## 5. Information Flow

```
Source Documents
      │
      ▼
  ┌──────────┐
  │ Ingestion │
  └──────────┘
      │
      ▼
  ┌──────────┐
  │ Extraction │
  └──────────┘
      │
      ▼
  ┌─────────────────┐
  │ Identity         │
  │ Resolution       │
  └─────────────────┘
      │
      ▼
  ┌──────────────┐
  │ Classification │
  └──────────────┘
      │
      ▼
  ┌──────────────┐
  │ Enrichment    │
  └──────────────┘
      │
      ▼
  ┌──────────────┐
  │ Normalization │
  └──────────────┘
      │
      ▼
  ┌──────────────┐
  │ Validation    │
  └──────────────┘
      │
      ▼
  ┌──────────────┐
  │ Quality       │
  │ Scoring       │
  └──────────────┘
      │
      ├──▶ Human Review (for low-confidence / high-risk)
      │
      ▼
  ┌──────────────┐
  │ Publishing    │
  └──────────────┘
      │
      ▼
  Channel-Ready Product Data
```

**Key principle:** This is a pipeline, but not strictly linear. Extraction may trigger re-classification. Validation failures may trigger re-extraction. Human review may correct values that trigger re-validation. The system must support iterative refinement.

---

## 6. Key Domain Concepts Explained

### 6.1 What is a "Canonical Product Record"?

**What:** The single, authoritative, structured representation of a product in the system.

**Why:** Without a canonical record, the same product may exist in multiple forms (from different sources), creating confusion and inconsistency.

**Example:** Supplier A calls it `UCF209-28`. Supplier B calls it `BRG-UCF209-28`. The manufacturer calls it `UCF209 1-3/16"`. The canonical record unifies these under one identity.

**Implication:** Identity resolution (matching, deduplication) is a critical prerequisite for enrichment and validation.

### 6.2 What is "Provenance"?

**What:** The chain of evidence connecting a product attribute value to its source.

**Why:** Without provenance, a value is unverifiable. You cannot determine whether it was extracted correctly, whether the source is trustworthy, or whether it needs human review.

**Example:** Bore diameter = `1-3/16 in` → Source: `UCF209-datasheet.pdf`, Page 2, Table 3, Row 1 → Extracted passage: `"Bore: 1-3/16 in (30.163 mm)"` → Confidence: `0.95` → Validation: `auto-validated`

**Implication:** Every enrichment or extraction step must preserve provenance. Provenance is not optional metadata — it is a core requirement.

### 6.3 What is "Confidence"?

**What:** A numeric score (typically 0.0-1.0) reflecting how trustworthy a specific attribute value is, based on source quality, extraction certainty, and validation results.

**Why:** Not all values are equally trustworthy. A value directly extracted from a manufacturer's official datasheet has higher confidence than one inferred from a similar product's specs. Confidence enables smart routing: high-confidence values can be auto-approved; low-confidence values need human review.

**Example:** 
- Bore diameter from manufacturer PDF: confidence 0.95 → auto-approve
- Material inferred from similar product: confidence 0.45 → route to review
- Description generated by AI: confidence 0.70 → flag for review

**Implication:** Confidence scoring must be honest. A system that reports 0.95 confidence for inferred values is misleading. Confidence must reflect the actual evidence chain.

### 6.4 What is "Commerce-Readiness"?

**What:** The degree to which a product record meets the requirements for use in a real buying/selling workflow.

**Why:** A product record can be internally consistent but still unsuitable for a specific channel. Commerce-readiness is per-channel and per-category.

**Example:** A bearing record may be 90% complete for the internal catalog but 60% complete for Amazon Business (which requires GTIN, specific image dimensions, and bullet points). The same record may be 95% complete for a B2B distributor portal that only requires technical specs.

**Implication:** The system must know the target channel's requirements and measure completeness against them.

### 6.5 What is "Attribute Schema"?

**What:** The definition of which attributes are required, optional, and what values they can take for a given product category.

**Why:** Without a schema, completeness cannot be measured. You cannot know whether a field is "missing" unless you know it should be there.

**Example:** For the "Mounted Bearing" category, the schema might require: bore diameter, housing style, housing material, locking method, seal type, dynamic load rating, static load rating, max speed. For the "Pipe Fitting" category, it might require: nominal size, material, pressure rating, connection type, end type.

**Implication:** Schema definition is a prerequisite for quality measurement. The system must either use an existing taxonomy's schema or define its own.

---

## 7. Domain Invariants

These are rules that must always hold in the domain:

1. **Every product has a unique identity.** No two different physical products share the same canonical record.

2. **Every attribute has a source.** No value exists without provenance (or is explicitly marked as "inferred" with no source).

3. **Confidence reflects evidence.** A confidence score must be grounded in source quality, extraction method, and validation results — not arbitrary.

4. **Unknown is better than wrong.** A blank field with "no source found" is preferable to a fabricated value.

5. **Classification determines schema.** The set of required attributes depends on the product's category.

6. **Validation runs before publication.** No product data reaches a channel without passing validation.

7. **Changes are traceable.** Every modification to a product record has an audit trail.

8. **Conflicts are surfaced.** When sources disagree, the conflict is visible — not silently resolved.

---

*This domain model will be refined in subsequent modules as the architecture and data model are developed.*
