# Review: test-failure-triage

## Findings

- `rules.md`, two MUST rules cite claims that carry only SHOULD (criterion 3, the strength rule). Every instance: (1) **evidence-states-what-was-observed** (MUST) cites `bp-separate-information-from-judgment`, whose trust basis says ICD 203 "carries 'should', a recommendation" and which research.md calls "a 'should' standard from outside software". It also cites `ev-get-data-first`, a secondary review (trust 48) that research.md puts at SHOULD ("The sources support only a SHOULD ... (bp-explain-uncertainty-and-gaps, ev-get-data-first)"). (2) **bug-names-observed-misbehavior** (MUST) cites `bp-failure-message-desired-actual`, whose quote is "it should clearly express the desired outcome, the actual outcome" and which comes from a secondary practitioner book. No other MUST rule cites a should-strength claim. The other three supported MUST rules cite tool definitions, tool data and a study's classification, and the five owner-list rules carry the accepted "This MUST hold:" lead-in. Fix: keep both rules at MUST and cite only the imperative claims that hold the MUST: `(claims: bp-bug-report-observed-vs-expected, bp-failure-record-copies-log)` for evidence-states-what-was-observed and `(claim: bp-bug-report-observed-vs-expected)` for bug-names-observed-misbehavior. Mozilla's "Clearly separate facts (observations) from speculations" still carries the "an argument from what is likely is not evidence" clause. The ICD 203, Agans and SWE-at-Google support can stay in `rationale.md`. If the author keeps those citations, the rule has to drop to SHOULD instead, and its line in `a-complete-review-must-establish.md` moves from the MUST list to the SHOULD list.
- `examples.md`, the example verdicts do not keep the MUST rule **high-confidence-needs-reproduction-and-mechanism** ("`confidence` is 1-10"), and one of them leans toward the owner's open question. Every instance: (1) the flake verdict states "Confidence: likely.", a likelihood term instead of a 1-10 value. That is the ICD 203 alternative the owner list leaves open ("or replaced by a stated likelihood term ... as ICD 203 has it"), so the illustration shows the unsettled option as if it were the practice. (2) The uncertain verdict states no confidence at all, although the 1-10 rule and **verdict-states-confidence-and-its-basis** apply to every verdict. Fix: give the flake example a value on the stated scale below 9, since it has no reproduction on demand and no confirmed mechanism, for example "Confidence: 6 (1-10). Rests on the same-revision pass and the history; not yet reproduced on demand, so a product-side race in the cart update is not ruled out." Add a confidence line with its basis and gaps to the uncertain example, for example "Confidence: 3 (1-10). One timeout and one passing rerun; no trace and no runner-wide signal."
- `examples.md`, flake verdict, the line "(log lines copied below)" points to log lines that the example never shows. The example therefore does not show what **evidence-states-what-was-observed** and **gather-failure-artifacts-before-classifying** ask for, or what `what-a-reviewer-looks-for.md` checks ("with the log lines copied in"). Fix: add two or three illustrative copied log lines under the `Observed:` entry, for example the assertion line and its file:line, or reword it to "(the assertion line and stack trace are copied into the record)".

## Checked

