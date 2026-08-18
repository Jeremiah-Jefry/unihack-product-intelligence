# Attribute Taxonomy

> **Status:** Complete  
> **Module:** 2 — Canonical Product Intelligence Model & Data Contract  
> **Purpose:** Define the attribute system — categories, data types, value types, units, ranges, enumerations, and extensibility strategy.  
> **Depends on:** `canonical-product-model.md`

---

## 1. Overview

The attribute system is the core of the product intelligence model. It must support:
- Products with very different attribute sets (motors vs. valves vs. sensors)
- Typed values with units
- Normalization and conversion
- Category-specific requirements
- Extensibility without schema changes

---

## 2. Attribute Naming Convention

All attribute names follow these rules:
- lowercase
- snake_case
- descriptive and unambiguous
- domain-prefixed when needed (e.g., `electrical_voltage`, `mechanical_torque`)
- controlled vocabulary for standard attributes

---

## 3. Value Types

### 3.1 Simple Types

| Type | Description | Example | Notes |
|------|-------------|---------|-------|
| `string` | Free text | "Cast iron housing" | Use for descriptions, names, materials |
| `number` | Numeric value | 30.163 | Always stored as float internally |
| `boolean` | True/false | true | Use for yes/no attributes |
| `enum` | Controlled vocabulary | "IP65" | Must have defined allowed values |

### 3.2 Measurement Types

| Type | Description | Example | Structure |
|------|-------------|---------|-----------|
| `measurement` | Number + unit | 15.9 kN | `{ value: 15.9, unit: "kN" }` |
| `range` | Min-max range | -20°C to +80°C | `{ min: -20, max: 80, unit: "°C" }` |
| `dimension` | L × W × H | 152 × 42 × 48 mm | `{ length: 152, width: 42, height: 48, unit: "mm" }` |
| `percentage` | Percentage value | 85% | `{ value: 85, unit: "%" }` |

### 3.3 Temporal Types

| Type | Description | Example | Format |
|------|-------------|---------|--------|
| `date` | Date value | 2027-06-15 | ISO 8601 date |
| `duration` | Time period | 2-3 weeks | `{ min: 2, max: 3, unit: "weeks" }` |

### 3.4 Complex Types

| Type | Description | Example | Structure |
|------|-------------|---------|-----------|
| `compound` | Structured object | M10 × 1.5 bolt | `{ thread: "M10", pitch: "1.5", grade: "8.8" }` |
| `list` | Multiple values | ["CE", "UL", "RoHS"] | Array of values |

### 3.5 Value Structure Reference

The `value` field on `Attribute` and `CandidateValue` is polymorphic — its structure depends on `value_type`. The expected structure for each type:

| value_type | Expected `value` structure | Example |
|------------|---------------------------|---------|
| `string` | `string` | `"Cast iron housing"` |
| `number` | `number` | `30.163` |
| `boolean` | `boolean` | `true` |
| `enum` | `string` | `"IP65"` |
| `measurement` | `{ "value": number, "unit": string }` | `{ "value": 15.9, "unit": "kN" }` |
| `range` | `{ "min": number, "max": number, "unit": string }` | `{ "min": -20, "max": 80, "unit": "°C" }` |
| `dimension` | `{ "length": number, "width": number, "height": number, "unit": string }` | `{ "length": 152, "width": 42, "height": 48, "unit": "mm" }` |
| `percentage` | `{ "value": number, "unit": "%" }` | `{ "value": 85, "unit": "%" }` |
| `date` | `string` (ISO 8601) | `"2027-06-15"` |
| `duration` | `{ "min": number, "max": number, "unit": string }` | `{ "min": 2, "max": 3, "unit": "weeks" }` |
| `compound` | `object` (structure varies by attribute) | `{ "thread": "M10", "pitch": "1.5", "grade": "8.8" }` |
| `list` | `array` of values | `["CE", "UL", "RoHS"]` |

---

## 4. Unit System

### 4.1 Unit Representation

Every measurement value stores:
- `value`: the numeric value
- `unit`: the unit string (canonical form)
- `original_value`: the original value before normalization (when different)
- `original_unit`: the original unit before normalization (when different)

### 4.2 Canonical Units

The system uses SI as the canonical unit system. All measurements can be normalized to SI.

| Quantity | Canonical Unit | Common Alternatives |
|----------|---------------|---------------------|
| Length | m | mm, cm, in, ft |
| Mass | kg | g, lb, oz |
| Force | N | kN, lbf |
| Pressure | Pa | kPa, MPa, bar, psi |
| Temperature | °C | °F, K |
| Electrical current | A | mA |
| Electrical voltage | V | mV, kV |
| Electrical power | W | kW, MW, hp |
| Flow rate | m³/s | L/min, GPM |
| Torque | N·m | lbf·ft |

### 4.3 Normalization Rules

