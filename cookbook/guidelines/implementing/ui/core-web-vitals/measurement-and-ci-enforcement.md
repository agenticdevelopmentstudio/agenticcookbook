
- Collect field data via the **`web-vitals` JavaScript library** (reports LCP, INP, CLS using the attribution build for debugging) or the Chrome User Experience Report (CrUX).
- Wire a CI gate such as **Lighthouse CI** (`lhci autorun`) with assertions on metric thresholds and resource/byte budgets defined in a `budget.json`.
- Express budgets as concrete limits (e.g., total JS transfer <= 170KB compressed for the critical path) and fail the build on regression — this turns performance into a `tight-feedback-loop` and a `support-automation` boundary rather than a manual review step.