- `cookr roles check` passes: 23 rules, no findings. All four skills compile: builder, build-verifier, reviewer and review-verifier.
- `cookr validate` shows no issue for this topic. Its only errors belong to sibling topics, not this one: `exploratory-testing-charters/research/research.md` and `test-impact-analysis/research/research.md` have no YAML frontmatter, and the guidelines index has drifted. Those go to the siblings `exploratory-testing-charters` and `test-impact-analysis`. This topic's five `owner-decides` lines are informational and match the owner list.
- `cookr compile` produces one doc with every section in the required order: intro, Rules, how-to, Examples, What a reviewer looks for, A complete review must establish, A build must establish, Rationale, References, Change History. The compiled doc was deleted afterwards.
- Every one of the 23 verdict rules has a named rule in `rules.md`, and no named rule lacks a verdict. All prior rule names are kept.
- Every rule ends with exactly one `(claim: …)` or `(claims: …)` citation with nothing after it, and every cited id is a claim in research.json that some verdict names.
- The refuted claim `bp-sheriffs-review-every-failure` is cited only by **named-triage-rotation-owns-failures**, which is a SHOULD. The author dropped it from **every-failure-gets-one-disposition** (MUST). The how-to's wording ("review the failures their trees show") does not repeat the refuted "every failure". No claim is listed under "citation dropped".
- All five owner-list rules keep their prior text word for word after the lead-in "This MUST hold:" that the owner list records. Each cites only its `<rule>-prior` claim.
- No open question is settled in the rules, the how-to or the rationale. The rationale names each one as open. The how-to's hand-off of a flake to the quarantine guideline does not decide whether a flake also opens a product investigation.
- The SHOULD and MAY strengths of the new rules match their claims. **never-force-a-verdict** is at SHOULD, as research.md says for a Worker Focus clause. **pass-on-retry-does-not-clear-a-bug** is SHOULD NOT, from warnings. **record-flake-cause-category** and **known-failure-marked-expected-with-reason** are MAY, from optional tool features.
- Each rule follows from its claims. Spot checks: the flake definitions on unchanged code (CircleCI, Azure, Firebase, Playwright, Surefire); the one-way reading of a rerun (Luo et al.); Trunk's and Meta's broken-versus-flaky split; Lam et al.'s CI-only flakiness; Jest's fix-before-regenerate; SWE at Google on tests changing only with an intended behavior change.
- The new rules were dropped as uncited claims only where that is allowed: `ev-google-flaky-failure-share` (trust 45, which research.md says supports disposition-from-fixed-set "only that far") is used in the rationale with its caveat. `bp-triage-acts-on-verdict` is named only by the contradicted verdict, and the rationale uses it to explain the open question.
- `a-build-must-establish.md` has exactly one line per named rule, each matching its rule. `a-complete-review-must-establish.md` lists the 10 MUST, 11 SHOULD and 2 MAY rules correctly.
- `rationale.md` states each figure as the research does: Labuschagne 18/13/74/26%; Luo's 4.56%, with its undisclosed-classification caveat; 24% and 94%; Lam's 86%; Gruber's 28% via Parry. It explains why the SHOULD rules allow departure (must-explain-rationale-for-should-requirements) and states the limitation that no source has an agent as triager.
- Informative parts say so at their start: how-to, examples, rationale and references. References are marked informative.
- Frontmatter: the summary is 153 characters and describes the new text. Tags (`testing`, `triage`, `flaky`, `ci`, `failure-classification`) share the `flaky` and `ci` vocabulary of flaky-test-quarantine. `platforms: []` fits a platform-neutral guideline. The five `related` UUIDs resolve to flaky-test-quarantine, flaky-test-prevention, snapshot-testing, incident-response and issue-tracking, and the intro and how-to link to them in `[rdid](cookbook:uuid)` form. The 40 `references` match research.json's 40 sources exactly.
- Cross-recipe consistency with flaky-test-quarantine: its "retry pass is flaky" and "flip rate on unchanged code" agree with **flake-cites-history-or-race** and the how-to's "A pass shows the test is flaky". Scope is split cleanly: the lifecycle is left to quarantine and prevention.
- The two names for the stale-test disposition ("spec-rot" in owner text, "stale test" elsewhere) are left alone, because the name is an open question on the owner list.

## Lint

/lint-artifact on `cookbook/guidelines/testing/quality-assurance/test-failure-triage` (guideline; compliance `tbd/compliance/artifact-formatting/guideline-formatting.md`):

```
[PASS] FM-01 .. FM-13 (frontmatter, UUID, index entry and rdid adc.guideline.testing.quality-assurance.test-failure-triage, type, semver, required fields, MIT, copyright, ISO dates, summary, H1 = title, 5 related UUIDs and 4 in-text cookbook: links resolve, Change History row, no placeholder text)
[PASS] GF-01: summary paragraph follows the H1
[PASS] GF-02: structured guidance
[PASS] GF-03: rules use MUST, SHOULD and MAY
[WARN] GF-04: no `## Compliance` section (optional)
[WARN] cookr validate research check: owner-decides on the owner-list rules
Pass: 18 | Warn: 2 | Fail: 0
RESULT: CLEAN
```

The two "no YAML frontmatter block found" failures in `cookr validate` are in sibling topics' research.md files, not this artifact.

lint: clean

verdict: fail
