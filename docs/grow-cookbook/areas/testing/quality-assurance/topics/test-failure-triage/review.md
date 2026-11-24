# Review: test-failure-triage

## Findings

none

## Checked

- `rules.md`: **evidence-states-what-was-observed** stays at MUST and now cites only `bp-bug-report-observed-vs-expected` and `bp-failure-record-copies-log`. Both claims exist in research.json and are imperative primary sources (Mozilla's "precisely describe the observed (actual) result and the expected result ... Clearly separate facts (observations) from speculations"; Chromium/Mozilla's "Copy+paste the relevant parts of the log"). Together they carry the MUST, including the "kept apart from what is inferred" clause.
- `rules.md`: **bug-names-observed-misbehavior** stays at MUST and now cites only `bp-bug-report-observed-vs-expected`, which carries the observed-versus-expected requirement at imperative strength.
- The claims dropped from those two rules are still accounted for: `bp-separate-information-from-judgment` is cited by **verdict-states-confidence-and-its-basis** (SHOULD), `ev-get-data-first` by **reproduce-in-the-failing-environment** (SHOULD), and `bp-failure-message-desired-actual` (SWE at Google) is kept as support in `rationale.md`. The verdict that names it (bug-names-observed-misbehavior, supported) still has its rule, so no supported verdict is left without a rule.
- `a-complete-review-must-establish.md` and `a-build-must-establish.md`: both rules stay on the MUST lists, which matches their unchanged MUST strength.
- `examples.md`, flake verdict: "Confidence: 6 (1-10)" uses the 1-10 scale of **high-confidence-needs-reproduction-and-mechanism**, stays below 9 because there is no reproduction on demand and no confirmed mechanism, and states its basis and gaps. It no longer shows the ICD 203 likelihood-term option the owner list leaves open.
- `examples.md`, uncertain verdict: it now has "Confidence: 3 (1-10)" with its basis and gaps, as **verdict-states-confidence-and-its-basis** asks and on the scale the owner-list rule sets.
- `examples.md`, flake verdict: the copied log lines (the assertion message and two stack frames with file:line) now appear under `Observed:`, so the example shows what **evidence-states-what-was-observed**, **gather-failure-artifacts-before-classifying** and `what-a-reviewer-looks-for.md` ("with the log lines copied in") ask for.
- The diff touches only these lines. No other text changed, and none of the changed text conflicts with a cited claim.
- `cookr roles check` on the guideline runs cleanly and emits the reviewer and review-verifier roles.

## Rulings

- R1.1: fixed — both MUST rules now cite only the imperative claims (`bp-bug-report-observed-vs-expected`, `bp-failure-record-copies-log`), and the should-strength support moved to other rules and to rationale.md.
- R1.2: fixed — the flake example states "Confidence: 6 (1-10)" with its basis and gaps instead of "likely", and the uncertain example gains "Confidence: 3 (1-10)" with its basis and gaps.
- R1.3: fixed — the flake example now shows the copied log lines (the assertion line and stack frames with file:line) under `Observed:`.

## Lint

/lint-artifact on `cookbook/guidelines/testing/quality-assurance/test-failure-triage`, with cookr run as instructed:

- Shared checks FM-01 to FM-13: all PASS. The frontmatter, UUID, index entry, type, semver, required fields, license, copyright, dates, summary, H1, links (`cookr validate` found no unresolved or format-1 links) and Change History are all valid, and the doc has no TODO or placeholder text.
- Guideline checks: GF-01 PASS (summary paragraph), GF-02 PASS (structured), GF-03 PASS (all 23 rules use MUST/SHOULD/MAY). GF-04 is a WARN: there is no `## Compliance` section, and the doc uses "A complete review must establish" and "A build must establish" instead.
- `cookr validate` lists five owner-decides items for this artifact, one for each owner-list rule whose `-prior` claim is unsupported or contradicted (environment-cites-cross-test-signal, spec-rot-names-new-assertion, uncertain-names-missing-evidence, high-confidence-needs-reproduction-and-mechanism, triage-changes-nothing). The owner decides these under owner-list.md, so they are not lint errors. The validate failures in other artifacts do not touch this one.
- LINT SUMMARY: Pass 16 | Warn 1 | Fail 0. RESULT: CLEAN.

lint: clean

verdict: pass
