
INP (Interaction to Next Paint) **replaced** FID as the responsiveness Core Web Vital on **2024-03-12**. Agents MUST NOT reference FID as a current Core Web Vital.

| Metric | Measures | "Good" (p75 field) | "Needs improvement" | "Poor" |
|--------|----------|--------------------|---------------------|--------|
| LCP — Largest Contentful Paint | Loading | <= 2.5s | <= 4.0s | > 4.0s |
| INP — Interaction to Next Paint | Responsiveness | <= 200ms | <= 500ms | > 500ms |
| CLS — Cumulative Layout Shift | Visual stability | <= 0.1 | <= 0.25 | > 0.25 |

- A page passes only when **all three** metrics are in the "good" range at the **75th percentile** of real-user (field) data.
- Thresholds are evaluated per metric, segmented by device class (mobile vs. desktop).

