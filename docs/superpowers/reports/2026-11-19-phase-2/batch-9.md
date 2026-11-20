# Phase 2 batch 9 report

Sixteen topics under `cookbook/guidelines/implementing/ui/` converted to roled parts. Format only: no research, no new rules, no rule's substance changed. Every topic passes `cookr roles lossless --base 0005775 --draft` and `cookr roles check`, was bumped, and printed `RESULT: APPROVED` from `approve.py`. No `judged` records were written.

| Topic | Commit | Rules | Moved | Obsolete |
|---|---|---|---|---|
| `high-dpi-display-scaling` | 1ce3cdc7 | 3 | 3 | 0 |
| `iconography` | 69e9653f | 7 | 8 | 0 |
| `layout` | 3cea24d2 | 12 | 15 | 0 |
| `material3-theming` | 0b36c80f | 18 | 9 | 0 |
| `modern-css` | e2b001c3 | 25 | 20 | 0 |
| `platform-design-languages` | 4019687d | 9 | 9 | 0 |
| `previews` | 10883c8f | 6 | 2 | 0 |
| `progressive-web-app` | 88cb260f | 23 | 16 | 0 |
| `spacing` | 9f6beb6d | 4 | 3 | 0 |
| `state-design` | e30fd04c | 11 | 12 | 0 |
| `theming` | 837dee41 | 4 | 4 | 0 |
| `theming-with-tokens` | a312406a | 19 | 27 | 0 |
| `touch-click-targets` | 6ac854ef | 6 | 7 | 0 |
| `typography` | 95cb3329 | 9 | 10 | 0 |
| `visual-hierarchy` | 532abf09 | 7 | 2 | 0 |
| `windows-11-materials` | ff5f5f79 | 14 | 4 | 0 |

## high-dpi-display-scaling

**Promoted**:

- "For custom rendering (Win2D, Direct3D interop), query `XamlRoot.RasterizationScale` and listen for `RasterizationScaleChanged`" → `should-track-rasterization-scale-for-custom-rendering`: "For custom rendering (Win2D, Direct3D interop), SHOULD query `XamlRoot.RasterizationScale` and listen for `RasterizationScaleChanged`."

**Bars**: `look-for` (review-focus) **authored**; `a-complete-review-must-establish` (review-bar) **authored**; `a-build-must-establish` (build-bar) **authored**. The topic held no reviewer text to move.

**Contradictions (R4, left unfixed)**: none.

**Unfinished**: none.

## iconography

**Promoted**:

- "Icons supplement text — they do not replace it (except for universally understood symbols like play, pause, close, and search)." → `should-not-replace-text-with-icons`: "Icons SHOULD supplement text and SHOULD NOT replace it (except for universally understood symbols like play, pause, close, and search)."
- "Maintain consistent size and weight across the UI — don't mix outlined and filled styles" → `should-keep-icon-size-and-weight-consistent`: "SHOULD maintain consistent size and weight across the UI."
- "Maintain consistent size and weight across the UI — don't mix outlined and filled styles without intention (e.g., filled = selected, outlined = unselected)" → `should-not-mix-outlined-and-filled-without-intention`: "SHOULD NOT mix outlined and filled styles without intention (e.g., filled = selected, outlined = unselected)."
- "Minimum icon size: 16x16pt for decorative, 24x24pt for interactive (see Touch & Click Targets for the full hit area)" → `should-meet-minimum-icon-size`: "Icons SHOULD be at least the minimum icon size: 16x16pt for decorative, 24x24pt for interactive (see Touch & Click Targets for the full hit area)."

**Bars**: `look-for` (review-focus) **authored**; `a-complete-review-must-establish` (review-bar) **authored**; `a-build-must-establish` (build-bar) **authored**. The topic held no reviewer text to move.

**Contradictions (R4, left unfixed)**: none.

**Notes**:

- Added a `references` part; its first line is the base's `References:` lead-in, kept verbatim (a base sentence cannot be obsolete, and a lead-in may map only to rules).

**Unfinished**: none.

## layout

**Promoted**:

- "Design for the content, not a fixed screen size." → `should-design-for-content-not-screen-size`: "SHOULD design for the content, not a fixed screen size."
- "Layouts should adapt gracefully from compact to expanded contexts." → `should-adapt-from-compact-to-expanded`: "Layouts SHOULD adapt gracefully from compact to expanded contexts."
- "**Single-column by default** — multi-column only when content density justifies it and screen width supports it" → `should-default-to-single-column`: "Single-column by default — SHOULD use multi-column only when content density justifies it and screen width supports it."
- "**Content-first** — decide what information the user needs, then choose a layout." → `should-decide-content-before-layout`: "Content-first — SHOULD decide what information the user needs, then choose a layout."
- "Don't start with a grid and fill it." → `should-not-start-with-a-grid`: "Don't start with a grid and fill it — a layout SHOULD NOT begin as a grid to be filled."
- "**Consistent alignment** — pick a leading edge and stick to it. Mixed alignment creates visual noise." → `should-keep-consistent-alignment`: "Consistent alignment — SHOULD pick a leading edge and stick to it. Mixed alignment creates visual noise."
- "**Scroll direction** — one primary scroll direction per view." → `should-keep-one-primary-scroll-direction`: "Scroll direction — SHOULD keep one primary scroll direction per view."

**Bars**: `look-for` (review-focus) **authored**; `a-complete-review-must-establish` (review-bar) **authored**; `a-build-must-establish` (build-bar) **authored**. The topic held no reviewer text to move.

**Contradictions (R4, left unfixed)**: none.

**Notes**:

- "allow denser layouts for productivity/data-heavy tools" was read as permission and named at MAY (`may-allow-denser-layouts-for-productivity-tools`); flag for the judge if it should be SHOULD.

**Unfinished**: none.

## material3-theming

**Promoted**:

- "Generate schemes with the Material Theme Builder rather than hand-authoring every role." → `should-generate-schemes-with-theme-builder`: "SHOULD generate schemes with the Material Theme Builder rather than hand-authoring every role."
- "Read colors at use sites via `MaterialTheme.colorScheme.<role>`." → `should-read-colors-via-color-scheme`: "SHOULD read colors at use sites via `MaterialTheme.colorScheme.<role>`."
- "Treat it as a deliberate decision, not a default — opt in when brand identity allows the OS to drive palette." → `should-treat-dynamic-color-as-deliberate`: "Dynamic color SHOULD be treated as a deliberate decision, not a default — opt in when brand identity allows the OS to drive palette."
- "When brand color fidelity is a hard requirement, prefer a fixed branded scheme over dynamic color." → `should-prefer-fixed-scheme-for-brand-fidelity`: "When brand color fidelity is a hard requirement, SHOULD prefer a fixed branded scheme over dynamic color."
- "Use the M3 type scale roles (`displayLarge` … `labelSmall`) via `MaterialTheme.typography.<role>`." → `should-use-m3-type-scale-roles`: "SHOULD use the M3 type scale roles (`displayLarge` … `labelSmall`) via `MaterialTheme.typography.<role>`."
- "Use the shape scale (`extraSmall` … `extraLarge`) via `MaterialTheme.shapes`." → `should-use-shape-scale`: "SHOULD use the shape scale (`extraSmall` … `extraLarge`) via `MaterialTheme.shapes`."
- "Pin the dependency, e.g." → `should-pin-material3-dependency`: "SHOULD pin the dependency, e.g. `androidx.compose.material3:material3:1.4.x` (stable line as of mid-2026), via the Compose BOM where possible."
- "Default to stable M3 color roles; adopt Expressive only behind a flag, on a pinned alpha, when a concrete UX need justifies the instability." → `should-default-to-stable-m3-color-roles`: "SHOULD default to stable M3 color roles."
- "Default to stable M3 color roles; adopt Expressive only behind a flag, on a pinned alpha, when a concrete UX need justifies the instability." → `should-adopt-expressive-only-behind-a-flag`: "SHOULD adopt Expressive only behind a flag, on a pinned alpha, when a concrete UX need justifies the instability."

**Bars**: `look-for` (review-focus) **authored**; `a-complete-review-must-establish` (review-bar) **authored**; `a-build-must-establish` (build-bar) **authored**. The topic held no reviewer text to move.

**Contradictions (R4, left unfixed)**: none.

**Notes**:

- Deleted the `typography-and-shape-scales` and `dark-theme` parts (all text now in rules). `color-roles-and-colorscheme` became how-to, `dynamic-color-material-you` examples, and `versioning-and-material-3-expressive-forecast` rationale.

**Unfinished**: none.

## modern-css

**Promoted**:

- "Requirements:" → `must-gate-adoption-on-baseline`: "Adoption of a CSS feature **MUST** be gated on its Baseline status, not on a single browser's support or anecdotal "Can I Use" glances."
- "Requirements:" → `may-use-widely-available-without-fallback`: "**Widely available** features **MAY** be used without a fallback."
- "Requirements:" → `should-fallback-for-newly-available`: "**Newly available** features **SHOULD** be used only with a documented fallback or progressive enhancement, because pre-cutoff browser versions still receiving traffic may not support them."
- "Requirements: Pin any Baseline claim to a date — statuses advance over time." → `should-date-baseline-claims`: "SHOULD pin any Baseline claim to a date — statuses advance over time."
- "Requirements: Verify against MDN or the Baseline data before assuming current status." → `should-verify-baseline-status`: "SHOULD verify against MDN or the Baseline data before assuming current status."
- "Author component responsiveness with **container queries** keyed to the component's own size: wrap the component in a query container (`container-type: inline-size`) and use `@container`, so the component adapts wherever it is placed." → `should-use-container-queries-for-components`: "SHOULD author component responsiveness with **container queries** keyed to the component's own size: wrap the component in a query container (`container-type: inline-size`) and use `@container`, so the component adapts wherever it is placed."
- "Use **viewport media queries** only for genuinely page-level concerns (overall page shell, print, `prefers-*` user preferences)." → `should-limit-viewport-media-queries-to-page-level`: "SHOULD use **viewport media queries** only for genuinely page-level concerns (overall page shell, print, `prefers-*` user preferences)."
- "Use **subgrid** to align nested items to an ancestor grid's tracks." → `should-use-subgrid-for-nested-alignment`: "SHOULD use **subgrid** to align nested items to an ancestor grid's tracks."
- "Provide a non-subgrid fallback (explicit tracks) only if you target pre-cutoff versions." → `should-fallback-subgrid-only-for-pre-cutoff`: "SHOULD provide a non-subgrid fallback (explicit tracks) only if you target pre-cutoff versions."
- "Prefer **logical properties** (`margin-inline`, `inset-block`) over physical ones for internationalization-ready layout." → `should-prefer-logical-properties`: "SHOULD prefer **logical properties** (`margin-inline`, `inset-block`) over physical ones for internationalization-ready layout."
- "Define an explicit **`@layer`** order (e.g." → `should-define-explicit-layer-order`: "SHOULD define an explicit **`@layer`** order (e.g. `@layer reset, base, components, utilities`) so cascade precedence is by layer, not by escalating specificity."
- "Import third-party CSS into a low-priority layer to keep it overridable without `!important`." → `should-import-third-party-css-into-low-layer`: "SHOULD import third-party CSS into a low-priority layer to keep it overridable without `!important`."
- "Use **`:has()`** to drive conditional styling from descendant or sibling state instead of toggling classes in JavaScript (e.g." → `should-use-has-for-conditional-styling`: "SHOULD use **`:has()`** to drive conditional styling from descendant or sibling state instead of toggling classes in JavaScript (e.g. `form:has(:invalid)`, `.card:has(> img)`)."
- "Use **native nesting** for co-locating related rules; do not nest deeply — flat, shallow rules stay readable and greppable." → `should-use-native-nesting`: "SHOULD use **native nesting** for co-locating related rules."
- "Use **native nesting** for co-locating related rules; do not nest deeply — flat, shallow rules stay readable and greppable." → `should-not-nest-deeply`: "SHOULD NOT nest deeply — flat, shallow rules stay readable and greppable."
- "Use the **same-document View Transitions API** (`document.startViewTransition`) for animated state/route changes in SPAs." → `should-use-same-document-view-transitions`: "SHOULD use the **same-document View Transitions API** (`document.startViewTransition`) for animated state/route changes in SPAs."
- "Feature-detect with `if (document.startViewTransition) { ... } else { /* apply update directly */ }`." → `should-feature-detect-view-transitions`: "SHOULD feature-detect with `if (document.startViewTransition) { ... } else { /* apply update directly */ }`."
- "Use them as pure progressive enhancement only; never make navigation depend on them." → `should-use-cross-document-transitions-only-as-enhancement`: "SHOULD use cross-document (MPA) View Transitions as pure progressive enhancement only."
- "Use them as pure progressive enhancement only; never make navigation depend on them." → `must-not-make-navigation-depend-on-cross-document-transitions`: "MUST NOT ever make navigation depend on cross-document (MPA) View Transitions."
- "Respect `prefers-reduced-motion: reduce` and disable or shorten transitions accordingly." → `should-respect-reduced-motion`: "SHOULD respect `prefers-reduced-motion: reduce` and disable or shorten transitions accordingly."
- "Do not reach for a CSS-in-JS runtime or a JS animation library when an interoperable native CSS feature covers the need." → `should-not-use-js-runtimes-native-css-covers`: "SHOULD NOT reach for a CSS-in-JS runtime or a JS animation library when an interoperable native CSS feature covers the need."
- "Do not escalate specificity or use `!important` to win the cascade — reach for `@layer` instead." → `should-not-escalate-specificity`: "SHOULD NOT escalate specificity or use `!important` to win the cascade — reach for `@layer` instead."
- "Do not gate a feature solely on `caniuse` percentages without checking Baseline tier and whether your traffic includes pre-cutoff versions." → `should-not-gate-solely-on-caniuse`: "SHOULD NOT gate a feature solely on `caniuse` percentages without checking Baseline tier and whether your traffic includes pre-cutoff versions."

