# Review: milestone-scheduling

## Findings

- `rules.md`, `define-and-sequence-milestones` against `milestone-has-status-and-target-date`: the same behaviours are required twice, at two strengths. `define-and-sequence-milestones` says Planning SHOULD "give each a target date" and "track each one's status". The owner-listed `milestone-has-status-and-target-date` holds "Every milestone has a status and target date" at MUST. Under behavioral-requirements (must-use-keywords-with-defined-semantics) and cookbook-compliance (must-not-contradict), one behaviour cannot be both absolute and waivable. This is the same class of finding decision-records R1.1 raised. The rule also bundles five behaviours into one sentence: define, sequence, date, record the chains, and track status and progress (behavioral-requirements must-not-bundle-behaviors-into-one-requirement). The overlap shows up again in `a-build-must-establish.md` (the `define-and-sequence-milestones` line), in the first bullet of `what-a-reviewer-looks-for.md` ("not defined, sequenced, dated or tracked") and in the first bullet of `a-complete-review-must-establish.md` ("sequenced, dated and tracked"). Fix: keep the rule's fixed name, but cut it to define the milestones, put them in sequence and record the dependency chains between them (same citations). Drop the target date and the status from it; they belong to the owner-listed rule, and their strength is the owner's open question. Move progress tracking into a new SHOULD rule, e.g. `track-milestone-progress`: "Each milestone's progress SHOULD be tracked, for example as the completion of the work linked to it (claims: github-milestones-due-date-progress, linear-milestones-optional-date)". Give it a build-bar line, then narrow the build-bar, review-focus and review-bar wording to match.
- `rules.md`, `justify-missing-logic` and `justify-unavoidable-hard-constraints` (these are the only two instances): both are SHOULD, but each cites a claim that states the requirement as "must", and neither claim was refuted. `missing-logic-justified` (trust 74, second check confirmed) quotes GAO: "any activity that is missing predecessor or successor logic must be clearly justified in the schedule documentation". `avoid-hard-date-constraints` (trust 74) quotes GAO: "If a hard constraint cannot be avoided, it must be used judiciously and must be fully justified by referring to some controlling event outside the schedule". The second check notes that the quote "matches the claim's scope and strength". Under criterion 3, each rule sits at the strength of the weakest claim it cites, so these two are understated. Both rules are conditional on a departure (a missing link, an unavoidable constraint), so MUST does not make the underlying SHOULD rules absolute. I checked every other rule for an unrefuted "must" claim cited at SHOULD and found none. `sequence-with-logic` quotes "must be logically sequenced", but it is refuted and cannot carry MUST. Fix: raise both rules to MUST: "...MUST be justified in the schedule documentation" and "...MUST be justified in the schedule's basis document by the event outside the schedule that controls it". Then update `rationale.md` paragraphs 1 and 2. They currently say "the rules carry its practice at SHOULD" and "The cycle rule is the one MUST"; they should name the two justification MUSTs too.
- `examples.md`, the sentence after the Python block: the cycle message it shows, `cycle in milestone chain: start -> launch -> beta -> api-freeze -> start`, is not what the code prints. I added `depends_on["start"] = {"launch"}` and ran the example under Python 3 with several `PYTHONHASHSEED` values. Every run printed `cycle in milestone chain: api-freeze -> docs-ready -> launch -> start -> api-freeze`. graphlib lists the cycle in successor order, each node followed by one that depends on it. The example shows dependency (predecessor) order, which graphlib never prints, and it names `beta` where graphlib names `docs-ready`. The hedge "(the order the error lists varies)" does not cover a reversed direction. This is a factual error against `topological-order-iff-acyclic`, which says graphlib reports the cycle. Fix: replace it with the real output, `cycle in milestone chain: api-freeze -> docs-ready -> launch -> start -> api-freeze`. Then change the parenthetical to say graphlib lists each milestone followed by one that depends on it, starting from whichever node it reaches first.
- `artifact.json` `related`, `intro.md` paragraph 2 and `rationale.md` last paragraph: the guideline hands parts of its scope to two indexed siblings, but it names them only by freeform description ("Delivery dependencies on other teams, tasks and their blockers ... are covered by their own guidelines"; "belong to the dependency-tracking guideline, tasks and their blockers to the task-breakdown guideline"). `related` is `[]`. The two siblings are dependency-tracking (`3f978ba7-c8c1-4b53-8fda-12e5a6966b75`) and task-breakdown (`f264cc0b-45d3-4593-a437-7371610c5a8a`). cross-recipe-consistency (must-reference-siblings-by-uuid, must-format-cross-references-consistently) and criterion 6 (`related` matches the new text) both apply, as in decision-records R1.4. Fix: add both UUIDs to `related`. In `rationale.md`, write them as `[adc.guideline.planning.project-management.dependency-tracking](cookbook:3f978ba7-c8c1-4b53-8fda-12e5a6966b75)` and `[adc.guideline.planning.project-management.task-breakdown](cookbook:f264cc0b-45d3-4593-a437-7371610c5a8a)`, and link the intro's mentions the same way. The project-record-linking mention stays freeform, because that topic has no artifact or UUID yet.

