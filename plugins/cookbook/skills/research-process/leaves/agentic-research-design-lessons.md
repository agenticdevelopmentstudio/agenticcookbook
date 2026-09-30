<!-- leaf: research-process/agentic-research-design-lessons · source: guidelines/researching/process/agentic-research-design-lessons.md -->

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
