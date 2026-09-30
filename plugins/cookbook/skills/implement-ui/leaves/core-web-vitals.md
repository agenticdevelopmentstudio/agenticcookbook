<!-- leaf: implement-ui/core-web-vitals · source: guidelines/implementing/ui/core-web-vitals.md -->

**Rules** (cite as `implement-ui/core-web-vitals#<slug>`):

- `03-12-agents-not-reference-fid-current-core` MUST — INP (Interaction to Next Paint) replaced FID as the responsiveness Core Web Vital on 2024-03-12. Agents MUST NOT …
- `core-web-vitals-measured-field-p75-rum` MUST — Core Web Vitals MUST be measured in the field at p75 (RUM), not solely in lab tools — lab single-runs do not represent …
- `performance-budget-enforced-ci-so-regressions` MUST — A performance budget MUST be enforced in CI so regressions fail the build rather than reaching production.
- `tooling-lighthouse-devtools-used-diagnosis-pre-merge` SHOULD — Lab tooling (Lighthouse, DevTools) SHOULD be used for diagnosis and pre-merge gating, with field data as the …
- `late-injected-banners-reserve-space-via-explicit` MUST — Layout-shift-prone elements (images, ads, embeds, late-injected banners) MUST reserve space via explicit width/height …

# Core Web Vitals and performance budgets

Core Web Vitals are the user-centric metrics Google treats as a ranking and quality signal. Treat the field (RUM) p75 values — not lab numbers — as the source of truth, and gate regressions with a CI performance budget.

## The three Core Web Vitals (current as of 2026)

INP (Interaction to Next Paint) **replaced** FID as the responsiveness Core Web Vital on **2024-03-12**. Agents MUST NOT reference FID as a current Core Web Vital.

| Metric | Measures | "Good" (p75 field) | "Needs improvement" | "Poor" |
|--------|----------|--------------------|---------------------|--------|
| LCP — Largest Contentful Paint | Loading | <= 2.5s | <= 4.0s | > 4.0s |
| INP — Interaction to Next Paint | Responsiveness | <= 200ms | <= 500ms | > 500ms |
| CLS — Cumulative Layout Shift | Visual stability | <= 0.1 | <= 0.25 | > 0.25 |

- A page passes only when **all three** metrics are in the "good" range at the **75th percentile** of real-user (field) data.
- Thresholds are evaluated per metric, segmented by device class (mobile vs. desktop).

## Requirements

- Core Web Vitals **MUST** be measured in the **field at p75** (RUM), not solely in lab tools — lab single-runs do not represent the percentile distribution real users experience.
- A **performance budget MUST be enforced in CI** so regressions fail the build rather than reaching production.
- Lab tooling (Lighthouse, DevTools) **SHOULD** be used for diagnosis and pre-merge gating, with field data as the authoritative pass/fail signal.
- Layout-shift-prone elements (images, ads, embeds, late-injected banners) **MUST** reserve space via explicit `width`/`height` or `aspect-ratio` to protect CLS.

## INP is usually the hardest to pass

INP captures the worst (near-worst) interaction latency across the page's lifetime, so a single janky handler fails it. Mitigations, in order of leverage:

- **Break up long tasks** — split work > 50ms into smaller chunks so the main thread can paint and handle input between them.
- **Yield to the main thread.** Prefer `scheduler.yield()` where available — note it is **Chromium-supported but NOT yet Baseline** as of 2026 (limited availability). Provide a fallback: feature-detect and degrade to `await new Promise(r => setTimeout(r))` (loses the prioritized continuation) or the `scheduler-polyfill`.
- **Move heavy computation to a Web Worker** (parsing, diffing, crypto, image work) to keep the main thread free for rendering and input.
- **Avoid layout thrashing** — batch DOM reads then writes; never interleave reads/writes in a loop that forces synchronous reflow.
- **Keep the DOM small** — oversized DOM trees (thousands of nodes) inflate style/layout cost on every interaction. Virtualize long lists.
- **Defer non-critical work** to idle time (`requestIdleCallback`) or post-interaction.

## LCP and CLS quick wins

- **LCP**: preload the LCP image/font, serve responsive images, avoid render-blocking CSS/JS, use `fetchpriority="high"` on the hero image, and prefer server-side rendering for above-the-fold content.
- **CLS**: reserve space for media and dynamic content; avoid inserting content above existing content; use `font-display: optional`/`swap` deliberately and preload fonts to reduce reflow.

## Measurement and CI enforcement

- Collect field data via the **`web-vitals` JavaScript library** (reports LCP, INP, CLS using the attribution build for debugging) or the Chrome User Experience Report (CrUX).
- Wire a CI gate such as **Lighthouse CI** (`lhci autorun`) with assertions on metric thresholds and resource/byte budgets defined in a `budget.json`.
- Express budgets as concrete limits (e.g., total JS transfer <= 170KB compressed for the critical path) and fail the build on regression — this turns performance into a `tight-feedback-loop` and a `support-automation` boundary rather than a manual review step.

## Notes

- Treating Core Web Vitals as a deliberate, budgeted constraint (not an after-the-fact audit) is the durable practice; specific thresholds are reviewed periodically by the Chrome team, so pin to the dated thresholds above and re-verify against `web.dev/articles/vitals/`.
