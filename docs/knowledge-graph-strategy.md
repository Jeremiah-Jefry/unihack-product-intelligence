# Knowledge Graph Strategy

Module 3 — Architecture Decision Record

---

## 1. Decision

**Knowledge graph: NOT REQUIRED for MVP.**

A knowledge graph is not introduced at this stage. Product relationships are stored as structured data within the canonical model and persisted in a relational/document database.

---

## 2. Analysis

### 2.1 What a Knowledge Graph Would Represent

The canonical product model defines `ProductRelationship` with 8 relationship types:

| Relationship | Example |
|---|---|
| `replaces` | Product B replaces Product A |
| `replaced_by` | Product A is replaced by Product B |
| `compatible_with` | Sensor X is compatible with Controller Y |
| `supersedes` | New spec supersedes old spec |
| `superseded_by` | Old spec is superseded by new spec |
| `component_of` | Valve is component of Pump Assembly |
| `has_component` | Pump Assembly has component Valve |
| `similar_to` | Product A is similar to Product B |

These relationships are already modeled as first-class entities. Each relationship has:

- `source_product_id`
- `target_product_id`
- `relationship_type`
- `confidence`
- `provenance`
- `evidence`

### 2.2 Value of a Knowledge Graph

A graph database (Neo4j, ArangoDB, etc.) excels at:

- **Multi-hop traversal** — "Find all products compatible with products that replace X"
- **Pattern matching** — "Find chains of compatibility across 4+ hops"
- **Dynamic relationship discovery** — Inferring new edges from traversal patterns
- **Graph algorithms** — Centrality, community detection, shortest path

### 2.3 Cost of a Knowledge Graph

| Cost | Impact |
|---|---|
| New database dependency | Operational complexity, deployment overhead |
| Query language (Cypher/Gremlin) | Learning curve, tooling gap |
| Data synchronization | Keep graph in sync with canonical store |
| Schema evolution | Graph schema changes require migration |
| Team knowledge | Graph modeling is specialized knowledge |
| Hackathon timeline | Significant integration effort for uncertain gain |

---

## 3. Comparison: Without vs With Graph

### Without Knowledge Graph (MVP)

```
Canonical Model
    ↓
Relational/Document DB (PostgreSQL, MongoDB)
    ↓
Simple relationship table/collection
    ↓
Direct queries: JOINs, array filters, aggregation
```

**Capabilities:**
- Store all 8 relationship types
- Query direct relationships (1 hop)
- Filter by relationship type, confidence, provenance
- Validate relationship consistency
- Support human review of relationships

**Limitations:**
- Multi-hop queries require application-level traversal
- No native graph algorithms
- Pattern matching is manual application logic

### With Knowledge Graph (Future)

```
Canonical Model
    ↓
Graph DB (Neo4j) + Relational DB
    ↓
Relationships as edges, Products as nodes
    ↓
Cypher queries, graph algorithms
```

**Additional capabilities:**
- Native multi-hop traversal
- Shortest path, community detection
- Relationship chain inference
- Visual graph exploration

**Additional costs:**
- Dual database maintenance
- Sync complexity
- Deployment overhead
- Query language divergence

---

## 4. Why Not for MVP

1. **Relationship queries are simple at MVP scale.** With fewer than 1,000 products, direct JOINs and array filters perform adequately.

2. **The canonical model already handles relationships.** `ProductRelationship` is a first-class entity with type, confidence, provenance, and evidence. No information is lost.

3. **Graph value requires scale.** Multi-hop traversal becomes valuable when relationship chains span hundreds or thousands of products. At hackathon scale, this is not the case.

4. **Hackathon time is limited.** Integrating a graph database, syncing data, building query layers, and testing graph-specific logic consumes significant time with low visibility to judges.

5. **Relational storage is sufficient for validation.** All validation rules (consistency, contradiction detection, completeness) can operate on flat relationship records.

---