**Bars**: `look-for` (review-focus) **authored**; `a-complete-review-must-establish` (review-bar) **authored**; `a-build-must-establish` (build-bar) **authored**. The topic held no reviewer text to move.

**Contradictions (R4, left unfixed)**: none.

**Notes**:

- Deleted `layout-and-structure`, `cascade-control`, `motion-and-transitions` and `anti-patterns` (all text now in rules); the Baseline definitions and cohort table are how-to; a new `rationale` part names the Baseline rules and carries the word "requirements" for the `Requirements:` lead-in.
- `must-degrade-view-transitions-gracefully`: its subject "It" was written out as "Same-document View Transitions" so the rule stands alone; no change of level or substance.

**Unfinished**: none.

## platform-design-languages

**Promoted**:

- "Defer to these canonical sources before applying the defaults in this file:" → `should-defer-to-canonical-sources`: "SHOULD defer to the canonical sources (Apple Human Interface Guidelines, Material Design 3, Fluent 2 Design System, WCAG 2.1 + platform-appropriate system) before applying the defaults in this file."
- "Use the defaults below to fill gaps or establish a cross-platform baseline." → `should-use-defaults-to-fill-gaps`: "SHOULD use the defaults below to fill gaps or establish a cross-platform baseline."
- "When writing UI ingredients or recipes, refer to these canonical platform design sources." → `should-refer-to-canonical-sources-when-writing-ui`: "When writing UI ingredients or recipes, SHOULD refer to these canonical platform design sources."
- "When specifying spacing, type sizes, or target sizes in an ingredient's Appearance section, defer to the platform HIG." → `should-defer-to-hig-in-appearance-sections`: "When specifying spacing, type sizes, or target sizes in an ingredient's Appearance section, SHOULD defer to the platform HIG."
- "If the platform prescribes a value, use it." → `should-use-the-prescribed-value`: "If the platform prescribes a value, SHOULD use it."
- "When the HIG has no opinion, specify a cross-platform default and note it as such." → `should-note-cross-platform-defaults`: "When the HIG has no opinion, SHOULD specify a cross-platform default and note it as such."
- "In the Platform Notes section of an ingredient, list any platform-specific overrides with links to the relevant HIG section." → `should-list-platform-overrides-in-platform-notes`: "In the Platform Notes section of an ingredient, SHOULD list any platform-specific overrides with links to the relevant HIG section."

**Bars**: `look-for` (review-focus) **authored**; `a-complete-review-must-establish` (review-bar) **authored**; `a-build-must-establish` (build-bar) **authored**. The topic held no reviewer text to move.

**Contradictions (R4, left unfixed)**:

- "Use the defaults below to fill gaps or establish a cross-platform baseline." and "Defer to these canonical sources before applying the defaults in this file:" refer to defaults this topic does not contain.
- "If the platform prescribes a value, use it." (`should-use-the-prescribed-value`, promoted to SHOULD) overlaps, at a weaker level, "When the platform HIG prescribes a specific value…, the platform value MUST be used." (`must-use-platform-prescribed-values`)

**Notes**:

- Deleted `introduction` and `how-this-applies`; the intro keeps the lead-in and the canonical-source links. The bars say "the artifact" instead of "the code", since this topic governs writing UI guidance.

**Unfinished**: none.

## previews

**Promoted**:

- "Previews should cover all significant states (default, loading, error, empty, populated)." → `should-cover-significant-states`: "Previews SHOULD cover all significant states (default, loading, error, empty, populated)."
- "Verification includes confirming previews render without crashes." → `should-verify-swiftui-previews-render`: "Verification SHOULD include confirming SwiftUI previews render without crashes."
- "Verification includes confirming preview functions compile." → `should-verify-compose-previews-compile`: "Verification SHOULD include confirming Compose preview functions compile."

**Bars**: `look-for` (review-focus) **authored**; `a-complete-review-must-establish` (review-bar) **authored**; `a-build-must-establish` (build-bar) **authored**. The topic held no reviewer text to move.

**Contradictions (R4, left unfixed)**: none.

**Notes**:

- Deleted the `swift` and `kotlin` parts; the intro is kept verbatim.

**Unfinished**: none.

## progressive-web-app

**Promoted**:

- "If installability is not a requirement, do not add a service worker for its own sake (YAGNI)." → `should-not-add-service-worker-without-installability`: "If installability is not a requirement, SHOULD NOT add a service worker for its own sake (YAGNI)."
- "Include a `maskable` icon for adaptive shaping." → `should-include-maskable-icon`: "SHOULD include a `maskable` icon for adaptive shaping."
- "Validate against Lighthouse / DevTools Application panel before shipping; do not hand-assert installability." → `should-validate-installability-with-tools`: "SHOULD validate against Lighthouse / DevTools Application panel before shipping, and SHOULD NOT hand-assert installability."
- "Register the service worker after the page loads and choose a caching strategy per request class — **do not** apply one strategy globally:" → `should-register-service-worker-after-load`: "SHOULD register the service worker after the page loads."
- "Register the service worker after the page loads and choose a caching strategy per request class — **do not** apply one strategy globally:" → `should-choose-caching-strategy-per-request-class`: "SHOULD choose a caching strategy per request class — **do not** apply one strategy globally."
- "Precache the app shell so navigations resolve offline." → `should-precache-app-shell`: "SHOULD precache the app shell so navigations resolve offline."
- "Prefer a maintained library (Workbox) over hand-rolled fetch handlers unless the surface is trivial — this is a deliberate trade for correctness on edge cases (range requests, opaque responses), not a mandate." → `should-prefer-maintained-service-worker-library`: "SHOULD prefer a maintained library (Workbox) over hand-rolled fetch handlers unless the surface is trivial — this is a deliberate trade for correctness on edge cases (range requests, opaque responses), not a mandate."
- "As of iOS 18 / Safari 18 the following hold; re-verify per release:" → `should-reverify-ios-constraints-per-release`: "The iOS / Safari constraints hold as of iOS 18 / Safari 18; SHOULD re-verify them per release."
- "**Background Sync / Periodic Background Sync are unavailable.** Do not depend on them; queue writes in IndexedDB and flush on next foreground." → `should-not-depend-on-background-sync`: "SHOULD NOT depend on Background Sync / Periodic Background Sync."
- "**Background Sync / Periodic Background Sync are unavailable.** Do not depend on them; queue writes in IndexedDB and flush on next foreground." → `should-queue-writes-in-indexeddb`: "SHOULD queue writes in IndexedDB and flush on next foreground."
- "Treat all client storage as a cache, never as the source of truth." → `must-treat-client-storage-as-cache`: "All client storage MUST be treated as a cache, never as the source of truth."
- "Web Push availability has been subject to EU regulatory variation (iOS 17.4+); confirm behavior in target regions rather than assuming uniform support. (FORECAST: regional policy continues to evolve.)" → `should-confirm-push-in-target-regions`: "Web Push availability has been subject to EU regulatory variation (iOS 17.4+); SHOULD confirm behavior in target regions rather than assuming uniform support."

**Bars**: `look-for` (review-focus) **authored**; `a-complete-review-must-establish` (review-bar) **authored**; `a-build-must-establish` (build-bar) **authored**. The topic held no reviewer text to move.

**Contradictions (R4, left unfixed)**:

- "MUST include, at minimum:" lists the maskable icon, whose own wording reads as SHOULD (`should-include-maskable-icon`). The two levels conflict.

**Notes**:

- Deleted `installability-criteria`; `service-worker-and-caching` is how-to (table only), `verification` stays how-to, not a bar, and the iOS part is rationale (facts only). "expect a tight Cache API quota" stays a rationale fact, not a rule.
- The maskable icon sat inside the base's "MUST include, at minimum:" list, but its own wording ("Include a maskable icon…") was read as SHOULD (`should-include-maskable-icon`). Flag for the judge: it may be meant as MUST.

**Unfinished**: none.

## spacing

**Promoted**:

- "Use a consistent spatial scale based on a **4px base unit** (8px primary grid)." → `should-use-4px-spatial-scale`: "SHOULD use a consistent spatial scale based on a **4px base unit** (8px primary grid)."
- "If a value isn't on the scale, reconsider." → `should-reconsider-off-scale-values`: "If a value isn't on the scale, SHOULD reconsider it."

**Bars**: `look-for` (review-focus) **authored**; `a-complete-review-must-establish` (review-bar) **authored**; `a-build-must-establish` (build-bar) **authored**. The topic held no reviewer text to move.

**Contradictions (R4, left unfixed)**: none.

**Notes**:

- New `spacing-scale` part (how-to) holds the scale list; a `references` part was added.

**Unfinished**: none.

## state-design

**Promoted**:

