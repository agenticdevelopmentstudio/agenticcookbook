# Phase 2 batch 8 report

Twenty UI guideline topics under `cookbook/guidelines/implementing/ui/` were converted to roled parts, one commit per topic. This was a format change only. No research, rules or subject matter was added, and no rule's substance changed. In every topic, `cookr roles lossless --base 0005775 --draft` and `cookr roles check` exit 0, and `approve.py` prints `RESULT: APPROVED`. No topic uses an `obsolete` entry, and no `judged` record was written.

| Topic | Commit | Rules | Moved | Obsolete |
|---|---|---|---|---|
| `always-show-progress` | `9d48c7af` | 3 | 4 | 0 |
| `android-edge-to-edge` | `d0bc9848` | 16 | 16 | 0 |
| `android-navigation` | `e9392bc3` | 15 | 7 | 0 |
| `android-predictive-back` | `b149306a` | 14 | 9 | 0 |
| `animation-motion` | `b576913a` | 6 | 2 | 0 |
| `appkit-and-uikit-patterns` | `42b6653b` | 17 | 2 | 0 |
| `apple-liquid-glass-and-widgets` | `12a59420` | 14 | 1 | 0 |
| `color` | `27d33da9` | 6 | 4 | 0 |
| `compose-performance-and-stability` | `2fd57412` | 17 | 19 | 0 |
| `compose-side-effects` | `fd34c516` | 12 | 3 | 0 |
| `compose-state-and-udf` | `46b66302` | 17 | 8 | 0 |
| `core-web-vitals` | `0010cd03` | 19 | 14 | 0 |
| `cross-platform-token-adaptation` | `c060b878` | 16 | 5 | 0 |
| `dashboard-service-is-display-only` | `d6d221cc` | 2 | 2 | 0 |
| `data-display` | `e854c21a` | 8 | 10 | 0 |
| `design-time-data` | `ad86e9b3` | 3 | 5 | 0 |
| `design-token-distribution` | `72b2e153` | 15 | 9 | 0 |
| `feedback-patterns` | `7fdc5752` | 10 | 9 | 0 |
| `fluent-design` | `b7c47455` | 5 | 3 | 0 |
| `form-design` | `b61f8099` | 16 | 21 | 0 |

## What the tools required, beyond the brief

- **A topic's own base text can never be `obsolete`.** The tool's refusal reads "a sentence of the topic's own base is never obsolete". So `References:` is kept verbatim at the top of each `references` part. Old `###` sub-headings (form-design) map to a rule that carries their word, or to a short `rationale` part that names the rules they grouped.
- **Lead-ins (sentences ending in `:`) map only to rules**, never to parts. In core-web-vitals, the INP lead-in "Mitigations, in order of leverage:" is kept verbatim in a `rationale` part, followed by the mitigation rules' names in their original order.
- **One sentence holding both MUST and SHOULD cannot be split across two rules** ("the matched clause drops its SHOULD"). Such a sentence stays verbatim, either in the intro (android-predictive-back) or inside one rule. A promoted "X; never Y" bullet becomes one rule carrying both levels (core-web-vitals `must-avoid-layout-thrashing`, form-design `must-not-signal-errors-by-color-alone`).
- **The tool reads keyword-like words.** "required" is read as MUST: feedback-patterns' "No user action required." was refused at SHOULD, so it is MUST. A moved rule must also hold at least 80% of the source's content words. That is why some rules keep the original phrase as a tail, for example "— never tune against them" or "— don't blame the user".
- **Hard-wrapped bullets are split at the line break**, so one sentence can need two `moved` entries (data-display, feedback-patterns, form-design).
- **The intro keeps a statement right after the H1** for `GF-01`. Where that statement is itself an instruction, it stays in the intro and is also restated as a promoted rule.
- **FM-13 respellings:** no topic in this batch holds "placeholder", "TODO", "TBD" or "FIXME" as a marker, and none was respelled. form-design keeps "placeholder" as the source has it.
- `cookr bump` wrote a `versions/<old>/` snapshot in each folder, and each snapshot is committed with its topic.

## cookbook/guidelines/implementing/ui/always-show-progress

Commit `9d48c7af`, 3 rules, 4 moved, 0 obsolete.

promoted: none (all MUST/MUST NOT in source). Lead-in "When the UI is waiting on an async task:" now in each rule; intro keeps "When the UI is waiting on an async task, it shows progress." for GF-01.
bars: all three authored. contradictions: none.

unfinished: none.

## cookbook/guidelines/implementing/ui/android-edge-to-edge

Commit `d0bc9848`, 16 rules, 16 moved, 0 obsolete.