1. **Preserve original.** Always store the original value and unit alongside the normalized value.
2. **Record transformation.** Every normalization is recorded as a Transformation in provenance.
3. **Precision.** Maintain sufficient precision to avoid rounding errors. Use at least 4 significant figures for normalized values.
4. **Ambiguous units.** When a unit is ambiguous (e.g., "in" could be inches or input), flag for human review rather than guess.

---

## 5. Attribute Domains

Attributes are organized into domains that correspond to the categories defined in the Module 1 problem definition.

### 5.1 Identity Domain

| Attribute | Value Type | Required | Description |
|-----------|-----------|----------|-------------|
| `mpn` | string | Yes | Manufacturer Part Number |
| `brand` | string | Yes | Manufacturer or brand name |
| `name` | string | Conditional | Product name |
| `gtin` | string | Optional | Global Trade Item Number |
| `upc` | string | Optional | Universal Product Code |
| `ean` | string | Optional | European Article Number |
| `sku` | string | Optional | Internal SKU |
| `model` | string | Optional | Model or series |
| `lifecycle_status` | enum | Yes | active, discontinued, obsolete, unknown |

### 5.2 Classification Domain

| Attribute | Value Type | Required | Description |
|-----------|-----------|----------|-------------|
| `primary_category` | string | Yes | Internal category path |
| `category_confidence` | number | Yes | Confidence in category assignment |
| `etim_class` | string | Optional | ETIM class code |
| `unspsc_code` | string | Optional | UNSPSC code |
| `eclass_code` | string | Optional | eCl@ss code |
| `gs1_gpc_brick` | string | Optional | GS1 GPC brick code |

### 5.3 Specification Domain (Category-Specific)

This domain contains attributes that vary by product category. The following are examples across different categories.

#### Bearings

| Attribute | Value Type | Unit | Description |
|-----------|-----------|------|-------------|
| `bore_diameter` | measurement | mm | Bore diameter |
| `outside_diameter` | measurement | mm | Outside diameter |
| `width` | measurement | mm | Width |
| `dynamic_load_rating` | measurement | kN | Dynamic load rating |
| `static_load_rating` | measurement | kN | Static load rating |
| `max_speed` | measurement | rpm | Maximum speed |
| `housing_style` | enum | — | pillow_block, flange, etc. |
| `locking_method` | enum | — | set_screw, eccentric, adapter |
| `seal_type` | enum | — | rubber_seal, metal_shield, open |

#### Valves

| Attribute | Value Type | Unit | Description |
|-----------|-----------|------|-------------|
| `port_size` | measurement | in | Port size |
| `pressure_rating` | measurement | psi | Maximum working pressure |
| `flow_coefficient` | number | — | Cv value |
| `body_material` | string | — | Body material |
| `actuation_type` | enum | — | manual, pneumatic, electric, hydraulic |
| `end_connection` | enum | — | threaded, flanged, welded, socket_weld |
| `seat_material` | string | — | Seat material |

#### Electrical Components

| Attribute | Value Type | Unit | Description |
|-----------|-----------|------|-------------|
| `voltage_rating` | measurement | V | Maximum voltage |
| `current_rating` | measurement | A | Maximum current |
| `power_rating` | measurement | W | Power rating |
| `frequency` | measurement | Hz | Operating frequency |
| `phase` | enum | — | single, three |
| `ip_rating` | enum | — | IP65, IP67, etc. |
| `mounting_type` | enum | — | din_rail, panel, surface |

#### Sensors

| Attribute | Value Type | Unit | Description |
|-----------|-----------|------|-------------|
| `measurement_range_min` | measurement | varies | Minimum measurable value |
| `measurement_range_max` | measurement | varies | Maximum measurable value |
| `accuracy` | percentage | % | Measurement accuracy |
| `output_signal` | enum | — | 4-20ma, 0-10v, digital |
| `response_time` | measurement | ms | Response time |
| `operating_temperature` | range | °C | Operating temperature range |

### 5.4 Physical Domain

| Attribute | Value Type | Unit | Description |
|-----------|-----------|------|-------------|
| `length` | measurement | mm | Length |
| `width` | measurement | mm | Width |
| `height` | measurement | mm | Height |
| `weight` | measurement | kg | Weight |
| `material` | string | — | Primary material |
| `finish` | string | — | Surface finish |
| `color` | string | — | Color |

### 5.5 Performance Domain

| Attribute | Value Type | Unit | Description |
|-----------|-----------|------|-------------|
| `efficiency` | percentage | % | Efficiency rating |
| `power_output` | measurement | W | Power output |
| `speed_rating` | measurement | rpm | Speed rating |
| `load_capacity` | measurement | N | Load capacity |

### 5.6 Electrical Domain

| Attribute | Value Type | Unit | Description |
|-----------|-----------|------|-------------|
| `voltage` | measurement | V | Operating voltage |
| `current` | measurement | A | Operating current |
| `power_factor` | number | — | Power factor (0-1) |
| `insulation_class` | enum | — | Class B, F, H |
| `conductor_size` | measurement | mm² | Conductor cross-section |

