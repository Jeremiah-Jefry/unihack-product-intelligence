# ADR-008: Agent Decision

**Status:** Accepted
**Date:** 2026-08-18

## Context

AI agents are mentioned as a key technology in the project. Agents offer autonomous multi-step reasoning: the ability to plan, use tools, evaluate results, and iterate. The system has multiple capabilities that could potentially benefit from agent-based approaches. The question is whether to build a multi-agent system or use agents selectively.

## Problem

Should we build a multi-agent system with specialized agents, or use agents selectively for specific tasks?

## Decision

**One enrichment agent with defined tools and constraints. No multi-agent orchestration.** The core pipeline uses deterministic orchestration.

## Rationale

The enrichment agent is justified because enrichment genuinely requires autonomous multi-step reasoning:
1. Analyze what attributes are missing
2. Search for relevant information (web search, indexed sources)
3. Evaluate the quality and relevance of retrieved information
4. Extract structured values from retrieved content
5. Decide whether extracted values meet confidence thresholds
6. Handle cases where search results are ambiguous or conflicting

This is a natural fit for an agent: it requires planning, tool use, iteration, and judgment calls at each step.

Multi-agent orchestration is NOT justified because:
1. The core pipeline is deterministic and well-defined (extract → normalize → validate → review → output). Deterministic orchestration is more reliable and testable than agent-based orchestration for these steps.
2. Agent non-determinism adds risk without proportional value for the core pipeline. Each step has clear inputs and outputs; there is no benefit to an agent "deciding" how to validate a value.
3. Coordination overhead between agents (shared state, conflict resolution, task assignment) is complex for the hackathon timeline and introduces failure modes that are hard to debug.

## Consequences

**Positive:**
- Limited agent complexity — one agent with defined tools is easier to build, test, and debug
- Clear responsibilities — the enrichment agent owns enrichment, the pipeline owns extraction and validation
- Testable enrichment — the agent can be evaluated against enrichment benchmarks
- Deterministic pipeline steps are reliable, fast, and auditable

**Negative:**
- No multi-agent benefits (parallel research, specialized expertise across agents)
- Enrichment agent is a single point of failure for the enrichment capability
- Enrichment agent cannot decompose into specialized sub-tasks (e.g., separate agent for web search vs. index search)
- If enrichment complexity grows, the single agent may become a bottleneck

## Rejected Alternatives

- **Multi-agent system:** Rejected because the core pipeline does not benefit from autonomous decision-making, and the coordination overhead between agents is complex for the hackathon timeline. The non-determinism of multiple agents interacting introduces hard-to-debug failure modes.
- **No agents at all:** Rejected because enrichment genuinely benefits from autonomous search and reasoning. A deterministic pipeline cannot dynamically search the web, evaluate search results, and extract values from unstructured retrieved content. This requires the planning and tool-use capabilities of an agent.
