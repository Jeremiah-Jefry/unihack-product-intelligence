# ADR-007: Knowledge Graph Decision

**Status:** Accepted
**Date:** 2026-08-18

## Context

Knowledge graphs are mentioned as a key technology in the project. They are powerful for representing and querying complex relationships between entities. The canonical product model includes a `ProductRelationship` entity that supports 8 relationship types: `compatible_with`, `requires`, `replaces`, `replaced_by`, `belongs_to_category`, `manufactured_by`, `uses_material`, `supersedes`. The question is whether a graph database is needed to store and query these relationships effectively.

## Problem

Does a knowledge graph add enough value to justify its complexity for the current project scope?

## Decision

**NOT REQUIRED for MVP.** Product relationships are stored as structured data in the canonical model's `ProductRelationship` entity using a relational or document store. A graph database will be evaluated for future versions when relationship queries become complex.

## Rationale

The canonical model already supports 8 relationship types with structured storage. For the hackathon scope, the primary relationship queries are:
- Find products compatible with a given product
- Find products by category
- Find products by manufacturer
- Find products using a specific material

These are all single-hop or simple two-hop queries that can be efficiently handled with indexed relational tables or document store queries. A graph database adds significant complexity:
- New database technology to deploy and maintain
- New query language (Cypher, Gremlin, or SPARQL) for the team to learn
- Data synchronization between the canonical store and the graph store
- Additional failure modes and operational overhead

The marginal benefit of a graph database for single-hop queries is negligible. Graph databases shine at multi-hop traversal (e.g., "find all products compatible with products that use the same material as product X"), but these queries are not required for the current scope.

## Consequences

**Positive:**
- Simpler architecture with fewer dependencies
- Faster implementation during hackathon timeline
- No additional database technology to learn or maintain
- Canonical model remains the single source of truth

**Negative:**
- Multi-hop relationship queries will be less efficient (require application-level traversal)
- Complex compatibility chains will be harder to represent and query
- If relationship requirements grow significantly, migration to a graph database will be needed
- Relationship queries must be implemented as application logic rather than graph-native traversal

## Rejected Alternatives

- **Graph database for MVP:** Rejected because the complexity cost outweighs the benefit for single-hop queries within hackathon scope. The canonical model already supports structured relationship storage.
- **No relationship support at all:** Rejected because relationships are a core part of product intelligence. Products exist in a web of compatibility, category, and manufacturing relationships that must be represented.
