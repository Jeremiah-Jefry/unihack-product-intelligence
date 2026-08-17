# Evaluation Framework

> **Status:** Complete  
> **Module:** 1 — Problem & Domain Understanding  
> **Purpose:** Define how we will measure success — what to measure, how to measure it, and what good looks like.  
> **Depends on:** `module-01-problem-definition.md`, `requirements.md`, `risks-and-failure-modes.md`

---

## 1. Evaluation Philosophy

**What it means:** We define measurable dimensions of success before building the system.

**Why it matters:** Without defined metrics, we cannot claim the system works. "It seems to produce good results" is not evaluation. We need numbers, measurement procedures, and targets.

**Example:** Instead of saying "extraction is accurate," we say "extraction accuracy is measured by comparing extracted attribute values against ground truth, across a stratified sample of 200 products, targeting ≥ 95% accuracy on critical attributes."

**Implication for our product:** Every module must contribute to measurable quality improvements. We will establish baselines early and track improvement.

---

## 2. Evaluation Dimensions

### 2.1 Extraction Accuracy

**What it measures:** How correctly does the system extract attribute values from source documents?

**How to measure:**
1. Select a stratified sample of products across categories
2. Establish ground truth from manufacturer-official sources
3. Compare system-extracted values against ground truth
4. Calculate per-attribute accuracy and overall accuracy

**Metrics:**
- **Attribute-level accuracy:** % of extracted values that match ground truth
- **Critical attribute accuracy:** % accuracy on attributes that drive purchasing decisions (bore diameter, load rating, voltage, etc.)
- **Type accuracy:** % of values with correct data type (number is a number, date is a date)
- **Unit accuracy:** % of values with correct unit assignment

**Target (to be refined with empirical data):**
- Overall attribute accuracy: ≥ 90%
- Critical attribute accuracy: ≥ 95%
- Type accuracy: ≥ 98%

**Measurement frequency:** Per evaluation cycle (initial build + after each significant change)

### 2.2 Completeness

**What it measures:** How many required attributes are populated for each product?

**How to measure:**
1. For each product, compare populated attributes against the attribute schema for its category
2. Apply weights: critical attributes weighted more than optional ones
3. Calculate weighted completeness score per product and per category

**Metrics:**
- **Raw completeness:** % of all attributes populated
- **Weighted completeness:** % of required/weighted attributes populated
- **Critical attribute completeness:** % of critical (filter-driving) attributes populated
- **Schema coverage:** % of category schemas that are fully satisfied

**Target:**
- Weighted completeness: ≥ 85% (starting target; to be refined)
- Critical attribute completeness: ≥ 90%

**Measurement frequency:** Per evaluation cycle

### 2.3 Consistency

**What it measures:** Are attribute values consistent across the record and across sources?

**How to measure:**
1. Check that the same concept uses the same terminology across products (e.g., "stainless steel" vs "SS304" vs "Inox")
2. Check that related fields agree (e.g., dimensions and weight are consistent)
3. Check that values are consistent across sources for the same product

**Metrics:**
- **Terminology consistency:** % of controlled vocabulary terms used consistently
- **Cross-field consistency:** % of records with no cross-field contradictions
- **Cross-source consistency:** % of multi-source products where sources agree on critical attributes

**Target:**
- Terminology consistency: ≥ 85%
- Cross-field consistency: ≥ 95%

**Measurement frequency:** Per evaluation cycle

### 2.4 Validation Accuracy

**What it measures:** How well does the validation layer detect actual errors?

**How to measure:**
1. Introduce known errors into a test dataset
2. Run validation rules
3. Measure detection rate (true positive) and false alarm rate (false positive)

**Metrics:**
- **Error detection rate:** % of introduced errors that validation catches
- **False positive rate:** % of validation alerts that flag correct data as errors
- **Blocking error accuracy:** % of truly blocking errors correctly identified as blocking

**Target:**
- Error detection rate: ≥ 90%
- False positive rate: ≤ 10%

**Measurement frequency:** Per evaluation cycle

### 2.5 Contradiction Detection

**What it measures:** How well does the system detect when sources disagree?

**How to measure:**
1. Create a test dataset with known contradictions between sources
2. Run the system's cross-source comparison
3. Measure detection rate and resolution accuracy

**Metrics:**
- **Contradiction detection rate:** % of known contradictions that are detected
- **False contradiction rate:** % of flagged contradictions that are actually agreements (different representations of the same value)
- **Resolution accuracy:** % of contradictions correctly resolved (when resolution is attempted)

**Target:**
- Contradiction detection rate: ≥ 85%
- False contradiction rate: ≤ 15%

**Measurement frequency:** Per evaluation cycle

### 2.6 Evidence Coverage

