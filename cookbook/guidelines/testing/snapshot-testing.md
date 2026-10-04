---
id: 3d9f5176-afaa-47a2-8a89-fc0402f3dff2
title: "Snapshot testing discipline"
domain: agenticdevelopercookbook://guidelines/testing/snapshot-testing
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Keep snapshots small and deterministic, and deliberately review every snapshot diff before accepting it."
platforms: []
tags:
  - testing
  - snapshot
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/testing/properties-of-good-tests
  - agenticdevelopercookbook://guidelines/testing/test-doubles
references:
  - https://kentcdodds.com/blog/effective-snapshot-testing
  - https://jestjs.io/docs/snapshot-testing
  - https://blog.stackademic.com/its-2025-stop-using-snapshot-testing-1afa6612259e
  - https://dev.to/dorshinar/why-i-ve-stopped-writing-snapshots-tests-in-jest-376d
  - https://selleo.com/blog/when-to-use-jest-snapshots
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - writing-tests
---

# Snapshot testing discipline

A snapshot (or approval) test is only as strong as the human review of its diff. A snapshot captures a serialized value once, then fails when future output diverges. That makes the *review* — not the assertion — the actual test. Use snapshots for stable, structured output; lean on explicit assertions everywhere logic matters.

## Review every diff deliberately

- You **MUST** review every snapshot diff before accepting it. Treat an unexpected diff as a potential bug, not a chore to clear.
- You **MUST NOT** reflexively run the update/accept-all command (`jest --updateSnapshot`/`-u`, `vitest -u`, Verify/ApprovalTests "accept all", `cargo insta accept`) to make a red suite green. Update only after confirming each change is intended.
- CI **MUST** run snapshots in non-updating mode (e.g. `--ci`) so a missing or stale snapshot fails rather than silently writing a new one.
- You **SHOULD** review snapshot files in code review as carefully as source. A diff nobody reads asserts nothing.

## Keep snapshots small and targeted

- A snapshot **SHOULD** cover one concern — a single component's rendered output, one function's serialized result — not an entire page or aggregate object graph.
- You **SHOULD** prefer many small inline snapshots (`toMatchInlineSnapshot`, inline approval) over one large external file. Inline snapshots keep the expected value next to the test, so reviewers see intent in the diff.
- You **SHOULD NOT** snapshot output you cannot reason about line by line. A giant auto-generated snapshot that no one reviews is the core anti-pattern: it appears to test much and tests nothing (`yagni`, `explicit-over-implicit`).

## Make snapshots deterministic

Non-deterministic snapshots produce noisy diffs that train reviewers to accept blindly (`fail-fast` erodes when failures are routine).

- You **MUST** strip or normalize non-deterministic values before serializing: timestamps, dates, durations, random IDs/UUIDs, hostnames, absolute paths, and ports.
- You **MUST** stabilize ordering of sets, maps, and query results — sort before snapshotting rather than depending on iteration order.
- You **SHOULD** use property matchers for unavoidable dynamics (Jest/Vitest `expect.any(...)` in `toMatchSnapshot({ id: expect.any(String) })`; ApprovalTests scrubbers; `insta` filters) instead of regenerating the snapshot each run.

## Prefer explicit assertions for logic

- You **SHOULD** assert specific values explicitly when the test verifies behavior or computation; a snapshot obscures *which* field mattered and why.
- You **SHOULD** reserve snapshots for output that is verbose, structurally stable, and tedious to assert by hand (serialized DOM, generated config, formatted reports).
- You **SHOULD** delete obsolete snapshots promptly (`--ci` reports them); a stale snapshot is dead weight that misleads future readers (`design-for-deletion`).

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