promoted:
- "For backward compatibility on Android 14 (API 34) and below, call `enableEdgeToEdge()` in `onCreate()` so behavior is consistent across versions." -> should-enable-edge-to-edge-in-oncreate "... apps SHOULD call `enableEdgeToEdge()` ..."
- "Prefer the `safeDrawing` inset type for general content; ..." -> should-prefer-safedrawing-insets "Apps SHOULD prefer the `safeDrawing` inset type ..."
- "Wrap top-level UI in `Scaffold`; ..." -> should-wrap-top-level-ui-in-scaffold "In Jetpack Compose, top-level UI SHOULD be wrapped in `Scaffold`; ..."
- "**Apply that padding** — ignoring it reintroduces the bug." -> should-apply-scaffold-inner-padding "Apps SHOULD **apply that padding** (the `Scaffold`'s `innerPadding`) — ignoring it reintroduces the bug." (bold emphasis could be read as MUST; judge to check)
- "For manual control, use `Modifier.windowInsetsPadding(...)` with the right inset type:" -> should-use-windowinsetspadding-for-manual-control "For manual control in Jetpack Compose, apps SHOULD use ..."
- "Let content scroll **edge to edge** but pad the interactive/last items, ..." -> should-pad-items-not-whole-list "Content SHOULD scroll **edge to edge** with the interactive/last items padded, ..."
- "Set a listener on the relevant view and consume insets:" -> should-consume-insets-with-view-listener "In Android Views, apps SHOULD set a listener on the relevant view and consume insets."
- "Use `WindowInsetsCompat.Type.ime()` for keyboard-aware layouts; do not hardcode bottom padding." -> should-use-ime-insets-for-keyboard "Apps SHOULD use `WindowInsetsCompat.Type.ime()` for keyboard-aware layouts and SHOULD NOT hardcode bottom padding."
- "For Android 10 (API 29) and below, call `ViewGroupCompat.installCompatInsetsDispatch(rootView)` ..." -> should-install-compat-insets-dispatch "... apps SHOULD call ..."
- "... `AppBarLayout` does not — add `android:fitsSystemWindows=\"true\"` for its top inset." -> should-set-fitssystemwindows-on-appbarlayout "... apps SHOULD add ..."
- "Test in both gesture and 3-button navigation, with a display cutout, and with the keyboard open." -> should-test-navigation-modes-cutout-and-keyboard "Apps SHOULD be tested in both gesture and 3-button navigation, ..."
bars: all three authored.
contradictions: "Apps **MUST NOT** depend on it." (why-this-matters, on the opt-out attribute) vs "Treat it only as a one-release emergency stopgap, if at all." (core requirements) -- the first forbids any dependency, the second allows a one-release stopgap. Both kept in must-not-rely-on-opt-out-attribute, unfixed.

unfinished: none.

## cookbook/guidelines/implementing/ui/android-navigation

Commit `e9392bc3`, 15 rules, 7 moved, 0 obsolete.

Intro kept verbatim (its summary imperatives are covered by must-use-single-activity, must-use-serializable-route-types, should-hoist-navcontroller-to-top).
promoted:
- "Use the stable type-safe APIs in `androidx.navigation:navigation-compose` (...)" -> should-use-stable-type-safe-navigation-apis "Apps SHOULD use the stable type-safe APIs in ..."
- "Build the graph with the type-safe builders and navigate by passing a route instance:" -> should-build-graph-with-type-safe-builders "Apps SHOULD build the graph with the type-safe builders and navigate by passing a route instance."
- "Pin a current `1.x` release before relying on it; ... so treat specific surface details as evolving (FORECAST) and re-check the release notes." -> should-pin-nav3-and-recheck-release-notes "Apps SHOULD pin a current `1.x` release of `androidx.navigation3` before relying on it; ... so apps SHOULD treat specific surface details as evolving (FORECAST) and re-check the release notes."
- "Choose Nav3 as a **deliberate decision** when ..." -> should-choose-nav3-deliberately "Nav3 SHOULD be chosen as a **deliberate decision** when ..."
- "Do **NOT** mix Nav2 `NavHost` and Nav3 `NavDisplay` for the same flow; ..." -> should-not-mix-nav2-and-nav3-in-a-flow "Apps SHOULD **NOT** mix ..." (emphasised "Do NOT" read as a plain imperative, SHOULD NOT; a judge may read it as MUST NOT)
- "Use a single `startDestination`; avoid clearing and rebuilding the entire graph to navigate — prefer ..." -> should-use-single-start-destination "Apps SHOULD use a single `startDestination` and SHOULD avoid clearing and rebuilding ..."
bars: all three authored. contradictions: none.

unfinished: none.

## cookbook/guidelines/implementing/ui/android-predictive-back

Commit `b149306a`, 14 rules, 9 moved, 0 obsolete.