**What it measures:** What percentage of attribute values have traceable provenance?

**How to measure:**
1. For each product record, check every attribute value for provenance data
2. Categorize provenance quality (source document exists, page/section identified, passage preserved)

**Metrics:**
- **Provenance coverage:** % of attribute values with at least one source reference
- **Provenance depth:** % of values with full provenance (source + page + passage + confidence)
- **Source diversity:** % of products with data from multiple sources

**Target:**
- Provenance coverage: ≥ 95% (of non-inferred values)
- Provenance depth: ≥ 80%

**Measurement frequency:** Per evaluation cycle

### 2.7 Unsupported Claim Rate

**What it measures:** What percentage of attribute values lack supporting evidence?

**How to measure:**
1. For each attribute value, check if provenance data exists
2. For inferred values, check if the inference basis is documented
3. Calculate the rate of "unsupported" values (no source, no inference basis)

**Metrics:**
- **Unsupported claim rate:** % of values with no provenance and no inference tag
- **Unsupported critical attribute rate:** % of critical attributes with no evidence

**Target:**
- Unsupported claim rate: ≤ 5%
- Unsupported critical attribute rate: ≤ 1%

**Measurement frequency:** Per evaluation cycle

### 2.8 Hallucination Rate

**What it measures:** What percentage of generated or enriched values are fabricated (not supported by any source)?

**How to measure:**
1. Sample enriched/inferred values
2. Trace each back to its source
3. Verify that the source actually contains the claimed information
4. Calculate the rate of values where the source does not support the claim

**Metrics:**
- **Hallucination rate:** % of enriched/inferred values that are fabricated
- **Critical hallucination rate:** % of critical attribute hallucinations (most dangerous)

**Target:**
- Hallucination rate: ≤ 3%
- Critical hallucination rate: ≤ 1%

**Measurement frequency:** Per evaluation cycle (requires human verification)

### 2.9 Human Review Rate

**What it measures:** What percentage of values require human review?

**Why it matters:** High review rate = low automation. Low review rate = potential quality issues slipping through.

**How to measure:**
1. Track the number of values flagged for human review vs. total values
2. Track the review outcome (approved, rejected, corrected)

**Metrics:**
- **Review rate:** % of values routed to human review
- **Review accuracy:** % of reviewed values where human agrees with system confidence
- **Review efficiency:** Average time per review action
- **Auto-approval rate:** % of values auto-approved without review

**Target:**
- Review rate: ≤ 20% (optimizing for efficient routing)
- Review accuracy (human agrees with confidence): ≥ 85%

**Measurement frequency:** Per evaluation cycle

### 2.10 Processing Time

**What it measures:** How long does it take to process products?

**How to measure:**
1. Measure end-to-end time from input to output for different input types
2. Measure per-stage timing (ingestion, extraction, enrichment, validation)

**Metrics:**
- **Per-product processing time:** Average time from input to usable output
- **Batch throughput:** Products processed per hour
- **Stage breakdown:** Time spent in each pipeline stage
- **Bottleneck identification:** Which stage takes the most time

**Target (initial, to be refined):**
- Per-product processing time: ≤ 5 minutes (for PDF input)
- Batch throughput: ≥ 100 products/hour

**Measurement frequency:** Per evaluation cycle

### 2.11 Cost Per Product

**What it measures:** What is the economic cost of processing one product?

**How to measure:**
1. Track API calls (LLM, OCR, etc.) per product
2. Track compute time per product
3. Track storage per product
4. Calculate total cost per product

**Metrics:**
- **API cost per product:** LLM + OCR + other API costs
- **Compute cost per product:** Processing time × compute rate
- **Total cost per product:** Sum of all costs
- **Cost breakdown by stage:** Which stage is most expensive

**Target (initial, to be refined):**
- Total cost per product: ≤ $0.50 (for standard PDF input)
- Cost should decrease with volume (economies of scale)

**Measurement frequency:** Per evaluation cycle

### 2.12 Scalability

**What it measures:** Does quality and performance hold as catalog size grows?

**How to measure:**
1. Process catalogs of increasing size (100, 1000, 10000 products)
2. Track quality metrics and processing time at each scale
3. Identify degradation points

**Metrics:**
- **Quality stability:** Do accuracy and completeness scores remain stable as catalog grows?
- **Time scaling:** Does processing time scale linearly, sub-linearly, or super-linearly?
- **Memory scaling:** Does memory usage grow proportionally?
- **Cost scaling:** Does cost per product decrease with volume?

**Target:**
- Quality degradation: ≤ 5% as catalog grows from 100 to 10,000 products
- Time scaling: Sub-linear (batch processing should be more efficient at scale)

**Measurement frequency:** Per major version or quarterly

---

## 3. Evaluation Methodology