- "**Loading** — show progress (see `[adc.guideline.implementing.ui.always-show-progress](cookbook:8d52028b-d358-4965-93a1-030fc8405068)`)." → `should-show-progress-while-loading`: "Loading — SHOULD show progress (see `[adc.guideline.implementing.ui.always-show-progress](cookbook:8d52028b-d358-4965-93a1-030fc8405068)`)."
- "Use skeleton screens for content-heavy views, spinners for actions." → `should-use-skeletons-and-spinners`: "SHOULD use skeleton screens for content-heavy views, spinners for actions."
- "Never block the entire screen for a partial load." → `must-not-block-screen-for-partial-load`: "MUST NOT ever block the entire screen for a partial load."
- "**Empty** — explain what belongs here, why it's empty, and provide a single clear action to populate it." → `should-explain-empty-state`: "Empty — SHOULD explain what belongs here, why it's empty, and provide a single clear action to populate it."
- "Use an icon or illustration, a brief message, and a CTA button." → `should-compose-empty-state`: "SHOULD use an icon or illustration, a brief message, and a CTA button."
- "**Error** — identify the problem, explain why if possible, and offer a recovery action (retry, go back, contact support)." → `should-explain-errors-with-recovery`: "Error — SHOULD identify the problem, explain why if possible, and offer a recovery action (retry, go back, contact support)."
- "Don't blame the user." → `should-not-blame-the-user`: "Don't blame the user — error text SHOULD NOT blame the user."
- "Design empty and error states with the same care as the loaded state — they are often the user's first impression." → `should-design-empty-and-error-with-care`: "SHOULD design empty and error states with the same care as the loaded state — they are often the user's first impression."

**Bars**: `look-for` (review-focus) **authored**; `a-complete-review-must-establish` (review-bar) **authored**; `a-build-must-establish` (build-bar) **authored**. The topic held no reviewer text to move.

**Contradictions (R4, left unfixed)**: none.

**Notes**:

- The four state names stay as a how-to part (`the-four-states`) under the verbatim `**The four states:**` lead-in; the links are a `references` part. Both intro MUST sentences stay verbatim in the intro and are also rules.

**Unfinished**: none.

## theming

**Promoted**:

- "Set app-level theme via `Application.RequestedTheme`, override per-element with `FrameworkElement.RequestedTheme`" → `should-set-theme-at-app-and-element-level`: "SHOULD set app-level theme via `Application.RequestedTheme`, override per-element with `FrameworkElement.RequestedTheme`"
- "Define custom theme-aware colors in a `ResourceDictionary` with `Default`/`Light`/`Dark` theme dictionaries" → `should-define-theme-dictionaries`: "SHOULD define custom theme-aware colors in a `ResourceDictionary` with `Default`/`Light`/`Dark` theme dictionaries"

**Bars**: `look-for` (review-focus) **authored**; `a-complete-review-must-establish` (review-bar) **authored**; `a-build-must-establish` (build-bar) **authored**. The topic held no reviewer text to move.

**Contradictions (R4, left unfixed)**: none.

**Notes**:

- The intro keeps its one-line statement; the XAML Good/Bad sample is an `examples` part.

**Unfinished**: none.

## theming-with-tokens

**Promoted**:

- "Keep three tiers so themes only rebind the middle one:" → `should-keep-three-token-tiers`: "SHOULD keep three tiers (primitive, semantic, component) so themes only rebind the middle one."
- "Resolve tokens at a single boundary: a CSS custom-property scope (`:root[data-theme]`, `@media (prefers-color-scheme)`), a SwiftUI `Environment`/asset catalog, a Compose `MaterialTheme`/`CompositionLocal`, or a WinUI `ResourceDictionary` theme dictionary." → `should-resolve-tokens-at-a-single-boundary`: "SHOULD resolve tokens at a single boundary: a CSS custom-property scope (`:root[data-theme]`, `@media (prefers-color-scheme)`), a SwiftUI `Environment`/asset catalog, a Compose `MaterialTheme`/`CompositionLocal`, or a WinUI `ResourceDictionary` theme dictionary."
- "A missing key is a defect — fail fast in a build/test check rather than falling back silently." → `should-fail-fast-on-a-missing-token`: "A missing key is a defect — SHOULD fail fast in a build/test check rather than falling back silently."
- "Under forced-colors / Windows High Contrast, defer to system colors; do not override them." → `should-defer-to-system-colors-under-forced-colors`: "Under forced-colors / Windows High Contrast, SHOULD defer to system colors and SHOULD NOT override them."
- "Automate this against the value sets in CI; do not eyeball it." → `should-automate-contrast-checks-in-ci`: "SHOULD automate this (the per-theme contrast check) against the value sets in CI; SHOULD NOT eyeball it."
- "Pin the token spec: align names/types to the W3C Design Tokens Community Group Format Module, whose first stable version is **2025.10** (designtokens.org)." → `should-align-tokens-to-dtcg-format`: "SHOULD pin the token spec: align names/types to the W3C Design Tokens Community Group Format Module, whose first stable version is **2025.10** (designtokens.org)."
- "It continues to evolve, so pin to a dated revision and isolate the parser/build step so a spec update is a localized change." → `should-pin-dated-spec-revision-and-isolate-parser`: "The spec continues to evolve, so SHOULD pin to a dated revision and isolate the parser/build step so a spec update is a localized change."
- "Adopt a token build pipeline (e.g., Style Dictionary) only when measured need justifies it — a small" → `should-adopt-token-pipeline-only-on-measured-need`: "SHOULD adopt a token build pipeline (e.g., Style Dictionary) only when measured need justifies it."
- "Adopt a token build pipeline (e.g., Style Dictionary) only when measured need justifies it — a small app may hand-author per-platform value sets (per YAGNI)." → `may-hand-author-value-sets-in-small-apps`: "A small app MAY hand-author per-platform value sets (per YAGNI)."

