<!-- leaf: review-networking/observable-behavior-contract · source: guidelines/reviewing/networking/observable-behavior-contract.md -->

**Rules** (cite as `review-networking/observable-behavior-contract#<slug>`):

- `enforce-guidance-here-level-apply-from-both` SHOULD — Hyrum's Law is a descriptive observation, stated by Hyrum Wright and named by Titus Winters: *"With a sufficient number …
- `you-explicitly-document-behaviors-guaranteed` SHOULD — You SHOULD explicitly document which behaviors are guaranteed and state the rest as non-guarantees (e.g., "iteration …
- `you-make-unpromised-behavior-visibly` SHOULD — You SHOULD make unpromised behavior visibly unstable so consumers cannot quietly couple to it — deliberately randomize …
- `you-version-interface-change-unspecified` SHOULD — You SHOULD version the interface and change unspecified behavior early and often, before a de facto contract forms.
- `upon-behavior-you-deprecate-discipline-announce-provide` SHOULD — When you must change a relied-upon behavior, you SHOULD deprecate with discipline: announce, provide a migration path, …
- `you-not-assume-undocumented-behavior-safe` MUST — You MUST NOT assume an undocumented behavior is safe to change just because the docs never promised it; with enough …
- `code-not-depend-behavior-provider-has` SHOULD — Code SHOULD NOT depend on any behavior the provider has not explicitly promised.
- `reviewers-flag-assertions-exact-error` SHOULD — Reviewers SHOULD flag: assertions on exact error message text, reliance on response/iteration ordering, hard-coded …
- `tests-assert-documented-contract-status` SHOULD — Tests SHOULD assert on documented contract (status code, typed error category, declared fields) rather than incidental …
- `genuinely-unavoidable-code-isolate-behind-adapter-document` SHOULD — When a dependency on unspecified behavior is genuinely unavoidable, the code SHOULD isolate it behind an adapter and …

# Hyrum's Law: all observable behavior becomes contract

Hyrum's Law is a descriptive observation, stated by Hyrum Wright and named by Titus Winters: *"With a sufficient number of users of an API, it does not matter what you promise in the contract: all observable behaviors of your system will be depended on by somebody."* Because it describes what consumers will do — not a rule you can enforce — guidance here is **SHOULD**-level. Apply it from both sides of an interface: when designing one and when consuming one.

## What counts as "observable behavior"

More than the documented signature. Consumers can and do depend on:

- Iteration / response ordering (e.g., map or JSON-field order that is "incidentally" stable)
- Exact error messages, error codes, and stack-trace text
- Timing, latency, and concurrency characteristics
- Floating-point precision, rounding, hash values, and tie-breaking
- Null-vs-absent fields, whitespace, and serialization quirks
- Side effects and the relative order of side effects

## When DESIGNING an interface

- You **SHOULD** explicitly document which behaviors are guaranteed and state the rest as **non-guarantees** (e.g., "iteration order is unspecified and may change").
- You **SHOULD** make unpromised behavior visibly unstable so consumers cannot quietly couple to it — deliberately randomize ordering, jitter timing, or vary error text where feasible (the "chaos" tactic Go and Abseil use for map iteration).
- You **SHOULD** version the interface and change unspecified behavior early and often, before a de facto contract forms.
- When you must change a relied-upon behavior, you **SHOULD** deprecate with discipline: announce, provide a migration path, and allow a window — do not break silently.
- You **MUST NOT** assume an undocumented behavior is safe to change just because the docs never promised it; with enough consumers, someone depends on it.

## When CONSUMING an interface (review focus)

AI-generated code is a known source of this fragility: agents readily encode incidental behavior (parsing a specific error string, asserting on response-field order, sleeping a fixed time) as if it were guaranteed.

- Code **SHOULD NOT** depend on any behavior the provider has not explicitly promised.
- Reviewers **SHOULD** flag: assertions on exact error message text, reliance on response/iteration ordering, hard-coded timing/sleep assumptions, and parsing of free-form provider strings.
- Tests **SHOULD** assert on documented contract (status code, typed error category, declared fields) rather than incidental output.
- When a dependency on unspecified behavior is genuinely unavoidable, the code **SHOULD** isolate it behind an adapter and document the assumption so the coupling is greppable and reversible.
