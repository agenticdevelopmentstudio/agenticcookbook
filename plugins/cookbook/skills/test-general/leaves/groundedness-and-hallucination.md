<!-- leaf: test-general/groundedness-and-hallucination · source: guidelines/testing/groundedness-and-hallucination.md -->

**Rules** (cite as `test-general/groundedness-and-hallucination#<slug>`):

- `retrieved-context-you-measure-groundedness-claim-level` MUST — For retrieval-grounded (RAG) systems, an answer is only trustworthy if each claim is supported by the retrieved …
- `you-measure-retrieval-quality-recall` MUST — You MUST measure retrieval quality (recall@k, context precision) independently — most ungrounded answers trace to …
- `system-emit-citations-specific-source` SHOULD — The system SHOULD emit citations to specific source spans (doc id + offset/quote), not just document-level pointers.
- `you-verify-cited-spans-rather` MUST — You MUST verify cited spans rather than trust them: re-check that each quoted span exists in the source and entails the …
- `llm-judge-score-groundedness-seeing-only` MAY — An LLM judge MAY score groundedness by seeing only the answer + retrieved chunks and labeling each claim. Keep the …
- `you-calibrate-judge-against-human` MUST — You MUST calibrate the judge against a human-labeled gold set and report agreement (e.g., Cohen's kappa) before …
- `supporting-evidence-system-abstain-don-have-enough` SHOULD — When retrieval returns no supporting evidence, the system SHOULD abstain ("I don't have enough information") rather …
- `you-include-unanswerable-from-context` MUST — You MUST include "unanswerable from context" cases in the eval set and score abstention explicitly — otherwise a model …
- `fixed-query-set-fail-build-hallucination-rate` MUST — Run groundedness and hallucination evals in CI on a fixed query set; MUST fail the build when the hallucination rate …

# Groundedness and hallucination checks

For retrieval-grounded (RAG) systems, an answer is only trustworthy if each claim is supported by the retrieved context. You **MUST** measure groundedness (claim-level support) and a hallucination rate against retrieved sources, and the system **SHOULD** abstain rather than fabricate when support is missing.

## What to measure

| Metric | Question it answers | Target |
|--------|--------------------|--------|
| Groundedness / faithfulness | Is every claim entailed by retrieved context? | Maximize |
| Hallucination rate | Fraction of answers with ≥1 unsupported claim | Minimize |
| Citation accuracy | Do cited spans actually support the claim? | Maximize |
| Retrieval recall@k | Did retrieval surface the needed evidence? | Maximize |
| Abstention correctness | Does it decline when context is insufficient? | Maximize |

- Score groundedness at **claim granularity**, not whole-answer granularity: decompose the answer into atomic claims and label each `supported` / `partial` / `unsupported` (the FActScore decomposition approach, [arxiv.org/abs/2305.14251](https://arxiv.org/abs/2305.14251)).
- You **MUST** measure retrieval quality (recall@k, context precision) independently — most ungrounded answers trace to missing evidence, not generation, and fixing the generator cannot recover evidence that was never retrieved.

## Require and verify citations

- The system **SHOULD** emit citations to specific source spans (doc id + offset/quote), not just document-level pointers.
- You **MUST** verify cited spans rather than trust them: re-check that each quoted span exists in the source and entails the claim. Models cite plausibly but incorrectly, so an unverified citation is not evidence of groundedness.

## LLM judge, calibrated to humans

- An LLM judge **MAY** score groundedness by seeing only the answer + retrieved chunks and labeling each claim. Keep the judge blind to any gold answer so it scores support, not agreement.
- You **MUST** calibrate the judge against a human-labeled gold set and report agreement (e.g., Cohen's kappa) before trusting its scores. An uncalibrated judge can saturate near 1.0 and hide real failures.
- Frameworks such as RAGAS, DeepEval, and TruLens implement these metrics; their absolute scores diverge on the same data (forecast: still true in 2026), so pin one framework + version and track trends rather than comparing raw cross-tool numbers.

## Abstain instead of fabricating

- When retrieval returns no supporting evidence, the system **SHOULD** abstain ("I don't have enough information") rather than answer from parametric memory.
- You **MUST** include "unanswerable from context" cases in the eval set and score abstention explicitly — otherwise a model that always answers looks perfect on answerable queries while hallucinating on the rest.
- An abstention is a **correct** outcome when context is insufficient; do not penalize it as a miss in aggregate scoring.

## CI and gating

- Run groundedness and hallucination evals in CI on a fixed query set; **MUST** fail the build when the hallucination rate regresses past a set threshold.
- Treat groundedness as a release gate alongside latency and cost, not a one-time benchmark — retriever index drift and model swaps both move it.

> Privacy note: when eval sets contain user data, redact or synthesize PII before sending to a judge model. This is engineering guidance, not legal advice; consult counsel for regulated data.
