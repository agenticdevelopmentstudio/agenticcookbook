<!-- leaf: test-general/agent-evaluation-and-safety · source: guidelines/testing/agent-evaluation-and-safety.md -->

**Rules** (cite as `test-general/agent-evaluation-and-safety#<slug>`):

- `change-agent-system-pass-both-gates-before` SHOULD — A change to an agent system SHOULD pass both gates before release; either gate failing blocks the deploy.
- `you-define-both-quality-slos` MUST — You MUST define both quality SLOs and safety SLOs as explicit numeric thresholds before a model reaches production — …
- `you-express-slo-against-versioned` MUST — You MUST express each SLO against a versioned dataset so a pass/fail is reproducible.
- `safety-slos-include-hard-ceiling-zero` SHOULD — Safety SLOs SHOULD include a hard ceiling (e.g., zero tolerance for secret/PII exfiltration) distinct from soft quality …
- `you-not-trade-safety-slo-quality` SHOULD — You SHOULD NOT trade a safety SLO for a quality gain; surface the conflict explicitly and decide deliberately.
- `you-trigger-both-gates-change` MUST — You MUST trigger both gates on every change to the model/version, system prompt, tool definitions, retrieval corpus, or …
- `you-treat-model-version-bump` MUST — You MUST treat a model-version bump from a provider as a code change: re-run both gates before rolling it forward, even …
- `you-record-result-against-dataset` SHOULD — You SHOULD record each result against the dataset revision and model id so regressions are attributable to a specific …
- `you-keep-held-out-set` SHOULD — You SHOULD keep a held-out set that never informs iteration, so the gate measures generalization, not memorization.
- `you-seed-safety-gate-adversarial` MUST — You MUST seed the safety gate with an adversarial suite (jailbreaks, direct and indirect prompt injection, role-play …
- `you-combine-curated-known-attack` SHOULD — You SHOULD combine curated known-attack cases with periodic automated/agentic red-teaming; treat any new bypass as a …
- `you-layer-runtime-guardrails-input` MUST — You SHOULD layer runtime guardrails (input/output filters, allow-lists, tool-permission scoping) as defense-in-depth, …
- `you-persist-per-run-gate` MUST — You MUST persist per-run gate results so a quality or safety drop is visible as a trend, not discovered by users.
- `you-alert-regression-across-releases` SHOULD — You SHOULD alert on regression across releases, including flakiness regressions (consistency dropping even when …

# Agent evaluation and safety

Shipping a reliable agent is one discipline with two gates: **evaluation** (is it good?) and **safety** (is it harmful or exploitable?). Treat both as release-gating, run in CI on every model, prompt, tool, or retrieval change — not as a post-launch afterthought. This guideline ties the cluster together; it cross-references rather than duplicates the detail in the related guidelines.

## Two gates, both required

A change to an agent system **SHOULD** pass both gates before release; either gate failing blocks the deploy.

| Gate | Question | SLO examples | Owned by |
|---|---|---|---|
| Eval (quality) | Does it do the job well? | task success rate, groundedness, tool-call accuracy, latency/cost budgets | eval-driven-development |
| Safety | Can it be made to cause harm? | jailbreak resistance, prompt-injection resistance, PII/secret leakage rate, refusal correctness | llm-application-security |

- For how to build graders, calibrate an LLM judge, and report `pass@k` vs `pass^k` consistency, follow **eval-driven-development**.
- For prompt injection, untrusted-output handling, and tool-agency constraints, follow **llm-application-security** (mapped to the OWASP Top 10 for LLM Applications **2025** revision — pin that edition).

## Defining SLOs

- You **MUST** define both quality SLOs and safety SLOs as explicit numeric thresholds before a model reaches production — not "looks good in testing."
- You **MUST** express each SLO against a versioned dataset so a pass/fail is reproducible.
- Safety SLOs **SHOULD** include a hard ceiling (e.g., zero tolerance for secret/PII exfiltration) distinct from soft quality targets you tune over time.
- You **SHOULD NOT** trade a safety SLO for a quality gain; surface the conflict explicitly and decide deliberately.

## Run both gates in CI

- You **MUST** trigger both gates on every change to the model/version, system prompt, tool definitions, retrieval corpus, or guardrail config — any of these can regress behavior.
- You **MUST** treat a model-version bump from a provider as a code change: re-run both gates before rolling it forward, even if the prompt is unchanged.
- You **SHOULD** record each result against the dataset revision and model id so regressions are attributable to a specific change.
- You **SHOULD** keep a held-out set that never informs iteration, so the gate measures generalization, not memorization.

## Red-teaming the safety gate

- You **MUST** seed the safety gate with an adversarial suite (jailbreaks, direct and indirect prompt injection, role-play coercion, encoding tricks) — passing benign inputs proves nothing about resistance.
- You **SHOULD** combine curated known-attack cases with periodic automated/agentic red-teaming; treat any new bypass as a permanent regression case added to the suite.
- You **SHOULD** layer runtime guardrails (input/output filters, allow-lists, tool-permission scoping) as defense-in-depth, and **MUST NOT** treat a guardrail as a substitute for the gate that tests it.

## Tracking regressions over time

- You **MUST** persist per-run gate results so a quality or safety drop is visible as a trend, not discovered by users.
- You **SHOULD** alert on regression across releases, including flakiness regressions (consistency dropping even when best-case quality holds).

> Privacy/PII leakage SLOs here are engineering guidance for measuring and constraining exposure — **not legal advice**. Confirm regulatory obligations (e.g., data-residency, consent) with qualified counsel.

## Adopt-when-measured

Heavy evaluation infrastructure (managed eval platforms, dedicated red-team services, continuous online scoring) is justified **when a measured need warrants it** — scale, regulated risk, or a real incident — not by default (per YAGNI). Start with a small versioned dataset and CI gates; add platform weight when the gate cost or coverage demands it.
