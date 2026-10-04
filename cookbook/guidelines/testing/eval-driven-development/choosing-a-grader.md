
| Grader type | Strengths | Limits | Use when |
|---|---|---|---|
| Code-based (assertion, regex, exact/structured match) | Fast, cheap, reproducible, easy to debug | Brittle to valid phrasing variations | Output is objectively checkable |
| Model-based (LLM-as-judge) | Flexible, scalable, captures nuance, handles open-ended tasks | Non-deterministic, costs tokens, can be biased | Output is open-ended or subjective |

- **MUST** prefer a code-based grader whenever the success criterion can be expressed in code.
- **SHOULD** grade each quality dimension (e.g., groundedness, coverage, tone) with a separate, isolated LLM-judge rather than one judge scoring everything at once.
- **SHOULD** use a judge model deliberately different from the model under test to reduce self-preference bias (a documented but still-active research concern, not a settled magnitude).

