# Phase 2 batch 16 report

Fourteen testing guidelines, each converted to roled parts. Every requirement is now a named rule in
`rules.md`. Worked tables and step lists stay as `how-to` parts, and reasons moved verbatim into `rationale`
parts. No topic had text written for a reviewer (a checklist or a "review" section), so all three bar parts
are **authored** in every topic. No sentence was marked obsolete: `cookr roles lossless` refuses `obsolete`
for a topic's own base sentences, so lead-ins such as "**Rules:**" map to the rules they introduce.

## Where these topics differ from the brief

- **A clause loses its keyword at a comma or parenthesis.** The lossless judge splits a rule at commas and
  parentheses, so a keyword in a later clause ("For large schemas, tests MAY …") does not count. Such rules
  were reworded to put the keyword in the first clause, keeping their words.
- **A sentence with two levels stays one rule.** "Retries MAY … but MUST NOT …" (flaky-test-quarantine) and
  "Argument checks SHOULD … but MUST stay strict …" (tool-call-evaluation) could not be split, because each
  half's clause then drops the other level. Each stays one rule carrying both levels.
- **A colon sentence with a keyword is not a lead-in.** "Every generated artifact MUST be verified:" and
  "From Kent Beck's Test Desiderata — tests should be:" carry a level, so the judge limits them to three
  targets. The first maps to `intro`, which restates it as a sentence. The second maps to a `rationale` part
  naming all twelve rules.
- **Line-wrapped sentences are split.** The judge reads a sentence wrapped across two source lines as two
  sentences (security-testing, the-testing-workflow). Each half has its own `moved` entry.

## cookbook/guidelines/testing/contract-testing

**promoted** (4 rules, plus one folded into a keyworded rule):
- "**Provider / schema contracts** — use for third-party or upstream APIs you consume but do **not** control." and "Pin to the provider's published schema (e.g. an OpenAPI document at a dated revision) and test that your client tolerates it; you cannot make them run your contract." → `should-use-schema-contracts-for-uncontrolled-apis`: "For third-party or upstream APIs you consume but do not control, SHOULD use provider / schema contracts: pin to the provider's published schema (e.g. an OpenAPI document at a dated revision) and test that your client tolerates it." The reason clause went to `rationale`.
- "Match on field presence and type, and on matcher-based values (e.g. "an ISO-8601 string", "a positive integer"), not on exact literals that change per request." → `should-match-presence-type-and-matchers`: "Contracts SHOULD match on field presence and type, and on matcher-based values (e.g. "an ISO-8601 string", "a positive integer"), not on exact literals that change per request."
- "Assert the error/status codes the consumer branches on; ignore codes it never inspects." → `should-assert-only-branched-codes`: "Contracts SHOULD assert the error/status codes the consumer branches on, and SHOULD ignore codes it never inspects."
- "A contract that breaks on a *backward-compatible* provider change (a new optional field, a reordered list) is too strict — loosen it." → `should-loosen-over-strict-contracts`: "A contract that breaks on a *backward-compatible* provider change (a new optional field, a reordered list) is too strict and SHOULD be loosened."
- "**Consumer-driven contracts** — use when you own *both* sides of the interaction (your own services calling each other)." was folded into the existing SHOULD rule `should-cover-owned-integrations-with-consumer-driven-contracts`, as a sub-bullet.
- In `must-not-track-moving-latest`, the imperative "re-pin deliberately" sits inside the MUST NOT rule and is read at MUST. A judge should check that reading.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/testing/database-testing

