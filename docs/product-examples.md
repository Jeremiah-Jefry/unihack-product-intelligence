# Product Examples

> **Status:** Complete  
> **Module:** 2 — Canonical Product Intelligence Model & Data Contract  
> **Purpose:** Realistic examples demonstrating that the model actually works across different industrial categories.  
> **Depends on:** `canonical-product-model.md`, `attribute-taxonomy.md`, `provenance-and-evidence-model.md`

---

## 1. Overview

This document provides three realistic product examples from different industrial categories. Each example demonstrates:
- Core product identity
- Category-specific attributes
- Measurements with units
- Provenance and evidence
- Validation status
- At least one missing field
- At least one normalized field
- At least one enriched or derived field
- At least one potential conflict

---

## 2. Example 1: Industrial Pillow Block Bearing

### 2.1 Product Identity

```json
{
  "id": "prod-001",
  "mpn": "UCF209-28",
  "brand": "IPTCI Bearings",
  "name": "UCF209 Pillow Block Bearing",
  "model": "UCF200 Series",
  "lifecycle_status": "active",
  "primary_category": "Mounted Bearings > Pillow Block",
  "category_confidence": 0.95,
  "manufacturer_name": "IPTCI Bearings",
  "manufacturer_id": "mfg-iptci"
}
```

### 2.2 Classification

```json
{
  "taxonomy_codes": {
    "ETIM": "EC000123",
    "UNSPSC": "31171501",
    "eCl@ss": "23-11-01-01"
  }
}
```

### 2.3 Core Attributes

#### Bore Diameter (Source Fact, Normalized)

```json
{
  "id": "attr-001",
  "product_id": "prod-001",
  "name": "bore_diameter",
  "domain": "specification",
  "value_type": "measurement",
  "value": { "value": 30.163, "unit": "mm" },
  "original_value": { "value": "1-3/16", "unit": "in" },
  "normalized_value": { "value": 30.163, "unit": "mm" },
  "normalized_unit": "mm",
  "information_category": "specification",
  "confidence": 0.95,
  "validation_status": "auto_validated",
  "lifecycle_state": "approved",
  "requires_review": false,
  "extracted_at": "2026-08-10T14:30:00Z",
  "last_validated_at": "2026-08-10T14:31:00Z",
  "candidates": [
    {
      "id": "cand-001",
      "value": { "value": 30.163, "unit": "mm" },
      "unit": "mm",
      "source_id": "src-001",
      "source_location": {
        "page": 2,
        "section": "Technical Data",
        "table_id": "table-3",
        "row": 1,
        "column": "Bore",
        "text_span": "Bore: 1-3/16 in (30.163 mm)"
      },
      "extraction_method": "text_extraction",
      "extraction_confidence": 0.95,
      "source_trust_score": 0.95,
      "freshness": {
        "source_published_at": "2024-03-15T00:00:00Z",
        "freshness_status": "current",
        "freshness_reason": "Datasheet published 2024, within 2-year threshold"
      },
      "extracted_at": "2026-08-10T14:30:00Z",
      "transformations": [
        {
          "type": "unit_conversion",
          "description": "Converted from inches to millimeters",
          "input_value": { "value": "1-3/16", "unit": "in" },
          "output_value": { "value": 30.163, "unit": "mm" },
          "applied_at": "2026-08-10T14:30:30Z",
          "applied_by": "unit-conversion-engine"
        }
      ]
    }
  ],
  "conflict_status": "none"
}
```

#### Dynamic Load Rating (Source Fact)

```json
{
  "id": "attr-002",
  "product_id": "prod-001",
  "name": "dynamic_load_rating",
  "domain": "performance",
  "value_type": "measurement",
  "value": { "value": 15.9, "unit": "kN" },
  "unit": "kN",
  "information_category": "specification",
  "confidence": 0.92,
  "validation_status": "auto_validated",
  "lifecycle_state": "approved",
  "requires_review": false,
  "extracted_at": "2026-08-10T14:30:00Z",
  "candidates": [
    {
      "id": "cand-002",
      "value": { "value": 15.9, "unit": "kN" },
      "source_id": "src-001",
      "source_location": {
        "page": 2,
        "section": "Technical Data",
        "table_id": "table-3",
        "row": 1,
        "column": "Dynamic Load",
        "text_span": "Dynamic Load: 15.9 kN"
      },
      "extraction_method": "table_parsing",
      "extraction_confidence": 0.92,
      "source_trust_score": 0.95,
      "freshness": { "freshness_status": "current" },
      "extracted_at": "2026-08-10T14:30:00Z"
    }
  ],
  "conflict_status": "none"
}
```