### 3.1 Ground Truth Dataset

**What:** A curated set of products with verified, accurate attribute values used as the reference standard for evaluation.

**How to build:**
1. Select 50-100 products across 5-10 categories
2. For each product, obtain manufacturer-official specifications
3. Manually verify and structure the ground truth
4. Include varied input quality (complete PDFs, partial data, minimal input)

**Requirements:**
- Stratified across product categories
- Includes edge cases (multi-product PDFs, scanned documents, conflicting sources)
- Ground truth verified by domain expert
- Version-controlled and reproducible

### 3.2 Evaluation Procedure

1. **Baseline measurement:** Before any processing, measure the state of the input data
2. **System processing:** Run the system on the evaluation dataset
3. **Output comparison:** Compare system output against ground truth
4. **Metric calculation:** Calculate all defined metrics
5. **Error analysis:** Examine failures to understand root causes
6. **Report generation:** Produce evaluation report with metrics, analysis, and recommendations

### 3.3 Evaluation Cadence

| Event | Evaluation scope |
|-------|-----------------|
| Initial build | Full evaluation against ground truth dataset |
| After each module | Targeted evaluation of affected dimensions |
| Before submission | Full evaluation with final metrics |
| Post-submission | Continuous monitoring (if deployed) |

### 3.4 Statistical Rigor

- Report confidence intervals, not just point estimates
- Use stratified sampling to ensure category coverage
- Report per-category and per-attribute breakdowns
- Track improvement trends over time
- Never cherry-pick favorable results

---

## 4. Evaluation Anti-Patterns

### 4.1 What NOT to do

| Anti-pattern | Why it's bad | What to do instead |
|-------------|-------------|-------------------|
| "The LLM says it's correct" | LLMs are not reliable judges of their own output | Compare against ground truth with human verification |
| "It looks good on a few examples" | Small samples are unreliable | Use statistically significant sample sizes |
| "Accuracy is 99%!" (on easy cases only) | Cherry-picking easy cases inflates metrics | Stratify evaluation across difficulty levels |
| "We measured once and it was fine" | No reproducibility | Document evaluation procedure; run repeatedly |
| "No errors found" (because we didn't look) | Absence of evidence is not evidence of absence | Actively search for errors using targeted test cases |
| "The system is better than nothing" | Very low bar | Define meaningful quality thresholds |

### 4.2 Honest Reporting

- Report both successes and failures
- Explain what each metric measures and its limitations
- Acknowledge uncertainty in measurements
- Distinguish between "we measured this" and "we estimate this"
- Never fabricate benchmark results

---

## 5. Evaluation Dataset Design

### 5.1 Required Product Categories

The evaluation dataset should include products from at least:

1. **Mounted bearings** (pillow blocks, flange units) — dimensional specs, load ratings
2. **Pipe fittings** (elbows, tees, couplings) — nominal sizes, materials, pressure ratings
3. **Electrical components** (circuit breakers, contactors) — voltage, current, ETIM classification
4. **Fasteners** (bolts, nuts, washers) — thread pitch, material, grade
5. **Safety equipment** (gloves, goggles, helmets) — certifications, ratings, standards

### 5.2 Required Input Varieties

Each category should include products with:

1. Complete PDF datasheet (high quality input)
2. Multi-product catalog PDF (table-heavy input)
3. Minimal input (MPN + brand only)
4. Partial input (some specs + image)
5. Conflicting sources (two documents with different values)
6. Scanned/low-quality document
7. Supplier CSV feed with inconsistent formatting

### 5.3 Ground Truth Structure

For each product in the evaluation dataset:

```
{
  "product_id": "eval-001",
  "mpn": "UCF209-28",
  "brand": "IPTCI Bearings",
  "category": "Mounted Bearings > Pillow Block",
  "ground_truth_attributes": {
    "bore_diameter": { "value": "1-3/16 in", "value_mm": 30.163, "source": "manufacturer-datasheet-v3.pdf" },
    "housing_material": { "value": "Cast iron", "source": "manufacturer-datasheet-v3.pdf" },
    ...
  },
  "input_variety": "complete-pdf",
  "difficulty": "medium"
}
```

---

## 6. Success Criteria for Module 1

Before proceeding to Module 2, the following must be established:

1. **Evaluation dataset exists** — at least 20 products across 3 categories with verified ground truth
2. **Baseline metrics measured** — what is the quality of the input data before processing?
3. **Metric definitions finalized** — all metrics in this document are agreed upon
4. **Measurement procedure documented** — another engineer could reproduce the evaluation
5. **Initial targets set** — based on baseline metrics and domain research

---

*This evaluation framework will be executed in later modules when the system is built. The metrics and targets will be refined based on empirical results.*