**promoted** (17 rules):
- "Use SQLite for unit tests where dialect differences do not affect the logic under test." → `should-use-sqlite-where-dialect-is-irrelevant`: "SQLite SHOULD be used for unit tests where dialect differences do not affect the logic under test."
- "Use `:memory:` databases for unit tests." → `should-use-memory-databases-for-unit-tests`: "Unit tests SHOULD use `:memory:` databases."
- "Use file-based databases only for integration tests that must verify WAL behavior, file locking, concurrent connections, or platform-specific I/O." → `should-use-file-databases-only-for-file-behavior`: "File-based databases SHOULD be used only for integration tests that must verify WAL behavior, file locking, concurrent connections, or platform-specific I/O."
- "In those cases, write the database to a temp directory and delete it in teardown." → `should-put-file-databases-in-temp-dir`: "In those cases, the test SHOULD write the database to a temp directory and delete it in teardown."
- "The `:memory:` URL creates a new database per connection; use named in-memory databases (`file:name?mode=memory&cache=shared`) only when multiple connections to the same in-memory database are intentionally required." → `should-use-named-memory-databases-only-when-intended`: "Named in-memory databases (`file:name?mode=memory&cache=shared`) SHOULD be used only when multiple connections to the same in-memory database are intentionally required." The first clause stays as how-to.
- "Use function-scoped fixtures for tests that write." → `should-use-function-scoped-fixtures-for-writes`: "Tests that write SHOULD use function-scoped fixtures."
- "Use session-scoped fixtures for read-only tests." → `should-use-session-scoped-fixtures-for-reads`: "Read-only tests SHOULD use session-scoped fixtures."
- "Apply them only in test fixtures." → `should-apply-relaxed-settings-only-in-tests`: "Tests SHOULD apply relaxed durability settings only in test fixtures."
- "Test idempotency by applying the migration set twice:" → `should-test-migration-idempotency-twice`: "Migration idempotency SHOULD be tested by applying the migration set twice."
- "Test backward migration (rollback) when rollback scripts exist." → `should-test-backward-migrations`: "Backward migration (rollback) SHOULD be tested when rollback scripts exist."
- "Always test migrations against a database seeded with production-representative data to catch data conversion errors — type coercions, NOT NULL violations, and constraint failures that only appear with real values." → `must-test-migrations-with-representative-data`: "Migrations MUST always be tested against a database seeded with production-representative data …" ("Always" read as MUST.)
- "Sync logic requires testing at the unit level (change detection, serialization) and integration level (round-trip apply)." → `must-test-sync-at-unit-and-integration-level`: "Sync logic MUST be tested at the unit level (change detection, serialization) and integration level (round-trip apply); it requires both." ("requires" read as MUST.)
- "**Change detection**: verify that the unsynced-records query returns the correct rows." → `should-test-change-detection`: "Change detection SHOULD be tested: verify that the unsynced-records query returns the correct rows."
- "**Sync apply**: verify that applying a changeset from the server updates the local database correctly, including soft-delete propagation." → `should-test-sync-apply`: "Sync apply SHOULD be tested: …"
- "**Outbox round-trip**: write a record locally, confirm it appears in the outbox, simulate a sync cycle, confirm the record is marked synced and the outbox entry is consumed." → `should-test-outbox-round-trip`: "The outbox round-trip SHOULD be tested: …"
- "**Tombstone propagation**: delete a record on one simulated peer, apply the tombstone to a second peer, confirm the record is absent on the second peer and not resurrected by a subsequent sync." → `should-test-tombstone-propagation`: "Tombstone propagation SHOULD be tested: …"
- "Conflict tests require two databases representing two peers." → `must-test-conflicts-with-two-peers`: "Conflict tests MUST use two databases representing two peers; conflict tests require them." ("require" read as MUST.)
- "Apply divergent changes to each, then merge and assert the outcome matches the defined resolution strategy." → `should-assert-merge-matches-resolution-strategy`: "Conflict tests SHOULD apply divergent changes to each peer, then merge and assert the outcome matches the defined resolution strategy."
- "Test all defined conflict cases:" → `should-test-all-conflict-cases`: "SHOULD test all defined conflict cases:" with the cases as sub-bullets.
- Not promoted but restructured: the isolation table's "(SHOULD be the default)" and "(MAY use …)" parentheticals became `should-default-to-fresh-database-per-test`, `may-use-transaction-rollback-for-large-schemas` and `may-use-template-and-backup-for-seeded-data`.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**:
- The cross-database differences table states SQLite `LIKE` is "Case-sensitive (ASCII)" and PostgreSQL is "Case-insensitive (`ILIKE`)". As SQLite and PostgreSQL document them, SQLite `LIKE` is case-insensitive for ASCII by default and PostgreSQL `LIKE` is case-sensitive (`ILIKE` is its case-insensitive form). The table looks inverted. Left unfixed.