#### Housing Material (Enriched Value)

```json
{
  "id": "attr-003",
  "product_id": "prod-001",
  "name": "material",
  "domain": "physical",
  "value_type": "string",
  "value": "Cast iron housing",
  "information_category": "physical",
  "confidence": 0.88,
  "validation_status": "auto_validated",
  "lifecycle_state": "approved",
  "requires_review": false,
  "extracted_at": "2026-08-10T15:00:00Z",
  "candidates": [
    {
      "id": "cand-003",
      "value": "Cast iron housing",
      "source_id": "src-002",
      "source_location": {
        "url_fragment": "#specifications",
        "text_span": "Housing Material: Cast iron"
      },
      "extraction_method": "web_scraping",
      "extraction_confidence": 0.90,
      "source_trust_score": 0.95,
      "freshness": { "freshness_status": "current" },
      "extracted_at": "2026-08-10T15:00:00Z"
    }
  ],
  "conflict_status": "none"
}
```

#### Bolt Pattern (Derived Value)

```json
{
  "id": "attr-004",
  "product_id": "prod-001",
  "name": "bolt_pattern",
  "domain": "physical",
  "value_type": "compound",
  "value": { "pattern": "2-bolt", "spacing_mm": 105 },
  "information_category": "specification",
  "confidence": 0.85,
  "validation_status": "auto_validated",
  "lifecycle_state": "approved",
  "requires_review": false,
  "extracted_at": "2026-08-10T15:10:00Z",
  "candidates": [
    {
      "id": "cand-004",
      "value": { "pattern": "2-bolt", "spacing_mm": 105 },
      "source_id": "src-001",
      "source_location": {
        "page": 3,
        "section": "Dimensions"
      },
      "extraction_method": "inference",
      "extraction_confidence": 0.85,
      "source_trust_score": 0.95,
      "freshness": { "freshness_status": "current" },
      "extracted_at": "2026-08-10T15:10:00Z"
    }
  ],
  "conflict_status": "none"
}
```

### 2.4 Missing Field

```json
{
  "id": "attr-005",
  "product_id": "prod-001",
  "name": "gtin",
  "domain": "identity",
  "value_type": "string",
  "value": null,
  "missing_status": "NOT_DISCOVERED",
  "information_category": "identity",
  "confidence": 0,
  "validation_status": "pending",
  "lifecycle_state": "discovered",
  "requires_review": true,
  "review_reason": "GTIN not found in any source; required for Amazon marketplace",
  "candidates": [],
  "conflict_status": "none"
}
```

### 2.5 Potential Conflict (Illustrative)

```json
{
  "id": "attr-006",
  "product_id": "prod-001",
  "name": "weight",
  "domain": "physical",
  "value_type": "measurement",
  "value": null,
  "information_category": "physical",
  "confidence": 0,
  "validation_status": "pending",
  "lifecycle_state": "extracted",
  "requires_review": true,
  "review_reason": "Conflicting sources: Source A says 1.2 kg, Source B says 1.35 kg",
  "candidates": [
    {
      "id": "cand-006a",
      "value": { "value": 1.2, "unit": "kg" },
      "source_id": "src-001",
      "source_location": { "page": 2, "text_span": "Weight: 1.2 kg" },
      "extraction_method": "text_extraction",
      "extraction_confidence": 0.90,
      "source_trust_score": 0.95,
      "freshness": { "freshness_status": "current" },
      "extracted_at": "2026-08-10T14:30:00Z"
    },
    {
      "id": "cand-006b",
      "value": { "value": 1.35, "unit": "kg" },
      "source_id": "src-003",
      "source_location": { "page": 1, "text_span": "Weight: 1.35 kg" },
      "extraction_method": "web_scraping",
      "extraction_confidence": 0.85,
      "source_trust_score": 0.80,
      "freshness": { "freshness_status": "current" },
      "extracted_at": "2026-08-10T15:20:00Z"
    }
  ],
  "conflict_status": "pending_resolution",
  "conflict": {
    "id": "conflict-001",
    "attribute_id": "attr-006",
    "candidate_ids": ["cand-006a", "cand-006b"],
    "conflict_type": "value_mismatch",
    "detected_at": "2026-08-10T15:20:00Z",
    "status": "open"
  }
}
```

---

## 3. Example 2: Hydraulic Gate Valve

