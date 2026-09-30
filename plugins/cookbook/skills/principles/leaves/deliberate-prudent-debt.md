<!-- leaf: principles/deliberate-prudent-debt · source: principles/deliberate-prudent-debt.md -->

# Deliberate, prudent technical debt

Trading rigor for speed is legitimate — but only when the trade is *deliberate* and *prudent*: a conscious, recorded choice with a payback trigger, never reckless or silent. Take the shortcut on purpose, write down what you deferred and why, budget time to repay it, and keep the debt visible rather than letting quality decay unnoticed.

- Deliberate and prudent only: "ship the simple version now, revisit when X happens" is fine when it's written down; an undocumented shortcut nobody chose is reckless debt.
- Record it at the point of compromise: leave a tracked marker (debt register, issue, or a TODO that states the condition) naming the trigger that should prompt repayment.
- Budget repayment: allocate capacity each iteration to pay debt down; debt with no payback plan compounds into decay.
- Account for AI volume: agent-generated code can inflate duplication and churn faster than debt is repaid — size debt budgets against the volume produced, and prefer paying down before adding more.
