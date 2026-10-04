
- Core Web Vitals **MUST** be measured in the **field at p75** (RUM), not solely in lab tools — lab single-runs do not represent the percentile distribution real users experience.
- A **performance budget MUST be enforced in CI** so regressions fail the build rather than reaching production.
- Lab tooling (Lighthouse, DevTools) **SHOULD** be used for diagnosis and pre-merge gating, with field data as the authoritative pass/fail signal.
- Layout-shift-prone elements (images, ads, embeds, late-injected banners) **MUST** reserve space via explicit `width`/`height` or `aspect-ratio` to protect CLS.