### 3.1 Product Identity

```json
{
  "id": "prod-002",
  "mpn": "GV-2IN-SS316",
  "brand": "FlowTech Industries",
  "name": "2-Inch Stainless Steel Gate Valve",
  "model": "GV Series",
  "lifecycle_status": "active",
  "primary_category": "Valves > Gate Valve",
  "category_confidence": 0.92,
  "manufacturer_name": "FlowTech Industries",
  "manufacturer_id": "mfg-flowtech"
}
```

### 3.2 Classification

```json
{
  "taxonomy_codes": {
    "UNSPSC": "40161603",
    "eCl@ss": "23-11-03-01"
  }
}
```

### 3.3 Core Attributes

#### Port Size (Source Fact, Normalized)

```json
{
  "id": "attr-010",
  "product_id": "prod-002",
  "name": "port_size",
  "domain": "mechanical",
  "value_type": "measurement",
  "value": { "value": 50.8, "unit": "mm" },
  "original_value": { "value": "2", "unit": "in" },
  "normalized_value": { "value": 50.8, "unit": "mm" },
  "normalized_unit": "mm",
  "information_category": "specification",
  "confidence": 0.95,
  "validation_status": "auto_validated",
  "lifecycle_state": "approved",
  "requires_review": false,
  "extracted_at": "2026-08-10T16:00:00Z",
  "candidates": [
    {
      "id": "cand-010",
      "value": { "value": 50.8, "unit": "mm" },
      "source_id": "src-010",
      "source_location": {
        "page": 1,
        "section": "Product Specifications",
        "text_span": "Port Size: 2\" (50.8 mm)"
      },
      "extraction_method": "text_extraction",
      "extraction_confidence": 0.95,
      "source_trust_score": 0.95,
      "freshness": { "freshness_status": "current" },
      "extracted_at": "2026-08-10T16:00:00Z",
      "transformations": [
        {
          "type": "unit_conversion",
          "description": "Converted from inches to millimeters",
          "input_value": { "value": "2", "unit": "in" },
          "output_value": { "value": 50.8, "unit": "mm" },
          "applied_at": "2026-08-10T16:00:30Z",
          "applied_by": "unit-conversion-engine"
        }
      ]
    }
  ],
  "conflict_status": "none"
}
```

#### Pressure Rating (Source Fact)

```json
{
  "id": "attr-011",
  "product_id": "prod-002",
  "name": "pressure_rating",
  "domain": "mechanical",
  "value_type": "measurement",
  "value": { "value": 2068.4, "unit": "kPa" },
  "original_value": { "value": "300", "unit": "psi" },
  "information_category": "specification",
  "confidence": 0.93,
  "validation_status": "auto_validated",
  "lifecycle_state": "approved",
  "requires_review": false,
  "extracted_at": "2026-08-10T16:00:00Z",
  "candidates": [
    {
      "id": "cand-011",
      "value": { "value": 2068.4, "unit": "kPa" },
      "source_id": "src-010",
      "source_location": {
        "page": 1,
        "text_span": "Working Pressure: 300 psi (2068 kPa)"
      },
      "extraction_method": "text_extraction",
      "extraction_confidence": 0.93,
      "source_trust_score": 0.95,
      "freshness": { "freshness_status": "current" },
      "extracted_at": "2026-08-10T16:00:00Z"
    }
  ],
  "conflict_status": "none"
}
```

#### Body Material (Source Fact)

```json
{
  "id": "attr-012",
  "product_id": "prod-002",
  "name": "body_material",
  "domain": "physical",
  "value_type": "string",
  "value": "Stainless Steel 316",
  "information_category": "physical",
  "confidence": 0.94,
  "validation_status": "auto_validated",
  "lifecycle_state": "approved",
  "requires_review": false,
  "extracted_at": "2026-08-10T16:00:00Z",
  "candidates": [
    {
      "id": "cand-012",
      "value": "Stainless Steel 316",
      "source_id": "src-010",
      "source_location": {
        "page": 1,
        "text_span": "Body Material: SS316"
      },
      "extraction_method": "text_extraction",
      "extraction_confidence": 0.94,
      "source_trust_score": 0.95,
      "freshness": { "freshness_status": "current" },
      "extracted_at": "2026-08-10T16:00:00Z",
      "transformations": [
        {
          "type": "terminology_mapping",
          "description": "Mapped 'SS316' to 'Stainless Steel 316'",
          "input_value": "SS316",
          "output_value": "Stainless Steel 316",
          "applied_at": "2026-08-10T16:00:30Z",
          "applied_by": "terminology-mapper"
        }
      ]
    }
  ],
  "conflict_status": "none"
}
```

