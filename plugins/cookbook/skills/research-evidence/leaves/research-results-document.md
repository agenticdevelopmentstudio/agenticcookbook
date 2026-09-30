<!-- leaf: research-evidence/research-results-document · source: guidelines/researching/evidence/research-results-document.md -->

**Rules** (cite as `research-evidence/research-results-document#<slug>`):

- `claim-carry` MUST — Each claim MUST carry:
- `document-record-topic-scope-research` SHOULD — The document SHOULD record: topic and scope; the research questions; methodology (search strategy and …

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
