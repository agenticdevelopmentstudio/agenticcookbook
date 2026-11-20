
[Baseline](https://web.dev/baseline) classifies each feature by interoperability across the two most recent major versions of Chrome, Edge, Firefox, and Safari:

- **Newly available** — interoperable across all core browsers as of a recent date. Usable, but older still-in-use versions may lack it.
- **Widely available** — Newly available plus 30 months elapsed. Treat as safe for general production with no fallback.

Requirements:

- Adoption of a CSS feature **MUST** be gated on its Baseline status, not on a single browser's support or anecdotal "Can I Use" glances.
- **Widely available** features **MAY** be used without a fallback.
- **Newly available** features **SHOULD** be used only with a documented fallback or progressive enhancement, because pre-cutoff browser versions still receiving traffic may not support them.
- Pin any Baseline claim to a date — statuses advance over time. Verify against MDN or the Baseline data before assuming current status.

