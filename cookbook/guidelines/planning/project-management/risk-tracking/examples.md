
This section is informative; the entry below is an illustration, not a template the guideline requires.

A risk entry kept as a tracker issue:

```markdown
Title: R-014 Payment provider API deprecation may break checkout

Description: Because the payment provider is retiring its v2 API (cause),
checkout calls may start failing after the cut-off (event), stopping all
online sales until we migrate (effect).
Concerns: checkout service
Raised by: Priya (2026-11-03)
Owner: Sam
Actionee: Lee
Proximity: within the stage
Probability: 3  Impact: 5  Score: 15
Response: reduce: migrate to the v3 API this sprint
Status: active; response ongoing
Status history: 2026-11-03 active, response pending; 2026-11-10 active, response ongoing
Next review: sprint review, 2026-11-28
```

