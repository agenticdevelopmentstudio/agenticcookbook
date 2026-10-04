---
id: 8ade0fa5-dd84-4fa2-9170-2ff30ef9691f
title: "Research type taxonomy"
domain: agenticdevelopercookbook://guidelines/researching/process/research-type-taxonomy
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-27
modified: 2026-06-27
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Classify a topic by intent and domain before researching; each type carries its own authoritative sources, method, and validation bar."
platforms: []
tags:
  - research
  - classification
  - methodology
depends-on: []
related:
  - agenticdevelopercookbook://principles/type-precedes-method
  - agenticdevelopercookbook://principles/domain-stratified-trust
  - agenticdevelopercookbook://guidelines/researching/process/research-methodology-and-sources
references:
  - https://dl.acm.org/doi/10.1145/792550.792552
  - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC1904193/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-27"
triggers:
  - research
---

# Research type taxonomy

Classify before you search. Apply three lenses — intent, domain, method — then let the type pick the sources, the method, and the bar.

## Three lenses

1. **Intent** — Know / Do / Decide / Verify / Navigate.
2. **Domain** — medical, technical, legal, financial, news, consumer, …
3. **Method** — qualitative / quantitative / mixed; primary / secondary.

## The types

| Type | Authoritative sources | Method | Bar |
|------|----------------------|--------|-----|
| Scientific / empirical | peer-reviewed journals | systematic search + replication | HIGH |
| Medical / clinical | PubMed, Cochrane, ClinicalTrials.gov | PICO + GRADE | VERY HIGH |
| Legal / regulatory | statutes, regulations, case law | primary authority + jurisdiction + currency | HIGH |
| Technology / software | official docs, standards, release notes | docs-first; recency-critical | MEDIUM |
| Business / market | disclosed-methodology reports | triangulate; follow the money | MEDIUM |
| Financial / economic | SEC/EDGAR, FRED/BLS, audited reports | primary filings | HIGH |
| Historical | primary sources + scholarship | independent corroboration | MED-HIGH |
| News / current events | 2+ independent outlets, primary docs | lateral reading | MED-HIGH |
| How-to / troubleshooting | official docs, reputable practitioners | reproduce the steps | MEDIUM |
| Statistical / data | government or peer-reviewed datasets | methodology check | MED-HIGH |
| Product comparison | independent testing + consensus | aggregate independent reviews | LOW-MEDIUM |
| Definitional / background | reference works, encyclopedic | corroborate across references | LOW-MEDIUM |

## Routing and escalation

Classify by keywords and intent. **Escalate one level** when life or safety, legal, or financial stakes appear, or when the answer will be acted on. When a topic spans types, the higher-stakes type sets the bar.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-27 | Mike Fullerton | Initial creation |
