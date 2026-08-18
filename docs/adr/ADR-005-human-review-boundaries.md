# ADR-005: Human Review Boundaries

**Status:** Accepted
**Date:** 2026-08-18

## Context

The system must determine when human review is required versus when auto-approval is safe. Industrial product data carries real business risk: incorrect safety ratings, invalid certifications, or wrong technical specifications can lead to liability, compliance failures, or downstream errors. A purely automated system risks approving values that should not be approved, while a purely human-reviewed system does not scale.

## Problem

How to minimize human review burden while ensuring high-risk values are verified?

## Decision

Confidence-based routing with hard rules for safety and certification attributes.

**Auto-approve when ALL of the following are true:**
- Confidence score >= 0.7
- Validation passes (schema, type, range, cross-field)
- Attribute is NOT safety-critical
- Attribute is NOT certification-related

**Route to human review when ANY of the following are true:**
- Confidence score < 0.7
- Attribute is safety-critical (e.g., operating temperature limits, pressure ratings, electrical safety)
- Attribute is certification-related (e.g., CE marking, UL listing, ISO compliance)
- Conflict detected between sources or between extraction and validation

## Rationale

Confidence scoring provides a principled basis for routing decisions. It is derived from multiple signals (extraction source, evidence count, model agreement, validation results) rather than being arbitrary.

Hard rules for safety and certification ensure no high-risk value is auto-approved regardless of confidence score. A confidence score of 0.95 on a safety-critical attribute still routes to human review. This is a deliberate constraint: the cost of a false auto-approval on safety attributes far exceeds the cost of reviewer time.

This approach balances automation with trustworthiness. The majority of routine attributes (dimensions, weight, material names) will be auto-approved, reducing reviewer burden. High-risk attributes are always verified.

## Consequences

**Positive:**
- Most values auto-approved, significantly reducing review burden
- High-risk values (safety, certification) always receive human verification
- Routing is deterministic and explainable
- System can be tuned by adjusting the confidence threshold

**Negative:**
- Confidence scoring must be well-calibrated; miscalibration leads to systematic under- or over-reviewing
- False positives (unnecessary reviews) waste reviewer time
- False negatives (missed reviews) create risk
- Requires ongoing calibration as extraction quality improves

## Rejected Alternatives

- **Fully automated approval:** Rejected because safety and certification attributes require human judgment regardless of confidence
- **Full human review of all attributes:** Rejected because it does not scale and creates reviewer fatigue, which itself introduces risk
- **Rule-only routing (no confidence):** Rejected because it ignores the variable quality of extraction across different attribute types and sources
