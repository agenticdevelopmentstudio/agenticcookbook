# Phase 2 batch 10 report

Nineteen planning/code-quality topics converted to roled parts. Every topic got a `rules` part, a `rationale` part and the three bar parts. No topic held text written for a reviewer (no checklist, no review section), so all three bar parts are **authored** in every topic. No `lossless.json` holds an `obsolete` entry, because `cookr roles lossless` refuses obsolete for a sentence of the topic's own base. Lead-ins such as "Apply these rules:" are `moved` to the rules they introduce instead. No topic is unfinished.

## How the lens topics were converted

Twelve topics are scope-group lenses with the same layout: intro, Signals and Indicators, Boundary Detection (numbered points with a bold head), Findings Format. In each one:

- **Boundary Detection** is gone. Each point is now one or more named rules. Its explanation sentences moved to `rationale`, naming the rule.
- **Signals and Indicators** and **Findings Format** stay word for word, with role `how-to`.
- **Explicit directives inside the signals** ("note …", "flag immediately", "treat them as one unit") were also added as SHOULD rules, and the signal text stayed where it was.
- **The intro stays whole.** GF-01 needs a statement after the H1. Any instruction in the intro is repeated as a rule.
- **Lowercase keywords:** "should", "should not", "must" and "may" in boundary points were read as the RFC level they spell. "Do not" and other plain imperatives were read as SHOULD NOT and SHOULD. Every such rule is listed as promoted, since the source had no uppercase RFC keyword.

The other seven topics (agent-instruction-files, dotnet-target-framework, essential-vs-accidental-complexity, kotlin-multiplatform, reuse-before-build, spec-driven-development, windows-ui-framework-and-deployment) had requirement sections. Those sections became `rules`, their reasons became `rationale`, and any part that is guidance only (a decision table, a cadence table, an example list) kept its text with role `how-to` or `examples`.

## Summary

| Topic | Commit | Rules | Promoted | Moved | Obsolete |
|---|---|---|---|---|---|
| agent-instruction-files | c0f63843 | 14 | 0 | 10 | 0 |
| algorithmic-complexity | 55b4a916 | 13 | 13 | 5 | 0 |
| app-interactions | 278e2f7e | 13 | 13 | 11 | 0 |
| cross-cutting-detection | b9a4f229 | 12 | 12 | 6 | 0 |
| dependency-clusters | 6e76ea4e | 11 | 11 | 7 | 0 |
| dotnet-target-framework | b7dc15d3 | 11 | 5 | 1 | 0 |
| essential-vs-accidental-complexity | 237fcf6d | 11 | 3 | 5 | 0 |
| framework-conventions | 3937ada3 | 8 | 8 | 6 | 0 |
| interface-cohesion | f25dad2f | 7 | 7 | 6 | 0 |
| kotlin-multiplatform | f883ed23 | 21 | 15 | 13 | 0 |
| lifecycle-patterns | 34680c64 | 15 | 15 | 8 | 0 |
| module-boundaries | 1d0390a9 | 8 | 8 | 8 | 0 |
| purpose-classification | 42d3c909 | 10 | 10 | 8 | 0 |
| reuse-before-build | c6336e2d | 8 | 3 | 8 | 0 |
| runtime-conditions | addd570e | 8 | 8 | 9 | 0 |
| spec-driven-development | a9ad2455 | 14 | 4 | 11 | 0 |
| system-dependencies | c496ebb2 | 6 | 6 | 6 | 0 |
| system-interactions | ae0b5c7d | 6 | 6 | 7 | 0 |
| windows-ui-framework-and-deployment | a461c67e | 25 | 10 | 18 | 0 |

## cookbook/guidelines/planning/code-quality/agent-instruction-files

**promoted**: None: every requirement already carried an RFC 2119 keyword.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/algorithmic-complexity

**promoted** (13 of 13 rules):
- "High-complexity algorithms warrant their own scope group. Code implementing O(n log n) or worse algorithms on large datasets is a distinct engineering concern — performance optimization, testing with large inputs, and benchmarking apply specifically to it." → `should-give-high-complexity-algorithms-own-scope-group`: "Code implementing O(n log n) or worse algorithms on large datasets SHOULD get its own scope group — high-complexity algorithms warrant their own scope group."
- "Caching layers are scope group candidates. A caching subsystem with its own eviction policy, invalidation logic, and hit/miss tracking is a meaningful independent component." → `should-treat-caching-layers-as-candidates`: "A caching subsystem with its own eviction policy, invalidation logic, and hit/miss tracking SHOULD be treated as a scope group candidate — caching layers are scope group candidates."
- "Computational code should not be mixed with I/O. Files that mix algorithm implementation with network calls or file system access conflate two different concerns — note this as a design smell." → `should-not-mix-computation-with-io`: "Computational code SHOULD NOT be mixed with I/O."
- "Computational code should not be mixed with I/O. Files that mix algorithm implementation with network calls or file system access conflate two different concerns — note this as a design smell." → `should-note-mixed-io-as-design-smell`: "Files that mix algorithm implementation with network calls or file system access SHOULD be noted as a design smell."
- "Simple CRUD code is not a boundary signal. Code that maps data structures to/from persistence formats and performs no interesting computation is not algorithmically significant — its boundaries come from `module-boundaries` or `purpose-classification`." → `should-not-treat-crud-as-boundary-signal`: "Simple CRUD code SHOULD NOT be treated as a boundary signal — simple CRUD code is not a boundary signal; its boundaries come from `module-boundaries` or `purpose-classification`."
- "Parallel computation implies a concurrency concern. Code using parallel execution primitives has distinct testing requirements (race conditions, thread safety) and likely belongs in its own scope group or must be flagged as a concurrency concern." → `must-scope-or-flag-parallel-computation`: "Code using parallel execution primitives likely belongs in its own scope group, or MUST be flagged as a concurrency concern — parallel computation implies a concurrency concern."
- "Explicit sort calls with custom comparators — note whether the comparator is simple (field comparison) or compound (multi-key, weighted)" → `should-note-comparator-shape`: "For explicit sort calls with custom comparators, the analysis SHOULD note whether the comparator is simple (field comparison) or compound (multi-key, weighted)."
- "BFS/DFS implementations — note cycle detection, visited sets" → `should-note-traversal-cycle-handling`: "For BFS/DFS implementations, the analysis SHOULD note cycle detection and visited sets."
- "Hash maps / dictionaries — O(1) lookup; note when used for frequency counting, grouping, or deduplication" → `should-note-hash-map-purpose`: "For hash maps / dictionaries, the analysis SHOULD note when they are used for frequency counting, grouping, or deduplication."
- "Sets for membership testing — note when used to eliminate duplicates from a stream" → `should-note-set-deduplication`: "For sets used for membership testing, the analysis SHOULD note when they are used to eliminate duplicates from a stream."
- "Triple or deeper nesting — O(n³) or worse; flag immediately" → `should-flag-triple-nesting-immediately`: "Triple or deeper loop nesting — O(n³) or worse — SHOULD be flagged immediately."
- "Floating point accumulation patterns — summation, running averages; note precision concerns" → `should-note-float-precision`: "For floating point accumulation patterns (summation, running averages), the analysis SHOULD note precision concerns."
- "Matrix multiplication — note if using accelerated libraries (Accelerate, BLAS, NumPy)" → `should-note-accelerated-matrix-libraries`: "For matrix multiplication, the analysis SHOULD note whether it uses accelerated libraries (Accelerate, BLAS, NumPy)."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/app-interactions

