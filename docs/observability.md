# Observability Specification

Module 3 — Architecture | UniHack Product Intelligence

## Purpose

Define what the system observes, how it measures, and when it alerts. Observability enables diagnosis of processing failures, extraction quality, validation behavior, conflict handling, human review bottlenecks, cost efficiency, and source freshness.

Without observability, the system is opaque. With it, every product's journey through the pipeline is traceable and every system behavior is explainable.

---

## 1. Processing Observability

Track the lifecycle of every product through each pipeline stage.

| Metric | Description | Granularity |
|---|---|---|
| `processing.success_rate` | % of products completing a stage without error | Per stage, per source type |
| `processing.failure_rate` | % of products failing at a stage | Per stage, per error class |
| `processing.throughput` | Products processed per time window | Per hour, per stage |
| `processing.latency` | Time from stage start to stage completion | Per product, per stage |
| `processing.queue_depth` | Number of products awaiting processing | Per stage |
| `processing.retry_rate` | % of products requiring retry | Per stage, per error class |
| `processing.timeout_rate` | % of products exceeding stage time budget | Per stage |

**Alerting thresholds:**
- `success_rate` < 95% for any 15-minute window → WARNING
- `success_rate` < 85% for any 15-minute window → CRITICAL
- `latency_p95` > 2x baseline for any stage → WARNING
- `throughput` drops > 50% from rolling 24h average → WARNING
- `timeout_rate` > 5% in any stage → WARNING

---

## 2. Extraction Observability

Monitor the LLM and rule-based extraction pipeline.

| Metric | Description | Granularity |
|---|---|---|
| `extraction.method_usage` | Count of products processed by each extraction method | Per method |
| `extraction.confidence_distribution` | Distribution of confidence scores across all extracted attributes | Per method, per attribute type |
| `extraction.confidence_mean` | Mean confidence score | Per method, per attribute type |
| `extraction.confidence_p10` | 10th percentile confidence score | Per method, per attribute type |
| `extraction.error_count` | Number of extraction failures | Per method, per error class |
| `extraction.error_rate` | Extraction failures as % of attempts | Per method |
| `extraction.error_type_breakdown` | Count by error class (timeout, malformed output, rate limit, content refusal) | Per method |
| `extraction.attributes_per_product` | Distribution of extracted attribute count per product | Per method |
| `extraction.extraction_time` | Time taken per extraction call | Per method, per product |

**Alerting thresholds:**
- `error_rate` > 10% for any method → WARNING
- `error_rate` > 25% for any method → CRITICAL
- `confidence_mean` drops > 15% from 7-day rolling average → WARNING
- `confidence_p10` < 0.4 for any attribute type → WARNING
- `extraction_time_p95` > 30s → WARNING

---

## 3. Validation Observability

Track each validation layer independently.

| Metric | Description | Granularity |
|---|---|---|
| `validation.layer_pass_rate` | % of attributes passing each validation layer | Per layer |
| `validation.layer_fail_rate` | % of attributes failing each validation layer | Per layer |
| `validation.most_common_failures` | Top failure reasons per validation layer | Per layer, per time window |
| `validation.critical_failures` | Count of attributes failing critical validations | Per layer |
| `validation.validation_time` | Time taken per validation check | Per layer |
| `validation.revalidation_rate` | % of products re-validated after correction | Per stage |
| `validation.schema_violation_count` | Count of schema violations | Per product |

**Validation layers:**
- Schema validation (structural correctness)
- Type validation (value types correct)
- Unit normalization (units parseable and consistent)
- Range validation (values within expected bounds)
- Cross-field consistency (related attributes agree)
- Source verification (claim matches source material)
- Contradiction detection (no conflicting claims within product)

**Alerting thresholds:**
- `layer_fail_rate` > 50% for any layer → WARNING
- `layer_fail_rate` > 80% for any layer → CRITICAL
- `critical_failures` > 20% of total attributes → CRITICAL
- `validation_time_p95` > 10s → WARNING

---

## 4. Conflict Observability

Monitor conflicts between sources, between extracted and normalized values, and between validation findings.

| Metric | Description | Granularity |
|---|---|---|
| `conflict.conflict_rate` | % of products with at least one unresolved conflict | Per product batch |
| `conflict.resolution_rate` | % of conflicts automatically resolved | Per conflict type |
| `conflict.escalation_rate` | % of conflicts escalated to human review | Per conflict type |
| `conflict.unresolved_rate` | % of conflicts remaining unresolved | Per conflict type |
| `conflict.common_types` | Top conflict categories by frequency | Per time window |
| `conflict.resolution_time` | Time from conflict detection to resolution | Per conflict type |
| `conflict.source_disagreement_rate` | % of multi-source products where sources disagree on same attribute | Per attribute type |

