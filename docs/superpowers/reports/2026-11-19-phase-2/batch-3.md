# Phase 2 batch 3 report

Twenty topics, converted to roled parts with named rules and the three bar parts: four on concurrency, nine on data, one on documentation, four on infrastructure and two on internationalization. The change is to format only. No research was added, and no rule's substance changed. Each topic has one commit, made with `commit_topic.py`.

## Across the batch

- **Keyword readings.**
  - "never" is read as MUST NOT, and "always" as MUST.
  - A plain imperative, or "needs", is read as SHOULD.
  - "Do not" / "Do NOT" is read as SHOULD NOT, unless a section heading puts it under MUST NOT.
  - Each topic's notes name the rules that took a level from these readings.
- **Bar wording.** Review-bar lines open with "whether". A build-bar line for a SHOULD rule ends with "or the code/work says why not", so the bar adds no requirement beyond the rule's own level.
- **Folded duplicates.** Several intros held two H1 blocks, or a part was duplicated, left from an earlier fold of duplicate topic copies: concurrency, localization and rtl-support. Each intro keeps one H1 and one statement. `cookr roles lossless` refuses `obsolete` for a sentence of a topic's own base, so the second H1 is mapped as moved to the intro. That is why every obsolete count is 0.
- **Existing names kept.** Where a topic already had named bullets (kubernetes-configuration, writing-comments-and-docs and others), each name is kept unchanged.
- **FM-13 check.** After the approve.py FM-13 narrowing, none of these topics' base text at `0005775` contains "placeholder", "TODO", "TBD" or "FIXME". So no source word was ever respelled, and nothing needed restoring.
- **Contradictions.** None found in any topic.
- **Unfinished.** Nothing.

## cookbook/guidelines/implementing/concurrency/concurrency