**promoted** (13 of 13 rules):
- "Delegation defines interface boundaries. A component with a clean delegate protocol is designed to be replaceable — the delegate protocol IS the interface." / "The component and its protocol belong in the same scope group; its concrete delegate implementations may belong elsewhere." → `should-scope-component-with-its-delegate-protocol`: "A component with a clean delegate protocol and that protocol SHOULD belong in the same scope group — delegation defines interface boundaries."
- "The component and its protocol belong in the same scope group; its concrete delegate implementations may belong elsewhere." → `may-scope-delegate-implementations-elsewhere`: "A component's concrete delegate implementations MAY belong in other scope groups."
- "Notification center usage is an implicit coupling signal. For every `NotificationCenter.post`, identify all files that observe that notification — they are implicitly coupled even if they have no import relationship." → `should-identify-notification-observers`: "For every `NotificationCenter.post`, the analysis SHOULD identify all files that observe that notification — notification center usage is an implicit coupling signal."
- "Singletons couple everything to everything. Any file that accesses a singleton is implicitly coupled to every other file that accesses the same singleton." / "Singletons accessed across many candidate groups indicate a cross-cutting dependency — flag for `cross-cutting-detection`." → `should-flag-cross-group-singletons`: "Singletons accessed across many candidate groups indicate a cross-cutting dependency and SHOULD be flagged for `cross-cutting-detection` — singletons couple everything to everything."
- "DI containers define the composition boundary. The DI container registration site is the architectural seam — it is where modules are wired together." / "Code on either side of the registration site belongs in separate scope groups." → `should-split-scope-groups-at-di-registration`: "Code on either side of the DI container registration site SHOULD belong in separate scope groups — DI containers define the composition boundary."
- "Coordinators are natural scope group boundaries. A coordinator object that manages navigation for a feature flow — and owns the child view controllers in that flow — is a natural scope group boundary." / "The coordinator and its owned screens form one group." → `should-group-coordinator-with-owned-screens`: "A coordinator object that manages navigation for a feature flow — and owns the child view controllers in that flow — SHOULD be treated as a natural scope group boundary, and the coordinator and its owned screens SHOULD form one group — coordinators are natural scope group boundaries."
- "Global state (Redux, MobX, Context) makes boundaries fuzzy. If all components read from a single global store, module boundaries are implicitly bypassed." / "Document which store slices each candidate group reads/writes — slices may suggest sub-boundaries." → `should-document-store-slices-per-group`: "Where components read from global state (Redux, MobX, Context), the analysis SHOULD document which store slices each candidate group reads/writes — slices may suggest sub-boundaries."
- "iOS: `NotificationCenter.default.addObserver()` / `post(name:)` — note the notification name, sender, and observer registration site." → `should-note-notification-endpoints`: "For `NotificationCenter` observers and posts, the analysis SHOULD note the notification name, sender, and observer registration site."
- "Reactive frameworks: `Combine` (Swift), `RxSwift`, `RxKotlin`, `RxJS` — publisher/subscriber chains; note where publishers are created vs where subscribers attach" → `should-note-publisher-and-subscriber-sites`: "For reactive frameworks (`Combine`, `RxSwift`, `RxKotlin`, `RxJS`), the analysis SHOULD note where publishers are created vs where subscribers attach."
- "Thread-local or actor-isolated state — note the isolation boundary" → `should-note-isolation-boundary`: "For thread-local or actor-isolated state, the analysis SHOULD note the isolation boundary."
- "DI containers: Swinject, Hilt, Dagger, Spring, Koin, inversify — note registration vs resolution sites" → `should-note-di-registration-and-resolution-sites`: "For DI containers, the analysis SHOULD note registration vs resolution sites."
- "Completion handler chains — `func doThing(completion: @escaping (Result) -> Void)` — note depth; chains of 3+ levels suggest refactoring to async/await" → `should-note-completion-chain-depth`: "For completion handler chains, the analysis SHOULD note depth; chains of 3+ levels suggest refactoring to async/await."
- "Promise chains — `.then().then().catch()` — note where error handling breaks the chain" → `should-note-promise-chain-error-breaks`: "For promise chains, the analysis SHOULD note where error handling breaks the chain."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/cross-cutting-detection

