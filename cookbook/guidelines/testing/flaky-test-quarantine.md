---
id: 4f5fe9ef-1bf8-4354-92c7-92d9e28673b8
title: "Flaky test quarantine lifecycle"
domain: agenticdevelopercookbook://guidelines/testing/flaky-test-quarantine
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Detect, quarantine with an owner and deadline, fix the root cause, then return flaky tests to the gating suite."
platforms: []
tags:
  - testing
  - flaky
  - ci
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/testing/flaky-test-prevention
references:
  - https://www.thoughtworks.com/insights/blog/quarantine
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - writing-tests
  - pre-pr
---

# Flaky test quarantine lifecycle

A flaky test passes and fails on the same code. This guideline defines the lifecycle for managing one once it exists: detect, quarantine, own, fix, restore. It complements `flaky-test-prevention` (which is about not writing flaky tests in the first place); this is about handling them when they slip through.

## Why quarantine

A flaky test that blocks the gating suite trains the team to ignore red builds and rerun blindly, eroding trust in the whole suite. Quarantine removes the test from the merge gate WITHOUT deleting or silencing it — it still runs and is still tracked, so the flakiness stays visible and accountable.

## Lifecycle

The lifecycle has five stages. A test MUST move forward through them; it MUST NOT stall in quarantine.

1. **Detect** — Identify flakiness from a signal, not a hunch (see Detection).
2. **Quarantine** — Move the test out of the gating suite into a non-gating bucket. It MUST still execute on every run and report results.
3. **Own** — Assign exactly one owner and a fix deadline at the moment of quarantine.
4. **Fix** — Diagnose and remove the root cause of nondeterminism.
5. **Restore** — Return the test to the gating suite once it is stable, or delete it if the behavior it covered is no longer worth testing.

## Detection

- Flakiness SHOULD be detected from an objective signal: a **flip rate** (pass/fail transitions on unchanged code) above an agreed threshold, or a test that passes only on retry.
- A test that needs a retry to pass MUST be treated as flaky, even when the retry hides the failure from the gate.
- Retries MAY be used as a detection signal but MUST NOT be used as a silent cure — a test that "passes on retry 3 of 3" is a flaky test, not a passing one.
- The CI system SHOULD record per-test pass/fail history so flip rate is measurable rather than anecdotal.

## Quarantine mechanics

- A quarantined test MUST be marked explicitly (e.g., a `@quarantined` tag, category, or skip-from-gate annotation) — never commented out or deleted.
- The gating suite MUST exclude quarantined tests; a separate non-gating job MUST continue running them on every build.
- Each quarantined test MUST carry: an owner, a fix deadline, and a link to the tracking issue, recorded in the annotation or a tracked registry.
- The quarantine bucket MUST be visible (a dashboard, report, or PR check summary). A quarantine no one looks at is a graveyard.

## Owner and deadline

- Quarantining a test MUST create a tracked work item with a single named owner and a concrete deadline.
- The deadline SHOULD be short (days, not quarters). Quarantine is a holding pattern, not a destination.
- When a deadline lapses, the team MUST decide explicitly: extend with justification, fix now, or delete the test — it MUST NOT silently roll over indefinitely.

## Restore or delete

- A test returns to the gating suite only after the root cause is fixed and it has run green enough times to clear the flip-rate threshold.
- Masking a failure with a retry, an increased timeout, or a loosened assertion is NOT a fix and MUST NOT qualify a test for restoration.
- If the covered behavior no longer warrants a test, the test SHOULD be deleted outright rather than left quarantined.

## Anti-patterns

- Quarantine MUST NOT become a permanent parking lot — an unbounded, unowned quarantine list is a failure of this lifecycle.
- Deleting a flaky test to make CI green, without addressing whether the behavior still needs coverage, is silent loss of coverage and MUST NOT be done.
- Globally enabling auto-retry across the whole suite to bury flakiness MUST NOT be used as a substitute for this lifecycle.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