The intro's summary sentence ("Apps MUST migrate off ... and SHOULD drive in-app transitions from the gesture's progress.") stays in intro verbatim: `roles lossless` refuses mapping one MUST+SHOULD sentence to two rules ("the matched clause drops its SHOULD"). Its two requirements are also carried by must-not-rely-on-deprecated-back-apis / must-register-onbackpressedcallback and should-animate-with-the-gesture.
promoted:
- "Prefer the AndroidX `androidx.activity` APIs over the platform `OnBackInvokedCallback` — ..." -> should-prefer-androidx-back-apis "Apps SHOULD prefer the AndroidX ..."
- "Use the platform `OnBackInvokedCallback` directly ONLY when you have no AndroidX dependency." -> should-use-platform-callback-only-without-androidx "Apps SHOULD use the platform `OnBackInvokedCallback` directly ONLY when you have no AndroidX dependency."
- "Keep callbacks single-responsibility: one callback per back-consuming UI state, ordered by registration." -> should-keep-callbacks-single-responsibility "Callbacks SHOULD be kept single-responsibility: ..."
- "Set it `true` (or omit it where the default is on) to receive system animations." -> should-enable-back-flag-for-system-animations "Apps SHOULD set `android:enableOnBackInvokedCallback` `true` (or omit it where the default is on) to receive system animations."
- "Pin the exact behavior to your `targetSdk` and re-check the linked doc before shipping — do not assume a fixed default across versions." -> should-pin-back-behavior-to-targetsdk "Apps SHOULD pin the exact behavior to your `targetSdk` and re-check the linked doc before shipping, and SHOULD NOT assume a fixed default across versions."
- "Compose: use `PredictiveBackHandler`, ... Commit the navigation when the flow completes; reset UI on `CancellationException` (gesture cancelled)." -> should-use-predictivebackhandler-in-compose "In Compose, apps SHOULD use `PredictiveBackHandler`, ..., SHOULD commit the navigation when the flow completes, and SHOULD reset UI on `CancellationException` (gesture cancelled)."
- "Views: extend `OnBackPressedCallback` and implement ... (API 34+) to animate, ..." -> should-implement-back-progress-callbacks-in-views "In Views, apps SHOULD extend ..."
- "Use it ONLY for non-consuming side effects; it MUST NOT alter navigation." -> split: should-use-observer-priority-only-for-side-effects "Apps SHOULD use `PRIORITY_SYSTEM_NAVIGATION_OBSERVER` ONLY for non-consuming side effects." (promoted; the MUST NOT half keeps its keyword as must-not-alter-navigation-from-observer)
bars: all three authored.
contradictions: should-animate-with-the-gesture's wording "guidance SHOULD animate with the gesture" names "guidance" as the subject (the source's own wording, likely meant "the app"); kept verbatim, not fixed.

unfinished: none.

## cookbook/guidelines/implementing/ui/animation-motion

Commit `b576913a`, 6 rules, 2 moved, 0 obsolete.

Intro keeps "Motion should be purposeful — guide attention, show spatial relationships, and provide feedback." as its statement (GF-01). "References:" stays verbatim at the top of the `references` part: `roles lossless` refuses it as obsolete ("a sentence of the topic's own base is never obsolete") and refuses mapping a lead-in to a non-rule part.
promoted:
- "Motion should be purposeful — guide attention, show spatial relationships, and provide feedback." (lowercase "should") -> should-make-motion-purposeful "Motion SHOULD be purposeful — guide attention, show spatial relationships, and provide feedback."
- "Never animate for decoration." -> must-not-animate-for-decoration "Motion MUST NOT be used for decoration — never animate for decoration."
- "**Duration defaults** (when no platform value exists):" + table -> should-use-duration-defaults "When no platform value exists, durations SHOULD follow the duration defaults (see *Duration defaults*)." (table kept as the how-to part)
- "When reduced motion is enabled, replace animations with instant state changes or simple cross-fades." stays inside must-respect-reduced-motion as that MUST rule's own detail (not a separate rule).
bars: all three authored. contradictions: none.

unfinished: none.

## cookbook/guidelines/implementing/ui/appkit-and-uikit-patterns

Commit `42b6653b`, 17 rules, 2 moved, 0 obsolete.

All rule bullets were already keyworded and kept verbatim (two-sentence bullets in main-thread split at the sentence: must-touch-ui-only-on-main-thread, should-mark-ui-types-mainactor). The folded reviewer copy's parts (introduction, responder-chain-2, delegates, main-thread-2, lifecycle, state-restoration-2) keep their text and take `review-focus`; the duplicate H1 line inside `introduction` was dropped (a heading, not a sentence). The explanatory responder-chain bullets stay as the `how-to` part; both why-this-matters parts are `rationale`.
promoted:
- "To insert an object into the chain, override `nextResponder` and return it." -> should-override-nextresponder-sparingly "To insert an object into the chain, code SHOULD override `nextResponder` and return it, and SHOULD do this sparingly; ..."
bars: look-for **authored** (two lines, for should-mark-ui-types-mainactor and must-implement-secure-restoration-callbacks, which the reused checklist does not cover) plus the six reused checklist parts **moved**; a-complete-review-must-establish authored; a-build-must-establish authored.
contradictions: must-make-delegates-weak "Delegate and data-source properties MUST be `weak` (or `unowned(unsafe)` on old APIs)" vs the reused checklist (delegates) "Every delegate and data-source property is `weak`. Flag a strong one unless a comment explains the ownership." — the checklist lets a commented strong delegate pass, the rule does not. Also should-keep-window-content-in-view-controllers is SHOULD, while the checklist (lifecycle) states "On macOS, window content lives in a view controller, not in the window controller." without exception. Left unfixed.

unfinished: none.

## cookbook/guidelines/implementing/ui/apple-liquid-glass-and-widgets

Commit `12a59420`, 14 rules, 1 moved, 0 obsolete.