**promoted** (12 of 12 rules):
- "Cross-cutting concerns are noted, not isolated. When a concern appears across all scope groups, note it in findings as cross-cutting and move on." → `should-note-cross-cutting-concerns-not-isolate`: "When a concern appears across all scope groups, the analysis SHOULD note it in findings as cross-cutting and move on — cross-cutting concerns are noted, not isolated."
- "Do not create a scope group whose members are "all the places that call log()"." → `should-not-group-call-sites`: "The analysis SHOULD NOT create a scope group whose members are "all the places that call log()"."
- "Shared infrastructure gets exactly one scope group. If a concern has its own files (a Logger class, a SessionManager), those files form one scope group." → `should-give-shared-infrastructure-one-scope-group`: "If a concern has its own files (a Logger class, a SessionManager), those files SHOULD form exactly one scope group — shared infrastructure gets exactly one scope group."
- "The call sites in other groups are dependencies on this group, not members of it." → `should-treat-call-sites-as-dependencies`: "The call sites of shared infrastructure in other groups SHOULD be treated as dependencies on its group, not members of it."
- "Logging infrastructure vs logging call sites. The `OSLog` / `Logger` configuration file is infrastructure." → `should-classify-logging-configuration-as-infrastructure`: "The `OSLog` / `Logger` configuration file, or a centralized `LogManager` or `Logger` configuration file that sets up log destinations, SHOULD be classified as infrastructure — a single `Logging Infrastructure` unit; an `os.log("did the thing")` call in a view controller SHOULD NOT — logging infrastructure vs logging call sites."
- "Pervasive coupling is an architectural smell, not a decomposition strategy. If every scope group directly calls a `GlobalSingleton`, note the anti-pattern — the solution is to inject the dependency, not to merge all groups into one because they share the dependency." → `should-note-pervasive-coupling-anti-pattern`: "If every scope group directly calls a `GlobalSingleton`, the analysis SHOULD note the anti-pattern — pervasive coupling is an architectural smell, not a decomposition strategy."
- "Pervasive coupling is an architectural smell, not a decomposition strategy. If every scope group directly calls a `GlobalSingleton`, note the anti-pattern — the solution is to inject the dependency, not to merge all groups into one because they share the dependency." → `should-inject-not-merge-shared-dependency`: "The remedy for pervasive coupling SHOULD be to inject the dependency, not to merge all groups into one because they share the dependency."
- "Security/auth infrastructure is always its own scope group. Never treat auth enforcement as merely cross-cutting — the SessionManager and token lifecycle have real behavior and state and warrant their own scope group (separate from where auth checks are enforced)." → `must-give-auth-infrastructure-own-scope-group`: "Security/auth infrastructure — the SessionManager and token lifecycle — MUST always be its own scope group, separate from where auth checks are enforced."
- "Security/auth infrastructure is always its own scope group. Never treat auth enforcement as merely cross-cutting — the SessionManager and token lifecycle have real behavior and state and warrant their own scope group (separate from where auth checks are enforced)." → `must-not-treat-auth-as-merely-cross-cutting`: "The analysis MUST NOT ever treat auth enforcement as merely cross-cutting."
- "Event definition files (`AnalyticsEvents.swift`, `events.ts`) — shared data definitions; belong with the analytics infrastructure, not split across callers" → `should-group-event-definitions-with-analytics`: "Event definition files (`AnalyticsEvents.swift`, `events.ts`) SHOULD belong with the analytics infrastructure, not be split across callers."
- "A DI container that wires together all scope groups is a composition root — it is not itself a scope group in the functional sense, but it is a file (or files) that must be cataloged separately as the bootstrap/wiring layer" → `must-catalog-di-container-separately`: "A DI container that wires together all scope groups is a composition root and MUST be cataloged separately as the bootstrap/wiring layer."
- "Ask: "Does this code have its own state, lifecycle, or logic — or does it exist only as calls woven into other code?" Code with its own state, lifecycle, or meaningful logic is shared infrastructure." → `should-apply-the-definitive-test`: "To tell cross-cutting from shared infrastructure, the analysis SHOULD ask: "Does this code have its own state, lifecycle, or logic — or does it exist only as calls woven into other code?""

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: 
- Signals and Indicators lists "`guard isAuthenticated else { return }` scattered in individual handlers — these are policy enforcement points, not a scope group", while the boundary point now `must-not-treat-auth-as-merely-cross-cutting` says "Never treat auth enforcement as merely cross-cutting". The first reads as permission to leave scattered auth guards out of any group; the second says auth enforcement is never only cross-cutting. Left as written.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/dependency-clusters

**promoted** (11 of 11 rules):
- "High internal coupling ratio (>0.6) = strong scope group candidate. If 80% of a directory's imports are within the same directory, it is self-contained." → `should-treat-high-coupling-ratio-as-candidate`: "A directory or cluster with a high internal coupling ratio (>0.6) SHOULD be treated as a strong scope group candidate."
- "Low coupling ratio (<0.3) = likely belongs elsewhere. A file that imports mostly from other directories is probably a leaf consumer or a shared utility — consider merging it into the scope group it depends on most." → `should-consider-merging-low-ratio-files`: "A file with a low coupling ratio (<0.3) likely belongs elsewhere; the analysis SHOULD consider merging it into the scope group it depends on most."
- "Unidirectional dependency = separate scope groups. If layer A only imports layer B (never the reverse), A and B are separate concerns even if they live near each other." → `should-separate-unidirectional-layers`: "If layer A only imports layer B (never the reverse), A and B SHOULD be separate scope groups even if they live near each other — unidirectional dependency = separate scope groups."
- "High fan-in files are shared infrastructure. A file imported by 10+ other files across multiple candidate groups is a cross-cutting dependency — flag it for `cross-cutting-detection` rather than assigning it to one group." → `should-flag-high-fan-in-files`: "A file imported by 10+ other files across multiple candidate groups SHOULD be flagged for `cross-cutting-detection` rather than assigned to one group — high fan-in files are shared infrastructure."
- "Circular dependencies force co-location. Files in a cycle must remain in the same scope group until the cycle is resolved." → `must-co-locate-cyclic-files`: "Files in a cycle MUST remain in the same scope group until the cycle is resolved — circular dependencies force co-location."
- "Document the cycle as a refactoring target." → `should-document-cycles-as-refactoring-targets`: "Each import cycle SHOULD be documented as a refactoring target."
- "Star imports inflate apparent coupling. A `import com.example.util.*` may only use one symbol — do not count star imports as full coupling without verifying symbol usage." → `should-not-count-star-imports-as-full-coupling`: "Star imports inflate apparent coupling; the analysis SHOULD NOT count star imports as full coupling without verifying symbol usage."
- "Coupling ratio: internal / (internal + external)." → `should-compute-coupling-metrics`: "The analysis SHOULD compute the coupling metrics: internal coupling, external coupling, coupling ratio, fan-in and fan-out."
- "Identify the direction of dependencies: do files in directory A import files in directory B, or vice versa?" → `should-identify-dependency-direction`: "The analysis SHOULD identify the direction of dependencies: do files in directory A import files in directory B, or vice versa?"
- "Note any import cycles — these are candidates for refactoring, but in the short term they force the cyclic files into the same scope group since they cannot be independently deployed." → `should-note-import-cycles`: "The analysis SHOULD note any import cycles."
- "Bidirectional dependencies (A imports B and B imports A) indicate either tight cohesion (same scope group) or a design problem (circular dependency that should be resolved)." → `should-resolve-circular-dependencies`: "A circular dependency is a design problem that SHOULD be resolved."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/dotnet-target-framework

**promoted** (5 of 11 rules):
- "separate-tfm-from-langversion: Treat `<LangVersion>` as a separate decision from the TFM; raising the language version does not change the runtime or its support window." → `separate-tfm-from-langversion`: "A project SHOULD treat `<LangVersion>` as a separate decision from the TFM; raising the language version does not change the runtime or its support window."
- "Choose it from the published support cadence, not from habit." → `choose-tfm-from-support-cadence`: "A project SHOULD choose its `TargetFramework` (TFM) from the published support cadence, not from habit."
- "State the exact version and its end-of-support date in the project so the decision is auditable and reversible." → `record-version-and-end-of-support`: "A project SHOULD state the exact version and its end-of-support date in the project, and record them in the PR description, so the decision is auditable and reversible."
- "Re-read the support policy reference and confirm today's LTS/STS versions and dates." → `reverify-support-dates`: "Before choosing a TFM, an agent SHOULD re-read the support policy reference and confirm today's LTS/STS versions and dates — Microsoft updates them."
- "Library: set `<TargetFrameworks>` to the union of consumer requirements; justify each TFM in a comment." → `justify-each-library-tfm`: "A library SHOULD justify each TFM in `<TargetFrameworks>` in a comment."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: 
- `multi-target-libraries` gives the example `net8.0;net10.0`, while `avoid-eol-targets` says a project "MUST NOT newly target a framework whose end-of-support date has passed", and the support-cadence part dates .NET 8 end of support 2026-11-10, already past on 2026-11-19. The example now models a forbidden target. Left as written.
- Minor: the intro says "State the exact version and its end-of-support date in the project", while decision step 5 says "Record the chosen version … in the PR description". `record-version-and-end-of-support` carries both; the two places differ. Left as written.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/essential-vs-accidental-complexity