## Checked

- All 17 verdict rules are named rules in `rules.md` under their fixed names: 4 `supported`, 2 `unsupported` (both on the owner list) and 11 `new`. The 19 extra rules (`schedule-has-start-and-finish-milestones`, `work-is-not-a-milestone`, `keep-milestones-few`, `document-standard-milestones`, `one-place-for-the-target-date`, `justify-missing-logic`, `no-hard-constraints-in-the-baseline`, `justify-unavoidable-hard-constraints`, `report-the-cycle-found`, `critical-chain-is-an-option`, `estimate-without-padding`, `size-contingency-by-risk-analysis`, `status-date-is-not-view-or-save-date`, `update-on-a-regular-cadence`, `track-more-often-than-reported`, `document-schedule-changes`, `act-on-blocked-milestones`, `forecast-charts-do-not-replace-empiricism`, `commit-after-uncertainty-narrows`) are new rules, which may be named freely.
- Every one of the 50 claims in research.json is named by some verdict, and every one is cited by at least one rule. No `supported` or `new` claim is left without a rule. Every cited id exists in research.json and is named by a verdict.
- Every named rule ends with exactly one `(claim: …)` or `(claims: …)` citation, with nothing after it. `cookr validate` reports "Every researched artifact's rules cite its research".
- Strength against refuted claims: none of the 12 refuted claims is cited by a MUST rule. They are cited only by SHOULD, SHOULD NOT or MAY rules (`define-and-sequence-milestones`, `document-standard-milestones` MAY, `link-milestones-by-logic-not-fixed-dates`, `no-hard-constraints-in-the-baseline`, `check-chains-by-topological-sort`, `critical-chain-is-an-option` MAY, `size-contingency-by-risk-analysis` MAY, `status-date-is-not-view-or-save-date`, `update-on-a-regular-cadence`, `identify-at-risk-or-blocked-milestones`, `at-risk-milestone-names-its-risk`, `forecast-dates-from-history-as-ranges`, `fix-the-date-flex-the-scope` MAY). The "citation dropped" list is empty.
- `milestone-chains-have-no-cycles` MUST cites only `assess-network-for-circular-logic` (80, confirmed) and `topological-order-iff-acyclic` (88, confirmed). The refuted `ms-project-refuses-circular-dependency` is cited only by the SHOULD `check-chains-by-topological-sort`, so the MUST is within its citations.
- The refuted claims are worded to their quotes. `critical-chain-is-an-option` leaves out the buffers the second check found unquoted. The how-to and rationale say Microsoft Project "offers to cancel" rather than cancelling by default. `status-date-is-not-view-or-save-date` and `no-hard-constraints-in-the-baseline` do not call these a "common error". `fix-the-date-flex-the-scope` does not set the Product Goal against dated milestones.
- Owner list: `milestone-has-status-and-target-date` reads "Each milestone MUST pass this check: Every milestone has a status and target date (claim: milestone-has-status-and-target-date-prior)". `blocked-milestone-has-issue-or-concern` reads "A blocked milestone MUST pass this check: no milestone is blocked without a corresponding issue or concern (claim: blocked-milestone-has-issue-or-concern-prior)". Each has its prior text word for word after the listed lead-in and cites its `-prior` claim. None of the six open questions is turned into a finding here. `rationale.md` lists all six as the owner's.
- `a-build-must-establish.md` has exactly one line per named rule (36), and each line names a rule. `cookr roles check` is ok: 36 rules, no findings, four skills compiled. The MAY rules' build lines are conditional ("where …"), so no MAY becomes an obligation.
- Structure follows gf-roled-parts: intro, Rules, three how-tos, Examples, What a reviewer looks for, A complete review must establish, A build must establish, Rationale, References, then Change History last. Every part except the intro and the history has a valid role. The how-tos, examples, rationale and references each say they are informative.
- Frontmatter: `summary` is 159 characters, one line, and describes the new text. `tags` fit the content and share `project-management` and `planning` with the siblings. `platforms` is `[]`, which matches research.md ("Apple, Android and Windows have no bearing on this topic"). The index entry exists (`adc.guideline.planning.project-management.milestone-scheduling`). Version, modified and history are left for `cookr bump`.
- `references.md` and the `references` frontmatter list the same 26 URLs, which are the sources research.json cites.
- The critical-path example is correct. The links sum to 30 days on start, api-freeze, beta, launch, against 23 days via docs-ready, so `dag_longest_path` returns the path shown. The status-update example carries a status date, status, baseline against forecast, a named risk and an explained change, as the rules ask.
- The rationale explains the SHOULD and MAY choices: GAO is written for large programmes, schedule risk analysis is heavy for software teams, and fix-the-date and critical chain are method options. This meets behavioral-requirements must-explain-rationale-for-should-requirements and should-document-conditions-for-may-requirements. The second-check paragraph names all 12 refuted claims correctly.