#### Certifications (Enriched Value)

```json
{
  "id": "attr-013",
  "product_id": "prod-002",
  "name": "certifications",
  "domain": "certification",
  "value_type": "list",
  "value": ["CE", "API 600"],
  "information_category": "certification",
  "confidence": 0.82,
  "validation_status": "pending",
  "lifecycle_state": "enriched",
  "requires_review": true,
  "review_reason": "Certifications enriched from third-party database; require verification",
  "extracted_at": "2026-08-10T16:30:00Z",
  "candidates": [
    {
      "id": "cand-013",
      "value": ["CE", "API 600"],
      "source_id": "src-011",
      "source_location": {
        "text_span": "Certifications: CE, API 600"
      },
      "extraction_method": "api_lookup",
      "extraction_confidence": 0.85,
      "source_trust_score": 0.80,
      "freshness": { "freshness_status": "current" },
      "extracted_at": "2026-08-10T16:30:00Z"
    }
  ],
  "conflict_status": "none"
}
```

### 3.4 Missing Field

```json
{
  "id": "attr-014",
  "product_id": "prod-002",
  "name": "flow_coefficient",
  "domain": "mechanical",
  "value_type": "number",
  "value": null,
  "missing_status": "NOT_DISCOVERED",
  "information_category": "specification",
  "confidence": 0,
  "validation_status": "pending",
  "lifecycle_state": "discovered",
  "requires_review": false,
  "candidates": [],
  "conflict_status": "none"
}
```

---

## 4. Example 3: Industrial Pressure Sensor

### 4.1 Product Identity

```json
{
  "id": "prod-003",
  "mpn": "PX309-100G5V",
  "brand": "Omega Engineering",
  "name": "100 psi Voltage Output Pressure Transducer",
  "model": "PX309 Series",
  "lifecycle_status": "active",
  "primary_category": "Sensors > Pressure Sensor",
  "category_confidence": 0.90,
  "manufacturer_name": "Omega Engineering",
  "manufacturer_id": "mfg-omega"
}
```

### 4.2 Classification

```json
{
  "taxonomy_codes": {
    "ETIM": "EC002056",
    "UNSPSC": "41111905",
    "eCl@ss": "27-20-15-01"
  }
}
```

### 4.3 Core Attributes

#### Measurement Range (Source Fact)

```json
{
  "id": "attr-020",
  "product_id": "prod-003",
  "name": "measurement_range",
  "domain": "specification",
  "value_type": "range",
  "value": { "min": 0, "max": 100, "unit": "psi" },
  "information_category": "specification",
  "confidence": 0.96,
  "validation_status": "auto_validated",
  "lifecycle_state": "approved",
  "requires_review": false,
  "extracted_at": "2026-08-10T17:00:00Z",
  "candidates": [
    {
      "id": "cand-020",
      "value": { "min": 0, "max": 100, "unit": "psi" },
      "source_id": "src-020",
      "source_location": {
        "page": 1,
        "table_id": "spec-table",
        "row": 1,
        "column": "Range",
        "text_span": "Range: 0 to 100 psi"
      },
      "extraction_method": "table_parsing",
      "extraction_confidence": 0.96,
      "source_trust_score": 0.98,
      "freshness": { "freshness_status": "current" },
      "extracted_at": "2026-08-10T17:00:00Z"
    }
  ],
  "conflict_status": "none"
}
```

#### Output Signal (Source Fact)

```json
{
  "id": "attr-021",
  "product_id": "prod-003",
  "name": "output_signal",
  "domain": "electrical",
  "value_type": "enum",
  "value": "0-10V",
  "information_category": "specification",
  "confidence": 0.94,
  "validation_status": "auto_validated",
  "lifecycle_state": "approved",
  "requires_review": false,
  "extracted_at": "2026-08-10T17:00:00Z",
  "candidates": [
    {
      "id": "cand-021",
      "value": "0-10V",
      "source_id": "src-020",
      "source_location": {
        "page": 1,
        "text_span": "Output: 0-10 VDC"
      },
      "extraction_method": "text_extraction",
      "extraction_confidence": 0.94,
      "source_trust_score": 0.98,
      "freshness": { "freshness_status": "current" },
      "extracted_at": "2026-08-10T17:00:00Z"
    }
  ],
  "conflict_status": "none"
}
```