**Bars**: `look-for` (review-focus) **authored**; `a-complete-review-must-establish` (review-bar) **authored**; `a-build-must-establish` (build-bar) **authored**. The topic held no reviewer text to move.

**Contradictions (R4, left unfixed)**: none.

**Notes**:

- Deleted `switching-the-active-set`, `respect-the-system-and-accessibility-settings`, `verify-contrast-per-theme` and `notes` (all text now in rules or references); the tier table stays as how-to.
- Two base sentences each carry two keywords and were kept as one rule each, so no keyword is split from its clause: `must-honor-os-theme-by-default` (MUST honor + SHOULD offer an override, wrapped at the base's own line breaks so it is verbatim) and `must-respond-to-system-contrast-signal` ("Provide a high-contrast / increase-contrast theme", promoted to SHOULD, + MUST respond).

**Unfinished**: none.

## touch-click-targets

**Promoted**:

- "Defer to the platform HIG first — each prescribes its own minimum:" → `should-defer-to-platform-hig-minimum`: "SHOULD defer to the platform HIG first — each prescribes its own minimum (see the platform minimums table)."
- "**Cross-platform default: 44x44** when no platform HIG applies." → `should-default-to-44x44`: "**Cross-platform default: 44x44** when no platform HIG applies — targets SHOULD be at least 44x44 then."
- "The visual element (icon, text) can be smaller than the touch target — pad the hit area" → `should-pad-hit-area-beyond-visual`: "The visual element (icon, text) MAY be smaller than the touch target — the hit area SHOULD then be padded to the target size."
- "Inline text links in paragraphs are exempt from size minimums but should have sufficient line height for comfortable tapping" → `should-give-inline-links-line-height`: "Inline text links in paragraphs are exempt from size minimums but SHOULD have sufficient line height for comfortable tapping."

**Bars**: `look-for` (review-focus) **authored**; `a-complete-review-must-establish` (review-bar) **authored**; `a-build-must-establish` (build-bar) **authored**. The topic held no reviewer text to move.

**Contradictions (R4, left unfixed)**: none.

**Notes**:

- The platform-minimum table is a how-to part; the accessibility cross-link and the links are a `references` part. "The visual element (icon, text) can be smaller … — pad the hit area" carries two levels: "can be smaller" is MAY and "pad the hit area" is SHOULD, kept in one rule (`should-pad-hit-area-beyond-visual`).

**Unfinished**: none.

## typography

**Promoted**:

- "Establish a type scale with clear roles — don't invent sizes ad-hoc." → `should-establish-type-scale-with-roles`: "SHOULD establish a type scale with clear roles — SHOULD NOT invent sizes ad-hoc (don't invent sizes ad-hoc)."
- "Defaults when no design system exists: **Body text**: 14-17pt (16px is the safest cross-platform default)" → `should-default-body-text-to-14-17pt`: "Defaults when no design system exists — **Body text** SHOULD be 14-17pt (16px is the safest cross-platform default)."
- "**Line height**: 1.4x-1.5x font size for body text" → `should-set-body-line-height-1-4-to-1-5`: "Defaults when no design system exists — **Line height** SHOULD be 1.4x-1.5x font size for body text."
- "**Heading scale**: Use the platform's built-in type scale (Dynamic Type, Material type tokens, Fluent type ramp) rather than inventing sizes" → `should-use-platform-heading-scale`: "Defaults when no design system exists — **Heading scale**: SHOULD use the platform's built-in type scale (Dynamic Type, Material type tokens, Fluent type ramp) rather than inventing sizes."
- "General principles: Limit to 2-3 font weights per screen (regular, medium/semibold, bold)" → `should-limit-font-weights-per-screen`: "General principles — SHOULD limit to 2-3 font weights per screen (regular, medium/semibold, bold)."
- "General principles: Paragraph width: 45-75 characters for comfortable reading" → `should-keep-paragraph-width-45-75-characters`: "General principles — **Paragraph width** SHOULD be 45-75 characters for comfortable reading."

**Bars**: `look-for` (review-focus) **authored**; `a-complete-review-must-establish` (review-bar) **authored**; `a-build-must-establish` (build-bar) **authored**. The topic held no reviewer text to move.

**Contradictions (R4, left unfixed)**: none.

**Notes**:

- The system-font list keeps its `Platform system fonts:` lead-in verbatim in a how-to part. The `Defaults when no design system exists:` and `General principles:` lead-ins are carried as prefixes on the rules they introduce, so each rule keeps its scope.

**Unfinished**: none.

## visual-hierarchy

**Promoted**:

- "Establish clear importance through size, weight, color, and spacing." → `should-establish-importance-through-visual-weight`: "SHOULD establish clear importance through size, weight, color, and spacing."
- "Every screen should have one obvious focal point — the primary action or content the user came for." → `should-have-one-obvious-focal-point`: "Every screen SHOULD have one obvious focal point — the primary action or content the user came for."
- "Use size and weight (not just color) to distinguish heading levels" → `should-distinguish-headings-by-size-and-weight`: "SHOULD use size and weight (not just color) to distinguish heading levels."
- "Group related content with proximity; separate unrelated content with whitespace" → `should-group-by-proximity`: "SHOULD group related content with proximity and separate unrelated content with whitespace."

**Bars**: `look-for` (review-focus) **authored**; `a-complete-review-must-establish` (review-bar) **authored**; `a-build-must-establish` (build-bar) **authored**. The topic held no reviewer text to move.

**Contradictions (R4, left unfixed)**: none.

**Notes**:

- The intro statement stays verbatim and is also two rules; the cross-link and links are a `references` part.

**Unfinished**: none.

## windows-11-materials

**Promoted**:

- "**win32-and-wpf**: For Win32/WPF hosts, follow the platform-specific "Apply Mica in Win32 desktop apps" path rather than assuming the WinUI API surface." → `win32-and-wpf`: "For Win32/WPF hosts, SHOULD follow the platform-specific "Apply Mica in Win32 desktop apps" path rather than assuming the WinUI API surface."
- "Using Acrylic as a full-window backdrop for a long-lived window (use Mica — Acrylic's real-time blur wastes power)." → `should-not-use-acrylic-as-long-lived-backdrop`: "Using Acrylic as a full-window backdrop for a long-lived window SHOULD NOT be done (use Mica — Acrylic's real-time blur wastes power)."
- "Re-enabling transparency or material after the system fell back to solid color." → `should-not-reenable-material-after-fallback`: "Re-enabling transparency or material after the system fell back to solid color SHOULD NOT be done."
- "Layering material on a single control instead of the window backdrop." → `should-not-layer-material-on-a-single-control`: "Layering material on a single control instead of the window backdrop SHOULD NOT be done."

**Bars**: `look-for` (review-focus) **authored**; `a-complete-review-must-establish` (review-bar) **authored**; `a-build-must-establish` (build-bar) **authored**. The topic held no reviewer text to move.

**Contradictions (R4, left unfixed)**:

- Anti-pattern "Re-enabling transparency or material after the system fell back to solid color." (`should-not-reenable-material-after-fallback`, SHOULD NOT) restates `honor-system-fallback`: "Code **MUST NOT** force material when the system disables it." at a weaker level.
- Anti-pattern "Layering material on a single control instead of the window backdrop." (`should-not-layer-material-on-a-single-control`, SHOULD NOT) restates `one-backdrop-per-window`: "…**MUST NOT** apply backdrop material to an individual UI element" at a weaker level.

**Notes**:

- Kept the base's existing rule names (`mica-for-long-lived-windows`, …) rather than renaming them; deleted the four section parts, gathering their bullets into one `rules` part. `use-systembackdrop` opens with the unkeyed imperative "Set the material declaratively via … `SystemBackdrop`", kept verbatim beside its own SHOULD.

**Unfinished**: none.

## Findings about `cookr roles lossless`

- A sentence of the topic's base can never be `obsolete`; obsolete is only for folded copies. Every lossless.json in this batch has `"obsolete": []`.
- A bare lead-in ending in ":" (such as `References:`) may map only to rules. Where the lead-in introduces links, it was kept verbatim as the first line of the `references` part, which needs no entry.
- Bold keyword markers (`**MUST**`) are not normalized, so a rule keeps the base's bold to stay verbatim.
- A reworded clause must keep every RFC keyword it held; a base line that carries two keywords was kept in one rule rather than split across two.

## Unfinished

Nothing.
