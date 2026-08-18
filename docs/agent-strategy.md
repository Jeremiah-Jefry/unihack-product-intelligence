# Agent Strategy

> **Status:** Complete
> **Module:** 3 — Architecture & Data Model
> **Purpose:** Define where autonomous agents are justified, where they are not, and the specification for the one agent we will use.
> **Depends on:** All Module 1 and Module 2 documents

---

## 1. Decision: Limited Agent Use

**Answer to "Do we need agents?"** Yes — one agent. A single enrichment agent.

**Answer to "Do we need a multi-agent system?"** No. One agent is sufficient.

The guiding principle from `AGENTS.md`:

> Agents should exist only when autonomous decision-making or multi-step orchestration provides a genuine advantage.

We apply this principle strictly. Most of our pipeline is deterministic and well-defined. One stage — enrichment of missing attributes — genuinely benefits from autonomous decision-making. Everything else does not.

---

## 2. Why Most Pipeline Stages Do NOT Need Agents

The product intelligence pipeline has these stages:

| Stage | Nature | Why deterministic orchestration is better |
|-------|--------|------------------------------------------|
| **Ingestion** | Read source files, extract metadata | Fixed I/O operations. No decisions to make. |
| **Extraction** | Parse text, tables, images from sources | Well-defined parsers. Deterministic extraction methods. |
| **Normalization** | Unit conversion, terminology mapping | Rule-based transformations. No ambiguity. |
| **Validation** | Schema, type, range, cross-field checks | Deterministic checks against the canonical model. |
| **Conflict detection** | Compare candidate values for contradictions | Algorithmic comparison. No judgment calls. |
| **Conflict resolution** | Select or defer conflicting values | Mostly human-driven. Simple cases use priority rules. |
| **Review routing** | Determine if human review is needed | Threshold checks (confidence < 0.7, safety attributes). |
| **Publishing** | Format and emit to channels | Template-based output. No decisions. |

Deterministic orchestration for these stages provides:

- **Reproducibility.** Same input → same output. Critical for debugging and evaluation.
- **Testability.** Each stage can be unit-tested with known inputs and expected outputs.
- **Auditability.** Every decision has a clear, inspectable rule.
- **Performance.** No LLM inference overhead for simple operations.
- **Cost.** No token cost for rule-based operations.

Agent non-determinism adds risk without proportional value for these stages.

---

## 3. Why Enrichment Genuinely Needs an Agent

Enrichment is the process of filling missing attributes (`missing_status: NOT_PROVIDED` or `NOT_DISCOVERED`) from external sources. This is the one stage where deterministic orchestration breaks down because:

### 3.1 The search space is unbounded

We do not know in advance where a product's missing information lives. It could be on the manufacturer's website, in a distributor catalog, in a standards database, or in an industry classification system. The agent must search autonomously and decide which sources to try.

### 3.2 Source evaluation is contextual

Not all sources are equally trustworthy for all attribute types. A manufacturer's website is authoritative for specifications but not for commercial attributes. An ETIM database is authoritative for classification codes but not for dimensions. The agent must evaluate source relevance per attribute, not just per product.

### 3.3 Search depth must be adaptive

Some products have easily findable specs; others require deeper searching. The agent must decide when to stop — not on a fixed iteration count, but based on whether remaining effort is likely to yield useful results.

### 3.4 Result evaluation requires judgment

Retrieved text may contain relevant information, partially relevant information, or irrelevant information. The agent must extract, evaluate, and attach provenance to each retrieved value. This is harder to do with a deterministic pipeline because:

- Source layouts vary (different websites, different formats).
- The same attribute may be expressed differently across sources.
- Confidence assessment requires evaluating source quality, extraction quality, and value plausibility together.

---

## 4. Enrichment Agent Specification

### 4.1 Identity

| Property | Value |
|----------|-------|
| Name | `EnrichmentAgent` |
| Type | Single autonomous agent (not multi-agent) |
| Lifecycle state | Operates when product is in `enriching` state |
| Module alignment | Fills attributes from `NOT_PROVIDED` / `NOT_DISCOVERED` toward `enriched` → `validated` |

### 4.2 Goal

Fill missing attributes on a partial product record by searching external sources, extracting values, and attaching full provenance. Every enriched attribute must be indistinguishable in traceability from a directly extracted attribute.

### 4.3 Input

The agent receives:

