---
id: 8e204b5b-4f27-4f25-b43a-bf0b3ec3a88c
title: "Research methodology and sources"
domain: agenticdevelopercookbook://guidelines/researching/process/research-methodology-and-sources
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-27
modified: 2026-06-27
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "The agentic research workflow beyond web search, plus the authoritative source / API / MCP catalogue organized by domain."
platforms: []
tags:
  - research
  - methodology
  - sources
depends-on: []
related:
  - agenticdevelopercookbook://principles/provenance-at-generation-time
  - agenticdevelopercookbook://principles/independence-before-corroboration
  - agenticdevelopercookbook://guidelines/researching/process/research-type-taxonomy
references:
  - https://docs.openalex.org/
  - https://www.ncbi.nlm.nih.gov/books/NBK25501/
  - https://www.sec.gov/edgar/sec-api-documentation
  - https://www.prisma-statement.org/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-27"
triggers:
  - research
---

# Research methodology and sources

Web search is the start, not the method. Orient, go to authoritative sources, chain citations, corroborate across independent sources, and record provenance as you go.

## Workflow

1. **Orient and classify** the topic's domain.
2. **Identify authoritative sources** for that domain (catalogue below).
3. **Search** with Boolean or controlled vocabulary (e.g. MeSH for medicine).
4. **Chain citations** — backward and forward snowballing — to saturation.
5. **Corroborate** across genuinely independent sources.
6. **Record provenance** at generation time. Use PRISMA when systematic rigor is required.

## Source catalogue

- **Academic:** OpenAlex (free, no key — a strong default), Semantic Scholar, PubMed / Entrez, arXiv, Crossref, OpenCitations, CORE, Unpaywall, Scite.
- **Primary / official:** RFC/IETF, W3C, NIST/NVD, USPTO, SEC EDGAR, data.gov, World Bank, Eurostat, Census, ClinicalTrials.gov, CourtListener/RECAP, Congress.gov.
- **Domain / community:** official docs + GitHub + Stack Exchange + package registries (technical); Cochrane / medRxiv (medical); FRED / BLS (finance); Chronicling America / DPLA / Europeana (history).

## Agentic access (APIs and MCP)

Most academic and government sources expose **free REST APIs** an agent can call directly, and many have ready-made **MCP servers** (arxiv, semantic-scholar, openalex, pubmed, github). Agentic search layers include Tavily, Exa, Firecrawl, and Perplexity Sonar. Prefer reading full sources over snippets.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-27 | Mike Fullerton | Initial creation |