**unfinished**: none.

## cookbook/guidelines/testing/eval-driven-development

**promoted** (2 rules):
- "Treat evals as the test suite for the non-deterministic parts of the system." → `should-treat-evals-as-test-suite`: "Evals SHOULD be treated as the test suite for the non-deterministic parts of the system."
- "Do not wrap deterministic code in an LLM judge." → `should-not-wrap-deterministic-code-in-judge`: "SHOULD NOT wrap deterministic code in an LLM judge." (A plain "do not" was read as SHOULD NOT, not "never".)

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/testing/flaky-test-prevention

**promoted** (2 rules, from one sentence):
- "Quarantine them immediately — fix or delete, never ignore." →
  - `should-quarantine-flaky-tests-immediately`: "Flaky tests SHOULD be quarantined immediately, then fixed or deleted."
  - `must-not-ignore-flaky-tests`: "A flaky test MUST NOT be ignored (never ignore)." ("never" read as MUST NOT.)
- The "**Rules:**" lead-in maps to the seven keyworded rules it introduced. The intro keeps "Flaky tests destroy confidence." A `references` part holds the sources.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**:
- flaky-test-prevention says "Quarantine them immediately — fix or delete, never ignore." (now `should-quarantine-flaky-tests-immediately`: "… then fixed or deleted"). flaky-test-quarantine says "Deleting a flaky test to make CI green, without addressing whether the behavior still needs coverage, … MUST NOT be done", and deletes a test only "If the covered behavior no longer warrants a test". Prevention offers deletion as a plain alternative to fixing. Quarantine allows it only after the coverage question is settled. Left unfixed.

**unfinished**: none.

## cookbook/guidelines/testing/flaky-test-quarantine

**promoted** (1 rule):
- "A test returns to the gating suite only after the root cause is fixed and it has run green enough times to clear the flip-rate threshold." → `should-restore-only-after-fix-and-green-runs`: "A test SHOULD return to the gating suite only after the root cause is fixed and it has run green enough times to clear the flip-rate threshold."
- The retry sentence carrying both MAY and MUST NOT stays one rule, `may-use-retries-only-as-detection-signal`. The "why quarantine" section became a `rationale` part.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: the deletion conflict with flaky-test-prevention, above.

**unfinished**: none.

## cookbook/guidelines/testing/fuzzing

**promoted** (5 rules):
- Table note "Run with sanitizers (ASan/UBSan/MSan)." (C / C++ row) → `should-run-c-cpp-fuzzers-with-sanitizers`: "C / C++ fuzzing (libFuzzer, AFL++, Honggfuzz) SHOULD run with sanitizers (ASan/UBSan/MSan)." The table stays in the `how-to` part.
- Table note "Use `arbitrary` for structured inputs." (Rust row) → `should-use-arbitrary-for-rust-structured-inputs`: "Rust fuzzing with `cargo-fuzz` SHOULD use `arbitrary` for structured inputs."
- "Treat as evolving; **pin and evaluate** before depending on it — standard `go test -fuzz` remains the durable baseline." → `should-pin-and-evaluate-forecast-go-fork`: "The 2026 `gosentry` Go-toolchain fork SHOULD be treated as evolving; pin and evaluate it before depending on it — standard `go test -fuzz` remains the durable baseline."
- "Reproduce with the saved crashing input; minimize it (most tools provide `-minimize`/`tmin`) before filing." → `should-reproduce-and-minimize-before-filing`: "A crash SHOULD be reproduced with the saved crashing input and minimized (most tools provide `-minimize`/`tmin`) before filing."
- "Classify by sanitizer report: memory-safety crashes are typically security-relevant (escalate per …); logic crashes may be ordinary bugs." → `should-classify-by-sanitizer-report`: "Crashes SHOULD be classified by sanitizer report: memory-safety crashes are typically security-relevant (escalate per …); logic crashes may be ordinary bugs."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/testing/groundedness-and-hallucination