**promoted** (3 of 11 rules):
- "Use it to guide attention, not to mechanically sort lines of code." → `should-use-boundary-to-guide-attention`: "You SHOULD use the boundary to guide attention, not to mechanically sort lines of code."
- "Treat "AI eliminates complexity" as a forecast/marketing claim, not an established result." → `should-treat-ai-eliminates-complexity-as-a-claim`: "You SHOULD treat "AI eliminates complexity" as a forecast/marketing claim, not an established result."
- "Spend the time saved on agents harvesting the incidental on sharper problem decomposition, not on shipping more under-specified features (see `yagni`)." → `should-spend-saved-time-on-decomposition`: "You SHOULD spend the time saved on agents harvesting the incidental on sharper problem decomposition, not on shipping more under-specified features (see `yagni`)."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/framework-conventions

**promoted** (8 of 8 rules):
- "Framework-conventional units are the default scope group. When the codebase follows framework conventions, those conventions define the scope groups." → `should-default-to-conventional-units`: "When the codebase follows framework conventions, those conventions SHOULD define the scope groups — framework-conventional units are the default scope group."
- "Do not decompose below the conventional unit without strong evidence from other lenses." → `should-not-decompose-below-conventional-unit`: "The analysis SHOULD NOT decompose below the conventional unit without strong evidence from other lenses."
- "Cross-feature sharing elevates to its own scope group. A ViewModel or service referenced by three or more feature modules is no longer feature-local — it belongs in a shared scope group." → `should-elevate-cross-feature-units`: "A ViewModel or service referenced by three or more feature modules is no longer feature-local and SHOULD be placed in a shared scope group — cross-feature sharing elevates to its own scope group."
- "Deviations are flagged, not respected. If logic is placed in the wrong layer (business logic in a view), note the deviation — do not create a scope group that legitimizes the misplacement." → `should-flag-convention-deviations`: "When a codebase violates framework conventions — for example logic placed in the wrong layer (business logic in a view) — the analysis SHOULD note the deviation — deviations are flagged, not respected."
- "Deviations are flagged, not respected. If logic is placed in the wrong layer (business logic in a view), note the deviation — do not create a scope group that legitimizes the misplacement." → `should-not-legitimize-misplacement`: "The analysis SHOULD NOT create a scope group that legitimizes a misplacement."
- "Lazy-loaded modules are independent scope groups. Any module configured for lazy loading in Angular, Next.js dynamic imports, or Webpack code splitting is designed to be independently loadable — treat it as an independent scope group." → `should-treat-lazy-loaded-modules-as-independent`: "Any module configured for lazy loading in Angular, Next.js dynamic imports, or Webpack code splitting SHOULD be treated as an independent scope group — lazy-loaded modules are independent scope groups."
- "Plugin/extension registries are composition roots. The registry that loads and wires plugins is a separate scope group from the plugins themselves." → `should-separate-plugin-registry`: "The registry that loads and wires plugins SHOULD be a separate scope group from the plugins themselves — plugin/extension registries are composition roots."
- "MediatR: `Query`/`Command` + `Handler` — the request type and its handler are one unit; group by feature domain" → `should-group-mediatr-handlers-by-feature`: "MediatR `Query`/`Command` + `Handler` units SHOULD be grouped by feature domain."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/interface-cohesion

**promoted** (7 of 7 rules):
- "Protocol/interface + implementors form one unit. If a file defines a protocol and a second file is its primary concrete implementation, they belong in the same scope group unless the implementation is independently large enough to warrant separation (50+ files)." → `should-group-protocol-with-primary-implementation`: "If a file defines a protocol and a second file is its primary concrete implementation, they SHOULD be in the same scope group unless the implementation is independently large enough to warrant separation (50+ files) — protocol/interface + implementors form one unit."
- "Barrel files define the interface boundary. Everything a barrel re-exports is part of the same public surface." / "If the barrel re-exports from five subdirectories, those subdirectories share an interface and are candidates for a single scope group — unless they are large enough to warrant separate groups that share a common API layer." → `should-treat-barrel-reexports-as-one-candidate`: "If a barrel re-exports from five subdirectories, those subdirectories share an interface and SHOULD be treated as candidates for a single scope group — unless they are large enough to warrant separate groups that share a common API layer — barrel files define the interface boundary."
- "Shared types follow their primary consumer, not their definition file. A `UserProfile` struct defined in `Models/` but used only by the `Auth` module belongs in the `Auth` scope group." → `should-place-shared-types-with-primary-consumer`: "A shared type SHOULD be placed with its primary consumer, not its definition file: a `UserProfile` struct defined in `Models/` but used only by the `Auth` module belongs in the `Auth` scope group — shared types follow their primary consumer, not their definition file."
- "Fragmented interfaces are a smell. If the same logical interface is declared across three files with no organizing barrel, note this as a cohesion anomaly — it indicates the public surface has not been intentionally designed." → `should-note-fragmented-interfaces`: "If the same logical interface is declared across three files with no organizing barrel, the analysis SHOULD note this as a cohesion anomaly — fragmented interfaces are a smell."
- "Internal helpers are not interface. Private/internal/file-private symbols do not contribute to interface cohesion; they contribute to implementation cohesion analyzed by `dependency-clusters`." → `should-not-count-internal-helpers-as-interface`: "Private/internal/file-private symbols SHOULD NOT be counted toward interface cohesion; they contribute to implementation cohesion analyzed by `dependency-clusters` — internal helpers are not interface."
- "Pay special attention to protocol + extension pairs — the extension often lives in a separate file but is inseparable from the protocol definition." → `should-attend-to-protocol-extension-pairs`: "For Swift `public` / `open` declarations, the analysis SHOULD pay special attention to protocol + extension pairs."
- "Java `interface` + `abstract class` + primary implementation triads are a common pattern; treat them as one unit." → `should-treat-java-interface-triads-as-one-unit`: "Java `interface` + `abstract class` + primary implementation triads SHOULD be treated as one unit."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/kotlin-multiplatform