## Lint

/lint-artifact (v2.0.1) on `cookbook/guidelines/planning/project-management/milestone-scheduling`, run with this checkout's cookr:

```
Type: guideline | Compliance: tbd/compliance/artifact-formatting/guideline-formatting.md

[PASS] FM-01: YAML frontmatter block present
[PASS] FM-02: id is a valid UUID (023d4c91-d797-4e82-880c-a4ad7906a54a)
[PASS] FM-03: Index entry matches folder (rdid adc.guideline.planning.project-management.milestone-scheduling)
[PASS] FM-04: type is guideline
[PASS] FM-05: version 1.0.0 valid semver
[PASS] FM-06: All required fields present
[PASS] FM-07: license MIT
[PASS] FM-08: copyright "2026 Mike Fullerton"
[PASS] FM-09: created/modified valid dates
[PASS] FM-10: summary non-empty
[PASS] FM-11: H1 matches title
[PASS] FM-11a: Links resolve (depends-on/related empty, no in-text cookbook links)
[PASS] FM-12: Change History present with one row
[PASS] FM-13: No TODO/placeholder text
[PASS] GF-01: Summary statement after H1
[PASS] GF-02: Structured guidance
[PASS] GF-03: RFC 2119 keywords in requirements
[WARN] GF-04: No "## Compliance" section
       -> Optional; add only if other compliance checks reference this guideline.
[FAIL] gf-rules-cite-research (cookr validate): rule 'milestone-has-status-and-target-date' cites 'milestone-has-status-and-target-date-prior', which the research rules unsupported
       -> Owner decides: keep, reword, or drop. Research verdict (research.md line 54): holds only as a SHOULD; the rule is worded "MUST pass this check".
[FAIL] gf-rules-cite-research (cookr validate): rule 'blocked-milestone-has-issue-or-concern' cites 'blocked-milestone-has-issue-or-concern-prior', which the research rules unsupported
       -> Owner decides: keep, reword, or drop. Research verdict: holds as a SHOULD; the rule is worded "MUST pass this check".

=== LINT SUMMARY ===
Artifact: milestone-scheduling
Type: guideline
Pass: 18 | Warn: 1 | Fail: 2
RESULT: NOT CLEAN — 2 failing checks. Fix these before the artifact can be approved.
```

The skill labelled the two gf-rules-cite-research items FAIL, but they are not lint errors:

- **What cookr reports:** `cookr validate` marks both as `!` "owner-decides" notices ("88 rule(s) the research does not support, left for the owner to decide"), not `✗` failures. Its own check passes: "Every researched artifact's rules cite its research".
- **They are owner-list rules:** both are the owner-listed rules, kept word for word with their accepted lead-ins under criterion 5. Their strength is the owner's first open question.
- **Sibling precedent:** sibling reviews (issue-tracking, dependency-tracking, task-breakdown) counted the same notices as WARN.
- **The WARN:** GF-04 is optional.

Outside this artifact, and not counted: `cookr validate` fails on sibling project-record-linking's `research/research.md` ("no YAML frontmatter block found") and reports index drift for `guidelines/INDEX.md`.

lint: clean

verdict: fail
