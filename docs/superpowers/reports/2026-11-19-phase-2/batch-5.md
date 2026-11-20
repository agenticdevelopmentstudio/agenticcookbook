# Phase 2 batch 5 report

Eighteen guideline topics converted to roled parts: the seven observability topics and the eleven
platform-integration topics. Each topic now has one `rules` part holding every requirement as a named
rule, plus three new bar parts (`look-for`, `a-complete-review-must-establish`, `a-build-must-establish`)
with one line per rule. Each topic was checked with `roles lossless --draft` and `roles check`, bumped,
passed by `approve.py` (`RESULT: APPROVED`), and committed alone. No topic has an `obsolete` entry.
Only `wsl` held text written for a reviewer, so its `look-for` part is **moved**. Every other bar part in
the batch is **authored**.

## Where these topics differ from the brief

- **Platform sections were instructions, not reference text.** Most platform-integration topics had an
  intro (a SHOULD statement plus keyword-free bullets) and one paragraph per platform made of plain
  imperatives ("Use `WorkManager` …"). Each imperative became a SHOULD rule that names its platform
  ("On Android, you SHOULD use `WorkManager` …"), so the section heading's scope stays in the rule. A
  platform part left with no text after that was removed. A part that still held a fact sentence keeps it
  as `how-to`. Most promotions in the batch come from these paragraphs.
- **Folded duplicate copies.** Several intros (analytics, deep-linking, shortcuts-and-automation and others)
  held a second copy of the topic under a second H1, left there by the 2026-11-19 fold. Where every sentence
  of the copy was already in the first copy, the copy was dropped. A copy H1 whose wording differs is mapped
  to the intro and to the rule that holds its other words. `roles lossless` refuses `obsolete` for any of
  this text because the fold is in the base, so every such sentence is mapped as `moved` or kept verbatim
  (see wsl).
- **Lossless wording constraints met along the way.** These are not substance changes:
  - Rule names with capitals were lower-cased, because `roles check` reads only lowercase kebab names.
  - A MUST NOT clause joined to a positive clause by ";" was split into two sentences.
  - The verb "avoid" was kept under SHOULD rather than rewritten as SHOULD NOT, because lossless treats
    "avoid" as a word whose loss flips meaning.
  - `slos-are-targets-not-100` opens with "SLOs are targets not 100 percent:" so its text keeps what its old
    name said.
- **One history table reordered.** In notifications, `cookr bump` refused a history table whose rows were out
  of order (1.0.0 above 2.0.0). The two rows were swapped to make the table newest-first, and no row text
  changed.
- **FM-13.** No topic in this batch respells "placeholder", "TODO", "TBD" or "FIXME"; this was checked
  against the base after the coordinator's notice.

## cookbook/guidelines/implementing/observability/ai-provider-observability
commit d566554f; rules 8; moved 2; obsolete 0
**promoted** (1):
- "Use prompt template IDs." → folded into `no-pii-in-prompt-logs`: "Production logs SHOULD use prompt template IDs instead."
**split** (no promotion): `prompt-tracking` split into `must-version-prompt-templates` (MUST) and `should-reference-prompt-template-in-logs` (SHOULD); the MAY sentence of `no-pii-in-prompt-logs` became `may-log-full-prompts-in-controlled-environments`.
**bars**: all three authored.
**contradictions**: none.

