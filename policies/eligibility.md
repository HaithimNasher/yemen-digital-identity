# Eligibility Policy — Draft

Status: `DRAFT`

YDII separates:

1. namespace status,
2. applicant type,
3. evidence requirements,
4. final operational approval.

The Eligibility Engine is a **decision-support prototype**. It does not make legally binding registration decisions.

## Decision states

- `ELIGIBLE`
- `NOT_ELIGIBLE`
- `REVIEW_REQUIRED`
- `PROPOSED_ZONE`
- `UNKNOWN_ZONE`

## Important rule

A positive rule match is not automatically a completed domain registration.

The operational system would still need:
- name availability
- reserved-name checks
- identity / organization verification
- policy review
- payment rules, if applicable
- registry create operation
- audit event

## Current model

### gov.ye
Applicant: government entity  
Evidence:
- institutional authorization
- authorized contact

### edu.ye
Applicant:
- university
- education institution

Evidence:
- education authorization/license
- authorized contact

### com.ye / org.ye / net.ye
Sector match leads to `REVIEW_REQUIRED` until operational policy is formally encoded.

## Proposed zones

`sch.ye`, `med.ye`, `name.ye`, `pro.ye`, and `museum.ye` always return `PROPOSED_ZONE` in this version.

`.اليمن` is a research track and also cannot return an operational eligibility approval.