## 5. When to Add a Knowledge Graph

A knowledge graph SHOULD be introduced when any of these conditions become true:

### Condition 1: Multi-Hop Traversal Is Required

**Trigger:** Users or system need to answer queries like:
- "Find all products compatible with products that are replacements for X"
- "What is the shortest compatibility chain between Product A and Product B?"
- "Which products in this chain have the lowest confidence ratings?"

**Evidence:** More than 30% of relationship queries require 2+ hops.

### Condition 2: Catalog Scale Exceeds 100K Products

**Trigger:** The product catalog grows to a size where relationship webs become too complex for JOIN-based queries.

**Evidence:** Query performance degrades below acceptable thresholds on relational storage.

### Condition 3: Dynamic Relationship Discovery Becomes a Core Feature

**Trigger:** The system begins inferring new relationships from:
- Text analysis of technical documents
- Cross-reference mining across catalogs
- Pattern detection in compatibility data

**Evidence:** Relationship count grows faster than products, requiring graph-native algorithms to manage.

### Condition 4: Graph Algorithms Provide Measurable Value

**Trigger:** Use cases emerge that require:
- Centrality analysis (which products are most connected?)
- Community detection (which product families form clusters?)
- Anomaly detection (which relationships are outliers?)

**Evidence:** These use cases are validated as high-priority in evaluation.

---

## 6. Alternative: Structured Relationship Storage

For MVP, relationships are stored using a structured approach within the canonical model.

### Schema

Each product contains a `relationships` array:

```json
{
  "product_id": "PROD-001",
  "relationships": [
    {
      "relationship_id": "REL-001",
      "relationship_type": "compatible_with",
      "target_product_id": "PROD-042",
      "confidence": 0.95,
      "evidence": [
        {
          "evidence_type": "source_extraction",
          "source_document_id": "DOC-003",
          "extracted_text": "Compatible with Model X controllers",
          "extraction_method": "llm_extraction",
          "confidence": 0.9
        }
      ],
      "provenance": {
        "method": "llm_extraction",
        "model": "gpt-4",
        "extracted_at": "2026-08-18T10:00:00Z",
        "reviewed": false
      }
    }
  ]
}
```

### Query Patterns

| Query | Method |
|---|---|
| Get all relationships for a product | Direct array access |
| Get all products compatible with X | Filter by `relationship_type == "compatible_with"` and `target_product_id` |
| Get 2-hop compatibility chain | Two sequential queries, join in application |
| Find replacement chains | Filter by `replaces`/`replaced_by`, traverse in application |
| Validate relationship consistency | Cross-check reciprocal relationships |
| Rank by confidence | Sort by `confidence` field |

### Performance

At MVP scale (< 1,000 products, < 10,000 relationships):
- Direct queries: < 10ms
- 2-hop traversal: < 100ms (application-level)
- Full catalog scan: < 500ms

These performance characteristics are acceptable for the hackathon.

---

## 7. Migration Path

When a knowledge graph becomes justified:

1. **Export** relationships from canonical model
2. **Import** into graph database (Neo4j preferred for query flexibility)
3. **Establish sync** between canonical store and graph
4. **Redirect** multi-hop queries to graph layer
5. **Keep** canonical model as source of truth for product data
6. **Use** graph as read-optimized query layer for relationships

This ensures the canonical model remains authoritative while the graph provides performance and algorithmic capabilities.

---

## 8. Summary

| Aspect | Decision |
|---|---|
| Knowledge graph for MVP | **Not required** |
| Relationship storage | Structured data in canonical model |
| MVP query capability | Direct access, 1-hop traversal, application-level multi-hop |
| Graph trigger conditions | Multi-hop queries > 30%, catalog > 100K, dynamic discovery, graph algorithms needed |
| Migration strategy | Canonical model remains source of truth; graph as read layer |

---

*Decision made: 2026-08-18*
*Module: 3 — Architecture*
*Status: Final*