### 5.7 Mechanical Domain

| Attribute | Value Type | Unit | Description |
|-----------|-----------|------|-------------|
| `torque` | measurement | N·m | Torque rating |
| `pressure` | measurement | Pa | Pressure rating |
| `flow_rate` | measurement | m³/s | Flow rate |
| `stroke_length` | measurement | mm | Stroke length |

### 5.8 Environmental Domain

| Attribute | Value Type | Unit | Description |
|-----------|-----------|------|-------------|
| `operating_temperature` | range | °C | Operating temperature range |
| `storage_temperature` | range | °C | Storage temperature range |
| `operating_humidity` | range | % | Operating humidity range |
| `ip_rating` | enum | — | Ingress protection rating |
| `corrosion_resistance` | string | — | Corrosion resistance class |
| `explosion_protection` | string | — | Explosion protection rating |

### 5.9 Certification Domain

| Attribute | Value Type | Required | Description |
|-----------|-----------|----------|-------------|
| `certifications` | list | Optional | List of certifications held |
| `ce_mark` | boolean | Optional | CE marking |
| `ul_listed` | boolean | Optional | UL listing |
| `rohs_compliant` | boolean | Optional | RoHS compliance |
| `reach_compliant` | boolean | Optional | REACH compliance |
| `certification_expiry` | date | Optional | Certification expiry date |
| `certification_body` | string | Optional | Certifying body |

### 5.10 Commercial Domain

| Attribute | Value Type | Required | Description |
|-----------|-----------|----------|-------------|
| `unit_of_measure` | enum | Yes | each, box, case, pallet |
| `minimum_order_quantity` | number | Optional | Minimum order quantity |
| `lead_time` | duration | Optional | Delivery lead time |
| `warranty_period` | duration | Optional | Warranty coverage period |
| `country_of_origin` | string | Optional | Country of manufacture |
| `hs_code` | string | Optional | Harmonized System code |

### 5.11 Compatibility Domain

| Attribute | Value Type | Description |
|-----------|-----------|-------------|
| `compatible_shaft_size` | measurement | Compatible shaft diameter |
| `replaces_part` | string | Part number this replaces |
| `cross_reference` | list<string> | Equivalent parts from other brands |
| `compatible_with` | list<string> | Compatible product identifiers |

### 5.12 Description Domain

| Attribute | Value Type | Description |
|-----------|-----------|-------------|
| `short_description` | string | Brief description (1-2 sentences) |
| `long_description` | string | Detailed description |
| `features` | list<string> | Key features |
| `applications` | list<string> | Typical applications |

### 5.13 Media Domain

| Attribute | Value Type | Description |
|-----------|-----------|-------------|
| `product_image_main` | string | Primary product image URL |
| `product_images` | list<string> | All product image URLs |
| `datasheet_url` | string | Datasheet URL |
| `cad_file_url` | string | CAD file URL |
| `installation_manual_url` | string | Installation manual URL |

---

## 6. Category-Specific Schema Strategy

### 6.1 How It Works

1. **Core attributes** (identity, classification, basic physical) apply to all products.
2. **Category-specific attributes** are defined by the attribute schema for the product's category.
3. **The schema is extensible** — new categories can define new attributes without changing the core model.
4. **Completeness is measured** against the schema — required attributes that are missing reduce the completeness score.

### 6.2 Schema Definition

A category schema is defined as:

```json
{
  "category_id": "mounted-bearing-pillow-block",
  "required_attributes": [
    { "name": "bore_diameter", "value_type": "measurement", "unit": "mm" },
    { "name": "housing_style", "value_type": "enum", "allowed_values": ["pillow_block", "flange", "take_up"] },
    { "name": "dynamic_load_rating", "value_type": "measurement", "unit": "kN" }
  ],
  "optional_attributes": [
    { "name": "seal_type", "value_type": "enum", "allowed_values": ["rubber_seal", "metal_shield", "open"] },
    { "name": "locking_method", "value_type": "enum", "allowed_values": ["set_screw", "eccentric", "adapter"] }
  ]
}
```

### 6.3 Schema Evolution

When a category schema changes:
1. Existing records are not broken — they keep their attributes.
2. New required attributes are flagged as missing on existing records.
3. Schema versioning tracks changes.
4. Affected records can be re-validated against the new schema.

---

## 7. Extensibility Rules

1. **New attributes can be added** to any domain without changing existing attributes.
2. **New domains can be created** for new product categories.
3. **New value types can be added** if needed, but existing types should be reused when possible.
4. **New enumerations** should be controlled vocabularies with defined allowed values.
5. **Custom attributes** (not in the standard taxonomy) are allowed but flagged as "custom" in their metadata.

---

*This attribute taxonomy is the foundation for category-specific schemas and completeness measurement. See `canonical-product-model.md` for the overall model structure.*