Intro keeps its first sentence as the statement; its SHOULD sentence becomes should-let-platform-supply-and-gate-new-apis verbatim. Every other rule bullet was keyworded and is kept verbatim.
promoted:
- "Treat its specifics as recent and evolving — pin to the iOS/macOS 26 cycle (2025–2026) and confirm against current docs before relying on exact API shapes." -> should-treat-liquid-glass-as-evolving "The agent SHOULD treat Liquid Glass specifics as recent and evolving — pin to ..."
- Intro statement "Build with Apple's system design language and standard components rather than reinventing chrome." stays in intro as the statement; its substance is held at MUST by must-use-standard-components, so it is not named again.
bars: all three authored. contradictions: none.

unfinished: none.

## cookbook/guidelines/implementing/ui/color

Commit `27d33da9`, 6 rules, 4 moved, 0 obsolete.

Intro keeps "Use color with intention — never as the sole means of conveying information." as its statement; its "never" half is held at MUST by must-not-rely-on-color-alone. "References:" stays at the top of the `references` part (see animation-motion).
promoted:
- "**Limit the palette** — 1 primary/accent color, 1-2 neutral tones, plus semantic colors for success/warning/error. Avoid rainbow UIs." -> should-limit-the-palette "**Limit the palette** — the palette SHOULD be limited to 1 primary/accent color, 1-2 neutral tones, plus semantic colors for success/warning/error. Rainbow UIs SHOULD be avoided."
- "**Contrast minimums** (WCAG AA, per [accessibility]):" + table -> must-meet-contrast-minimums "**Contrast minimums** — text and non-text UI components MUST meet the WCAG AA contrast minimums (per [accessibility]) in *Contrast minimums*." Read at MUST because the source calls them minimums; a plain-label reading would give SHOULD, so a judge should check the level. The table is the `how-to` part.
- "Test both." -> should-test-light-and-dark "Both light and dark themes SHOULD be tested."
bars: all three authored. contradictions: none.

unfinished: none.

## cookbook/guidelines/implementing/ui/compose-performance-and-stability

Commit `2fd57412`, 17 rules, 19 moved, 0 obsolete.

Intro kept verbatim (statement plus its summary SHOULD sentence, whose two requirements the rules also carry). Explanations of stability and strong skipping stay as the `rationale` part; the compiler-metrics sentence is the `how-to` part.
promoted:
- "Pass **immutable** data into composables. Prefer `val` over `var`, ..." -> should-pass-immutable-data "Composables SHOULD be passed **immutable** data. Code SHOULD prefer `val` over `var`, ..."
- "Prefer genuinely stable inputs." -> should-prefer-genuinely-stable-inputs "Code SHOULD prefer genuinely stable inputs; strong skipping does not make a type stable."
- "Annotate `@Immutable` ... **only** when ... A false annotation causes missed recompositions and stale UI — do not annotate to silence the compiler." -> should-annotate-stability-only-when-true "Code SHOULD annotate ... **only** when ... — code SHOULD NOT annotate to silence the compiler."
- "Read state as **late** as possible. Hoist the read into a lambda-based modifier ..." -> should-read-state-late "State SHOULD be read as **late** as possible. Code SHOULD hoist the read ..."
- "Pass **lambdas** instead of already-read values when ..." -> should-pass-lambdas-for-frequently-changing-values "Code SHOULD pass **lambdas** ..."
- "Use `derivedStateOf { ... }` when ... crosses a threshold (e.g. `firstVisibleItemIndex > 0`)." -> should-use-derivedstateof-for-thresholds "Code SHOULD use `derivedStateOf { ... }` when ..."
- "Do not use it for one-to-one transforms — that adds overhead with no benefit." -> should-not-use-derivedstateof-for-one-to-one-transforms "Code SHOULD NOT use `derivedStateOf` for one-to-one transforms — ..."
- "`remember(keys) { expensive() }` to cache costly computation across recompositions; recompute only when a key changes." -> should-remember-expensive-computation "Code SHOULD use `remember(keys) { expensive() }` to cache costly computation across recompositions, recomputing only when a key changes."
- "Do **NOT** perform backwards writes — never write to a state value that the same composable already read; ..." -> must-not-perform-backwards-writes "Code **MUST NOT** perform backwards writes — never write to ..." (MUST NOT from "never")
- "Keep composables side-effect free and idempotent." -> should-keep-composables-side-effect-free "Composables SHOULD be kept side-effect free and idempotent."
- "Avoid allocating new collections, ...; hoist or `remember` them." -> should-avoid-allocating-in-composable-body "Code SHOULD avoid allocating ...; it SHOULD hoist or `remember` them."
- "Profile **release** builds with R8 enabled and a **Baseline Profile** applied." -> should-profile-release-builds "Code SHOULD be profiled in **release** builds with R8 enabled and a **Baseline Profile** applied."
- "Debug builds run unoptimized Compose and produce misleading numbers — never tune against them." -> must-not-tune-against-debug-builds "... — code MUST NOT be tuned against them; never tune against them." (MUST NOT from "never")
- "Use **Layout Inspector** recomposition counts ..." -> should-use-layout-inspector-recomposition-counts "Code SHOULD use **Layout Inspector** recomposition counts ..."
- "For regression gates, use Macrobenchmark ..." -> should-gate-regressions-with-macrobenchmark "For regression gates, code SHOULD use Macrobenchmark ..."
- "Optimize a hotspot **only** after a measurement justifies it (...); do not pre-optimize composables that are not hot." -> should-optimize-only-after-measurement "Code SHOULD optimize a hotspot **only** after ... and SHOULD NOT pre-optimize composables that are not hot."
bars: all three authored. contradictions: none.

