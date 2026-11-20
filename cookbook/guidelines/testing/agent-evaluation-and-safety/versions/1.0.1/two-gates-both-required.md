
A change to an agent system **SHOULD** pass both gates before release; either gate failing blocks the deploy.

| Gate | Question | SLO examples | Owned by |
|---|---|---|---|
| Eval (quality) | Does it do the job well? | task success rate, groundedness, tool-call accuracy, latency/cost budgets | eval-driven-development |
| Safety | Can it be made to cause harm? | jailbreak resistance, prompt-injection resistance, PII/secret leakage rate, refusal correctness | llm-application-security |

- For how to build graders, calibrate an LLM judge, and report `pass@k` vs `pass^k` consistency, follow **eval-driven-development**.
- For prompt injection, untrusted-output handling, and tool-agency constraints, follow **llm-application-security** (mapped to the OWASP Top 10 for LLM Applications **2025** revision — pin that edition).

