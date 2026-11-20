
Classify severity at declaration to scale the response, and **MUST** re-evaluate as understanding changes. Use a small fixed ladder; exact thresholds are org-specific.

| Severity | Rough meaning | Typical response |
|----------|---------------|------------------|
| SEV1 | Major outage / data loss / broad customer impact | Full roles, immediate page, exec/comms notified |
| SEV2 | Significant degradation or partial outage | IC + ops lead, page on-call |
| SEV3 | Minor / contained impact, workaround exists | On-call handles, no full mobilization |

- Severity **MUST** map to concrete actions (who is paged, who is notified, update cadence) — a label with no behavior attached is noise.
- Tie thresholds to SLO error budgets where they exist (see related) rather than to gut feel.