**promoted** (5 rules):
- "Score groundedness at **claim granularity**, not whole-answer granularity: decompose the answer …" → `should-score-at-claim-granularity`: "Groundedness SHOULD be scored at **claim granularity**, not whole-answer granularity: …"
- "Keep the judge blind to any gold answer so it scores support, not agreement." → `should-keep-judge-blind-to-gold-answer`: "The judge SHOULD be kept blind to any gold answer so it scores support, not agreement."
- "Frameworks such as RAGAS, DeepEval, and TruLens implement these metrics; their absolute scores diverge on the same data (forecast: still true in 2026), so pin one framework + version and track trends rather than comparing raw cross-tool numbers." → `should-pin-one-eval-framework`: "SHOULD pin one framework + version and track trends rather than comparing raw cross-tool numbers.", with the framework clause as its sub-bullet.
- "An abstention is a **correct** outcome when context is insufficient; do not penalize it as a miss in aggregate scoring." → `should-not-penalize-correct-abstention`: "An abstention is a **correct** outcome when context is insufficient; it SHOULD NOT be penalized as a miss in aggregate scoring."
- "Run groundedness and hallucination evals in CI on a fixed query set; **MUST** fail the build …" → `should-run-evals-in-ci-on-fixed-set`: "Groundedness and hallucination evals SHOULD run in CI on a fixed query set." The keyworded half is `must-fail-build-on-hallucination-regression`.
- "Treat groundedness as a release gate alongside latency and cost, not a one-time benchmark — retriever index drift and model swaps both move it." → `should-treat-groundedness-as-release-gate`: "Groundedness SHOULD be treated as a release gate …"
- "> Privacy note: when eval sets contain user data, redact or synthesize PII before sending to a judge model." → `should-redact-pii-before-judge`: "When eval sets contain user data, PII SHOULD be redacted or synthesized before sending to a judge model."
- Not promoted: the intro's "You **MUST** measure groundedness … and the system **SHOULD** abstain rather than fabricate when support is missing." became `must-measure-groundedness-and-hallucination-rate` and the lead clause of `should-abstain-without-evidence`. The intro keeps its first statement for GF-01.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/testing/mutation-testing

**promoted** (1 rule):
- "5. Repeat until mutation score is acceptable" → `should-repeat-until-score-acceptable`: "The loop (write tests, run mutation testing, examine surviving mutants, kill them) SHOULD repeat until the mutation score is acceptable." The loop list stays in the `how-to` part. Its other steps are procedure, carried by the two MUST rules.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/testing/post-generation-verification

**promoted**: none. The six numbered steps sat under "Every generated artifact MUST be verified:" and take its MUST: `must-build-for-all-target-platforms`, `must-pass-full-test-suite`, `must-run-platform-linter`, `must-verify-expected-log-messages`, `must-audit-accessibility`, `must-review-against-best-practices`. A judge should check that the steps with no keyword of their own (Build, Lint, Log verification, Accessibility audit, Code review) were meant at MUST, as the lead-in says.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/testing/properties-of-good-tests

**promoted** (7 rules; the lead-in "tests should be:" gives a lowercase should, read as SHOULD):
- "**Fast** — milliseconds per unit test, seconds per integration test" → `should-be-fast`: "Tests SHOULD be **Fast** — milliseconds per unit test, seconds per integration test."
- "**Writable** — easy to author, low ceremony" → `should-be-writable`: "Tests SHOULD be **Writable** — easy to author, low ceremony."
- "**Readable** — a failing test tells you what broke and why" → `should-be-readable`: "Tests SHOULD be **Readable** — …"
- "**Automated** — no manual steps, no human judgment needed" → `should-be-automated`: "Tests SHOULD be **Automated** — …"
- "**Specific** — a failure points to exactly one cause" → `should-be-specific`: "Tests SHOULD be **Specific** — …"
- "**Predictive** — passing tests mean the code works in production" → `should-be-predictive`: "Tests SHOULD be **Predictive** — …"
- "**Inspiring** — confidence to refactor and ship" → `should-be-inspiring`: "Tests SHOULD be **Inspiring** — …"
- The five keyworded properties keep their MUST, MUST NOT, SHOULD and SHOULD NOT.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/testing/security-testing

