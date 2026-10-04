---
id: 2795e06d-b081-43ac-97d9-20ff3d0a93b1
title: "Research results document"
domain: agenticdevelopercookbook://guidelines/researching/evidence/research-results-document
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-27
modified: 2026-06-27
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "What a research results document must store — per-claim provenance and a structured container — so a later consumer can trust and reuse it."
platforms: []
tags:
  - research
  - provenance
  - attribution
depends-on: []
related:
  - agenticdevelopercookbook://principles/provenance-at-generation-time
  - agenticdevelopercookbook://principles/cite-the-claim-not-the-document
  - agenticdevelopercookbook://guidelines/researching/evidence/verification-and-trust-scoring
references:
  - https://www.w3.org/TR/prov-o/
  - https://www.go-fair.org/fair-principles/
  - https://schema.org/ClaimReview
  - https://nanopub.net/
  - https://arxiv.org/abs/1803.09010
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-27"
triggers:
  - research
---

# Research results document

A research results document is not a thesis or an essay; it is a structured, auditable record of findings that a later consumer must be able to trust and reuse. Capture provenance, not prose.

## Per-claim record

Each claim MUST carry:

- The claim stated as one verifiable sentence.
- At least one citation with: title, author or organization, publisher or venue, date, DOI or URL, and the **access date**.
- The resource / **source type** (peer-reviewed, official docs, government data, clinical trial, news, reference, …).
- The **exact supporting quote** — verbatim, never paraphrased.
- Who or what generated the claim, and the **query** used to find it.
- A trust / confidence score and the basis for it.
- The **independence** of its support (corroboration: multi-independent, single, uncorroborated).

## Document container

The document SHOULD record: topic and scope; the research questions; methodology (search strategy and inclusion/exclusion); the agents and sources involved; dates; an executive summary; the findings; open questions; limitations; and license.

## Provenance standards to align with

- **W3C PROV** — entity / activity / agent, with `wasDerivedFrom`, `wasAttributedTo`, `hadPrimarySource`.
- **PAV** — `retrievedFrom`, `retrievedOn`, `createdWith`, `version`.
- **FAIR** — persistent identifiers (F1) and detailed provenance (R1.2).
- **schema.org Claim / ClaimReview** — for fact-check-style records.
- **DataCite / Dublin Core / Crossref** — for citation metadata.
- **Nanopublications** — the assertion / provenance / publication-info pattern for atomic, attributable claims.
- **Datasheets for Datasets / Data Cards** — when the result is itself a dataset.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-27 | Mike Fullerton | Initial creation |
