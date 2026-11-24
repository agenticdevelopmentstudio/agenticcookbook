# Integrate: test-failure-triage

Lossless: a new topic, with no base text in the cookbook (`roles lossless` reports the artifact is not in the base 77a898dbc718928bbd96ef617723c83ec69cd549); nothing to account for.

## For the owner

`cookr validate` owner-decides warnings for this topic. Each rule below cites its `-prior` claim, which the research rules unsupported (or, for `triage-changes-nothing`, contradicted). The owner decides each rule: keep it as it is, reword it, or drop it. Each stands, word for word under the lead-in "This MUST hold:", until the owner decides.

- `environment-cites-cross-test-signal` (unsupported)
- `spec-rot-names-new-assertion` (unsupported)
- `uncertain-names-missing-evidence` (unsupported)
- `high-confidence-needs-reproduction-and-mechanism` (unsupported)
- `triage-changes-nothing` (contradicted)

The prior text of these rules, kept word for word as the owner list requires, carries the old team's words: "sites", "spec-rot", `suggested_fix` and a `confidence` field on a 1-10 scale. A reword would make them general.

Open questions from owner-list.md:

- Whether triage stays a disposition-only output that files, closes, edits and reverts nothing (the team's rule triage-changes-nothing), or follows the sheriff and gardener practice in which the triager files the tracking bug, reverts the culprit or disables the test; the owner decides whether the cookbook states a general rule or leaves this to each team.
- Whether a stale-test (spec-rot) verdict must carry the assertion the test should make now, or only identify the intended behavior change that made the test stale (the change and its intent), leaving the new assertion to whoever updates the test.
- Whether the 1-10 confidence scale with 9-10 reserved for an observed reproduction and a stated mechanism is kept as the cookbook's scale, or replaced by a stated likelihood term with its basis and the gaps that limit it, as ICD 203 has it.
- Whether an environment verdict may rest on one test's cross-run or cross-machine pattern (as Gruber et al.'s infrastructure flakiness does), or only on a signal spanning unrelated tests or an infrastructure status observation as the team's rule requires.
- Whether 'an uncertain verdict names what evidence is missing and what would settle it' is kept as a must-hold check or stated at SHOULD, the strength ICD 203's standard on uncertainty carries.
- What the stale-test disposition is called in the cookbook: the team's 'spec-rot', Labuschagne et al.'s 'broken or obsolete test', or another name.
- Whether a flake disposition must also open a bug investigation of the product code, given that 24% of flaky-test fixes in Luo et al.'s sample changed the code under test, or whether that question is left to the flaky-test-quarantine lifecycle the flake is handed to.

integrated: 2026-11-24
