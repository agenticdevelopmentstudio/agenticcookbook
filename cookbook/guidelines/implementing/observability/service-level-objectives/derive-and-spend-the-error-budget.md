
The error budget is `1 - SLO` — the allowed unreliability over the window. A 99.9% SLO over 30 days permits ~43 min of downtime-equivalent.

- **budget-governs-velocity**: A healthy budget SHOULD license shipping faster; an exhausted budget SHOULD trigger an agreed response (freeze risky changes, prioritize reliability work) until it recovers.
- **agree-the-policy-first**: The consequences of budget exhaustion MUST be agreed by both product and engineering owners *before* a breach, not negotiated during an incident.

