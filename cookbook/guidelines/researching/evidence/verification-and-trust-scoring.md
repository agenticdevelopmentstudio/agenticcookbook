---
id: a94d7efc-746e-4d93-8ea2-c4ff28f1f28a
title: "Verification and trust scoring"
domain: agenticdevelopercookbook://guidelines/researching/evidence/verification-and-trust-scoring
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-27
modified: 2026-06-27
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Domain-aware verification frameworks, a 0-100 trust rubric with domain ceilings, and the false-positive patterns that mark an untrustworthy claim."
platforms: []
tags:
  - research
  - verification
  - trust
depends-on: []
related:
  - agenticdevelopercookbook://principles/domain-stratified-trust
  - agenticdevelopercookbook://principles/suppress-unsupported-confidence
  - agenticdevelopercookbook://principles/independence-before-corroboration
references:
  - https://hapgood.us/2019/06/19/sift-the-four-moves/
  - https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2981887/
  - https://beallslist.net/
  - https://www.ifcncodeofprinciples.poynter.org/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-27"
triggers:
  - research
---

# Verification and trust scoring

How trustworthy a claim is depends on its domain. Verify with the right framework, score on a common scale, and cap claims that fail their domain's minimum — so a casually-asked medical claim is still held to the medical bar.

## Verification frameworks

- **SIFT / Four Moves** — Stop, Investigate the source, Find better coverage, Trace to the original. Fast triage.
- **Lateral reading** — leave the page to check the source's reputation elsewhere.
- **CRAAP / RADAR** — currency, relevance, authority, accuracy, purpose.
- **GRADE + evidence hierarchies** — strength of medical/scientific evidence (RCT > cohort > case report).
- **IFCN code** — journalistic fact-checking standards.
- **Predatory-venue (Beall's) and retraction (Retraction Watch) checks** — void credit for fake or withdrawn sources.

## Domain bars

Medical VERY HIGH (RCT / systematic review; check retractions) · Scientific HIGH (+ replication) · Legal HIGH (primary authority, jurisdiction, currency) · Financial HIGH (SEC / government primary) · News MED-HIGH (two independent outlets) · Historical MED-HIGH · Statistical MED-HIGH (disclosed methodology) · Technical MEDIUM (official current docs; recency) · Business MEDIUM · Product / how-to / definitional LOW-MEDIUM (broad independent consensus).

## Scoring (0-100)

Blend: **Authority (30) + Independent corroboration (25) + Accuracy/verifiability (20) + Currency (10, domain-scaled) + Transparency (15)**. Then apply a **domain ceiling** that caps a claim failing its domain's minimum source — e.g. a medical claim caps near 45 without a peer-reviewed RCT or systematic review, however confident it sounds.

## False-positive catalog

Score LOW when a claim is: single-source; citation laundering / loops; confident-but-unsupported; published in a predatory venue; carrying an undisclosed conflict of interest; wrapped in urgency / emotional framing; outdated in a fast-moving domain; an anecdote generalized to a population; viral-but-unverified; backed by a fabricated or hallucinated citation; from an authority speaking outside their field; p-hacked / unreplicated; or AI content-farm output.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-27 | Mike Fullerton | Initial creation |