unfinished: none.

## cookbook/guidelines/implementing/ui/compose-side-effects

Commit `fd34c516`, 12 rules, 3 moved, 0 obsolete.

Intro kept verbatim. Core-rule and MUST/MUST NOT bullets moved into `rules` verbatim (the two-requirement bullets split at sentence boundaries). API table is `how-to`; the lifecycle code sample is `examples`; the too-few/too-many keys consequences are a `rationale` part naming the keying rules.
promoted:
- "`LaunchedEffect(Unit)` / `LaunchedEffect(true)` runs once per entry into composition; use it **only** when the effect is genuinely lifecycle-scoped, ..." -> should-use-launchedeffect-unit-only-when-lifecycle-scoped "...; code SHOULD use it **only** when the effect is genuinely lifecycle-scoped."
- "Adopt it only when profiling shows wasted recompositions." -> (in should-reserve-derivedstateof) "Code SHOULD adopt it only when profiling shows wasted recompositions."
- "Prefer hoisting state and side effects into the ViewModel where the work outlives composition; ..." -> should-hoist-long-lived-work-to-viewmodel "Code SHOULD prefer hoisting state and side effects into the ViewModel where ..."
bars: all three authored.
contradictions: none found. (Judgment noted: "use it **only** when" was read as SHOULD per the plain-imperative rule, though "only" could be read as MUST.)

unfinished: none.

## cookbook/guidelines/implementing/ui/compose-state-and-udf

Commit `46b66302`, 17 rules, 8 moved, 0 obsolete.

Intro kept verbatim. Keyword bullets moved into `rules` verbatim. Hoisting explanation and the remember/rememberSaveable table are `how-to` parts; the two code samples are one `examples` part; the strong-skipping note is a `rationale` part naming the two parameter rules.
promoted:
- "Keep the `MutableStateFlow` private and expose the immutable upcast." -> should-keep-mutablestateflow-private "A `ViewModel` SHOULD keep the `MutableStateFlow` private and expose the immutable upcast."
- "Collect `StateFlow` with `collectAsStateWithLifecycle()` (...) so collection stops in the background — prefer it over `collectAsState()` on Android." -> should-collect-with-lifecycle "Code SHOULD collect `StateFlow` with ... — code SHOULD prefer it over `collectAsState()` on Android."
- "Confirm the lifecycle-compose dependency is present." -> should-confirm-lifecycle-compose-dependency "Code SHOULD confirm the lifecycle-compose dependency is present."
- "Model screen state as a single immutable `data class` or a `sealed interface` of cases (...)." -> should-model-screen-state-immutably "Code SHOULD model screen state as ..."
- "Pass the **narrowest** parameters a composable needs (e.g. `title: String`), ..." -> should-pass-narrowest-parameters "Code SHOULD pass the **narrowest** parameters ..."
- "Prefer **stable** types as parameters: ..." -> should-prefer-stable-parameter-types "Code SHOULD prefer **stable** types as parameters: ..."
- "Use Kotlin immutable collections (...) or annotate types as `@Immutable` / `@Stable` only when the contract genuinely holds — ..." -> should-mark-stability-only-when-contract-holds "Code SHOULD use Kotlin immutable collections ... only when the contract genuinely holds — ..."
- "Treat unnecessary recomposition as a **performance** concern, not a correctness one: make it work and right first, then measure ..." -> should-treat-recomposition-as-performance-concern "Code SHOULD treat unnecessary recomposition as a **performance** concern, not a correctness one, and SHOULD make it work and right first, then measure ..."
- (kept verbatim, no keyword on the instruction itself) "Use `rememberSaveable` for state that **SHOULD** survive rotation or process death ..." -> should-use-remembersaveable-for-surviving-state, unchanged text; its only keyword sits in the condition, so the rule's level is read as SHOULD.
bars: all three authored.
contradictions: none.

unfinished: none.

## cookbook/guidelines/implementing/ui/core-web-vitals

Commit `0010cd03`, 19 rules, 14 moved, 0 obsolete.