20 rules. The intro held two H1 blocks (the platform list under "No blocking the main thread", then a "# Concurrency" paragraph with the topic's three keyword rules). The intro keeps the first H1 and its statement, now ending in a period. The platform list is a `how-to` part (`platform-async-primitives`), and each platform section's instructions are named rules. The Kotlin, C# and Windows code blocks are `examples` parts. The Swift and TypeScript sections held only rules, so their parts are gone.

**promoted** (14 rules):
- "Use Swift Concurrency (`async`/`await`, `Task`, actors) for all async work." → `should-use-swift-concurrency`: "In Swift, SHOULD use Swift Concurrency (`async`/`await`, `Task`, actors) for all async work."
- "Use `@MainActor` for UI updates." → `should-use-mainactor-for-ui-updates`: "In Swift, SHOULD use `@MainActor` for UI updates."
- "Use Kotlin Coroutines for all async work." → `should-use-kotlin-coroutines`: "In Kotlin, SHOULD use Kotlin Coroutines for all async work."
- "Run I/O on `Dispatchers.IO`." → `should-run-kotlin-io-on-dispatchers-io`: "In Kotlin, SHOULD run I/O on `Dispatchers.IO`."
- "Use `viewModelScope` for ViewModel-scoped coroutines." → `should-use-viewmodelscope`: "In Kotlin, SHOULD use `viewModelScope` for ViewModel-scoped coroutines."
- "Use `Promise`/`async`/`await` for async operations." → `should-use-promises-for-async`: "In TypeScript, SHOULD use `Promise`/`async`/`await` for async operations."
- "Use Web Workers for CPU-intensive tasks." → `should-use-web-workers-for-cpu-work`: "In TypeScript, SHOULD use Web Workers for CPU-intensive tasks."
- "Use `async`/`await` for all async work." (C#) → `should-use-async-await-in-csharp`: "In C#, SHOULD use `async`/`await` for all async work."
- "`ConfigureAwait(false)` in library code to avoid capturing the synchronization context" → `should-configure-await-false-in-library-code`: "In C# library code, SHOULD use `ConfigureAwait(false)` to avoid capturing the synchronization context."
- "Use `ValueTask<T>` only when the method frequently completes synchronously" → `should-use-valuetask-only-when-mostly-synchronous`: "In C#, SHOULD use `ValueTask<T>` only when the method frequently completes synchronously."
- "Use `Task.Run` for CPU-bound work, never on the UI thread" → split in two:
  - `should-use-task-run-for-cpu-work`: "In C#, SHOULD use `Task.Run` for CPU-bound work."
  - `must-not-run-cpu-work-on-ui-thread`: "In C#, CPU-bound work MUST NOT run on the UI thread." ("never" read as MUST NOT; the source's "never on the UI thread" is read as the CPU-bound work, so a judge should check it.)
- "Use `DispatcherQueue.TryEnqueue` to marshal work back to the UI thread from background tasks" → `should-marshal-ui-work-with-dispatcherqueue`: "For WinUI 3 specifically, SHOULD use `DispatcherQueue.TryEnqueue` to marshal work back to the UI thread from background tasks."
- "Never access UI elements from non-UI threads" → `must-not-access-ui-from-non-ui-threads`: "For WinUI 3 specifically, UI elements MUST NOT be accessed from non-UI threads."

The four platform sections' "Never block the main thread." map to `must-not-block-main-thread`, which already stood at MUST NOT in the intro. The rule now opens with those words. The base's second heading "# Concurrency" cannot be obsolete, because `roles lossless` refuses obsolete for a topic's own base. It maps to the `platform-async-primitives` part, now headed "Platform Concurrency Primitives".

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/concurrency/immutability

19 rules. The intro keeps its first sentence ("Mutable shared state is the root cause of most concurrency bugs.") as the statement. Its three keyword sentences are now rules, kept verbatim. The Kotlin and TypeScript sections held only rules, so their parts are gone. The C# code block is the `examples` part `c`.

**promoted** (16 rules):
- "Use `val` by default." → `should-use-val-by-default`: "In Kotlin, SHOULD use `val` by default."
- "Use `data class` for value types." → `should-use-data-class-for-value-types`: "In Kotlin, SHOULD use `data class` for value types."
- "Introduce `var` only when mutation is required, and contain mutable state behind `StateFlow`." → split in two:
  - `should-introduce-var-only-when-required`: "In Kotlin, SHOULD introduce `var` only when mutation is required."
  - `should-contain-mutable-state-behind-stateflow`: "In Kotlin, SHOULD contain mutable state behind `StateFlow`."
- "Use `const` by default." → `should-use-const-by-default`: "In TypeScript, SHOULD use `const` by default."
- "Use `var`/`let` only when mutation is required." → `should-use-var-or-let-only-when-required`: "In TypeScript, SHOULD use `var`/`let` only when mutation is required."
- "Prefer `useState` (React) for contained mutable state." → `should-prefer-usestate-for-mutable-state`: "In TypeScript, SHOULD prefer `useState` (React) for contained mutable state."
- "Use `readonly` fields and `readonly struct` by default. Introduce mutability only when required." → `should-use-readonly-by-default`: "In C#, SHOULD use `readonly` fields and `readonly struct` by default, and introduce mutability only when required."
- "Prefer `System.Collections.Immutable` (`ImmutableList<T>`, `ImmutableDictionary<K,V>`) for shared collections" → `should-prefer-immutable-collections`: "In C#, SHOULD prefer `System.Collections.Immutable` (…) for shared collections."
- "Use `record` for DTOs, API responses, domain events, value objects" → `should-use-records-for-data`: "In C#, SHOULD use `record` for DTOs, API responses, domain events, value objects."
- "Use `record struct` / `readonly record struct` for small immutable value types" → `should-use-record-structs-for-small-values`: "In C#, SHOULD use `record struct` / `readonly record struct` for small immutable value types."
- "Prefer positional records (`record Person(string Name, int Age)`) for simple data carriers" → `should-prefer-positional-records`: "In C#, SHOULD prefer positional records (…) for simple data carriers."
- "Use `init` setters and `required` keyword for mandatory properties" → `should-use-init-and-required`: "In C#, SHOULD use `init` setters and `required` keyword for mandatory properties."
- "Use `with` expressions for non-destructive mutation" → `should-use-with-expressions`: "In C#, SHOULD use `with` expressions for non-destructive mutation."
- "Contain mutable state behind `ObservableObject` (UI) or thread-safe wrappers" → `should-contain-mutable-state-behind-wrappers`: "In C#, SHOULD contain mutable state behind `ObservableObject` (UI) or thread-safe wrappers."
- "Reserve `class` with mutable state for entities with identity semantics" → `should-reserve-mutable-classes-for-entities`: "In C#, SHOULD reserve `class` with mutable state for entities with identity semantics."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/concurrency/kotlin-flow-stateflow

15 rules. The intro is unchanged. Each section's code blocks stay in their own part (`exposing-state` and `injecting-dispatchers` as `examples`). The "Choosing a SharingStarted policy" table is now its own `how-to` part. The Compose and Views explanations stay in `collecting-lifecycle-aware-the-critical-part` (`how-to`). The four "why" sentences are in a `rationale` part, verbatim and keyed by rule. The "Anti-patterns — flag and fix" heading maps to `look-for`, whose three anti-pattern lines carry those words.

**promoted** (5 rules):
- "Back it with a private `MutableStateFlow` and expose `.asStateFlow()`." → `should-back-with-private-mutablestateflow`: "The ViewModel SHOULD back its exposed state with a private `MutableStateFlow` and expose `.asStateFlow()`." (It follows a MUST sentence and could be read as part of that MUST. As a plain imperative it is SHOULD, so a judge should check it.)
- Table row "`Lazily` | Start on first subscriber, never stop. Use only when restart cost is unacceptable." → `should-use-lazily-only-when-restart-cost-unacceptable`: "`Lazily` (start on first subscriber, never stop) SHOULD be used only when restart cost is unacceptable." (The table stays verbatim in the how-to part.)
- "**Compose**: use `collectAsStateWithLifecycle()` (from `androidx.lifecycle:lifecycle-runtime-compose`)." → `should-use-collectasstatewithlifecycle-in-compose`: "In Compose, SHOULD use `collectAsStateWithLifecycle()` (from `androidx.lifecycle:lifecycle-runtime-compose`)."
- "**Views / Fragments / Activities**: collect inside `repeatOnLifecycle(Lifecycle.State.STARTED)` from `lifecycleScope`." → `should-use-repeatonlifecycle-in-views`: "In Views / Fragments / Activities, SHOULD collect inside `repeatOnLifecycle(Lifecycle.State.STARTED)` from `lifecycleScope`."
- "In tests, inject `StandardTestDispatcher` / `UnconfinedTestDispatcher` and drive virtual time with `runTest`." → `should-inject-test-dispatchers`: "In tests, SHOULD inject `StandardTestDispatcher` / `UnconfinedTestDispatcher` and drive virtual time with `runTest`."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored. The anti-patterns list was written as MUST NOT requirements, so it became rules, not the `review-focus` part.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/concurrency/swift6-strict-concurrency

23 rules. The intro is unchanged. `core-model` keeps its two definition bullets as `rationale`, and its "**Requirement**" bullet is now a rule. The Swift 6.2 section keeps its descriptive sentences as a `how-to` part, and its instructions are rules. A `rationale` part carries the lead-in "Recommended order (durable practice from the Swift migration guide):" for the four ordered migration steps. The lead-in maps to that part, because one entry can name at most three targets. The making-types-sendable, actor-isolation, incremental-migration and verification sections held only rules, so their parts are gone.

**promoted** (13 rules):
- "Use `actor` to protect mutable state; its members are isolated and accessed with `await` from outside." → `should-use-actor-for-mutable-state`: "SHOULD use `actor` to protect mutable state; …"
- "Annotate UI types and view models that touch UIKit/AppKit/SwiftUI state with `@MainActor`." → `should-annotate-ui-types-with-mainactor`: "SHOULD annotate UI types and view models that touch UIKit/AppKit/SwiftUI state with `@MainActor`."
- "Enable checks as **warnings** first via the `StrictConcurrency` upcoming-feature flag (…) while still in Swift 5 mode." → `should-enable-checks-as-warnings-first`: "SHOULD enable checks as **warnings** first via … while still in Swift 5 mode."
- "Migrate **leaf modules first** (no dependents), then work upward; switch the **app target last**." → `should-migrate-leaf-modules-first`: "SHOULD migrate **leaf modules first** (no dependents), then work upward; switch the **app target last**."
- "Flip a module to the Swift 6 language mode only once its warnings are clear." → `should-flip-to-swift-6-only-when-warnings-clear`: "SHOULD flip a module to the Swift 6 language mode only once its warnings are clear."
- "Use `@preconcurrency` on imports/conformances … — treat it as a **temporary** shim, not a destination." → `should-use-preconcurrency-as-temporary-shim`: "SHOULD use `@preconcurrency` … — treat it as a **temporary** shim, not a destination."
- "Do not flip the whole workspace to Swift 6 mode at once; that produces an unactionable wall of errors." → `should-not-flip-whole-workspace-at-once`: "SHOULD NOT flip the whole workspace to Swift 6 mode at once; that produces an unactionable wall of errors." ("Do not" was read as a plain imperative, SHOULD NOT, not as "never".)
- "Behavior depends on settings — confirm what a target actually enables before assuming it." → `should-confirm-target-settings-before-assuming`: "Swift 6.2 behavior depends on settings — SHOULD confirm what a target actually enables before assuming it."
- "Enable each **individually** when migrating an existing project, because …" → `should-enable-approachable-features-individually`: "SHOULD enable each of `InferIsolatedConformances` and `NonisolatedNonsendingByDefault` **individually** when migrating an existing project, because …"
- "Use the `@concurrent` attribute to explicitly opt a function into running off the main actor." → `should-use-concurrent-to-opt-off-main-actor`: "SHOULD use the `@concurrent` attribute …"
- "Treat any default-isolation choice as a **deliberate per-target decision**, not a global mandate; record it where the target is configured." → `should-treat-default-isolation-as-per-target-decision`: "SHOULD treat any default-isolation choice as a **deliberate per-target decision**, …; record it where the target is configured."
- "Build each migrated module in Swift 6 language mode with zero concurrency warnings before moving up the graph." (Verification) → `should-build-migrated-modules-warning-free`: "SHOULD build each migrated module …"

The `@unchecked Sendable` sentence carried MAY, MUST and MUST NOT in one sentence. It is split into `may-use-unchecked-sendable-when-guaranteed`, `must-justify-unchecked-sendable` and `must-not-expose-unsynchronized-mutable-state`, each at its own keyword.

**bars**: `look-for` partly moved. The Verification step "Grep for `@unchecked Sendable` and confirm each has a justifying comment and real synchronization." is text written for a reviewer. It is the `must-justify-unchecked-sendable` line verbatim, and the other 22 lines are authored. `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/data/advanced-indexing

16 rules. The sections already held named rules. They are gathered, names unchanged, into one `rules` part, and the section parts that held only rules are gone. The index-type table is a `how-to` part (`choose-the-type-by-access-pattern`). `type-matches-query` ended in a colon to introduce that table, and now points to it. The intro keeps its statement, and its last sentence ("Examples below assume PostgreSQL 16/17; pin behavior to your server's version.") is now a rule.

**promoted** (2 rules):
- "Examples below assume PostgreSQL 16/17; pin behavior to your server's version." → `pin-to-server-version`: "Examples assume PostgreSQL 16/17; the author SHOULD pin behavior to the server's version."
- "**measured-need**: Specialized strategies — … — are adopt-only-when-a-concrete-measured-need-justifies-it, not defaults (YAGNI; …)." → `measured-need`: "Specialized strategies — … — SHOULD be adopted only when a concrete measured need justifies it, not as defaults (YAGNI; …)."

`jsonb-write-cost` held two SHOULDs. It is split: `jsonb-write-cost` keeps "measure write impact before adding one", and the new `jsonb-scalar-expression-index` holds "prefer an expression index on a single extracted scalar key when that is all queries need". That rule adds "over a GIN index" to name what "one" referred to.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/data/connection-pooling

18 rules. The intro is unchanged. The sections' named bullets gather into one `rules` part. The pooling-modes table is a `how-to` part. A `rationale` part holds the footguns' reason sentence ("Transaction mode reassigns the server connection …") and the PgBouncer prepared-statement history. The footgun list's lead-in "Code that runs under transaction-mode pooling **MUST NOT** depend on:" introduced five rules, more than one entry can name, so it maps to that `rationale` part, which names all five rules and carries the lead-in's words. Each footgun rule now opens with the lead-in's words, so each one stands alone at MUST NOT.

**promoted** (8 rules):
- "**session-mode-fallback**: Use **session mode** only when the workload genuinely needs session-scoped features (below) and …" → `session-mode-fallback`: "**Session mode** SHOULD be used only when the workload genuinely needs session-scoped features (those the transaction-mode rules below forbid) and …"
- "Verify your pooler version and that your driver uses the extended protocol, not text-mode `PREPARE`. Confirm against your deployed pooler's docs." → `verify-pooler-prepared-statement-support`: "SHOULD verify your pooler version and that your driver uses the extended protocol, not text-mode `PREPARE`, and confirm against your deployed pooler's docs."
- "**disable-driver-side-prepare**: When unsure of pooler support, configure the driver/ORM …" → `disable-driver-side-prepare`: "When unsure of pooler support, SHOULD configure the driver/ORM …"
- "**size-the-pool**: Set the pooler's server pool (`default_pool_size`) below `max_connections` with headroom …" → `size-the-pool`: "SHOULD set the pooler's server pool …". The bullet's second sentence, "Total server connections across all poolers **MUST** stay under `max_connections`.", is now its own rule, `total-connections-under-max`, verbatim.
- "**fail-fast-on-exhaustion**: Configure short client-side connection acquisition timeouts …" → `fail-fast-on-exhaustion`: "SHOULD configure short client-side connection acquisition timeouts …"
- Verify: "Run the app's full transaction set against a transaction-mode pooler in staging; assert no … errors under concurrency." → `staging-transaction-mode-run`: "SHOULD run the app's full transaction set … in staging, and assert no … errors under concurrency."
- Verify: "Grep the codebase for `SET ` (non-`LOCAL`), `LISTEN`, `pg_advisory_lock(` (non-`_xact_`), and session temp-table usage before deploying behind transaction pooling." → `grep-for-session-state`: "SHOULD grep the codebase for … before deploying behind transaction pooling."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored. The Verify steps are pre-deploy instructions, so they became rules.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/data/data-retention-and-deletion

22 rules. The intro keeps its statement. Its last sentence, the counsel caveat, is now a rule. The five sections' bullets gather into one `rules` part. The soft/hard/anonymize table stays verbatim as a `how-to` part. Its two MUST cells are also named rules: `must-not-count-soft-delete-as-erasure` and `must-make-anonymization-irreversible`. A `rationale` part holds the two why-sentences, "Storage limitation (GDPR Art. 5(1)(e) …)" and "A deletion that misses a copy is not a deletion.", and names the rules they support. Bullets that held two keywords are split into one rule each:
- must-define-retention-period / must-justify-missing-retention-period
- should-make-cascade-idempotent / must-make-failed-cascade-resumable
- should-decide-delete-mode-per-category / must-resolve-erasure-to-hard-delete-or-anonymization
- should-suppress-erased-data-immediately / must-not-restore-without-reapplying-deletions
- should-reconcile-expiry-periodically / should-treat-reconciliation-miss-as-defect

**promoted** (11 rules):
- "This is engineering guidance, not legal advice — confirm concrete retention periods with counsel." → `should-confirm-retention-periods-with-counsel`: "… concrete retention periods SHOULD be confirmed with counsel."
- "Maintain a **retention schedule** as code or config …" → `should-maintain-retention-schedule`: "SHOULD maintain a **retention schedule** as code or config …"
- "Record a `created_at` (and where relevant `expires_at`) timestamp on every retained record …" → `should-record-retention-timestamps`: "SHOULD record a `created_at` …"
- "Maintain an explicit inventory of where each category is copied; …" → `should-maintain-copy-inventory`: "SHOULD maintain an explicit inventory …"
- "Prefer **event-driven** cascade …" → `should-prefer-event-driven-cascade`: "SHOULD prefer **event-driven** cascade …"
- "Make cascade steps **idempotent** and retryable; …" → `should-make-cascade-idempotent`: "SHOULD make cascade steps **idempotent** and retryable."
- "Decide soft vs. hard **per category**, not globally." → `should-decide-delete-mode-per-category`: "SHOULD decide soft vs. hard **per category**, not globally."
- "Define and publish a backup retention/purge policy …" → `should-publish-backup-purge-policy`: "SHOULD define and publish …"
- "For an erasure request, suppress the data from active systems immediately and rely on backup rotation for residual copies; …" → `should-suppress-erased-data-immediately`: "For an erasure request, SHOULD suppress …"
- "Log every deletion (who/what/when, category, request reference) to a tamper-evident, separately retained **audit trail** …" → `should-audit-every-deletion`: "SHOULD log every deletion …"
- "Reconcile periodically: scan for records past their `expires_at` that were not purged, and alert. Treat a reconciliation miss as a defect (fail fast)." → `should-reconcile-expiry-periodically` ("SHOULD reconcile periodically: …") and `should-treat-reconciliation-miss-as-defect` ("SHOULD treat a reconciliation miss as a defect (fail fast).")

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/data/database

2 rules. The topic was a single intro. Its statement stays in `intro`, as GF-01 needs. Its two sentences are also the two named rules, each verbatim: `must-use-sqlite-wal-for-concurrent-reads` and `must-not-use-orm`. The `PRAGMA journal_mode=WAL` snippet is an `examples` part, "Enabling WAL mode". No sentence needed an entry, so `lossless.json` is empty.

**promoted**: none. Both rules carried MUST / MUST NOT.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/data/deterministic-ids

3 rules. The topic was a single intro of three keyword sentences. The intro keeps them as its statement, as GF-01 needs. The `rules` part names each one verbatim: `must-use-roadmap-frontmatter-uuid`, `must-not-generate-random-uuids` and `must-be-deterministic-and-reproducible`. No sentence needed an entry, so `lossless.json` is empty.

**promoted**: none.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/data/partitioning-and-time-series

15 rules. The intro is unchanged. The four sections' requirements gather into one `rules` part. The strategy table and its lead sentence form a `how-to` part, "Choosing a partition strategy". A `rationale` part holds the extension trade-off sentences and the FORECAST / version-sensitive note, and names the rules they support.

**promoted** (5 rules):
- "Per **YAGNI** and **make-it-work-make-it-right-make-it-fast**, do NOT partition by default." → `should-not-partition-by-default`: "… you SHOULD NOT partition by default." This is a plain negative imperative with no "never", so it is read as SHOULD NOT. The capitalised NOT could be read as stronger; that call is left to the judge.
- "**Range partition by time** (e.g. one partition per day/week/month …)." → `should-range-partition-time-series-by-time`: "Time-series data SHOULD be **range partitioned by time** (e.g. …)."
- "**Retention by dropping partitions**: `DROP TABLE`/`DETACH PARTITION` on an old partition is near-instant …" → `should-retain-by-dropping-partitions`: "Retention SHOULD be done **by dropping partitions**: …"
- "**Rollups / continuous aggregates**: precompute summaries for queries spanning long history instead of scanning raw rows." → `should-precompute-rollups-for-long-history`: "… you SHOULD precompute summaries …"
- "Pin to your deployed major version and re-verify `EXPLAIN` plans after upgrades." → `should-pin-and-reverify-after-upgrades`: "You SHOULD pin to your deployed major version and re-verify `EXPLAIN` plans after upgrades."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/data/room-persistence

26 rules. The intro keeps its first two sentences. Its third, the "Prefer coroutine-first DAO APIs" sentence, is now a rule. Every section's requirements gather into one `rules` part. The version facts (Room 2.8.4 stable, KMP from 2.7.0, what Room 3.0.0-alpha01 changes) stay verbatim as a `how-to` part, "Version landscape (as of 2026-06)". The transaction-isolation cross-link is a `references` part. Bullets that held two keywords or two instructions are split into one rule each:
- must-not-call-blocking-dao-on-main-thread / should-not-allow-main-thread-queries-outside-tests
- must-index-foreign-key-columns / should-treat-unindexed-fk-warning-as-error
- should-treat-room-3-as-forecast / should-not-migrate-production-to-room-3
- must-bump-version-and-supply-migration / must-not-ship-destructive-migration-fallback

The keyword for `@Relation` queries changes in wording only. "`@Transaction` is also **REQUIRED** on `@Query` methods …" becomes `must-use-transaction-on-relation-queries`: "`@Transaction` **MUST** also be on `@Query` methods …". RFC 2119 makes REQUIRED and MUST equivalent, and the rule format takes MUST|SHOULD|MAY.

**promoted** (13 rules):
- "Prefer coroutine-first DAO APIs: observable reads as `Flow`, …" → `should-prefer-coroutine-first-dao-apis`: "You SHOULD prefer coroutine-first DAO APIs — …"
- "State KMP support as "2.7.0+" — do not back-port the claim to older versions." → `should-state-kmp-support-as-2-7-plus`: "You SHOULD state KMP support as "2.7.0+" — …"
- "**Room 3.0 is ALPHA — treat its API and the `androidx.room3:room3-*` artifact rename as a FORECAST, not a shipped default." → `should-treat-room-3-as-forecast`: "**Room 3.0 is ALPHA** — you SHOULD treat its API …"
- "Do not migrate production code to it yet.**" → `should-not-migrate-production-to-room-3`: "You SHOULD NOT migrate production code to Room 3.0 yet."
- "Pin the Room version explicitly in the version catalog; do not float to `+`." → `should-pin-room-version`: "You SHOULD pin the Room version …"
- "Keep transactions short; do no network or long CPU work inside `withTransaction`." → `should-keep-transactions-short`: "You SHOULD keep transactions short; …"
- "Define one `@Entity` per normalized table." → `should-define-one-entity-per-normalized-table`: "You SHOULD define one `@Entity` per normalized table."
- "Declare relationships with `@ForeignKey` and load them via `@Relation`, not by denormalizing." → `should-declare-relationships-not-denormalize`: "You SHOULD declare relationships …"
- "Room emits a build warning for unindexed foreign keys; treat it as an error to fix." → `should-treat-unindexed-fk-warning-as-error`: "…; you SHOULD treat it as an error to fix."
- "Add an `@Index(unique = true)` for natural-key uniqueness instead of relying on app-side checks." → `should-use-unique-index-for-natural-keys`: "You SHOULD add an `@Index(unique = true)` …"
- From the section headed **MUST NOT**: "Do not hold the `RoomDatabase` instance per-screen; build one application-scoped singleton via `Room.databaseBuilder(...)`." → `must-not-hold-database-per-screen`: "You MUST NOT hold the `RoomDatabase` instance per-screen; …"
- From the section headed **MUST NOT**: "Do not expose `LiveData` for new code when the consumer is a coroutine/Compose layer; prefer `Flow`." → `must-not-expose-livedata-to-coroutine-consumers`: "You MUST NOT expose `LiveData` …"
- From the section headed **MUST NOT**: "Do not perform multi-step writes as separate suspend calls without a transaction — …" → `must-not-split-multi-step-writes-without-transaction`: "You MUST NOT perform multi-step writes …"

The last three take MUST NOT, not the SHOULD NOT a bare "Do not" would get, because their section's own heading was "MUST NOT".

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/data/transaction-isolation

12 rules. The intro is unchanged. The `requirements` section becomes the `rules` part, and its seven named rules keep their names. Three bullets that held two distinct requirements are split, each new rule keeping the original sentence:
- `deliberate-level`, plus the new `justified-level` ("The choice MUST be justified …")
- `bounded-backoff`, plus the new `surface-on-exhaustion` ("on exhaustion it MUST surface the failure" → "On exhaustion of its bounded retries, code MUST surface the failure.")
- `explicit-locking-for-queues`, plus the new `no-serializable-queue-dispatch` ("They SHOULD NOT rely on Serializable …" → "Worker/queue claim patterns SHOULD NOT rely on Serializable …")

The isolation-level table with its notes and the "Choosing a level" guide are `how-to` parts. The retry pseudocode is an `examples` part.

**promoted** (2 rules):
- From the isolation-levels note: "Confirm semantics against your engine's dated docs, not by analogy to PostgreSQL." → `confirm-engine-semantics`: "Engines differ, so you SHOULD confirm semantics against your engine's dated docs, not by analogy to PostgreSQL."
- From the anti-patterns: "Using Read Committed for a check-then-update invariant (read balance, then debit) — this loses updates; use `SELECT ... FOR UPDATE` or Serializable." → `check-then-update-locking`: "A check-then-update invariant (read balance, then debit) SHOULD NOT run at Read Committed alone — this loses updates; use `SELECT ... FOR UPDATE` or Serializable."

**bars**:
- `look-for` partly moved. Its three Anti-patterns bullets, which were written for a reviewer, are carried verbatim as the lines for `retry-serialization-failure`, `idempotent-retry` and `check-then-update-locking`. The other nine lines are authored.
- `a-complete-review-must-establish` authored.
- `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/data/zero-downtime-migrations

20 rules. The intro keeps its first and last sentences. Its middle sentence, "Split every schema change …", is now a rule. Every section's requirements gather into one `rules` part. The phase table is a `how-to` part. The SQL expand snippet is an `examples` part, "Expand step in SQL". A `rationale` part holds three passages and names the rules each one supports:
- the rolling-deploy N/N-1 sentence;
- the lock-queue sentence;
- the engine-variation note.

Two bullets are split:
- the `lock_timeout` bullet into `must-set-lock-timeout` and `should-set-statement-timeout`;
- the concurrent-index bullet into `must-not-wrap-concurrent-index-in-transaction` and `should-clean-up-invalid-index`.

**promoted** (8 rules):
- Intro: "Split every schema change into small, individually-deployable, backward-compatible steps so …" → `should-split-schema-changes-into-compatible-steps`: "You SHOULD split every schema change …"
- "Spread one logical change across multiple releases:" (the table's lead-in) → `should-spread-change-across-releases`: "You SHOULD spread one logical change across multiple releases, through the Expand, Migrate, Switch and Contract phases."
- "Bound the wait so a contended migration aborts cleanly and can be retried." → `should-bound-ddl-lock-wait`: "You SHOULD bound the wait so …"
- "Set `statement_timeout` too, to bound the statement's own runtime." → `should-set-statement-timeout`: "You SHOULD set `statement_timeout` too, …"
- "Because each step is additive and backward-compatible, the rollback is to **redeploy the previous app version** — …" → `should-roll-back-by-redeploying`: "… the rollback SHOULD be to **redeploy the previous app version** — …"
- "Avoid down-migrations that drop just-added columns during an incident; …" → `should-avoid-dropping-down-migrations`: "You SHOULD avoid down-migrations …"
- Note: "The Postgres examples here are illustrative; confirm against your engine's current `ALTER TABLE` documentation before relying on a clause being non-blocking." → `should-confirm-engine-lock-behavior`: "You SHOULD confirm against your engine's current `ALTER TABLE` documentation …". "The Postgres examples here are illustrative" is kept in `rationale`.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/documentation/writing-comments-and-docs

27 rules. The intro is unchanged. The four guidance sections gather into one `rules` part. A `rationale` part holds the plain-language section's lead sentence and names the rules it introduces. "Why this matters" stays a part of its own, with the `rationale` role. Only `should-comment-the-why` carried a keyword; the other 26 rules are promoted. How the keywords were read:
- a bare imperative became SHOULD;
- "Do not …" became SHOULD NOT;
- "needs" (in "New public behavior needs a description …" and "Removed behavior needs its description removed …") became SHOULD;
- the two "Never …" sentences became MUST NOT: `must-not-make-up-sources` and `must-use-visible-characters-only`.

The rest of each bullet stays verbatim in its rule. That covers the trailing sentences such as "Comment what is left." and "Do not hedge by reflex."

**promoted** (26 rules):
- "Do not restate the line below it." → `should-not-restate-the-line`: "A comment SHOULD NOT restate the line below it. `# increment counter` above `counter += 1` adds noise and a second thing to keep in sync."
- "If a comment is needed to explain what a block does, first try a clearer name or a smaller function." → `should-try-a-clearer-name-first`: "If a comment is needed to explain what a block does, you SHOULD first try a clearer name or a smaller function. Comment what is left."
- "Name the source of a surprising value: the spec section, the ticket, the measurement." → `should-name-the-source-of-surprising-values`: "You SHOULD name the source of a surprising value: the spec section, the ticket, the measurement."
- "**Specifics over abstractions.** Name the thing, the number, the file." → `should-prefer-specifics`: "**Specifics over abstractions.** You SHOULD name the thing, the number, the file. If you do not know the specific, leave the sentence out rather than invent one."
- "Never make up a statistic, source or quote." → `must-not-make-up-sources`: "You MUST NOT make up a statistic, source or quote."
- "**Cut throat-clearing.** Do not open by restating the title or announcing what you are about to say, and do not close by summarizing what you just said." → `should-cut-throat-clearing`: "**Cut throat-clearing.** You SHOULD NOT open by restating the title or announcing what you are about to say, and do not close by summarizing what you just said. Ask of each sentence what it adds."
- "**Short ordinary words.** Prefer "use" to "utilize" and "show" to "demonstrate"." → `should-use-short-ordinary-words`: "**Short ordinary words.** You SHOULD prefer "use" to "utilize" and "show" to "demonstrate". Avoid stock filler vocabulary and stacked hedges."
- "**Do not swap synonyms to disguise a tic.** If a word is vague, rewrite the clause so it is not needed." → `should-not-swap-synonyms-to-disguise-a-tic`: "You **SHOULD NOT swap synonyms to disguise a tic.** If a word is vague, rewrite the clause so it is not needed."
- "**Verbs over nominalizations.** Write "we decide" rather than "we make a decision"." → `should-prefer-verbs-over-nominalizations`: "**Verbs over nominalizations.** You SHOULD write "we decide" rather than "we make a decision"."
- "**Active voice by default.** Passive is fine when the actor does not matter." → `should-use-active-voice-by-default`: "You SHOULD use **active voice by default.** Passive is fine when the actor does not matter."
- "**Hedge only real uncertainty**, and say what is uncertain." → `should-hedge-only-real-uncertainty`: "You SHOULD **hedge only real uncertainty**, and say what is uncertain. Do not hedge by reflex."
- "**Vary rhythm because the content calls for it**, not to hit a quota." → `should-vary-rhythm-by-content`: "You SHOULD **vary rhythm because the content calls for it**, not to hit a quota. Do not break every list into groups of three or end every paragraph on a tidy one-line moral."
- "**Punctuation does a job.** Use a comma, colon, parentheses or a new sentence rather than a dash." → `should-make-punctuation-do-a-job`: "**Punctuation does a job.** You SHOULD use a comma, colon, parentheses or a new sentence rather than a dash. Do not run clauses together to avoid one."
- "**Keep one tense and one register** through a passage." → `should-keep-one-tense-and-register`: "You SHOULD **keep one tense and one register** through a passage."
- "**State the premise** behind a claim, or weaken the claim to what you can support." → `should-state-the-premise`: "You SHOULD **state the premise** behind a claim, or weaken the claim to what you can support."
- "**Visible characters only.** Never paste look-alike or invisible Unicode characters into text." → `must-use-visible-characters-only`: "**Visible characters only.** You MUST NOT paste look-alike or invisible Unicode characters into text."
- "Where the host has the humanize skill, run it over prose you wrote and review its findings." → `should-run-humanize-where-available`: "Where the host has the humanize skill, you SHOULD run it over prose you wrote and review its findings. Where it does not, apply these rules by hand."
- "When a change alters behavior, update the comments, docstrings, README sections and instruction files that describe it in that same change." → `should-update-docs-in-the-same-change`: "When a change alters behavior, you SHOULD update the comments, docstrings, README sections and instruction files that describe it in that same change. Do not leave a doc update as a follow-up."
- "Search the docs for the names you changed, as you would search code." → `should-search-docs-for-changed-names`: "You SHOULD search the docs for the names you changed, as you would search code."
- "New public behavior needs a description where users will look for it." → `should-describe-new-public-behavior`: "New public behavior SHOULD get a description where users will look for it."
- "Removed behavior needs its description removed (see `docs-match-code`)." → `should-remove-docs-of-removed-behavior`: "Removed behavior SHOULD have its description removed (see `docs-match-code`)."
- "Both readers need the same things: exact names they can search for, the real command to run, the real path, and a statement of when a rule applies." → `should-give-both-readers-exact-specifics`: "Docs SHOULD give both readers the same things they need: exact names they can search for, the real command to run, the real path, and a statement of when a rule applies."
- "Lead with the point." → `should-lead-with-the-point`: "You SHOULD lead with the point. An agent loads a file partially and a person skims, so put the answer first and the background after."
- "Prefer concrete examples with real values over abstract descriptions." → `should-prefer-concrete-examples`: "You SHOULD prefer concrete examples with real values over abstract descriptions. Keep each example short enough to be correct."
- "Keep one canonical term for each concept, and use it everywhere." → `should-keep-one-canonical-term`: "You SHOULD keep one canonical term for each concept, and use it everywhere. A synonym reads as a different thing to a literal-minded reader."
- "Say what is true now." → `should-say-what-is-true-now`: "You SHOULD say what is true now. Leave out narration of how it got that way."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/infrastructure/containerization

17 rules. The intro is unchanged. The six sections' named bullets gather into one `rules` part, and every existing name is kept. `workdir` is split: its `ENTRYPOINT`/`CMD` sentence becomes `entrypoint-and-cmd`. The layer-caching numbered list is a `how-to` part, "Layer order". The list's lead-in becomes the rule `order-layers-by-change-frequency`. The unnamed "Adopt-when-justified" bullet becomes the rule `adopt-when-justified`.

**promoted** (8 rules):
- "Adopt them when a measured need justifies the cost (scale, multi-service coordination, compliance) — not by default (per YAGNI)." → `adopt-when-justified`: "Orchestration platforms (Kubernetes, ECS, Nomad) and per-image vulnerability scanners add real operational weight. You SHOULD adopt them when a measured need justifies the cost (scale, multi-service coordination, compliance) — not by default (per YAGNI). A single image deployed to a managed container host is often sufficient early on."
- "**workdir**: Use `WORKDIR` with absolute paths rather than chained `cd`." → `workdir`: "You SHOULD use `WORKDIR` with absolute paths rather than chained `cd`."
- "Use `ENTRYPOINT` for the executable and `CMD` for default arguments." → `entrypoint-and-cmd`: "You SHOULD use `ENTRYPOINT` for the executable and `CMD` for default arguments."
- "Order instructions from least- to most-frequently changed so the dependency layer is reused when only source changes:" → `order-layers-by-change-frequency`: "You SHOULD order instructions from least- to most-frequently changed so the dependency layer is reused when only source changes."
- "**combine-run**: Combine `apt-get update` with `apt-get install` in one `RUN`, pin package versions where practical, and clean caches in the same layer (`rm -rf /var/lib/apt/lists/*`) to avoid stale-cache bugs and image bloat." → `combine-run`: "You SHOULD combine `apt-get update` with `apt-get install` in one `RUN`, pin package versions where practical, and clean caches in the same layer (`rm -rf /var/lib/apt/lists/*`) to avoid stale-cache bugs and image bloat."
- "**deterministic-deps**: Install from a locked manifest (`requirements.txt` with hashes, `package-lock.json`, `go.sum`, `Cargo.lock`) so builds are repeatable." → `deterministic-deps`: "Builds SHOULD install from a locked manifest (`requirements.txt` with hashes, `package-lock.json`, `go.sum`, `Cargo.lock`) so builds are repeatable."
- "**least-files**: Use a `.dockerignore` to exclude `.git`, secrets, local env files, build output, and `node_modules` from the build context — this shrinks context, speeds builds, and prevents accidental secret leakage." → `least-files`: "You SHOULD use a `.dockerignore` to exclude `.git`, secrets, local env files, build output, and `node_modules` from the build context — this shrinks context, speeds builds, and prevents accidental secret leakage."
- "**drop-extras**: Do not install packages "just in case." Fewer packages means fewer CVEs to patch." → `drop-extras`: "You SHOULD NOT install packages "just in case." Fewer packages means fewer CVEs to patch."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/infrastructure/kubernetes-configuration

14 rules. The intro keeps its statement sentence. Its "Treat a Kubernetes Secret as base64-encoded…" sentence and its "Adopt Kubernetes only when…" note become rules. The four sections' named bullets gather into one `rules` part, and every existing name is kept. The external-manager section's lead paragraph is appended verbatim to `prefer-managed-store`. The approach table is a `how-to` part, "Secret sourcing approaches". A `rationale` part holds the base64-is-not-encryption paragraph and the forecast's first clause, and names the rules each supports.

**promoted** (6 rules):
- "Treat a Kubernetes Secret as **base64-encoded, not encrypted** — protect it at the cluster level or source it from a dedicated secret manager." → `treat-secret-as-encoded-not-encrypted`: "You SHOULD treat a Kubernetes Secret as **base64-encoded, not encrypted** — protect it at the cluster level or source it from a dedicated secret manager."
- "> Adopt Kubernetes only when a measured operational need justifies it (per YAGNI)." → `adopt-only-on-measured-need`: "You SHOULD adopt Kubernetes only when a measured operational need justifies it (per YAGNI). A single container, a serverless platform, or a managed PaaS is often the simpler default; the guidance below applies once you have committed to Kubernetes."
- "**mount-choice**: Inject config as environment variables for simple scalars; mount as a volume when files, larger payloads, or live updates are needed." → `mount-choice`: "You SHOULD inject config as environment variables for simple scalars; mount as a volume when files, larger payloads, or live updates are needed. Volume-mounted ConfigMaps/Secrets update in place; env vars do **not** and require a Pod restart."
- "**immutable-when-stable**: Mark ConfigMaps and Secrets `immutable: true` when their values are fixed for the release, reducing apiserver load and preventing accidental edits." → `immutable-when-stable`: "You SHOULD mark ConfigMaps and Secrets `immutable: true` when their values are fixed for the release, reducing apiserver load and preventing accidental edits."
- "> Forecast: secret-management tooling and CSI/operator APIs evolve quickly — pin Helm charts and operator versions, and re-validate against the dated upstream docs before adopting new flows." → `pin-and-revalidate-secret-tooling`: "You SHOULD pin Helm charts and operator versions, and re-validate against the dated upstream docs before adopting new flows."
- "Privacy note: handling credentials and PII in clusters is engineering guidance, **not legal advice**; consult the relevant regulations and counsel for compliance obligations." → `consult-counsel-on-compliance`: "Handling credentials and PII in clusters is engineering guidance, **not legal advice**; you SHOULD consult the relevant regulations and counsel for compliance obligations."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/infrastructure/kubernetes-workloads

21 rules. The intro is unchanged. The six sections' bullets gather into one `rules` part. The probe table stays verbatim as a `how-to` part, "Health probes". Its three keyword cells are also named rules: `should-use-startup-probe-for-long-init`, `must-define-readiness-probe` and `should-define-liveness-probe`. Splits:
- The CPU bullet's MAY and its "always" clause become two rules, `may-omit-cpu-limit` and `must-always-set-cpu-request`.
- The `RollingUpdate` bullet's trailing `minReadySeconds` instruction becomes `should-set-min-ready-seconds`.

**promoted** (4 rules):
- "> Security and isolation guidance here is engineering practice, not a compliance certification; validate against your own regulatory and threat-model requirements." → `should-validate-against-own-requirements`: "Security and isolation guidance here is engineering practice, not a compliance certification; you SHOULD validate against your own regulatory and threat-model requirements."
- "Set `requests.memory == limits.memory` for predictable, non-burstable memory." → `should-set-memory-request-equal-to-limit`: "You SHOULD set `requests.memory == limits.memory` for predictable, non-burstable memory."
- "For CPU, **MAY** omit `limits.cpu` to avoid throttling latency-sensitive workloads, but always set `requests.cpu`." → `must-always-set-cpu-request`: "Even when `limits.cpu` is omitted, you MUST always set `requests.cpu`."
- "Set `minReadySeconds` so new pods prove healthy before old ones retire." → `should-set-min-ready-seconds`: "You SHOULD set `minReadySeconds` so new pods prove healthy before old ones retire."

`must-always-set-cpu-request` takes MUST from the source's "always".

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/infrastructure/twelve-factor-config

12 rules. The intro is unchanged. The five "Core rules" bullets keep their text verbatim under new names. "What counts as config" stays as a `how-to` part. Its "It is NOT…" sentence becomes `should-keep-constants-in-code`, opening "Config is **NOT** …" so that the negation is kept. The three practical patterns become four promoted rules, because the secret-store bullet's YAGNI sentence becomes its own rule. The forecast and privacy notes each yield one promoted rule. Their explanatory sentences go to a `rationale` part that names those rules.

**promoted** (6 rules):
- "Treat any newer factor revisions as forecasts until officially published, and pin to the current published guidance at https://12factor.net/config." → `should-treat-new-factor-revisions-as-forecasts`: "You SHOULD treat any newer factor revisions as forecasts until officially published, and pin to the current published guidance at https://12factor.net/config."
- "Provide a `.env.example` (committed, no real values) listing every variable the app reads; keep the real `.env` git-ignored and out of images." → `should-provide-env-example`: "You SHOULD provide a `.env.example` (committed, no real values) listing every variable the app reads; keep the real `.env` git-ignored and out of images."
- "Validate and coerce config once at boot into a typed config object; the rest of the code reads that object, not `process.env`/`os.environ` directly." → `should-validate-config-once-at-boot`: "You SHOULD validate and coerce config once at boot into a typed config object; the rest of the code reads that object, not `process.env`/`os.environ` directly."
- "Inject secrets at runtime from a managed secret store (cloud secret manager, orchestrator secret, or vault) rather than baking them into the artifact." → `should-inject-secrets-at-runtime`: "You SHOULD inject secrets at runtime from a managed secret store (cloud secret manager, orchestrator secret, or vault) rather than baking them into the artifact."
- "Treat the choice of a heavyweight secrets platform as adopt-when-measured-need-justifies, not a default (YAGNI) — start with environment injection." → `should-start-with-environment-injection`: "You SHOULD treat the choice of a heavyweight secrets platform as adopt-when-measured-need-justifies, not a default (YAGNI) — start with environment injection."
- "This is engineering guidance and is **NOT** legal advice; consult counsel for regulatory obligations." → `should-consult-counsel`: "This is engineering guidance and is **NOT** legal advice; you SHOULD consult counsel for regulatory obligations."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/internationalization/localization

11 rules. The intro held two copies of its statement, left by an earlier fold of a duplicate topic: a "Localizability" summary with platform bullets, and then a "---" and a second H1, "# Localization", with a fuller paragraph. The intro now keeps the H1 "Localizability" and the fuller paragraph, verbatim. The platform bullets are mapped to the platform rules they repeat, and "# Localization" is mapped as moved to the intro. Two other changes:
- The `windows-2` part was a byte-identical duplicate of `windows`, so it was dropped. Its sentences are held verbatim in the remaining parts.
- The Swift, Kotlin and TypeScript sections became rules. The `windows` part keeps the `x:Uid` explanation, the mapping bullet and the XAML example as `how-to`. Its folder-structure and code-behind bullets became rules.

Each "No hardcoded user-facing strings" line maps to `must-make-user-facing-strings-localizable`.

**promoted** (10 rules; every rule except `must-make-user-facing-strings-localizable`):
- "**Apple**: `String(localized:)` or `NSLocalizedString`." → `should-use-string-localized-on-apple`: "On Apple platforms, you SHOULD use `String(localized:)` (Swift 5.7+) or `NSLocalizedString`."
- "Store in `.xcstrings` or `.strings`." → `should-store-apple-strings-in-xcstrings`: "You SHOULD store Apple strings in `.xcstrings` (Xcode 15+) or `.strings` files."
- "**Android**: `strings.xml` resources." → `should-use-strings-xml-on-android`: "On Android (Kotlin), you SHOULD use `strings.xml` resource files."
- "Reference via `R.string.*` or `stringResource()`." → `should-reference-android-strings-via-resources`: "You SHOULD reference Android strings via `R.string.*` in code or `stringResource()` in Compose."
- "**Web**: i18n library (`react-intl`, `i18next`)." → `should-use-i18n-library-on-web`: "On the web (TypeScript), you SHOULD use an i18n library (`react-intl`, `i18next`, `FormatJS`)."
- "Extract to message catalogs." → `should-extract-to-message-catalogs`: "You SHOULD extract all user-facing strings into message catalogs."
- "**Windows**: `.resw` resource files with `x:Uid` in XAML." → `should-use-mrt-core-resw-on-windows`: "On Windows, you SHOULD use MRT Core with `.resw` resource files, with `x:Uid` in XAML."
- "`ResourceLoader` from MRT Core for code-behind access." → `should-use-resource-loader-in-code-behind`: "Windows code-behind SHOULD access strings via `ResourceLoader` from MRT Core (`Microsoft.Windows.ApplicationModel.Resources.ResourceLoader`)."
- "Use `strings.xml` resource files." → `should-use-strings-xml-on-android`: "On Android (Kotlin), you SHOULD use `strings.xml` resource files."
- "Reference via `R.string.*` in code or `stringResource()` in Compose." → `should-reference-android-strings-via-resources`: "You SHOULD reference Android strings via `R.string.*` in code or `stringResource()` in Compose."
- "Use `String(localized:)` (Swift 5.7+) or `NSLocalizedString`." → `should-use-string-localized-on-apple`: "On Apple platforms, you SHOULD use `String(localized:)` (Swift 5.7+) or `NSLocalizedString`."
- "Store strings in `.xcstrings` (Xcode 15+) or `.strings` files." → `should-store-apple-strings-in-xcstrings`: "You SHOULD store Apple strings in `.xcstrings` (Xcode 15+) or `.strings` files."
- "Use an i18n library (`react-intl`, `i18next`, `FormatJS`)." → `should-use-i18n-library-on-web`: "On the web (TypeScript), you SHOULD use an i18n library (`react-intl`, `i18next`, `FormatJS`)."
- "Extract all user-facing strings into message catalogs." → `should-extract-to-message-catalogs`: "You SHOULD extract all user-facing strings into message catalogs."
- "Use MRT Core with `.resw` resource files." → `should-use-mrt-core-resw-on-windows`: "On Windows, you SHOULD use MRT Core with `.resw` resource files, with `x:Uid` in XAML."
- "Folder structure: `Strings/<language-tag>/Resources.resw` (e.g., `Strings/en-US/Resources.resw`)" → `should-follow-windows-strings-folder-structure`: "Windows resource files SHOULD follow the folder structure `Strings/<language-tag>/Resources.resw` (e.g., `Strings/en-US/Resources.resw`)."
- "Code-behind access via `Microsoft.Windows.ApplicationModel.Resources.ResourceLoader`" → `should-use-resource-loader-in-code-behind`: "Windows code-behind SHOULD access strings via `ResourceLoader` from MRT Core (`Microsoft.Windows.ApplicationModel.Resources.ResourceLoader`)."
- "Store strings in platform-standard resource files and reference them through the platform's localization API." (intro, kept there) → `should-store-in-platform-resource-files`: "You SHOULD store strings in platform-standard resource files and reference them through the platform's localization API."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/implementing/internationalization/rtl-support

13 rules. The intro held two copies of its guidance, left by an earlier fold of a duplicate topic: a numbered list with platform notes, and then a "---" and a second H1, "# RTL Support", with a one-paragraph restatement. The intro now keeps its H1 and that paragraph, verbatim. "# RTL Support" maps as moved to the intro. The numbered list, the platform notes and the Kotlin, TypeScript and Windows sections became rules. The Windows section's two mirroring bullets repeat the intro's and are held verbatim. The two "handles leading/trailing automatically" notes go to a `rationale` part, "Platform notes", which names the rules it supports.

`should-not-mirror-non-directional-icons` reads "Do NOT" as SHOULD NOT. No MUST NOT heading governs it.

**promoted** (12 rules; every rule except `must-support-rtl-languages`):
- "Use **leading/trailing** (not left/right) for alignment and padding" → `should-use-leading-trailing`: "You SHOULD use **leading/trailing** (not left/right) for alignment and padding."
- "Mirror icons with directional meaning (forward/back arrows)" → `should-mirror-directional-icons`: "You SHOULD mirror icons with directional meaning (forward/back arrows)."
- "Do NOT mirror non-directional icons (checkmarks, clocks)" → `should-not-mirror-non-directional-icons`: "You SHOULD NOT mirror non-directional icons (checkmarks, clocks)."
- "Test with RTL locale enabled" → `should-test-with-rtl-locale`: "You SHOULD test with an RTL locale enabled."
- "Platform notes:" → `should-use-leading-trailing`: "You SHOULD use **leading/trailing** (not left/right) for alignment and padding."; `should-preview-rtl-on-apple`: "On the Apple platform, you SHOULD use `.environment(\.layoutDirection, .rightToLeft)` in previews."; `should-set-flow-direction-on-windows`: "On Windows, you SHOULD use the `FlowDirection` property: set `FlowDirection="RightToLeft"` on the root element for RTL locales."
- "**Apple**: Use `.environment(\.layoutDirection, .rightToLeft)` in previews." → `should-preview-rtl-on-apple`: "On the Apple platform, you SHOULD use `.environment(\.layoutDirection, .rightToLeft)` in previews."
- "**Android**: Set `android:supportsRtl="true"`." → `should-set-supports-rtl-on-android`: "On Android, you SHOULD set `android:supportsRtl="true"` in the manifest."
- "Use `start`/`end` instead of `left`/`right`." → `should-use-start-end-on-android`: "You SHOULD use `start`/`end` instead of `left`/`right` in Android layouts."
- "**Web**: Use `dir="rtl"` attribute." → `should-set-dir-rtl-on-web`: "On the web, you SHOULD set the `dir="rtl"` attribute on the root element for RTL locales."
- "Use CSS logical properties (`margin-inline-start` not `margin-left`)." → `should-use-css-logical-properties`: "On the web (TypeScript), you SHOULD use CSS logical properties throughout (`margin-inline-start` not `margin-left`):"
- "**Windows**: Use `FlowDirection` property." → `should-set-flow-direction-on-windows`: "On Windows, you SHOULD use the `FlowDirection` property: set `FlowDirection="RightToLeft"` on the root element for RTL locales."
- "Set `android:supportsRtl="true"` in the manifest." → `should-set-supports-rtl-on-android`: "On Android, you SHOULD set `android:supportsRtl="true"` in the manifest."
- "Use `start`/`end` instead of `left`/`right` in layouts." → `should-use-start-end-on-android`: "You SHOULD use `start`/`end` instead of `left`/`right` in Android layouts."
- "Force RTL in developer options for testing." → `should-force-rtl-for-android-testing`: "You SHOULD force RTL in Android developer options for testing."
- "Use CSS logical properties throughout:" → `should-use-css-logical-properties`: "On the web (TypeScript), you SHOULD use CSS logical properties throughout (`margin-inline-start` not `margin-left`):"
- "Set `dir="rtl"` attribute on the root element for RTL locales." → `should-set-dir-rtl-on-web`: "On the web, you SHOULD set the `dir="rtl"` attribute on the root element for RTL locales."
- "Set `FlowDirection="RightToLeft"` on the root element for RTL locales" → `should-set-flow-direction-on-windows`: "On Windows, you SHOULD use the `FlowDirection` property: set `FlowDirection="RightToLeft"` on the root element for RTL locales."
- "Test with RTL language packs installed" → `should-test-with-rtl-language-packs-on-windows`: "On Windows, you SHOULD test with RTL language packs installed."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.