**promoted**: none. The one rule, `must-run-security-scans-in-post-generation-verification`, keeps its MUST verbatim. The SAST, dependency and DAST tool lists stay as the `how-to` part "Scanners". The closing "See the security guidelines …" sentence is the `references` part.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/testing/snapshot-testing

**promoted** (2 rules, plus one intro sentence folded into two keyworded rules):
- "Treat an unexpected diff as a potential bug, not a chore to clear." → `should-treat-unexpected-diff-as-bug`: "You SHOULD treat an unexpected diff as a potential bug, not a chore to clear."
- "Update only after confirming each change is intended." → `should-update-only-after-confirming-intent`: "You SHOULD update only after confirming each change is intended."
- The intro's "Use snapshots for stable, structured output; lean on explicit assertions everywhere logic matters." became sub-bullets of `should-reserve-snapshots-for-stable-verbose-output` and `should-assert-logic-explicitly`, which already carry SHOULD.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/testing/the-testing-workflow

**promoted** (3 rules):
- "2. **Write unit tests** — informed by property-based testing for data transformations" → `should-inform-unit-tests-with-property-based-testing`: "Unit tests SHOULD be written informed by property-based testing for data transformations."
- "4. **Validate test quality** — `mutmut run` / `npx stryker run` / `muter` / `dotnet stryker`" → `should-validate-test-quality-with-mutation-testing`: "After tests run, test quality SHOULD be validated with mutation testing (`mutmut run` / `npx stryker run` / `muter` / `dotnet stryker`)."
- "7. **E2E verification** — Playwright for web UIs, platform test runners for native" → `should-verify-end-to-end`: "E2E verification SHOULD use Playwright for web UIs and platform test runners for native."
- The step list stays verbatim in the `how-to` part, except that the two MUST clauses moved to `must-write-tests-targeting-surviving-mutant-gaps` and `must-run-security-scan`. Steps 1 and 3 (write code, run tests) are procedure with no requirement of their own.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/testing/tool-call-evaluation

**promoted** (7 rules, one of them partly):
- "Treat this suite as a fixed, versioned regression set." → `should-treat-suite-as-versioned-regression-set`: "You SHOULD treat this suite as a fixed, versioned regression set."
- "Score against the trajectory, not just the final output — an agent can reach a correct answer through an unsafe or wasteful path." → `should-score-against-trajectory`: "You SHOULD score against the trajectory, not just the final output — …"
- "Include cases where the correct action is to call **no** tool, to confirm the agent does not invoke tools spuriously." → `should-include-no-tool-cases`: "You SHOULD include cases where the correct action is to call **no** tool, …"
- "Add multi-step cases that exercise the realistic tool count the agent ships with, and report accuracy as a function of chain length." → `should-add-realistic-multi-step-cases`: "You SHOULD add multi-step cases …"
- "Run each case multiple times; tool selection is non-deterministic, so **SHOULD** report pass rates with trial counts, not a single run." → `should-report-pass-rates-with-trial-counts`: "You SHOULD run each case multiple times; tool selection is non-deterministic, so SHOULD report pass rates with trial counts, not a single run." (Only "Run each case multiple times" is promoted.)
- "Gate releases on the suite and track per-dimension scores over time so a regression in argument correctness is not masked by stable task-completion numbers." → `should-gate-releases-and-track-per-dimension-scores`: "You SHOULD gate releases on the suite and track per-dimension scores over time …"
- "Keep cases hermetic: stub or record tool responses so the eval measures the agent, not live backend flakiness." → `should-keep-cases-hermetic`: "You SHOULD keep cases hermetic: …"
- The dimensions table stays as the `how-to` part "What to score". Its SHOULD lead-in is `should-report-each-dimension-separately`. The benchmark observation about long chains is a `rationale` part.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.