Intro kept verbatim. The metrics section (FID replacement date, threshold table, pass criteria) is `how-to`; its "Agents MUST NOT reference FID" sentence and the four Requirements bullets moved into `rules` verbatim. The INP lead-in paragraph ("... Mitigations, in order of leverage:") is kept verbatim in a `rationale` part, followed by the mitigation rules' names in their original order, so the order-of-leverage ranking is kept.
promoted:
- "**Break up long tasks** — split work > 50ms ..." -> should-break-up-long-tasks "Code SHOULD **break up long tasks** — split work > 50ms ..."
- "**Yield to the main thread.**" -> should-yield-to-main-thread "Code SHOULD **yield to the main thread.**"
- "Prefer `scheduler.yield()` where available — note it is **Chromium-supported but NOT yet Baseline** ..." -> should-prefer-scheduler-yield "Code SHOULD prefer `scheduler.yield()` where available — ..."
- "Provide a fallback: feature-detect and degrade to ..." -> should-provide-yield-fallback "Code SHOULD provide a fallback: ..."
- "**Move heavy computation to a Web Worker** (...) ..." -> should-move-heavy-computation-to-web-worker "Code SHOULD **move heavy computation to a Web Worker** ..."
- "**Avoid layout thrashing** — batch DOM reads then writes; never interleave reads/writes in a loop that forces synchronous reflow." -> must-avoid-layout-thrashing "Code SHOULD **avoid layout thrashing** — batch DOM reads then writes; code MUST NOT interleave reads/writes in a loop that forces synchronous reflow — never interleave them." (MUST NOT from "never"; the batching half stays SHOULD)
- "**Keep the DOM small** — ... Virtualize long lists." -> should-keep-dom-small "Code SHOULD **keep the DOM small** — ... Code SHOULD virtualize long lists."
- "**Defer non-critical work** to idle time ..." -> should-defer-non-critical-work "Code SHOULD **defer non-critical work** ..."
- "**LCP**: preload the LCP image/font, ..." -> should-apply-lcp-quick-wins "For **LCP**, code SHOULD preload the LCP image/font, ..."
- "**CLS**: reserve space for media and dynamic content; ..." -> should-apply-cls-quick-wins "For **CLS**, code SHOULD reserve space for media and dynamic content; ..."
- "Collect field data via the **`web-vitals` JavaScript library** ..." -> should-collect-field-data "Code SHOULD collect field data via ..."
- "Wire a CI gate such as **Lighthouse CI** ..." -> should-wire-a-ci-gate "Code SHOULD wire a CI gate ..."
- "Express budgets as concrete limits (...) and fail the build on regression — ..." -> should-express-budgets-as-concrete-limits "Code SHOULD express budgets as concrete limits ..."
- "... so pin to the dated thresholds above and re-verify against `web.dev/articles/vitals/`." -> should-pin-dated-thresholds "... so work SHOULD pin to the dated thresholds above and re-verify against `web.dev/articles/vitals/`." ("above" now points at the `how-to` part's table.)
bars: all three authored.
contradictions:
- "**CLS**: reserve space for media and dynamic content" (a plain imperative, so should-apply-cls-quick-wins is SHOULD) overlaps "Layout-shift-prone elements (images, ads, embeds, late-injected banners) **MUST** reserve space ..." (must-reserve-space-for-shifting-elements). The same requirement for media sits at two levels. Left unfixed.
- "A **performance budget MUST be enforced in CI**" (MUST) versus "Wire a CI gate such as **Lighthouse CI** ..." and "Express budgets as concrete limits ... and fail the build on regression" (promoted to SHOULD). The failing-build half is MUST in one rule and SHOULD in the other. Left unfixed.

unfinished: none.

## cookbook/guidelines/implementing/ui/cross-platform-token-adaptation

Commit `c060b878`, 16 rules, 5 moved, 0 obsolete.

Intro kept verbatim. Keyword bullets moved into `rules` verbatim. The unit table is the `how-to` part.
promoted:
- "Use the W3C Design Tokens Community Group format (DTCG), which reached ... in October 2025; pin to a dated revision so one source feeds ..." -> should-use-dtcg-format "Code SHOULD use the W3C ... in October 2025, and SHOULD pin to a dated revision so one source feeds ..."
- "Adapt the same numeric intent to each platform's density-independent unit." -> should-adapt-to-density-independent-units "Code SHOULD adapt the same numeric intent to each platform's density-independent unit."
- "Do not ship raw `px` everywhere." -> should-not-ship-raw-px-everywhere "Code SHOULD NOT ship raw `px` everywhere."
- "Adapt to the host idiom — navigation patterns, ... — rather than forcing one platform's look onto another." -> should-adapt-to-host-idiom "Code SHOULD adapt to the host idiom — ..."
- "... (per YAGNI): start with a single shared file and per-platform transforms; add heavier infrastructure only when ..." -> should-start-with-single-shared-file "... (per YAGNI): code SHOULD start with a single shared file and per-platform transforms, and SHOULD add heavier infrastructure only when ..."
bars: all three authored.
contradictions:
- "Platform-specific overrides **SHOULD** live as transforms or aliases over the shared source, never as a forked copy of it." The keyword is SHOULD while "never" reads as MUST NOT. Left unfixed.
- "Do not ship raw `px` everywhere." (SHOULD NOT) sits beside "Dimension tokens **MUST** be emitted in the target's density-independent unit" (MUST). The table also allows `px` for web hairlines. Left unfixed.

unfinished: none.

## cookbook/guidelines/implementing/ui/dashboard-service-is-display-only

Commit `d6d221cc`, 2 rules, 2 moved, 0 obsolete.

The intro keeps its statement sentence. Its two MUST sentences became the `rules` part, with "It"/"it" replaced by "the dashboard service" so each rule stands alone (both are moved entries).
promoted: none (both rules already carried MUST / MUST NOT).
bars: all three authored.
contradictions: none.

unfinished: none.

## cookbook/guidelines/implementing/ui/data-display

Commit `e854c21a`, 8 rules, 10 moved, 0 obsolete.

The intro keeps its statement ("Choose the right pattern for the content type and user task."). The four pattern descriptions ("**List** — ... Best for ...") are the `how-to` part (heading "Choosing a pattern"). The requirement sentences in them became rules, and the reference list is the `references` part, with "References:" kept verbatim. Eight of the moved entries are line-wrap fragments: the lossless tool splits a bullet at its hard line breaks, so one sentence such as "Tables MUST be sortable / by column." counts as two fragments.
promoted:
- "Choose the right pattern for the content type and user task." (intro statement, kept there too) -> should-choose-pattern-by-content-and-task "Work SHOULD choose the right pattern (list, table, cards or grid) for the content type and user task."
- "Support pull-to-refresh and pagination for dynamic data." -> should-support-refresh-and-pagination-in-lists "Lists SHOULD support pull-to-refresh and pagination for dynamic data."
- "On mobile, consider collapsing to cards or a detail-on-tap list." -> should-consider-collapsing-tables-on-mobile "On mobile, work SHOULD consider collapsing tables to cards or a detail-on-tap list."
- "Cards should each be a single tappable unit with one primary action." (lower-case "should") -> should-make-each-card-one-tappable-unit "Cards SHOULD each be a single tappable unit with one primary action."
- "Maintain consistent aspect ratios." -> should-maintain-grid-aspect-ratios "Grids SHOULD maintain consistent aspect ratios."
bars: all three authored.
contradictions:
- "Tables MUST be sortable by column." (every table, MUST) versus "Collections of **10+ items** SHOULD provide sort and/or filter controls." (SHOULD). A table of 10+ rows is held to MUST by one rule and SHOULD by the other. Left unfixed.

unfinished: none.

## cookbook/guidelines/implementing/ui/design-time-data

Commit `ad86e9b3`, 3 rules, 5 moved, 0 obsolete.

The intro keeps its statement. Its two bullets and the "What to verify" list say the same two things twice, so the duplicates merge into one rule each, each keeping both phrasings. The "Introduction" part (the Windows-equivalent explanation) is now `rationale`, without its duplicate H1. "What to verify" was read as developer verification during testing, not as reviewer text, so all three bars are authored.
promoted:
- "Verify all significant view states are previewable: default, empty, error, loading, populated" -> should-preview-all-significant-states "Work SHOULD verify all significant view states are previewable: default, empty, error, loading, populated."
- "Use XAML Hot Reload for rapid visual iteration during testing" -> folded into should-use-xaml-hot-reload "XAML Hot Reload SHOULD be used for live iteration during development, and for rapid visual iteration during testing."
bars: all three authored.
contradictions: none.

unfinished: none.

## cookbook/guidelines/implementing/ui/design-token-distribution

Commit `72b2e153`, 15 rules, 9 moved, 0 obsolete.

Intro kept verbatim. Keyword bullets moved into `rules` verbatim. The per-platform table is the `how-to` part. The three anti-pattern bullets had a keyword but no subject, so they gained one ("Projects", "Feature code"). They are moved entries, not promotions.
promoted:
- "Regenerate on **every** token change, and run generation in CI so drift fails fast (per fail-fast)." -> should-regenerate-on-every-change-in-ci "Code SHOULD regenerate on **every** token change, and SHOULD run generation in CI so drift fails fast (per fail-fast)."
- "Version the token source. Treat token releases like any other versioned dependency so ..." -> should-version-token-source "The token source SHOULD be versioned. Token releases SHOULD be treated like any other versioned dependency so ..."
- "Run generation as a checked-in, reproducible step (...), not a one-off manual command." -> should-run-generation-as-reproducible-step "Generation SHOULD run as a checked-in, reproducible step (...), not a one-off manual command."
- "Keep the transform configuration in version control alongside the token source." -> should-version-transform-config "The transform configuration SHOULD be kept in version control alongside the token source."
- "Reach for a managed token pipeline or design-tool sync service only when a measured need justifies it (per YAGNI); ..." -> should-adopt-managed-pipeline-only-on-measured-need "Work SHOULD reach for a managed token pipeline ... only when a measured need justifies it (per YAGNI); ..."
bars: all three authored.
contradictions:
- The intro says generated outputs are "never hand-edited", and the drift check that enforces this is only SHOULD: "A drift check **SHOULD** run in CI: regenerate, then fail if the working tree differs from committed outputs." Also, "Regenerate on **every** token change, and run generation in CI" (promoted to SHOULD) is weaker than "Generated outputs **MUST NOT** be hand-edited." These are consistent in intent but differ in strength. Left unfixed.

unfinished: none.

## cookbook/guidelines/implementing/ui/feedback-patterns

Commit `7fdc5752`, 10 rules, 9 moved, 0 obsolete.

The intro keeps both statement sentences verbatim, and they are restated as the first two rules. The pattern descriptions (Inline, Toast, Banner, Dialog) are the `how-to` part (heading "Choosing a pattern"). The requirements inside them became rules, and the reference list is the `references` part, with "References:" kept verbatim. Several moved entries are line-wrap fragments of one sentence, for example "Auto-dismiss / after 3-5 seconds.".
promoted:
- "Every user action should have visible feedback." (lower-case "should"; kept in intro too) -> should-give-every-action-visible-feedback "Every user action SHOULD have visible feedback."
- "The weight of the feedback should match the weight of the action." (lower-case; kept in intro too) -> should-match-feedback-weight-to-action "The weight of the feedback SHOULD match the weight of the action."
- "Auto-dismiss after 3-5 seconds." -> should-auto-dismiss-toasts "Toasts SHOULD auto-dismiss after 3-5 seconds."
- "No user action required." -> must-require-no-action-on-toasts "Toasts MUST require no user action — no user action required." The lossless check reads "required" as MUST and refused SHOULD ("the matched clause drops its MUST"), so this rule is MUST. A judge should confirm that level.
- "Dismissible." -> should-make-banners-dismissible "Banners and inline alerts SHOULD be dismissible."
- "Use sparingly — dialog fatigue leads to click-through without reading." -> should-use-dialogs-sparingly "Dialogs SHOULD be used sparingly — dialog fatigue leads to click-through without reading."
- "Default focus should be on the safe option (Cancel)." (lower-case "should") -> should-default-focus-to-safe-option "Default focus SHOULD be on the safe option (Cancel)."
bars: all three authored.
contradictions: none.

unfinished: none.

## cookbook/guidelines/implementing/ui/fluent-design

Commit `b7c47455`, 5 rules, 3 moved, 0 obsolete.

The intro keeps its statement ("Use built-in WinUI 3 controls — they implement Fluent 2 natively."), which is also restated as a rule. The MUST NOT sentence and the MUST bullet moved into `rules`.
promoted:
- "Use built-in WinUI 3 controls — they implement Fluent 2 natively." (kept in intro too) -> should-use-built-in-winui-controls "Applications SHOULD use built-in WinUI 3 controls — they implement Fluent 2 natively."
- "Typography: Segoe UI Variable" -> should-use-segoe-ui-variable "Typography SHOULD use Segoe UI Variable."
- "Icons: Segoe Fluent Icons" -> should-use-segoe-fluent-icons "Icons SHOULD use Segoe Fluent Icons."
bars: all three authored.
contradictions: none.

unfinished: none.

## cookbook/guidelines/implementing/ui/form-design

Commit `b61f8099`, 16 rules, 21 moved, 0 obsolete.

The intro keeps its two statement sentences, and the second is also restated as a rule. All bullets under the four `###` sub-headings became rules. The reference list is the `references` part, with "References:" kept verbatim. The sub-headings "### Layout", "### Validation" and "### Error messages" map to a rule that carries their word. "### Other principles" maps to a short `rationale` part that names the three rules it grouped, because the tool refuses `obsolete` for a topic's own base text. The word "placeholder" is kept as the source has it.
promoted:
- "Reduce friction at every step." (kept in intro too) -> should-reduce-friction-at-every-step "Forms SHOULD reduce friction at every step."
- "Top-aligned or floating labels — fastest to scan and complete" -> should-use-top-aligned-or-floating-labels "Labels SHOULD be top-aligned or floating — fastest to scan and complete."
- "Group related fields visually with spacing or section headers" -> should-group-related-fields "Forms SHOULD group related fields visually ..."
- "Place primary action (Submit/Save) at the bottom, aligned with the form fields" -> should-place-primary-action-at-bottom "Forms SHOULD place the primary action (Submit/Save) at the bottom, ..."
- "Validate on **blur** (when user leaves the field), not on every keystroke" -> should-validate-on-blur "Forms SHOULD validate on **blur** ..."
- "Validate the **full form on submit** as a final safety net" -> should-validate-full-form-on-submit "Forms SHOULD validate the **full form on submit** ..."
- "Success indicators (checkmarks) only for fields where the user genuinely wonders if input was accepted (...)" -> should-show-success-indicators-only-where-wondered "Success indicators (checkmarks) SHOULD appear only for fields where ..."
- "Use color + icon + text (never color alone)" -> must-not-signal-errors-by-color-alone "Errors SHOULD use color + icon + text and MUST NOT rely on color alone (never color alone)." (MUST NOT from "never"; the three-channel half stays SHOULD)
- "Be specific and actionable: \"Password must be at least 8 characters\" not \"Invalid input\"" -> should-write-specific-actionable-errors "Error messages SHOULD be specific and actionable: ..."
- "Don't blame the user" -> should-not-blame-the-user "Error messages SHOULD NOT blame the user — don't blame the user."
- "Use placeholder text for format hints, not as label replacement — placeholders disappear on focus" -> should-use-placeholder-for-format-hints-only "Forms SHOULD use placeholder text for format hints, not as label replacement — ..."
- "Pre-fill and default where possible to reduce effort" -> should-pre-fill-and-default "Forms SHOULD pre-fill and default where possible to reduce effort."
- "Mark optional fields, not required ones (most fields should be required; if they're not, reconsider asking)" -> should-mark-optional-fields "Forms SHOULD mark optional fields, not required ones (...)."
bars: all three authored.
contradictions: none.

unfinished: none.

## Unfinished

Nothing. All twenty topics are converted and committed, and this report is committed. Nothing was pushed.