**promoted** (15 of 21 rules):
- "Keep platform-idiomatic UI (SwiftUI, Jetpack Compose, web framework) on the consuming side unless a shared-UI decision is made deliberately." → `should-keep-platform-ui-on-consumer`: "Teams SHOULD keep platform-idiomatic UI (SwiftUI, Jetpack Compose, web framework) on the consuming side unless a shared-UI decision is made deliberately."
- "treat it as a deliberate scope expansion" → `should-treat-shared-presentation-as-deliberate`: "A shared presentation layer SHOULD be treated as a deliberate scope expansion, not a default."
- "Apply boundaries per [adc.principle.manage-complexity-through-boundaries](cookbook:555ad5e1-800f-4848-8c58-6f726bdcb42b): expose narrow interfaces from the shared module so platforms stay swappable." → `should-expose-narrow-interfaces`: "Teams SHOULD apply boundaries per [adc.principle.manage-complexity-through-boundaries](cookbook:555ad5e1-800f-4848-8c58-6f726bdcb42b) and expose narrow interfaces from the shared module so platforms stay swappable."
- "Prefer interfaces plus dependency injection over `expect`/`actual` when the seam is non-trivial — it is easier to test and delete." → `should-prefer-interfaces-over-expect-actual`: "Teams SHOULD prefer interfaces plus dependency injection over `expect`/`actual` when the seam is non-trivial."
- "Use the hierarchical source-set structure (e.g., an intermediate `appleMain` shared by `iosMain`/`macosMain`) so common-but-not-universal code is not duplicated." → `should-use-hierarchical-source-sets`: "Teams SHOULD use the hierarchical source-set structure (e.g., an intermediate `appleMain` shared by `iosMain`/`macosMain`) so common-but-not-universal code is not duplicated."
- "Pin the CMP version explicitly in the build and re-check the release notes before relying on a specific UI feature." → `should-pin-cmp-version`: "Teams SHOULD pin the CMP version explicitly in the build."
- "Pin the CMP version explicitly in the build and re-check the release notes before relying on a specific UI feature." → `should-recheck-cmp-release-notes`: "Teams SHOULD re-check the release notes before relying on a specific UI feature."
- "iOS UI parity (text selection, native scrolling, accessibility/VoiceOver, gestures) is improving release-over-release but still evolving — FORECAST any unreleased item against the version you pin, and validate accessibility on-device." → `should-forecast-unreleased-ios-parity`: "Teams SHOULD FORECAST any unreleased iOS UI parity item against the version they pin."
- "iOS UI parity (text selection, native scrolling, accessibility/VoiceOver, gestures) is improving release-over-release but still evolving — FORECAST any unreleased item against the version you pin, and validate accessibility on-device." → `should-validate-accessibility-on-device`: "Teams using shared CMP UI SHOULD validate accessibility on-device."
- "Choose shared CMP UI only when the team accepts current iOS maturity and values UI reuse over fully native look-and-feel; otherwise keep SwiftUI on iOS and Compose on Android while still sharing all non-UI logic." → `should-choose-shared-ui-only-when-accepted`: "Teams SHOULD choose shared CMP UI only when the team accepts current iOS maturity and values UI reuse over fully native look-and-feel."
- "Present this as a deliberate decision per app, not a mandate." → `should-present-shared-ui-as-per-app-decision`: "Shared CMP UI SHOULD be presented as a deliberate decision per app, not a mandate."
- "Android consumes the shared module directly as a Gradle dependency. iOS consumes it as an Apple framework (XCFramework / CocoaPods / SPM) — design the public API to be Swift-friendly: avoid Kotlin-only constructs (sealed-class exhaustiveness, default args) at the boundary." → `should-design-swift-friendly-api`: "Teams SHOULD design the shared module's public API to be Swift-friendly: avoid Kotlin-only constructs (sealed-class exhaustiveness, default args) at the boundary."
- "Expose `suspend` functions and `Flow` through a documented bridge (e.g., a `Skie`-style or hand-written wrapper) so Swift callers get idiomatic async; do not leak raw coroutines across the boundary." → `should-bridge-suspend-and-flow`: "Teams SHOULD expose `suspend` functions and `Flow` through a documented bridge (e.g., a `Skie`-style or hand-written wrapper) so Swift callers get idiomatic async."
- "Expose `suspend` functions and `Flow` through a documented bridge (e.g., a `Skie`-style or hand-written wrapper) so Swift callers get idiomatic async; do not leak raw coroutines across the boundary." → `should-not-leak-raw-coroutines`: "Teams SHOULD NOT leak raw coroutines across the boundary."
- "Run platform builds in CI for every target the project ships; a green Android build does not prove the iOS framework links." → `should-build-every-target-in-ci`: "Teams SHOULD run platform builds in CI for every target the project ships."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/lifecycle-patterns

