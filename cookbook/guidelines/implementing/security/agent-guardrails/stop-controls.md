
- **kill-switch**: A kill switch that halts the agent and revokes its tool access **MUST** exist and be reachable by operators.
- **circuit-breakers**: Repeated failures, guardrail trips, or anomalous cost/rate **SHOULD** trip a circuit breaker that pauses the agent and alerts.
- **audit-trail**: Inputs, tool calls, confirmations, and guardrail decisions **SHOULD** be logged for after-the-fact review.