**Alerting thresholds:**
- `conflict_rate` > 30% for any batch → WARNING
- `escalation_rate` > 40% → WARNING
- `unresolved_rate` > 10% after 24 hours → CRITICAL

---

## 5. Human Review Observability

Track human review activity and its outcomes.

| Metric | Description | Granularity |
|---|---|---|
| `human.review_rate` | % of products routed to human review | Per stage, per reason |
| `human.approval_rate` | % of reviewed products approved as-is | Per reviewer, per reason |
| `human.correction_rate` | % of reviewed products requiring correction | Per reviewer, per reason |
| `human.rejection_rate` | % of reviewed products rejected | Per reviewer, per reason |
| human.review_time | Time from assignment to review completion | Per reviewer, per reason |
| `human.review_queue_depth` | Number of items awaiting review | Per stage |
| `human.common_correction_types` | Top attributes requiring human correction | Per time window |
| `human.ai_vs_human_agreement` | % of cases where AI confidence and human judgment agree | Per attribute type |
| `human.review_impact_on_quality` | Change in completeness/accuracy after human review | Per batch |

**Alerting thresholds:**
- `review_rate` > 50% → WARNING (may indicate extraction quality issue)
- `review_queue_depth` > 100 items → WARNING
- `correction_rate` > 60% of reviewed items → WARNING (may indicate AI overconfidence)
- `review_time_p95` > 24 hours → WARNING

---

## 6. Cost Observability

Track API costs and resource consumption per product.

| Metric | Description | Granularity |
|---|---|---|
| `cost.total_api_cost_usd` | Total API cost in USD | Per time window |
| `cost.cost_per_product` | Average API cost per product processed | Per time window |
| `cost.api_calls_per_product` | Average API calls per product | Per method, per time window |
| `cost.cost_by_stage` | API cost attributed to each pipeline stage | Per stage |
| `cost.cost_by_method` | API cost by extraction method | Per method |
| `cost.cost_by_attribute_type` | API cost per attribute type extracted | Per attribute type |
| `cost.token_usage` | Total tokens consumed | Per model, per time window |
| `cost.cost_trend` | Rolling cost per product over time | Per day |
| `cost.cost_budget_remaining` | Remaining budget for current period | Per budget period |

**Alerting thresholds:**
- `cost_per_product` > 2x 7-day rolling average → WARNING
- `total_api_cost_usd` > 80% of period budget → WARNING
- `total_api_cost_usd` > 95% of period budget → CRITICAL
- Token usage spike > 3x baseline in any hour → WARNING

---

## 7. Quality Observability

Track product quality dimensions over time.

| Metric | Description | Granularity |
|---|---|---|
| `quality.completeness_rate` | % of expected attributes present per product | Per product, per category |
| `quality.completeness_trend` | Rolling completeness rate over time | Per day, per category |
| `quality.accuracy_rate` | % of extracted attributes verified correct (via validation or human review) | Per attribute type |
| `quality.accuracy_trend` | Rolling accuracy rate over time | Per day |
| `quality.hallucination_rate` | % of extracted attributes that are unsupported by any source | Per method |
| `quality.hallucination_trend` | Rolling hallucination rate over time | Per day, per method |
| `quality.consistency_rate` | % of products with no internal contradictions | Per batch |
| `quality.provenance_coverage` | % of attributes with full provenance chain | Per product |
| `quality.quality_score` | Composite quality score per product | Per product |
| `quality.quality_distribution` | Distribution of quality scores across all products | Per batch |

**Alerting thresholds:**
- `completeness_rate` < 60% for any batch → WARNING
- `accuracy_rate` < 80% → WARNING
- `accuracy_rate` < 60% → CRITICAL
- `hallucination_rate` > 15% → WARNING
- `hallucination_rate` > 25% → CRITICAL
- `provenance_coverage` < 50% → WARNING

---

## 8. Freshness Observability

Monitor source data currency and re-verification needs.

| Metric | Description | Granularity |
|---|---|---|
| `freshness.source_age_distribution` | Distribution of source document age | Per source type |
| `freshness.staleness_rate` | % of products with sources older than defined threshold | Per source type |
| `freshness.reverification_rate` | % of products re-verified against updated sources | Per time window |
| `freshness.source_availability` | % of source URLs/paths still accessible | Per source type |
| `freshness.content_hash_change_rate` | % of source files with changed content on re-fetch | Per source type |
| `freshness.source_update_lag` | Time between source change and system detection | Per source type |

**Freshness thresholds (configurable):**
- Product source age > 12 months → STALE
- Safety/regulatory source age > 6 months → STALE
- Technical specification source age > 18 months → STALE