#### Accuracy (Source Fact)

```json
{
  "id": "attr-022",
  "product_id": "prod-003",
  "name": "accuracy",
  "domain": "specification",
  "value_type": "percentage",
  "value": { "value": 0.25, "unit": "%" },
  "information_category": "specification",
  "confidence": 0.93,
  "validation_status": "auto_validated",
  "lifecycle_state": "approved",
  "requires_review": false,
  "extracted_at": "2026-08-10T17:00:00Z",
  "candidates": [
    {
      "id": "cand-022",
      "value": { "value": 0.25, "unit": "%" },
      "source_id": "src-020",
      "source_location": {
        "page": 1,
        "text_span": "Accuracy: ±0.25% FSO"
      },
      "extraction_method": "text_extraction",
      "extraction_confidence": 0.93,
      "source_trust_score": 0.98,
      "freshness": { "freshness_status": "current" },
      "extracted_at": "2026-08-10T17:00:00Z"
    }
  ],
  "conflict_status": "none"
}
```

#### Operating Temperature (Source Fact with Potential Conflict)

```json
{
  "id": "attr-023",
  "product_id": "prod-003",
  "name": "operating_temperature",
  "domain": "environmental",
  "value_type": "range",
  "value": null,
  "information_category": "specification",
  "confidence": 0,
  "validation_status": "pending",
  "lifecycle_state": "extracted",
  "requires_review": true,
  "review_reason": "Conflicting sources: datasheet says -40°C to 85°C, website says -20°C to 85°C",
  "candidates": [
    {
      "id": "cand-023a",
      "value": { "min": -40, "max": 85, "unit": "°C" },
      "source_id": "src-020",
      "source_location": {
        "page": 2,
        "text_span": "Operating Temperature: -40°F to 185°F (-40°C to 85°C)"
      },
      "extraction_method": "text_extraction",
      "extraction_confidence": 0.92,
      "source_trust_score": 0.98,
      "freshness": { "freshness_status": "current" },
      "extracted_at": "2026-08-10T17:00:00Z"
    },
    {
      "id": "cand-023b",
      "value": { "min": -20, "max": 85, "unit": "°C" },
      "source_id": "src-021",
      "source_location": {
        "url_fragment": "#specs",
        "text_span": "Operating Temp: -20°C to 85°C"
      },
      "extraction_method": "web_scraping",
      "extraction_confidence": 0.88,
      "source_trust_score": 0.90,
      "freshness": { "freshness_status": "current" },
      "extracted_at": "2026-08-10T17:10:00Z"
    }
  ],
  "conflict_status": "pending_resolution",
  "conflict": {
    "id": "conflict-003",
    "attribute_id": "attr-023",
    "candidate_ids": ["cand-023a", "cand-023b"],
    "conflict_type": "value_mismatch",
    "detected_at": "2026-08-10T17:10:00Z",
    "status": "open"
  }
}
```

### 4.4 Missing Field (Not Applicable)

```json
{
  "id": "attr-024",
  "product_id": "prod-003",
  "name": "flow_rate",
  "domain": "mechanical",
  "value_type": "measurement",
  "value": null,
  "missing_status": "NOT_APPLICABLE",
  "information_category": "specification",
  "confidence": 0,
  "validation_status": "pending",
  "lifecycle_state": "discovered",
  "requires_review": false,
  "notes": "Flow rate does not apply to pressure sensors",
  "candidates": [],
  "conflict_status": "none"
}
```

---

## 5. Summary of Demonstrated Concepts

| Concept | Bearing Example | Valve Example | Sensor Example |
|---------|----------------|---------------|----------------|
| Source fact | Bore diameter, load rating | Port size, pressure rating | Range, output signal |
| Normalized value | 1-3/16 in → 30.163 mm | 2 in → 50.8 mm | — |
| Enriched value | Housing material (from web) | Certifications (from API) | — |
| Derived value | Bolt pattern (from bore + housing) | — | — |
| Missing field | GTIN (not discovered) | Flow coefficient (not discovered) | Flow rate (not applicable) |
| Conflict | Weight (1.2 kg vs 1.35 kg) | — | Operating temperature (-40°C vs -20°C) |
| Information category | specification, physical | specification, certification | specification, environmental |
| Confidence range | 0.85 - 0.95 | 0.82 - 0.94 | 0.88 - 0.96 |
| Freshness | current | current | current |

---

*These examples demonstrate that the canonical product model can handle real-world industrial products with full provenance, conflict representation, and missing data handling.*