| Input | Type | Description |
|-------|------|-------------|
| `product_record` | ProductRecord | The partial product record with missing attributes |
| `missing_attributes` | list\<AttributeRef\> | Which attributes to enrich (filtered by missing_status) |
| `category_schema` | CategorySchema | Defines which attributes are required and their expected types |
| `existing_sources` | list\<SourceDocument\> | Sources already ingested (to avoid re-searching) |
| `enrichment_config` | EnrichmentConfig | Max sources, max iterations, confidence threshold |

**EnrichmentConfig:**

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `max_sources_per_attribute` | integer | 5 | Maximum external sources to consult per attribute |
| `max_total_iterations` | integer | 20 | Hard cap on total search iterations (safety) |
| `confidence_threshold` | float | 0.7 | Below this, route to human review |
| `source_priority` | list\<TrustLevel\> | [manufacturer_official, authorized_distributor, third_party_verified, third_party_unverified] | Source preference order |
| `required_information_categories` | list\<InformationCategory\> | [specification, classification, certification] | Which categories to attempt enrichment for |

### 4.4 Tools

The agent has access to three tools. Each tool maps to a specific retrieval or extraction mechanism.

#### Tool 1: Web Search

| Property | Detail |
|----------|--------|
| Purpose | Find manufacturer websites, distributor pages, and product databases |
| Input | Query string (typically: brand + MPN + attribute name) |
| Output | List of candidate URLs with snippets |
| Provenance mapping | Creates SourceDocument with `type: web_page`, `extraction_method: web_scraping` |
| Trust scoring | Initial trust_level set to `third_party_unverified` unless URL pattern matches known manufacturer domain |

#### Tool 2: RAG Retrieval

| Property | Detail |
|----------|--------|
| Purpose | Search previously ingested and indexed documents for attribute values |
| Input | Query embedding (product identity + missing attribute name) |
| Output | Retrieved text passages with similarity scores |
| Provenance mapping | Reuses existing SourceDocument; creates new CandidateValue with original extraction metadata preserved |
| Trust scoring | Inherits trust_level from the original SourceDocument |

#### Tool 3: LLM Extraction

| Property | Detail |
|----------|--------|
| Purpose | Extract structured attribute values from retrieved text |
| Input | Retrieved text passage + target attribute schema |
| Output | Extracted value + confidence score + source location |
| Provenance mapping | Sets `extraction_method` to `web_scraping` (for web results) or `text_extraction` (for document results); `extraction_confidence` from LLM self-assessment |
| Constraints | Must cite the specific text span used for extraction; must not generate values not present in the text |

### 4.5 Output

The agent produces an **enrichment result** per attribute:

| Field | Type | Description |
|-------|------|-------------|
| `attribute_name` | string | Which attribute was enriched |
| `status` | enum | enriched, not_discovered, conflict_detected |
| `candidate` | CandidateValue? | The enriched value (when status = enriched) |
| `candidates` | list\<CandidateValue\>? | Multiple candidates (when status = conflict_detected) |
| `sources_consulted` | list\<UUID\> | Which sources were searched |
| `sources_used` | list\<UUID\> | Which sources produced usable values |
| `iterations_used` | integer | How many search iterations were performed |
| `reason` | string | Explanation (especially for not_discovered and conflict_detected) |

Each `CandidateValue` in the output follows the canonical model from `canonical-product-model.md`:

- `value` — the extracted value (conforms to the attribute's `value_type`)
- `unit` — unit of measurement (when applicable)
- `source_id` — reference to SourceDocument (the external source found by the agent)
- `source_location` — precise location (URL, section, text span)
- `extraction_method` — `web_scraping`, `api_lookup`, or `text_extraction`
- `extraction_confidence` — float 0.0-1.0
- `source_trust_score` — float 0.0-1.0 (based on source type and URL pattern)
- `freshness` — FreshnessInfo (best-effort assessment from page metadata)
- `transformations` — any normalization applied (unit conversion, etc.)

### 4.6 Constraints

These constraints are non-negotiable:

| Constraint | Rationale | Reference |
|-----------|-----------|-----------|
| **Must not fabricate sources** | A value without a real source is hallucination | `AGENTS.md` Section 4: AI Principles |
| **Must attach full provenance** | Every enriched value must be as traceable as a directly extracted value | `provenance-and-evidence-model.md` Section 4.7 |
| **Must set extraction_method correctly** | Enables downstream trust assessment | `canonical-product-model.md` Section 2.4 |
| **Must set lifecycle_state to `enriched`** | Distinguishes enriched values from directly extracted values | `validation-and-lifecycle-model.md` Section 2.1 |
| **Confidence < 0.7 triggers human review** | Low-confidence enrichment requires human verification | `validation-and-lifecycle-model.md` Section 5.1 |
| **Must preserve original value when normalizing** | Enables traceability back to source representation | `canonical-product-model.md` Section 2.3 |
| **Must set information_category** | Enables downstream systems to weight evidence by type | `canonical-product-model.md` Section 2.3 |

### 4.7 Execution Loop

```
ENRICHMENT AGENT LOOP
══════════════════════

Input: product_record, missing_attributes, category_schema

1. IDENTIFY missing attributes
   └─ Filter: missing_status IN (NOT_PROVIDED, NOT_DISCOVERED)
   └─ Filter: attribute IN required_information_categories
   └─ Sort: by category weight (critical attributes first)

2. FOR EACH missing attribute:
   a. CONSTRUCT search query
      └─ Include: brand, MPN, attribute name, category context
      └─ Include: attribute synonyms and unit context

   b. SEARCH (up to max_sources_per_attribute iterations)
      ├─ Try 1: RAG retrieval from existing indexed documents
      ├─ Try 2: Web search (manufacturer domain first)
      ├─ Try 3: Web search (distributor and industry databases)
      └─ Try 4+: Additional web searches with varied queries

   c. EXTRACT values from each source
      └─ Use LLM Extraction tool on retrieved text
      └─ Require: explicit text span citation
      └─ Require: confidence score

   d. EVALUATE results
      ├─ If no values found → set missing_status = NOT_DISCOVERED
      ├─ If one value found → create CandidateValue, set lifecycle_state = enriched
      ├─ If multiple values from different sources → create Conflict
      └─ If confidence < 0.7 → set requires_review = true

   e. ATTACH provenance
      └─ Full SourceDocument + SourceLocation + FreshnessInfo
      └─ extraction_method = web_scraping / api_lookup / text_extraction
      └─ source_trust_score based on source type

3. RETURN enrichment results
```

### 4.8 Stopping Criteria

The agent stops for an attribute when **any** of these conditions is met:

| Condition | What happens |
|-----------|-------------|
| Value found with confidence ≥ 0.7 | Attribute enriched, lifecycle_state → `enriched` |
| All `max_sources_per_attribute` sources exhausted with no value | Attribute marked `NOT_DISCOVERED` |
| `max_total_iterations` reached globally | Remaining attributes marked `NOT_DISCOVERED` with reason "iteration limit" |
| Source returns error or is inaccessible | Skip source, continue with next |
| All required information categories for the product are resolved or exhausted | Agent completes |

The agent does NOT stop early just because it found one easy attribute. It attempts all missing attributes before returning.

### 4.9 Failure Handling

| Failure | Handling | Lifecycle impact |
|---------|----------|-----------------|
| Source inaccessible (404, timeout, blocked) | Log failure, skip source, try next | No change to attribute state |
| LLM extraction returns no value | Log failure, try next source | No change to attribute state |
| LLM extraction confidence too low (< 0.3) | Discard result, try next source | No change to attribute state |
| Multiple conflicting values from different sources | Create Conflict record, set conflict_status = `pending_resolution` | lifecycle_state → `enriched`, conflict flagged for human review |
| All sources exhausted, no value found | Set missing_status = `NOT_DISCOVERED`, set lifecycle_state = `discovered` | Attribute remains in discovered state |
| Agent itself fails (LLM error, tool error) | Catch error, mark all remaining attributes as `NOT_DISCOVERED` with reason "agent_failure" | Partial enrichment preserved; failed attributes remain in discovered state |

**Critical rule:** Partial enrichment is always better than failed enrichment. If the agent finds values for 3 out of 7 missing attributes before failing, those 3 are preserved. The remaining 4 are marked `NOT_DISCOVERED`.

### 4.10 Post-Agent Validation

Every enriched attribute passes through the **same validation pipeline** as directly extracted attributes:

| Validation Layer | Applicable to enriched values? |
|-----------------|-------------------------------|
| Schema validation | Yes |
| Type validation | Yes |
| Unit validation | Yes |
| Range validation | Yes |
| Cross-field consistency | Yes |
| Cross-source agreement | Yes (compared against existing candidates) |
| Contradiction detection | Yes |
| Source verification | Yes (URL must be accessible) |
| Freshness check | Yes |
| Provenance check | Yes (mandatory — enriched values always need provenance) |
| Category-specific rules | Yes |

Enriched values receive no special treatment in validation. This is by design — an enriched value must meet the same quality bar as any other value in the system.

After validation, the normal lifecycle continues: `enriched` → `validated` → (human review if needed) → `approved`.

---

## 5. Why NOT Multi-Agent Orchestration

A multi-agent system would involve multiple specialized agents coordinating (e.g., a Search Agent, an Extraction Agent, a Validation Agent, a Conflict Agent). This is **not justified** for our project because:

### 5.1 The core pipeline is sequential and deterministic

```
ingestion → extraction → normalization → [enrichment] → validation → review → publishing
```

Each stage has clear inputs, clear outputs, and no ambiguity about what happens. Agent orchestration adds complexity where deterministic function calls suffice.

### 5.2 Agent non-determinism adds risk without proportional value

Multi-agent coordination introduces:

- **Emergent behavior.** Agents may make conflicting decisions about the same product.
- **Debugging difficulty.** When something goes wrong, tracing which agent caused the issue is harder.
- **Non-reproducibility.** Same input may produce different outputs across runs.
- **Coordination overhead.** Agents need shared state, message passing, or a shared store.

For a hackathon project, these costs are high and the benefits are low.

### 5.3 Only one stage genuinely needs autonomy

Only enrichment requires autonomous search, evaluation, and decision-making. Every other stage can be implemented as a deterministic function. Adding agents to stages that don't need them violates the principle:

> Agents should exist only when autonomous decision-making or multi-step orchestration provides a genuine advantage.

### 5.4 The enrichment agent handles its own orchestration

The enrichment agent internally sequences its own steps (search → evaluate → extract → attach provenance). This is sufficient for the problem. We do not need a meta-agent to orchestrate sub-agents when one agent can handle the full enrichment workflow.

---

## 6. When Agents Might Be Added in the Future

The following capabilities would justify additional agents **if and when** the project scales beyond the hackathon:

| Capability | Why an agent would help | When to consider |
|-----------|------------------------|------------------|
| **Contradiction resolution agent** | When sources conflict, an agent could autonomously investigate by searching for tiebreaker sources, checking manufacturer versioning, or comparing against authoritative databases | When automated conflict resolution rules prove insufficient |
| **Quality assessment agent** | An agent could holistically evaluate a product record, decide which attributes need re-verification, and prioritize human review queues | When catalog scale makes manual prioritization impractical |
| **Cross-product intelligence agent** | An agent could discover relationships between products (compatibility, supersession, family grouping) by analyzing patterns across the catalog | When product relationship mapping is required |
| **Multi-source ingestion agent** | An agent could autonomously discover and ingest new sources for products (e.g., finding new distributor feeds, monitoring manufacturer website changes) | When source discovery at scale is needed |
| **Compliance verification agent** | An agent could verify certifications and regulatory compliance by searching official databases and cross-referencing claims | When regulatory compliance verification is required |

Each of these would follow the same specification pattern as the enrichment agent: clear goal, defined tools, explicit constraints, provenance requirements, and human review thresholds.

**Do not add these agents now.** Build the system with one agent, validate that it works, and only add more when a specific capability is needed and the enrichment agent pattern has been proven.

---

## 7. Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Use agents? | Yes — one | Enrichment genuinely needs autonomous search and evaluation |
| Multi-agent? | No | Core pipeline is deterministic; coordination overhead not justified |
| Which agent? | `EnrichmentAgent` | Fills missing attributes from external sources with full provenance |
| Confidence threshold | 0.7 | Matches review routing threshold from `validation-and-lifecycle-model.md` |
| Failure handling | Partial enrichment preserved; missing → `NOT_DISCOVERED` | Partial success > total failure |
| Post-agent validation | Same pipeline as all other values | No special treatment for enriched values |
| Future agents | Add only when specific capability is needed and proven | Follow the one-agent pattern first |

---

## 8. References

| Document | What it provides |
|----------|-----------------|
| `canonical-product-model.md` | Attribute, CandidateValue, SourceDocument, SourceLocation structure |
| `provenance-and-evidence-model.md` | Enriched value provenance model, extraction methods, trust levels |
| `validation-and-lifecycle-model.md` | Lifecycle states, missing data states, review routing, validation layers |
| `attribute-taxonomy.md` | Value types, unit system, category-specific attribute schemas |
| `risks-and-failure-modes.md` | Hallucination risk, extraction failure modes, mitigation strategies |
| `AGENTS.md` | Agent principles, AI principles, product quality principles |