## cookbook/guidelines/implementing/observability/analytics
commit b7368b1e; rules 4; moved 2; obsolete 0
The intro held the text twice (a fold left an identical second copy under a second `# Analytics`); the copy is dropped, its sentences all held by the rules.
**promoted** (2):
- "No direct coupling to any analytics backend." → `must-not-couple-to-analytics-backend`: "There MUST NOT be direct coupling to any analytics backend." (read as a prohibition, MUST NOT)
- "Provide a logging-only default; swap in a backend (Mixpanel, Amplitude, PostHog) later." → `should-provide-logging-only-default`: "SHOULD provide a logging-only default, and swap in a backend (Mixpanel, Amplitude, PostHog) later."
Platform parts (Swift, Kotlin, TypeScript, C#) are `how-to`.
**bars**: all three authored.
**contradictions**: none.

## cookbook/guidelines/implementing/observability/continuous-profiling
commit aeb9a9aa; rules 17; moved 6; obsolete 0
The four rule sections (when to adopt, how to do it, standards status, anti-patterns) fold into one `rules` part; the OTLP Profiles status facts become a `rationale` part naming the rules they support. The intro's "Treat it as a maturity addition ..., not a day-one default." stays in the intro as written; `must-not-add-profiling-by-default` carries it as a rule.
**promoted** (4):
- "**Adopt it ONLY when** a concrete, measured need justifies the added pipeline, storage, and operational cost:" → `must-adopt-only-on-measured-need`: "You MUST adopt it ONLY when a concrete, measured need justifies the added pipeline, storage, and operational cost, such as:" (its three needs kept as sub-bullets; "ONLY" read as MUST)
- "If a one-off `pprof`/perf capture or a load-test profile answers the question, **prefer that** over standing infrastructure (small-reversible-decisions)." → `should-prefer-one-off-capture`: "... you SHOULD prefer that over standing infrastructure (small-reversible-decisions)."
- "(FORECAST: automatic span-level correlation is uneven across profilers/runtimes as of 2026 — verify support per language before relying on it.)" → `should-verify-span-correlation-support`: "(FORECAST: automatic span-level correlation is uneven across profilers/runtimes as of 2026.) You SHOULD verify support per language before relying on it."
- "(FORECAST: production-ready OTLP-Profiles backends are still emerging; **prefer** a profiler whose data you can convert if the backend changes.)" → `should-prefer-convertible-profiler`: "(FORECAST: production-ready OTLP-Profiles backends are still emerging.) You SHOULD prefer a profiler whose data you can convert if the backend changes."
**split**: the SHOULD/MAY eBPF sentence became `should-prefer-ebpf-for-diverse-targets` and `may-use-in-runtime-profilers`; the two-MUST overhead bullet became `must-choose-low-overhead-sampling-profiler` and `must-validate-overhead-in-own-environment`.
**bars**: all three authored.
**contradictions**: none. (`must-not-ship-unmeasured-profiler` and `must-validate-overhead-in-own-environment` overlap — both require measured overhead — but agree.)

## cookbook/guidelines/implementing/observability/distributed-tracing
commit 172debbd; rules 23; moved 12; obsolete 0
The five rule sections fold into one `rules` part; two explanatory sentences (the W3C Level 1 date; why consumer spans link) become a `rationale` part naming their rules. The old sub-heading "### Async and messaging boundaries" maps to `must-propagate-context-in-messages`, which now opens "At async and messaging boundaries, …" (lossless refuses `obsolete` for a topic's own base text). The intro's "Standardize instrumentation on OpenTelemetry (OTel) and propagation on W3C Trace Context …" stays in the intro; `must-create-spans-via-otel-api` and `should-propagate-w3c-trace-context` carry it as rules.
**promoted** (9):
- "Prefer auto-instrumentation for common frameworks/clients; reserve manual spans for domain-specific work." → `should-prefer-auto-instrumentation`: "Code SHOULD prefer auto-instrumentation for common frameworks/clients, and reserve manual spans for domain-specific work."
- "*Level 2 is a Candidate Recommendation Draft as of 2026 — treat its additions as a forecast and pin to Level 1 for interop.*" → `should-pin-trace-context-level-1`: "Level 2 is a Candidate Recommendation Draft as of 2026; code SHOULD treat its additions as a forecast and pin to Level 1 for interop."
- "… emit `traceparent` in lowercase." (second clause of the MUST header sentence) → `should-emit-lowercase-traceparent`: "Code SHOULD emit `traceparent` in lowercase." (A judge should check whether the clause sat under the sentence's MUST; read here as a separate plain imperative.)
- "Inject and extract context at the transport edge (middleware/interceptors), not scattered through business logic." → `should-inject-context-at-transport-edge`: "Code SHOULD inject and extract context at the transport edge (middleware/interceptors), not scattered through business logic."
- "Prefer **tail-based sampling** at the OpenTelemetry Collector over head-based sampling in the SDK: …" → `should-prefer-tail-based-sampling`: "Code SHOULD prefer **tail-based sampling** at the OpenTelemetry Collector over head-based sampling in the SDK: …"
- "A sane default policy: keep 100% of traces containing an error or high latency, and sample a fraction (e.g., ~10%) of successful traces." → `should-keep-errors-and-sample-successes`: "The default sampling policy SHOULD keep 100% of traces containing an error or high latency, and sample a fraction (e.g., ~10%) of successful traces."
- "Tune the rate from what proves useful — do not treat any one number as a fixed rule." → `should-tune-sampling-rate`: "Code SHOULD tune the rate from what proves useful, and SHOULD NOT treat any one number as a fixed rule."
- "Use the same `trace_id` field name across services; agents grep on it to correlate signals." → `should-use-same-trace-id-field-name`: "Services SHOULD use the same `trace_id` field name across services; agents grep on it to correlate signals."
- "Where applicable, follow the OpenTelemetry GenAI semantic conventions (e.g., `gen_ai.request.model`) for attribute names." → `should-follow-genai-semantic-conventions`: "Where applicable, code SHOULD follow the OpenTelemetry GenAI semantic conventions (e.g., `gen_ai.request.model`) for attribute names."
- "*These conventions are still in Development status as of 2026 and may change — record the convention version you target.*" → `should-record-genai-convention-version`: "These conventions are still in Development status as of 2026 and may change; code SHOULD record the convention version it targets."
**bars**: all three authored.
**contradictions**: none.

## cookbook/guidelines/implementing/observability/logging
commit 13a0d194; rules 18; moved 18; obsolete 0
The intro held the text twice (a fold left a second copy under `# Logging`); the copy is dropped and its one new sentence (the PII ban) is a rule. The intro keeps the statement, ending in a period. The platform parts keep their lead sentences and code as `how-to`; their bullets move to `rules`. The OpenTelemetry section's four SHOULD bullets become rules, its framing sentence a `rationale` entry, and its cross-reference a `references` part. "# Logging" (the copy's H1) maps to `intro`; "Additionally:" maps to the three Windows rules, with a `rationale` entry naming them.
**promoted** (15):
- "Every component and flow must be instrumented with structured logging using the platform's best-in-class framework:" (lower-case "must") → `must-instrument-with-platform-framework`: "Every component and flow MUST be instrumented with structured logging using the platform's best-in-class framework:" (the five platform bullets kept as sub-bullets)
- "Use `debug` level for flow instrumentation." + Swift's "Use `debug` level for UI flow instrumentation" → `should-use-debug-for-flow-instrumentation`: "Code SHOULD use `debug` level for flow instrumentation, UI flow instrumentation included."
- "Log state transitions, user interactions, async task start/completion/failure, and branching logic." → `should-log-flow-events`: "Code SHOULD log state transitions, …"
- "Never log personally identifiable information, even at debug level." + "The PII guidance still applies — never emit personally identifiable information in any field, even at debug level." → `must-not-log-pii`: "Code MUST NOT log personally identifiable information in any field, even at debug level."
- "If no dependency is desired, use `android.util.Log` with consistent tags." → `should-use-android-log-with-consistent-tags`: "On Android, if no dependency is desired, code SHOULD use `android.util.Log` with consistent tags." (the Kotlin part keeps the sentence too)
- "Use structured message templates: …" → `should-use-structured-message-templates`: "In C#, code SHOULD use structured message templates: …"
- "**Never** use string interpolation (`$"..."`) in log calls — …" → `must-not-interpolate-in-log-calls`: "In C#, code MUST NOT use string interpolation (`$"..."`) in log calls — …"
- "Use the `[LoggerMessage]` source generator attribute for high-performance hot paths" → `should-use-loggermessage-for-hot-paths`: "In C#, code SHOULD use …"
- "Configure log levels per category via `appsettings.json`" → `should-configure-log-levels-per-category`: "In C#, code SHOULD configure log levels per category via `appsettings.json`."
- "Use ETW tracing (`EventSource`) for system-level diagnostics and startup timing" → `should-use-etw-for-system-diagnostics`: "On Windows, code SHOULD use ETW tracing …"
- "Use XAML Live Visual Tree in Visual Studio for debugging visual tree issues" → `should-use-xaml-live-visual-tree`: "On Windows, developers SHOULD use XAML Live Visual Tree …"
- "Use [Visual Studio Performance Profiler](…) for CPU, memory, and UI responsiveness analysis" → `should-use-vs-performance-profiler`: "On Windows, developers SHOULD use [Visual Studio Performance Profiler](…) …"
- The Swift bullets "Subsystem MUST match the bundle ID" and "Category MUST be one per component or flow" kept their MUST; they are scoped "On Apple platforms" (`must-match-subsystem-to-bundle-id`, `must-use-one-category-per-component`) and are not promotions.
**bars**: all three authored.
**contradictions**: none.

## cookbook/guidelines/implementing/observability/metrics-red-use
commit 1cc01f57; rules 15; moved 4; obsolete 0
The existing named rules (RED, USE, conventions) move into `rules` verbatim. "When to use which" and the USE dimensions table are `how-to`; "Relationship to other methods" is `rationale`; the "Avoid" list becomes three rules. `resource-coverage` held a SHOULD and a MUST NOT, and is split.
**promoted** (4):
- "Instrument every request-serving **service** with RED (Rate, Errors, Duration) and every consumable **resource** with USE (Utilization, Saturation, Errors)." (intro, kept there too) → `should-instrument-with-red-and-use`: "Code SHOULD instrument every request-serving **service** with RED … and every consumable **resource** with USE …"
- Avoid: "Recording duration as a gauge or average instead of a histogram (loses percentiles)." → `should-not-record-duration-as-gauge`: "Code SHOULD NOT record duration as a gauge or average instead of a histogram (loses percentiles)."
- Avoid: "High-cardinality labels that explode the time-series count and cost." → `should-not-use-high-cardinality-labels`: "Code SHOULD NOT use high-cardinality labels that explode the time-series count and cost."
- Avoid: "Tracking utilization while ignoring saturation, then being surprised by latency cliffs." → `should-not-track-utilization-without-saturation`: "Code SHOULD NOT track utilization while ignoring saturation, then being surprised by latency cliffs."
**split**: `resource-coverage` (SHOULD) and `must-not-omit-saturation` (MUST NOT) from one bullet.
**bars**: all three authored.
**contradictions** (overlaps at different levels, left as written):
- `duration-metric`: "Each service **MUST** emit request duration as a histogram (not just a mean) …" vs `should-not-record-duration-as-gauge`: "… SHOULD NOT record duration as a gauge or average instead of a histogram" — the Avoid item restates a MUST at SHOULD NOT.
- `cardinality-limit`: "Labels **MUST NOT** include unbounded values …" vs `should-not-use-high-cardinality-labels` at SHOULD NOT.
- `must-not-omit-saturation`: "… **MUST NOT** be silently omitted" vs `should-not-track-utilization-without-saturation` at SHOULD NOT.

## cookbook/guidelines/implementing/observability/service-level-objectives
commit 2a78fe0b; rules 18; moved 11; obsolete 0
Each section's definition sentence (SLI, SLO, error budget, burn rate) stays in its part as `how-to`; the named bullets move to `rules`. Three rule names held capitals, which `roles check` does not read as names; they are lower-cased (`slos-are-targets-not-100`, `user-facing-needs-an-slo`, `scale-windows-to-your-slo`). `slos-are-targets-not-100` now opens "SLOs are targets not 100 percent:" so its text carries what its old name said. The burn-rate tier table stays under `tier-by-severity`.
**promoted** (7):
- "Define **multiple thresholds** to capture both typical and tail experience, e.g. *90% of requests < 100 ms AND 99% < 400 ms*." → `define-multiple-latency-thresholds`: "Latency SLIs SHOULD define **multiple thresholds** …" (split from `latency-uses-percentiles`)
- "Choose the lowest reliability users won't notice." → `choose-lowest-unnoticed-reliability`: "You SHOULD choose the lowest reliability users won't notice." (split from `slos-are-targets-not-100`)
- "Set the initial SLO from observed performance, then tighten deliberately. Do not promise a number you have never measured." → `start-from-data`: "You SHOULD start from data: set the initial SLO from observed performance, then tighten deliberately, and SHOULD NOT promise a number you have never measured."
- "Page on fast burn; open a ticket on slow burn." → `tier-by-severity`: "Alerts SHOULD page on fast burn and open a ticket on slow burn."
- Anti-pattern: "Alerting on a single fixed error-count threshold (no relation to budget; floods or misses)." → `should-not-alert-on-fixed-error-count`: "Alerting SHOULD NOT rest on a single fixed error-count threshold (…)."
- Anti-pattern: "One global SLO covering unrelated journeys (…)." → `should-not-use-one-global-slo`: "You SHOULD NOT have one global SLO covering unrelated journeys (…)."
- Anti-pattern: "SLOs measured only inside the service, missing client-side and edge failures." → `should-not-measure-slos-only-inside-service`: "SLOs SHOULD NOT be measured only inside the service, missing client-side and edge failures."
**bars**: all three authored.
**contradictions**: `should-not-alert-on-fixed-error-count` (SHOULD NOT) restates part of `alert-on-symptom-not-cause` ("Alerting MUST target budget burn …, not resource thresholds") at a lower level; they agree in direction, left as written.

## cookbook/guidelines/implementing/platform-integration/app-intents
commit 81caf77e; rules 16; moved 5; obsolete 0
Every section's bullets move to one `rules` part; each section keeps its lead sentence as `how-to`. The two explanation sentences (SiriKit is legacy; Apple Intelligence surfaces evolve) stay in their sections as `rationale` entries naming the rules. The intro keeps its SHOULD sentence, also carried by `model-key-actions-as-app-intents`.
**promoted** (5):
- "Conform one type to `AppShortcutsProvider` and return `AppShortcut` values from the `appShortcuts` builder." → `conform-one-type-to-appshortcutsprovider`: "You SHOULD conform one type to `AppShortcutsProvider` and return …"
- "Provide an `EntityQuery` (or `EntityStringQuery`/`EnumerableEntityQuery`) so the system can resolve entities …" → `provide-an-entityquery`: "You SHOULD provide an `EntityQuery` …"
- "For new work, prefer the App Intents framework." → `prefer-app-intents-for-new-work`: "For new work, you SHOULD prefer the App Intents framework."
- "Do **NOT** add a new SiriKit custom intent for an action that App Intents can express; migrate existing custom intents when touched." → `should-not-add-sirikit-custom-intent`: "You **SHOULD NOT** add a new SiriKit custom intent for an action that App Intents can express." and `migrate-custom-intents-when-touched`: "You SHOULD migrate existing custom intents when touched." (the emphatic "Do NOT" carries no "never", so it is read as a plain imperative; an owner may want MUST NOT)
- "Treat any \"App Intents power feature X\" capability beyond … as a FORECAST and confirm against the App Intents documentation …" → `treat-other-capabilities-as-forecasts`: "You SHOULD treat any … as a FORECAST and confirm against …"
**bars**: all three authored.
**contradictions**: none found.

## cookbook/guidelines/implementing/platform-integration/background-tasks
commit d38c1502; rules 20; moved 19; obsolete 0
The intro bullets and every platform section's imperatives become rules; each platform rule opens with its platform ("On Android, …") so the section heading's scope stays in the rule. The Apple, Android and Web parts held only instructions and are removed; the Windows part keeps its one fact sentence (MSIX process isolation) as `how-to`. The intro keeps its statement paragraph; its SHOULD sentence is also `use-platform-background-apis`.
**promoted** (19): every rule but `use-platform-background-apis`, each a plain imperative read as SHOULD:
- "Use the platform's sanctioned background APIs — unsanctioned workarounds get killed and drain battery" → `use-sanctioned-background-apis`: "You SHOULD use the platform's sanctioned background APIs — …"
- "Design tasks to be resumable — …" → `design-tasks-to-be-resumable`: "You SHOULD design tasks to be resumable — …"
- "Minimize resource usage — …" → `minimize-resource-usage`: "You SHOULD minimize resource usage — …"
- "Report progress and completion through notifications when appropriate" → `report-progress-through-notifications`: "You SHOULD report progress …"
- "Use `BGAppRefreshTask` and `BGProcessingTask` via the BackgroundTasks framework for deferred work." → `apple-use-bgtasks-for-deferred-work`: "On Apple platforms, you SHOULD use …"
- "Use `URLSession` background transfers …" → `apple-use-urlsession-background-transfers`: "On Apple platforms, you SHOULD use `URLSession` background transfers …"
- "On macOS, longer-running background work is less restricted but should still use `ProcessInfo.performActivity` to prevent App Nap." → `macos-prevent-app-nap`: "… but SHOULD still use …" (lower-case "should" raised to the keyword)
- "Use `NSBackgroundActivityScheduler` for periodic maintenance tasks on macOS." → `macos-use-nsbackgroundactivityscheduler`: "On macOS, you SHOULD use `NSBackgroundActivityScheduler` for periodic maintenance tasks."
- "Use `WorkManager` for all deferrable background work — …" → `android-use-workmanager-for-deferrable-work`: "On Android, you SHOULD use `WorkManager` …"
- "Use `ForegroundService` with a persistent notification …" → `android-use-foregroundservice-for-visible-work`: "On Android, you SHOULD use `ForegroundService` …"
- "Respect Doze mode and App Standby buckets." → `android-respect-doze-and-standby`: "On Android, you SHOULD respect …"
- "Avoid `AlarmManager` for work that `WorkManager` can handle." → `android-avoid-alarmmanager`: "On Android, you SHOULD avoid `AlarmManager` …"
- "Use `BackgroundTask` with the Windows App SDK …" → `windows-use-backgroundtask`: "On Windows, you SHOULD use …"
- "Register triggers (time, network state change, push notification) in the app manifest." → `windows-register-triggers-in-manifest`: "On Windows, you SHOULD register triggers …"
- "For long-running tasks, use `ExtendedExecutionSession`." → `windows-use-extendedexecutionsession`: "On Windows, for long-running tasks, you SHOULD use …"
- "Use Service Workers for background sync …" → `web-use-service-workers`: "On the web, you SHOULD use Service Workers …"
- "Use the Periodic Background Sync API …" → `web-use-periodic-background-sync`: "On the web, you SHOULD use …"
- "Use Web Workers for CPU-intensive tasks …" → `web-use-web-workers-for-cpu-work`: "On the web, you SHOULD use Web Workers …"
- "Fall back to `requestIdleCallback` for low-priority deferred work." → `web-fall-back-to-requestidlecallback`: "On the web, you SHOULD fall back to …"
**bars**: all three authored.
**contradictions**: none found.

## cookbook/guidelines/implementing/platform-integration/deep-linking
commit a5942fa9; rules 10; moved 9; obsolete 0
The intro's lead-in now ends with a period, so it is a plain statement for GF-01; the per-platform mechanism bullets it introduced move to a `how-to` part, "Native mechanisms by platform". The folded duplicate copy in the intro is dropped (its two sentences were already in the first copy). The TypeScript and Windows parts held only instructions and are removed; their instructions are rules, each opening with its platform.
**promoted** (7):
- Web bullet: "Every view should have a unique, shareable URL." → `web-view-should-have-shareable-url`: "On the web, every view SHOULD have a unique, shareable URL." (lower-case "should" raised to the keyword)
- "Use framework routing (React Router, Next.js routing, etc.)." → `typescript-use-framework-routing`: "In TypeScript, you SHOULD use framework routing (…)."
- "Declare protocol handlers in `Package.appxmanifest` and handle activation through the Windows App SDK lifecycle APIs." → `windows-declare-and-handle-protocol`: "On Windows, you SHOULD declare protocol handlers …"
- "Declare: `<uap:Protocol Name=\"myapp\"/>` in manifest" → `windows-declare-protocol-in-manifest`: "On Windows, you SHOULD declare `<uap:Protocol Name=\"myapp\"/>` in the manifest."
- "Handle via `AppInstance.GetActivatedEventArgs()` in `App.OnLaunched`" → `windows-handle-activation-in-onlaunched`: "On Windows, you SHOULD handle activation via …"
- "Parse URI to determine target page/state, navigate accordingly" → `windows-parse-uri-and-navigate`: "On Windows, you SHOULD parse the URI to determine the target page/state, and navigate accordingly."
- "Use `AppInstance.FindOrRegisterForKey()` for single-instancing (recommended for deep links)" → `windows-single-instance-for-deep-links`: "On Windows, you SHOULD use `AppInstance.FindOrRegisterForKey()` for single-instancing (recommended for deep links)."
**bars**: all three authored.
**contradictions**: the web intro bullet "Every view should have a unique, shareable URL." (now `web-view-should-have-shareable-url`, SHOULD) and the TypeScript part's "Every view MUST have a unique, shareable URL." (now `typescript-view-must-have-shareable-url`, MUST) give the same requirement at two levels. Both are kept as written.

## cookbook/guidelines/implementing/platform-integration/handoff-and-continuity
commit 7eb6b19a; rules 15; moved 14; obsolete 0
Same shape as background-tasks: intro bullets and per-platform imperatives become rules, each platform rule opening with its platform. The Android and Web parts held only instructions and are removed; the Apple part keeps its one fact sentence (Spotlight and Siri Suggestions eligibility) as `how-to`.
**promoted** (13): every rule but `support-continuity-features` and `continuity-must-feel-instant`, each a plain imperative read as SHOULD:
- "Capture enough state to reconstruct the user's context on the receiving device" → `capture-enough-state`: "You SHOULD capture enough state …"
- "Fall back gracefully when the receiving device lacks a feature the originating device had" → `fall-back-gracefully`: "You SHOULD fall back gracefully …"
- "Use deep links as the universal handoff payload — every platform can resolve a URL" → `use-deep-links-as-payload`: "You SHOULD use deep links …"
- "Use `NSUserActivity` to advertise the current activity." → `apple-advertise-with-nsuseractivity`: "On Apple platforms, you SHOULD use `NSUserActivity` …"
- "Set `isEligibleForHandoff = true` and populate `userInfo` with state needed to restore context." → `apple-enable-handoff-and-populate-userinfo`: "On Apple platforms, you SHOULD set …"
- "Implement `application(_:continue:)` on the receiving device." → `apple-implement-continue-on-receiver`: "On Apple platforms, you SHOULD implement …"
- "Support Universal Clipboard for cross-device copy/paste." → `apple-support-universal-clipboard`: "On Apple platforms, you SHOULD support Universal Clipboard …"
- "Use Google Play Services' Nearby Connections API or Chrome's cross-device features …" → `android-use-nearby-or-chrome-continuity`: "On Android, you SHOULD use …"
- "For Android-to-web continuity, use Firebase Dynamic Links or deep links …" → `android-use-links-that-resolve-natively-and-on-web`: "On Android, for Android-to-web continuity, you SHOULD use …"
- "Support clipboard sync through Google account integration." → `android-support-clipboard-sync`: "On Android, you SHOULD support clipboard sync …"
- "Use shared URLs as the primary continuity mechanism — …" → `web-use-shared-urls`: "On the web, you SHOULD use shared URLs …"
- "Support the Credential Management API …" → `web-support-credential-management`: "On the web, you SHOULD support …"
- "Consider WebSocket or server-sent events for real-time state sync between active sessions." → `web-consider-realtime-sync`: "On the web, you SHOULD consider WebSocket or server-sent events …"
**bars**: all three authored.
**contradictions**: none found.

## cookbook/guidelines/implementing/platform-integration/notifications
commit 0e8bbf38; rules 18; moved 17; obsolete 0
Same shape as background-tasks. The Apple, Android and Web parts are removed; the Windows part keeps its fact sentence (MSIX identity) as `how-to`. `cookr bump` refused the history table because its rows were out of order (1.0.0 listed above 2.0.0), so the two rows were swapped to make the table newest-first. No row text changed.
**promoted** (16): every rule but `use-platform-notification-system` and `must-be-actionable`, each a plain imperative read as SHOULD:
- "Request permission at the moment of relevance, not at launch" → `request-permission-at-relevance`: "You SHOULD request permission …"
- "Support notification grouping and categories to reduce clutter" → `support-grouping-and-categories`: "You SHOULD support …"
- "Respect Do Not Disturb, Focus modes, and quiet hours" → `respect-dnd-focus-and-quiet-hours`: "You SHOULD respect …"
- "Use `UNUserNotificationCenter` for local and push notifications." → `apple-use-unusernotificationcenter`: "On Apple platforms, you SHOULD use …"
- "Support actionable notifications with `UNNotificationCategory` and `UNNotificationAction`." → `apple-support-actionable-notifications`: "On Apple platforms, you SHOULD support …"
- "On iOS, support Notification Summary and Time Sensitive interruption levels." → `ios-support-summary-and-time-sensitive`: "On iOS, you SHOULD support …"
- "Use `NotificationCompat.Builder` for backward-compatible notifications." → `android-use-notificationcompat`: "On Android, you SHOULD use …"
- "Declare notification channels (`NotificationChannel`) so users can control categories individually." → `android-declare-channels`: "On Android, you SHOULD declare …"
- "Support Direct Reply, bubbles, and conversation style for messaging apps." → `android-support-messaging-styles`: "On Android, you SHOULD support …"
- "Use `AppNotificationManager` + `AppNotificationBuilder` fluent API for local notifications." → `windows-use-appnotification-api`: "On Windows, you SHOULD use …"
- "Support text, images, buttons with activation arguments, progress bars, and scheduled delivery." → `windows-support-rich-content`: "On Windows, you SHOULD support …"
- "Handle notification activation alongside protocol activation." → `windows-handle-activation`: "On Windows, you SHOULD handle …"
- "Use the Notifications API with service workers for push notifications." → `web-use-notifications-api-with-service-workers`: "On the web, you SHOULD use …"
- "Request permission contextually." → `web-request-permission-contextually`: "On the web, you SHOULD request permission contextually."
- "Support notification actions and badges via the Badging API." → `web-support-actions-and-badges`: "On the web, you SHOULD support …"
- "Fall back gracefully when notifications are denied or unavailable." → `web-fall-back-when-denied`: "On the web, you SHOULD fall back gracefully …"
**bars**: all three authored.
**contradictions**: none found.

## cookbook/guidelines/implementing/platform-integration/prefer-explicit-apple-apis
commit 35d3edd0; rules 4; moved 2; obsolete 0
The intro keeps its statement paragraph, whose two MUST sentences are also the first two rules. The five why-not-SwiftUI bullets move unchanged to a `rationale` part naming both rules. The macOS and iOS parts stay as they were, as `how-to`. Their opening "Use AppKit." and "Use UIKit." are carried at MUST by `must-use-appkit-and-uikit`, so they are not made into separate SHOULD rules. "When SwiftUI is required" keeps its surface list as `how-to`, and its last paragraph becomes two rules.
**promoted** (1):
- "Pin the minimum deployment target and avoid deprecated APIs to reduce generation ambiguity." → `pin-target-and-avoid-deprecated-apis`: "Where SwiftUI is required, you SHOULD pin the minimum deployment target and avoid deprecated APIs to reduce generation ambiguity."
- (`keep-swiftui-layer-thin` keeps its SHOULD; "In these cases" became "Where SwiftUI is required" so the rule reads on its own.)
**bars**: all three authored.
**contradictions**: none found.

## cookbook/guidelines/implementing/platform-integration/search-integration
commit 64db46d0; rules 18; moved 17; obsolete 0
Same shape as background-tasks. All four platform parts held only instructions, so all four are removed; each instruction is a rule that opens with its platform.
**promoted** (16): every rule but `content-discoverable-in-system-search` and `must-deep-link-indexed-items`, each a plain imperative read as SHOULD:
- "Index content that users would reasonably search for — …" → `index-what-users-search-for`: "You SHOULD index content …"
- "Keep the search index current — add items when created, remove when deleted" → `keep-index-current`: "You SHOULD keep the search index current — …"
- "Include rich metadata (thumbnails, descriptions, categories) for meaningful search results" → `include-rich-metadata`: "You SHOULD include rich metadata …"
- "Use Core Spotlight (`CSSearchableItem`, `CSSearchableItemAttributeSet`) to index content." → `apple-index-with-core-spotlight`: "On Apple platforms, you SHOULD use Core Spotlight …"
- "On iOS 17+, conform entities to `IndexedEntity` …" → `ios17-conform-to-indexedentity`: "On iOS 17+, you SHOULD conform entities …"
- "Support `NSUserActivity` donation for Handoff-eligible items …" → `apple-donate-nsuseractivity`: "On Apple platforms, you SHOULD support `NSUserActivity` donation …"
- "Use Firebase App Indexing or `AppIndexingApi` …" → `android-use-app-indexing`: "On Android, you SHOULD use …"
- "Declare searchable content in `searchable.xml` and implement `SearchableInfo`." → `android-declare-searchable-content`: "On Android, you SHOULD declare …"
- "Support Google Assistant via structured content markup." → `android-support-assistant-markup`: "On Android, you SHOULD support …"
- "Use the Windows Search indexer with `ISearchManager` and property handlers." → `windows-use-search-indexer`: "On Windows, you SHOULD use …"
- "Register file type associations and protocol handlers so content appears in Start menu search." → `windows-register-associations-and-protocols`: "On Windows, you SHOULD register …"
- "For UWP/WinUI, use `SearchPane` or in-app search with system integration." → `windows-uwp-winui-search`: "On Windows, for UWP/WinUI, you SHOULD use …"
- "Use structured data (JSON-LD, Schema.org) for search engine discoverability." → `web-use-structured-data`: "On the web, you SHOULD use …"
- "Implement OpenGraph and Twitter Card meta tags." → `web-implement-social-meta-tags`: "On the web, you SHOULD implement …"
- "Support the Web App Manifest for PWA search integration." → `web-support-web-app-manifest`: "On the web, you SHOULD support …"
- "Ensure server-side rendering or pre-rendering for crawlability." → `web-ensure-crawlability`: "On the web, you SHOULD ensure …"
**bars**: all three authored.
**contradictions**: none found.

## cookbook/guidelines/implementing/platform-integration/share-and-inter-app-data
commit 830b0d91; rules 24; moved 23; obsolete 0
Same shape as search-integration: all four platform parts held only instructions and are removed; each instruction is a rule that opens with its platform.
**promoted** (23): every rule but `participate-in-share-mechanisms`, each a plain imperative read as SHOULD:
- "Declare `<intent-filter>` with `ACTION_SEND` and appropriate MIME types to receive shared content." → `android-declare-send-intent-filter`: "On Android, you SHOULD declare `<intent-filter>` with `ACTION_SEND` and appropriate MIME types to receive shared content."
- "Use `Intent.createChooser()` to send." → `android-send-with-createchooser`: "On Android, you SHOULD use `Intent.createChooser()` to send."
- "Implement Direct Share targets with `ChooserTargetService` for frequently shared-to contacts." → `android-implement-direct-share`: "On Android, you SHOULD implement Direct Share targets with `ChooserTargetService` for frequently shared-to contacts."
- "Support `ContentProvider` for structured data sharing between apps." → `android-support-contentprovider`: "On Android, you SHOULD support `ContentProvider` for structured data sharing between apps."
- "Register as a document provider via `DocumentsProvider` for the system file picker." → `android-register-documentsprovider`: "On Android, you SHOULD register as a document provider via `DocumentsProvider` for the system file picker."
- "Implement `UIActivityViewController` (iOS) or `NSSharingServicePicker` (macOS) to share content." → `apple-share-with-system-picker`: "On Apple platforms, you SHOULD implement `UIActivityViewController` (iOS) or `NSSharingServicePicker` (macOS) to share content."
- "Create Share Extensions to receive content from other apps." → `apple-create-share-extensions`: "On Apple platforms, you SHOULD create Share Extensions to receive content from other apps."
- "Register UTI declarations in `Info.plist` for file type associations." → `apple-register-utis`: "On Apple platforms, you SHOULD register UTI declarations in `Info.plist` for file type associations."
- "Support drag and drop via `NSItemProvider` on iPadOS and macOS." → `apple-drag-and-drop-with-nsitemprovider`: "On Apple platforms, you SHOULD support drag and drop via `NSItemProvider` on iPadOS and macOS."
- "On macOS, support the Services menu via `NSServices` for system-wide text operations." → `macos-support-services-menu`: "On macOS, you SHOULD support the Services menu via `NSServices` for system-wide text operations."
- "Support both sending and receiving data through the platform share sheet" → `send-and-receive-via-share-sheet`: "You SHOULD support both sending and receiving data through the platform share sheet."
- "Register as a handler for relevant file types and UTIs/MIME types" → `register-for-relevant-types`: "You SHOULD register as a handler for relevant file types and UTIs/MIME types."
- "Support drag and drop for content that makes sense in multi-window contexts" → `support-drag-and-drop`: "You SHOULD support drag and drop for content that makes sense in multi-window contexts."
- "Validate all received data — inter-app data is an untrusted input boundary" → `validate-received-data`: "You SHOULD validate all received data — inter-app data is an untrusted input boundary."
- "Use the Web Share API (`navigator.share()`) to invoke the native share sheet." → `web-use-web-share-api`: "On the web, you SHOULD use the Web Share API (`navigator.share()`) to invoke the native share sheet."
- "Register as a share target in the Web App Manifest (`share_target`)." → `web-register-share-target`: "On the web, you SHOULD register as a share target in the Web App Manifest (`share_target`)."
- "Support drag and drop via the HTML Drag and Drop API." → `web-support-html-drag-and-drop`: "On the web, you SHOULD support drag and drop via the HTML Drag and Drop API."
- "Use the File Handling API to register as a handler for specific file types in PWAs." → `web-use-file-handling-api`: "On the web, you SHOULD use the File Handling API to register as a handler for specific file types in PWAs."
- "Implement the Share Contract (`DataTransferManager`) to send and receive content." → `windows-implement-share-contract`: "On Windows, you SHOULD implement the Share Contract (`DataTransferManager`) to send and receive content."
- "Register as a share target in the app manifest." → `windows-register-share-target`: "On Windows, you SHOULD register as a share target in the app manifest."
- "Support drag and drop via `DragDrop` APIs." → `windows-support-dragdrop`: "On Windows, you SHOULD support drag and drop via `DragDrop` APIs."
- "Register file type associations in `Package.appxmanifest` for Open With integration." → `windows-register-file-associations`: "On Windows, you SHOULD register file type associations in `Package.appxmanifest` for Open With integration."
- "Support clipboard with rich content formats." → `windows-support-rich-clipboard`: "On Windows, you SHOULD support clipboard with rich content formats."
**bars**: all three authored.
**contradictions**: none between rules. Note: "Validate all received data — inter-app data is an untrusted input boundary" has no keyword and no never/always, so `validate-received-data` is SHOULD; an owner may judge an untrusted input boundary to need MUST.

## cookbook/guidelines/implementing/platform-integration/shortcuts-and-automation
commit e5388eef; rules 5; moved 6; obsolete 0
Same shape as deep-linking. The intro lead-in ends with a period and joins the folded copy's rationale sentence; the folded duplicate copy is dropped. Its H1, "# Shortcuts and Automation", is mapped to the intro and `swift-use-appintents`, which together hold its words. The platform bullets move unchanged to a `how-to` part, "Automation mechanisms by platform". The Swift and Kotlin parts held only instructions and are removed.
**promoted** (4):
- "# Shortcuts and Automation" → `intro`; `swift-use-appintents`: "In Swift, you SHOULD use the `AppIntents` framework for Shortcuts and Siri integration."
- "Use `AppActions` for Google Assistant integration." → `kotlin-use-appactions`: "In Kotlin, you SHOULD use `AppActions` for Google Assistant integration."
- "Support `Intent`-based automation." → `kotlin-support-intent-automation`: "In Kotlin, you SHOULD support `Intent`-based automation."
- "Use the `AppIntents` framework for Shortcuts and Siri integration." → `swift-use-appintents`: "In Swift, you SHOULD use the `AppIntents` framework for Shortcuts and Siri integration."
- "On macOS, support AppleScript via `NSScriptCommand` where appropriate." → `macos-support-applescript`: "On macOS, you SHOULD support AppleScript via `NSScriptCommand` where appropriate."
**bars**: all three authored.
**contradictions**: none found.

## cookbook/guidelines/implementing/platform-integration/widgets-and-glanceable-surfaces
commit f78573c4; rules 20; moved 19; obsolete 0
Same shape as search-integration: all three platform parts held only instructions and are removed; each instruction is a rule that opens with its platform ("On Apple platforms", "On Android", "For a PWA").
**promoted** (18): every rule but `provide-widgets-for-glanceable-data` and `must-deep-link-on-tap`, each a plain imperative read as SHOULD ("Explore" and "consider" kept as the verbs under SHOULD):
- "Use Jetpack Glance with Compose-style APIs for home screen widgets." → `android-use-jetpack-glance`: "On Android, you SHOULD use Jetpack Glance with Compose-style APIs for home screen widgets."
- "Define widget metadata in `appwidget-provider` XML." → `android-define-appwidget-provider`: "On Android, you SHOULD define widget metadata in `appwidget-provider` XML."
- "Support resizable widgets and respond to `onUpdate` broadcasts." → `android-support-resize-and-onupdate`: "On Android, you SHOULD support resizable widgets and respond to `onUpdate` broadcasts."
- "Use `WorkManager` for background data refresh." → `android-refresh-with-workmanager`: "On Android, you SHOULD use `WorkManager` for background data refresh."
- "Follow Material You theming for visual consistency with the system." → `android-follow-material-you`: "On Android, you SHOULD follow Material You theming for visual consistency with the system."
- "Use WidgetKit with SwiftUI views." → `apple-use-widgetkit`: "On Apple platforms, you SHOULD use WidgetKit with SwiftUI views."
- "Support small, medium, and large widget families." → `apple-support-widget-families`: "On Apple platforms, you SHOULD support small, medium, and large widget families."
- "On iOS 17+, support interactive widgets with `AppIntent`-backed buttons and toggles." → `ios17-support-interactive-widgets`: "On iOS 17+, you SHOULD support interactive widgets with `AppIntent`-backed buttons and toggles."
- "On iOS 16+, support Lock Screen widgets." → `ios16-support-lock-screen-widgets`: "On iOS 16+, you SHOULD support Lock Screen widgets."
- "Use `TimelineProvider` for scheduled updates and `WidgetCenter.shared.reloadTimelines` for event-driven refresh." → `apple-use-timelineprovider-and-reload`: "On Apple platforms, you SHOULD use `TimelineProvider` for scheduled updates and `WidgetCenter.shared.reloadTimelines` for event-driven refresh."
- "For real-time status, use Live Activities with `ActivityKit` and the Dynamic Island on supported devices." → `apple-use-live-activities-for-realtime`: "On Apple platforms, for real-time status, you SHOULD use Live Activities with `ActivityKit` and the Dynamic Island on supported devices."
- "Show only the most important information — widgets are not miniature apps" → `show-only-most-important-information`: "You SHOULD show only the most important information — widgets are not miniature apps."
- "Support multiple widget sizes when the platform offers them" → `support-multiple-sizes`: "You SHOULD support multiple widget sizes when the platform offers them."
- "Tapping a widget MUST deep link to the relevant content in the app" → `must-deep-link-on-tap`: "Tapping a widget MUST deep link to the relevant content in the app."
- "Update widget content on a reasonable cadence — balance freshness against battery and data usage" → `update-on-reasonable-cadence`: "You SHOULD update widget content on a reasonable cadence — balance freshness against battery and data usage."
- "Use the Badging API for app icon notification counts." → `pwa-use-badging-api`: "For a PWA, you SHOULD use the Badging API for app icon notification counts."
- "Support periodic background sync via service workers for data freshness." → `pwa-support-periodic-background-sync`: "For a PWA, you SHOULD support periodic background sync via service workers for data freshness."
- "Explore experimental Widget API proposals where available." → `pwa-explore-widget-api-proposals`: "For a PWA, you SHOULD explore experimental Widget API proposals where available."
- "On desktop PWAs, consider system tray or menu bar presence where the platform allows." → `pwa-consider-tray-or-menu-bar`: "On desktop PWAs, you SHOULD consider system tray or menu bar presence where the platform allows."
**bars**: all three authored.
**contradictions**: none found.

## cookbook/guidelines/implementing/platform-integration/wsl
commit 0e909f63; rules 18; moved 3; obsolete 0
Every rule already held its keyword. Bullets that joined two requirements are split into separate rules: line endings into `must-set-in-gitattributes` and `shell-scripts-must-stay-lf`, Git into `install-git-per-file-system` and `must-configure-git-same-convention`, and interop into a `how-to` fact plus `must-check-program-exists`. The split rules name their subject, so "It" became "The line-ending convention" and "each" became "Each Git installation". The facts (automount root, `wslpath` outputs, permission translation, case sensitivity, interop defaults, configuration scope) stay in their own sections as `how-to`, and the cross-boundary-cost sentence moves to "Why this matters" (`rationale`), which also absorbs the folded copy's "Why this matters" paragraph. The folded review copy (introduction, files-and-paths, line-endings-2, permissions-and-case-2, interop-2, configuration) becomes the `review-focus` part, which keeps its opening "Review changes … against …" sentence verbatim. `roles lossless` refuses to mark it obsolete because the fold is part of the base.
**promoted**: none.
**bars**: `look-for` **moved**: the folded checklist's ten lines, each now naming its rule, plus eight authored lines for `windows-files-in-windows-fs`, `must-not-hardcode-mnt-c`, `must-start-distribution-first`, `must-use-one-line-ending-convention`, `install-git-per-file-system`, `must-configure-git-same-convention`, `must-check-program-exists` and `must-not-assume-networking-mode`. `a-complete-review-must-establish` and `a-build-must-establish` are authored.
**contradictions**: the folded checklist line "Code does not depend on Linux permissions of files on a Windows drive without the `metadata` option." has no matching rule; it sits under `set-automount-options`, the nearest rule. The checklist line "Per-directory case-sensitivity changes are intentional and documented." likewise has no rule of its own and sits under `should-not-differ-only-by-case`. Both are review text only and add no requirement; left as written.

## Unfinished

Nothing. All eighteen topics are committed.
