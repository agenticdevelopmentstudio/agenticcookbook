---
id: cf9c8df3-24b7-4094-a2bd-3a10ed2da006
title: "Conformance: The Criterion Walk"
domain: agenticdevelopercookbook://guidelines/reviewing/conformance-criterion-walk
type: guideline
version: 1.0.1
status: draft
language: en
created: 2026-06-29
modified: 2026-10-03
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Adjudicate a change against an acceptance contract criterion by criterion — met, unmet, or divergent — with an always-on full-criterion-walk backstop and evidence demanded for every 'met'."
platforms: []
tags:
  - reviewing
  - code-review
  - conformance
triggers: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-03"
depends-on: []
related: []
references: []
---

# Conformance: The Criterion Walk

Conformance review asks a different question than quality review: did the change do what it was asked to do, completely? It judges a diff against an explicit acceptance contract.

## Acceptance Contracts
- **conformance-explicit-contract**: Conformance MUST be judged against an explicit, criterion-by-criterion acceptance contract, not an implicit sense of "done".

## Met / Unmet / Divergent
- **conformance-per-criterion-verdict**: Each acceptance criterion MUST be judged individually as met, unmet, or divergent.
- **conformance-divergent-distinct**: Divergent — built, but in a way that conflicts with the intent ("built right but wrong") — MUST be distinguished from unmet (not built at all); they have different fixes.

## Coverage Backstop
- **conformance-full-walk**: An always-on reviewer MUST walk every criterion as a coverage backstop, so no criterion is silently skipped when the diff does not obviously touch it.

## Demand Evidence
- **conformance-demand-evidence**: A "met" verdict MUST cite evidence in the diff; absence of evidence is not "met".

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-29 | Mike Fullerton | Initial creation |
| 1.0.1 | 2026-10-03 | Mike Fullerton | Add the missing Change History section |
