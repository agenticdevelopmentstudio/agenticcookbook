---
id: ed0b7eb6-9e33-41f7-954f-1e1a0f813462
title: "Agentic research design lessons"
domain: agenticdevelopercookbook://guidelines/researching/process/agentic-research-design-lessons
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-27
modified: 2026-06-27
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Architecture, sourcing, citation, and verification lessons distilled from production deep-research agents."
platforms: []
tags:
  - research
  - agents
  - architecture
depends-on: []
related:
  - agenticdevelopercookbook://principles/cite-the-claim-not-the-document
  - agenticdevelopercookbook://principles/independence-before-corroboration
  - agenticdevelopercookbook://guidelines/researching/evidence/verification-and-trust-scoring
references:
  - https://github.com/assafelovic/gpt-researcher
  - https://github.com/stanford-oval/storm
  - https://github.com/langchain-ai/open_deep_research
  - https://huggingface.co/blog/open-deep-research
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-27"
triggers:
  - research
---

# Agentic research design lessons

Lessons distilled from production deep-research agents — GPT-Researcher, Stanford STORM, LangChain and HuggingFace Open Deep Research, OpenAI and Gemini Deep Research, and Perplexity.

## Orchestration

- The orchestrator **plans and synthesizes; it never does ground research itself.**
- Budget per-subtopic specialists with isolated context.
- **Outline before searching;** reflect at both supervisor and worker level.
- Stop on **coverage** (two independent sources, or one authoritative one), not on a loop count.

## Sourcing and retrieval

- Multi-engine, domain-routed sources; **rerank and quality-gate before the LLM sees them.**
- Filter by freshness and authority / venue reputation.
- **Read full pages, not snippets.**

## Citation and provenance

- **Attach citation metadata at retrieval time, not after generation** — pre-embedding citations gave the best observed accuracy (~92% in Perplexity).
- Cite at the claim / sentence level with the supporting quote.
- Keep stable, numbered citations through summarization.

## Verification

- A **dedicated reviewer** with explicit acceptance criteria.
- **Cross-source corroboration** is the primary anti-hallucination defense.
- Check URL health / citation existence — even top tools hallucinate 3-13% of URLs.
- Perspective diversity is structural anti-hallucination.

## Reporting

- Outline-driven report with a **confidence / coverage indicator per section.**
- Keep intermediate artifacts (outline, mind-map) for human review.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-27 | Mike Fullerton | Initial creation |