**Alerting thresholds:**
- `staleness_rate` > 30% → WARNING
- `staleness_rate` > 60% → CRITICAL
- `source_availability` < 80% → WARNING
- `source_availability` < 50% → CRITICAL

---

## 9. Dashboard Requirements

### 9.1 Operational Dashboard

Real-time view of system health.

- Pipeline stage status (green/yellow/red)
- Current throughput and latency
- Error rates per stage
- Queue depths
- Active alerts
- Cost burn rate vs. budget

### 9.2 Quality Dashboard

Quality trends over time.

- Completeness trend (7-day, 30-day)
- Accuracy trend (7-day, 30-day)
- Hallucination rate trend
- Confidence distribution histogram
- Validation failure heatmap by layer
- Quality score distribution

### 9.3 Cost Dashboard

Cost analysis and optimization.

- Cost per product trend
- Cost breakdown by stage (stacked bar)
- Cost breakdown by extraction method
- Cost vs. quality correlation
- Budget utilization gauge
- Cost anomaly timeline

### 9.4 Conflict & Human Review Dashboard

Decision support for escalation design.

- Conflict rate and type distribution
- Resolution rate trend
- Escalation queue status
- Human review throughput
- Correction rate and type analysis
- AI vs. human agreement rate

### 9.5 Product Trace View

Per-product observability.

- Full pipeline trace (stages, times, outcomes)
- Extraction details (method, confidence, raw output)
- Validation results per layer
- Conflicts and resolution status
- Human review history
- Source provenance chain
- Quality score breakdown
- Cost attribution

---

## 10. Implementation Approach

### 10.1 Event Logging

Every pipeline event emits a structured log entry:

```json
{
  "event_type": "extraction.completed",
  "timestamp": "2026-08-18T14:32:01Z",
  "product_id": "PROD-001",
  "stage": "extraction",
  "method": "llm_structured",
  "duration_ms": 4200,
  "attributes_extracted": 12,
  "confidence_mean": 0.83,
  "errors": [],
  "cost_usd": 0.0042,
  "tokens_consumed": 2100
}
```

### 10.2 Metrics Aggregation

Metrics are aggregated at configurable intervals (default: 5-minute windows). Aggregations produce:
- Counts (events, errors, successes)
- Rates (per second, per minute)
- Distributions (percentiles, histograms)
- Totals (cost, tokens)

### 10.3 Alert Routing

Alerts are classified by severity:
- **INFO**: Informational, no action required
- **WARNING**: Investigate if persistent; may indicate degrading behavior
- **CRITICAL**: Immediate investigation required; system may be producing unreliable output

Alerts are routed to operational dashboard and optionally to external notification channels.

### 10.4 Retention

- Raw event logs: 30 days
- Aggregated metrics: 12 months
- Alert history: 12 months
- Product trace data: lifetime of product record

---

## 11. Key Observability Questions

This specification enables answering:

| Question | Dimensions Used |
|---|---|
| Why did product X fail processing? | Processing, Extraction, Validation |
| Which extraction method is most accurate? | Extraction, Quality |
| Is confidence scoring calibrated? | Extraction, Quality, Human Review |
| Where do bottlenecks occur at scale? | Processing, Cost |
| What is the system's cost efficiency? | Cost |
| Are sources becoming stale? | Freshness |
| Is the system improving or degrading? | Quality trends, all trends |
| What types of conflicts are most common? | Conflicts |
| How often do humans disagree with AI? | Human Review, Quality |
| What is the hallucination rate? | Quality |
| Is provenance coverage sufficient? | Quality |

---

## 12. Trade-offs

| Choice | Gain | Lose |
|---|---|---|
| Structured event logging per product | Full traceability | Storage overhead |
| Per-stage latency tracking | Bottleneck identification | Slight instrumentation complexity |
| Confidence distribution tracking | Calibration insight | More data to aggregate |
| Per-product cost attribution | Cost transparency | Requires careful accounting |
| Rolling quality trends | Degradation detection | Lag in detecting sudden changes |
| Human vs. AI agreement tracking | Trust calibration | Requires consistent human review |

---

## Dependencies

- Builds on: Module 2 canonical product model, validation layers, provenance model
- Enables: Module 4 (implementation), Module 7 (evaluation), Module 9 (deployment)
- Required by: Cost justification, quality claims, judge demonstration

---

## Acceptance Criteria

This document is complete when:

- [x] All observability dimensions are defined
- [x] Metrics are specified per dimension
- [x] Alerting thresholds are defined with rationale
- [x] Dashboard requirements are specified
- [x] Cost tracking approach is defined
- [x] Quality trend monitoring is specified
- [x] Failure analysis capability is described
- [x] Implementation approach is outlined
- [x] Trade-offs are acknowledged
