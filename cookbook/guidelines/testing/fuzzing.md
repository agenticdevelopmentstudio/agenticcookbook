---
id: d197a1e3-eba5-4f3f-acc7-c2fabd51144f
title: "Fuzz testing"
domain: agenticdevelopercookbook://guidelines/testing/fuzzing
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Fuzz untrusted-input parsing surfaces — especially in memory-unsafe code — with coverage-guided fuzzers; adopt elsewhere only on measured need."
platforms: []
tags:
  - testing
  - fuzzing
  - security
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/testing/property-based-testing
  - agenticdevelopercookbook://guidelines/testing/security-testing
references:
  - https://github.com/google/oss-fuzz
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - writing-tests
  - security-review
---

# Fuzz testing

Coverage-guided fuzzing feeds mutated and random inputs to a target, using code-coverage feedback to evolve inputs toward new paths, surfacing crashes, hangs, and undefined behavior. Its highest value is at boundaries that parse, decode, or deserialize untrusted input — most acutely in memory-unsafe languages.

## Where to apply it (measured-need guardrail)

Per `yagni` and `make-it-work-make-it-right-make-it-fast`, fuzzing is **adopted where a concrete attack surface justifies it**, not mandated repository-wide.

- You **SHOULD** fuzz any code that parses, decodes, or deserializes data crossing a trust boundary: file/media parsers, network protocol decoders, serialization formats, regex/template/expression evaluators, decompressors.
- You **SHOULD** prioritize fuzzing in memory-unsafe languages (C, C++, and `unsafe` Rust/Go FFI) where defects become memory-corruption vulnerabilities.
- You **SHOULD NOT** treat broad business/UI logic with no untrusted-input boundary as a default fuzzing target; prefer property-based testing (see `agenticdevelopercookbook://guidelines/testing/property-based-testing`) there.
- Targets **MUST** be deterministic for a given input (no clock/network/global-state dependence) so crashes reproduce.

## Tooling (per language)

| Language | Engine / tool | Notes |
|----------|---------------|-------|
| C / C++ | libFuzzer, AFL++, Honggfuzz | Run with sanitizers (ASan/UBSan/MSan). |
| Rust | `cargo-fuzz` (libFuzzer) | Use `arbitrary` for structured inputs. |
| Go | native `go test -fuzz` (since Go 1.18) | `testing.F` corpus + mutator. |
| JVM | Jazzer (libFuzzer-backed, in-process) | Java/Kotlin/Scala. |
| Python | Atheris (libFuzzer-backed) | Native-extension and pure-Python targets. |

- Open-source projects **SHOULD** consider [OSS-Fuzz](https://github.com/google/oss-fuzz) for free continuous fuzzing (libFuzzer, AFL++, Honggfuzz, ClusterFuzz) once a stable harness exists.
- FORECAST (recent, unverified-for-production): a 2026 Go-toolchain fork (`gosentry`/LibAFL-backed `go test -fuzz`) advertises struct-aware and grammar-based fuzzing. Treat as evolving; **pin and evaluate** before depending on it — standard `go test -fuzz` remains the durable baseline.

## Writing and running harnesses

- A fuzz target **MUST** accept raw bytes (or a deterministically derived structured input) and exercise exactly one parsing entry point.
- Harnesses **MUST** fail loudly: assert invariants and let sanitizers/panics surface defects (`fail-fast`).
- You **SHOULD** seed a starting corpus from real and edge-case samples; coverage grows far faster from good seeds.
- Every crash a fuzzer finds **MUST** be committed as a regression-corpus test case so the fix is permanently guarded.
- Long fuzzing campaigns **SHOULD** run in CI/nightly, not on the per-commit critical path; gate PRs on the seeded regression corpus and a short smoke run instead.

## Triage

- Reproduce with the saved crashing input; minimize it (most tools provide `-minimize`/`tmin`) before filing.
- Classify by sanitizer report: memory-safety crashes are typically security-relevant (escalate per `agenticdevelopercookbook://guidelines/testing/security-testing`); logic crashes may be ordinary bugs.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