**promoted** (15 of 15 rules):
- "Shared init/deinit = same scope group. If object A creates object B in its `init` and destroys it in its `deinit`, A owns B and they belong together." → `should-group-owner-with-owned-objects`: "If object A creates object B in its `init` and destroys it in its `deinit`, A owns B and they SHOULD be in the same scope group — shared init/deinit = same scope group."
- "Subscription ownership defines lifecycle coupling. If object A stores a `Cancellable` / `DisposeBag` subscription to object B's stream, A's lifecycle bounds the subscription — A and B are lifecycle-coupled." → `should-treat-subscription-owners-as-lifecycle-coupled`: "If object A stores a `Cancellable` / `DisposeBag` subscription to object B's stream, the analysis SHOULD treat A and B as lifecycle-coupled — subscription ownership defines lifecycle coupling."
- "State machines are atomic. An explicit state machine — all states, transitions, and the object that executes them — is a single unit." / "Do not split state machines across scope groups." → `should-not-split-state-machines`: "An explicit state machine — all states, transitions, and the object that executes them — is a single unit, and the analysis SHOULD NOT split state machines across scope groups — state machines are atomic."
- "Session objects define natural scope group boundaries. A session — authentication session, network session, user session — and all objects that exist only for the duration of that session form one scope group." → `should-group-session-with-its-objects`: "A session — authentication session, network session, user session — and all objects that exist only for the duration of that session SHOULD form one scope group — session objects define natural scope group boundaries."
- "Weak references mark scope group edges. A `weak` reference from A to B means B does not own A." / "If A's lifecycle is independent of B's, they may belong in separate scope groups communicating through a narrow interface." → `may-separate-weakly-referenced-objects`: "If A holds a `weak` reference to B and A's lifecycle is independent of B's, they MAY be in separate scope groups communicating through a narrow interface — weak references mark scope group edges."
- "Disposal chain = lifecycle chain. Follow `Dispose()` / `cancel()` / `close()` calls — each object that disposes another is part of the same lifecycle chain." → `should-follow-disposal-chains`: "The analysis SHOULD follow `Dispose()` / `cancel()` / `close()` calls and treat each object that disposes another as part of the same lifecycle chain — disposal chain = lifecycle chain."
- "Timer lifecycle — `Timer.scheduledTimer()` must be invalidated; note where invalidation happens relative to the owning object's teardown" → `must-invalidate-timers`: "A `Timer.scheduledTimer()` MUST be invalidated."
- "Timer lifecycle — `Timer.scheduledTimer()` must be invalidated; note where invalidation happens relative to the owning object's teardown" → `should-note-timer-invalidation-site`: "The analysis SHOULD note where timer invalidation happens relative to the owning object's teardown."
- "Factory methods — `SomeClass.make()`, `SomeClass.create(with:)`, static constructors — note what the factory assembles" → `should-note-factory-assembly`: "For factory methods, the analysis SHOULD note what the factory assembles."
- "Two-phase initialization — `init()` followed by explicit `setup()` / `configure()` / `start()` — note what state exists between phases" → `should-note-state-between-init-phases`: "For two-phase initialization, the analysis SHOULD note what state exists between phases."
- "`deinit` (Swift), `finalize()` (Java), destructor `~ClassName()` (C++), `Dispose()` / `IDisposable` (C#), `close()` / `Closeable` (Java/Kotlin) — note what resources are released" → `should-note-released-resources`: "For `deinit`, `finalize()`, destructors, `Dispose()` and `close()`, the analysis SHOULD note what resources are released."
- "`onDestroy()`, `onStop()`, `viewWillDisappear()`, `componentWillUnmount()` — framework-managed teardown hooks; note what cleanup is performed" → `should-note-teardown-hook-cleanup`: "For framework-managed teardown hooks (`onDestroy()`, `onStop()`, `viewWillDisappear()`, `componentWillUnmount()`), the analysis SHOULD note what cleanup is performed."
- "Network session objects — `URLSession`, `OkHttpClient`, `HttpClient` — note whether sessions are per-request or long-lived" → `should-note-session-scope`: "For network session objects, the analysis SHOULD note whether sessions are per-request or long-lived."
- "State transition methods — `func transitionTo(_ state: State)` — note valid transitions" → `should-note-valid-transitions`: "For state transition methods, the analysis SHOULD note valid transitions."
- "`NotificationCenter` observer registration — note whether removal is explicit (`removeObserver`) or managed by token disposal" → `should-note-observer-removal`: "For `NotificationCenter` observer registration, the analysis SHOULD note whether removal is explicit (`removeObserver`) or managed by token disposal."

The lowercase "`Timer.scheduledTimer()` must be invalidated" in Signals and Indicators was read as MUST (`must-invalidate-timers`); the signal text stays in place.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/module-boundaries

**promoted** (8 of 8 rules):
- "Each independently declared build target or package is a primary scope group candidate." / "One target, one candidate. If the build system declares it separately, treat it as a candidate scope group regardless of size." / "Apply these rules:" → `should-treat-each-declared-target-as-candidate`: "Each independently declared build target or package SHOULD be treated as a primary scope group candidate regardless of size: if the build system declares it separately, it is a candidate — one target, one candidate."
- "Merge trivial wrappers. If a target contains only re-exports of another target with no logic of its own, it may belong with the target it wraps." / "Apply these rules:" → `may-merge-trivial-wrappers`: "If a target contains only re-exports of another target with no logic of its own, it MAY be merged with the target it wraps — merge trivial wrappers."
- "Split large monolithic targets. A single build target containing 200+ files likely conflates multiple concerns." / "Flag for secondary analysis using `interface-cohesion` and `dependency-clusters` lenses." / "Apply these rules:" → `should-flag-large-monolithic-targets`: "A single build target containing 200+ files SHOULD be flagged for secondary analysis using the `interface-cohesion` and `dependency-clusters` lenses — split large monolithic targets."
- "Test targets follow their main target. `AuthTests` belongs with `Auth` — do not create a separate scope group for test targets unless they test multiple main targets." / "Apply these rules:" → `should-group-test-targets-with-main-target`: "A test target SHOULD follow its main target: `AuthTests` belongs with `Auth` — test targets follow their main target."
- "Test targets follow their main target. `AuthTests` belongs with `Auth` — do not create a separate scope group for test targets unless they test multiple main targets." / "Apply these rules:" → `should-not-separate-test-targets`: "The analysis SHOULD NOT create a separate scope group for test targets unless they test multiple main targets."
- "Vendor/third-party directories are excluded. `node_modules/`, `Pods/`, `vendor/`, `.build/` — these are external dependencies, not scope groups." / "Apply these rules:" → `should-exclude-vendor-directories`: "Vendor/third-party directories — `node_modules/`, `Pods/`, `vendor/`, `.build/` — SHOULD be excluded: these are external dependencies, not scope groups."
- "Directories named `core`, `common`, `shared`, or `util` at the root of a module often represent deliberate cross-cutting infrastructure — note but do not automatically split them" → `should-note-shared-directories`: "Directories named `core`, `common`, `shared`, or `util` at the root of a module SHOULD be noted, as they often represent deliberate cross-cutting infrastructure."
- "Directories named `core`, `common`, `shared`, or `util` at the root of a module often represent deliberate cross-cutting infrastructure — note but do not automatically split them" → `should-not-auto-split-shared-directories`: "The analysis SHOULD NOT automatically split `core`, `common`, `shared`, or `util` directories."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/purpose-classification

**promoted** (10 of 10 rules):
- "Purpose categories — classify each file into exactly one primary category:" → `should-classify-each-file-into-one-category`: "The analysis SHOULD classify each file into exactly one primary purpose category."
- "Purpose-coherent groups are correctly scoped. If every file in a candidate scope group has the same primary purpose, the group is coherent." / "Different purposes within the same group indicate either misclassification or a need to split." → `should-keep-groups-purpose-coherent`: "Every file in a candidate scope group SHOULD have the same primary purpose; different purposes within the same group indicate either misclassification or a need to split — purpose-coherent groups are correctly scoped."
- "Scope groups whose files serve multiple unrelated purposes are incoherent and should be split." → `should-split-incoherent-groups`: "Scope groups whose files serve multiple unrelated purposes are incoherent and SHOULD be split."
- "Each scope group should have one sentence purpose. Test: can you complete "This scope group exists to ___" with a single clear answer?" → `should-have-one-sentence-purpose`: "Each scope group SHOULD have one sentence purpose."
- "Mixed-purpose files are a smell — document them and recommend refactoring, but do not create a mixed-purpose scope group to accommodate them." → `should-document-mixed-purpose-files`: "Mixed-purpose files are a smell, and the analysis SHOULD document them and recommend refactoring."
- "Mixed-purpose files are a smell — document them and recommend refactoring, but do not create a mixed-purpose scope group to accommodate them." → `should-not-create-mixed-purpose-groups`: "The analysis SHOULD NOT create a mixed-purpose scope group to accommodate mixed-purpose files."
- "Mixed-purpose files mark the fault line. A file that mixes UI and networking is a symptom — the fault line is between those two purposes." / "Recommend splitting the file along that line." → `should-split-mixed-files-along-fault-line`: "For a file that mixes purposes (UI and networking, say), the analysis SHOULD recommend splitting the file along the fault line between those two purposes — mixed-purpose files mark the fault line."
- "Configuration is rarely its own scope group. Configuration files belong with the components they configure, unless they configure the entire application (in which case they belong in an application bootstrap scope group)." → `should-place-configuration-with-its-components`: "Configuration files SHOULD belong with the components they configure, unless they configure the entire application, in which case they SHOULD belong in an application bootstrap scope group — configuration is rarely its own scope group."
- "Testing infrastructure belongs adjacent to its subject. Test mocks and fakes belong in the same scope group as the types they mock, or in a shared test infrastructure scope group if used across multiple groups." → `should-place-test-infrastructure-with-subject`: "Test mocks and fakes SHOULD belong in the same scope group as the types they mock, or in a shared test infrastructure scope group if used across multiple groups — testing infrastructure belongs adjacent to its subject."
- "Build tooling is always its own scope group. Build scripts, code generators, and Gradle/Webpack configuration are not part of any runtime scope group — they form a `Build Tooling` scope group that is excluded from runtime analysis." → `must-give-build-tooling-own-group`: "Build tooling MUST always be its own scope group: build scripts, code generators, and Gradle/Webpack configuration are not part of any runtime scope group — they form a `Build Tooling` scope group that is excluded from runtime analysis."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/reuse-before-build

**promoted** (3 of 8 rules):
- "Before building non-trivial functionality, spend a moment to look for what already solves it." → `should-look-for-existing-solution`: "Before building non-trivial functionality, you SHOULD spend a moment to look for what already solves it."
- "Check before adding anything." → `should-check-dependencies-before-adding`: "You SHOULD check the dependencies you already have before adding anything."
- "Do not install a package name an AI suggested without verifying it — hallucinated and typosquatted names ("slopsquatting") are a real supply-chain attack surface." → `should-not-install-unverified-ai-suggested-package`: "You SHOULD NOT install a package name an AI suggested without verifying it."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: 
- Level mismatch, not a conflict: "Do not install a package name an AI suggested without verifying it" has no keyword and became SHOULD NOT (`should-not-install-unverified-ai-suggested-package`), but it sits beside "You MUST confirm a candidate package actually exists …" (`must-verify-candidate-package`), which already requires the same check at MUST. A judge may want the two at one level. Left as written.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/runtime-conditions

**promoted** (8 of 8 rules):
- "Permission-gated code clusters. Files that all request or check the same permission belong together — they share an operational prerequisite and a failure mode when the permission is denied." → `should-group-permission-gated-code`: "Files that all request or check the same permission SHOULD be in the same scope group — permission-gated code clusters."
- "Entitlements define hard boundaries. Code that requires an entitlement cannot run without it." / "If one candidate group requires an entitlement that others do not, they are distinct operational units." → `should-separate-entitlement-groups`: "If one candidate group requires an entitlement that others do not, they SHOULD be treated as distinct operational units — entitlements define hard boundaries."
- "OS version gates mark optional feature envelopes. Code behind `@available(iOS 16.0, *)` is conditionally executable — flag it as a version-gated feature within its scope group." → `should-flag-version-gated-features`: "Code behind an OS version gate such as `@available(iOS 16.0, *)` SHOULD be flagged as a version-gated feature within its scope group — OS version gates mark optional feature envelopes."
- "If it constitutes a large portion of the group, it may warrant its own scope group." → `may-give-large-version-gated-code-own-group`: "If version-gated code constitutes a large portion of the group, it MAY warrant its own scope group."
- "Environment-specific code belongs in a configuration scope group. Code that reads environment variables, loads config files, or applies build-time conditionals is configuration infrastructure — it typically belongs in one scope group rather than scattered." → `should-group-environment-specific-code`: "Environment-specific code — code that reads environment variables, loads config files, or applies build-time conditionals — SHOULD typically belong in one configuration scope group rather than scattered."
- "Document the flags but do not create scope groups around unenabled code paths." → `should-document-feature-flags`: "The analysis SHOULD document the feature flags in feature-flagged code."
- "Feature-flagged code is pre-production. Large blocks of feature-flagged code indicate in-flight work." / "Document the flags but do not create scope groups around unenabled code paths." → `should-not-group-unenabled-code-paths`: "The analysis SHOULD NOT create scope groups around unenabled code paths — feature-flagged code is pre-production."
- "Remote config dependencies imply a network prerequisite. Code that requires a remote config fetch before it can function has an implicit startup dependency — note this as an operational ordering constraint." → `should-note-remote-config-ordering`: "Code that requires a remote config fetch before it can function SHOULD be noted as an operational ordering constraint — remote config dependencies imply a network prerequisite."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/spec-driven-development

**promoted** (4 of 14 rules):
- "Separate research and planning from execution: produce a written, self-contained spec before any non-trivial change, then implement against it." → `should-implement-against-the-spec`: "After producing the spec, you SHOULD implement against it; the spec — not the conversation history or the agent's working memory — is the source of truth."
- "Right-size the ceremony to the change." → `should-right-size-ceremony`: "You SHOULD right-size the ceremony to the change."
- "Adopt the *methodology*; do NOT hard-code a specific tool, command set, or vendor flow into your process." → `should-adopt-the-methodology`: "You SHOULD adopt the *methodology* of the staged flow."
- "Adopt the *methodology*; do NOT hard-code a specific tool, command set, or vendor flow into your process." → `should-not-hard-code-tool`: "You SHOULD NOT hard-code a specific tool, command set, or vendor flow into your process."

The table of required spec sections is now the sub-bullets of `must-include-required-sections`, one per section. The table's "Out of scope" reason ("This is the highest-signal section for keeping an agent on task.") moved to `rationale`.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/system-dependencies

**promoted** (6 of 6 rules):
- "Heavy OS framework usage marks a boundary. Files that import three or more OS-specific frameworks are tightly coupled to the platform runtime and likely belong in a platform-specific scope group." → `should-place-heavy-os-framework-users-in-platform-group`: "Files that import three or more OS-specific frameworks SHOULD typically be placed in a platform-specific scope group — heavy OS framework usage marks a boundary."
- "Hardware APIs are natural boundaries. Camera, GPS, Bluetooth, and biometric code has distinct permission requirements and testing needs — group these files together and mark the scope group as hardware-dependent." → `should-group-hardware-api-code`: "Camera, GPS, Bluetooth, and biometric code files SHOULD be grouped together — hardware APIs are natural boundaries."
- "Hardware APIs are natural boundaries. Camera, GPS, Bluetooth, and biometric code has distinct permission requirements and testing needs — group these files together and mark the scope group as hardware-dependent." → `should-mark-hardware-dependent-groups`: "The analysis SHOULD mark a scope group of hardware API code as hardware-dependent."
- "Network and persistence are separate concerns. Files that talk to the network and files that write to local storage are often conflated — separate them unless they are part of a unified data synchronization layer." → `should-separate-network-and-persistence`: "Files that talk to the network and files that write to local storage SHOULD be separated unless they are part of a unified data synchronization layer — network and persistence are separate concerns."
- "Third-party SDK boundaries. If a third-party SDK is touched by more than 2–3 files, those files likely form a wrapper/adapter scope group that isolates the SDK from the rest of the codebase." / "Identify this group explicitly." → `should-identify-sdk-wrapper-groups`: "If a third-party SDK is touched by more than 2–3 files, those files likely form a wrapper/adapter scope group that isolates the SDK from the rest of the codebase, and the analysis SHOULD identify this group explicitly — third-party SDK boundaries."
- "System dependencies that appear in many groups are cross-cutting. Logging frameworks and analytics SDKs that appear across all candidate groups are not boundaries — they are cross-cutting concerns (see `cross-cutting-detection`)." → `should-not-treat-widespread-dependencies-as-boundaries`: "Logging frameworks and analytics SDKs that appear across all candidate groups SHOULD NOT be treated as boundaries — they are cross-cutting concerns (see `cross-cutting-detection`); system dependencies that appear in many groups are cross-cutting."

"likely belong in a platform-specific scope group" was read as SHOULD (`should-place-heavy-os-framework-users-in-platform-group`, "SHOULD typically be placed"). "are not boundaries — they are cross-cutting concerns" became SHOULD NOT (`should-not-treat-widespread-dependencies-as-boundaries`), because `cookr roles lossless` refuses a matched clause that drops the negation.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/system-interactions

**promoted** (6 of 6 rules):
- "Lifecycle callback implementations are natural scope group anchors. Files that implement `UIApplicationDelegate`, `AndroidApplication`, or equivalent are the entry points of the application — they are architectural seams where scope groups plug in." → `should-anchor-groups-on-lifecycle-callbacks`: "Files that implement `UIApplicationDelegate`, `AndroidApplication`, or equivalent SHOULD be treated as natural scope group anchors — the architectural seams where scope groups plug in."
- "Each OS integration point is a potential boundary. A file that handles push notification payloads is in the notification scope group." / "Treat each OS integration point as a distinct concern." → `should-treat-each-os-integration-point-as-distinct`: "The analysis SHOULD treat each OS integration point as a distinct concern and a potential boundary."
- "Background execution code belongs in its own scope group. Background tasks have distinct lifecycle, resource, and testing constraints." → `should-give-background-code-own-group`: "Background execution code SHOULD belong in its own scope group."
- "Code that runs in background contexts should not be mixed with foreground UI code." → `should-not-mix-background-with-foreground-ui`: "Code that runs in background contexts SHOULD NOT be mixed with foreground UI code."
- "IPC code is infrastructure. An app extension that communicates with its host app via shared container is infrastructure-layer code — it should be grouped with other infrastructure, not with the feature it serves." → `should-group-ipc-with-infrastructure`: "IPC code — such as an app extension that communicates with its host app via shared container — is infrastructure-layer code and SHOULD be grouped with other infrastructure, not with the feature it serves."
- "Lifecycle callbacks that dispatch to many subsystems are composition roots. An `AppDelegate` that calls 15 different services is a composition root, not a feature — it belongs in an `App` or `Bootstrap` scope group that wires everything together." → `should-place-composition-roots-in-bootstrap-group`: "A lifecycle callback that dispatches to many subsystems — an `AppDelegate` that calls 15 different services — is a composition root, not a feature, and SHOULD belong in an `App` or `Bootstrap` scope group that wires everything together."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/planning/code-quality/windows-ui-framework-and-deployment

**promoted** (10 of 25 rules):
- "Make both explicitly and early — they shape API access, distribution, and migration cost for the life of the app." → `should-make-both-decisions-explicitly-and-early`: "You SHOULD make both the UI framework and the deployment model decisions explicitly and early."
- "Pick the framework from target devices and existing investment, not from hype." → `should-pick-framework-from-targets-and-investment`: "You SHOULD pick the framework from target devices and existing investment, not from hype."
- "Build with Visual Studio + MSBuild — the only officially supported toolchain." → `should-build-winui3-with-visual-studio-msbuild`: "You SHOULD build a new WinUI 3 app with Visual Studio + MSBuild — the only officially supported toolchain."
- "Keep WPF and modernize in place unless there is a concrete reason to move." → `should-keep-wpf-and-modernize`: "For an existing WPF app, you SHOULD keep WPF and modernize in place unless there is a concrete reason to move."
- "Stay unless a concrete need forces a change." → `should-keep-winforms`: "For an existing WinForms app, you SHOULD stay unless a concrete need forces a change."
- "Treat UWP as feature-frozen, not abandoned." → `should-treat-uwp-as-feature-frozen`: "You SHOULD treat UWP as feature-frozen, not abandoned."
- "Cross-platform native: consider .NET MAUI (produces a WinUI app on Windows) or React Native for Desktop." → `should-consider-maui-or-react-native-for-cross-platform`: "For cross-platform native, you SHOULD consider .NET MAUI (produces a WinUI app on Windows) or React Native for Desktop."
- "Do not pick unpackaged for these apps." → `should-not-pick-unpackaged-for-identity-apps`: "You SHOULD NOT pick unpackaged for apps that need identity-gated features."
- "Defer the framework choice no later than the first UI module; defer the deployment choice no later than the first identity-gated feature." → `should-settle-framework-by-first-ui-module`: "You SHOULD defer the framework choice no later than the first UI module."
- "Defer the framework choice no later than the first UI module; defer the deployment choice no later than the first identity-gated feature." → `should-settle-deployment-by-first-identity-feature`: "You SHOULD defer the deployment choice no later than the first identity-gated feature."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: 
- "Defer the framework choice no later than the first UI module; defer the deployment choice no later than the first identity-gated feature." reads as "decide no later than", but says "defer". The rules keep the word "defer" (`should-settle-framework-by-first-ui-module`, `should-settle-deployment-by-first-identity-feature`); the names say what the sentence seems to mean. A judge should check. Left as written.
- Level mismatch: `must-have-package-identity-for-gated-features` (MUST have package identity) sits beside the keyword-less "Do not pick unpackaged for these apps.", promoted to SHOULD NOT (`should-not-pick-unpackaged-for-identity-apps`). The MUST already forbids it. Left as written.
- `must-bootstrap-unpackaged-apps` keeps "; set `<WindowsPackageType>None</WindowsPackageType>` in the project" inside the MUST sentence it came from, so that keyword-less clause is read under the sentence's MUST, not promoted on its own.

**unfinished**: none.
