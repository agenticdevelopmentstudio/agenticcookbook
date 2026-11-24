# Review: dependency-tracking

## Findings

- `examples.md`, the RAID-log table: the identity-team dependency is marked "Internal", but `map-internal-and-external-dependencies` defines internal as "under the team's control" and external as "beyond it", and the claim it cites (`internal-and-external-dependency-classes`) gives "delivery of a product from another project" as an external dependency. Another team delivering an endpoint is beyond the mobile team's control, so the example contradicts the rule it illustrates. Fix: mark the entry "External", or change the example to a dependency that is under the team's own control.
- `rationale.md`, last paragraph: "PRINCE2 was reached only through secondary sources, so no rule rests on them" is untrue. `escalate-blocked-dependency-before-milestone` cites `prince2-manage-by-exception` (prince2.wiki, secondary) and names "the PRINCE2 project board once tolerance is exceeded", and `map-internal-and-external-dependencies` cites `internal-and-external-dependency-classes`, whose internal/external definitions are PRINCE2's as quoted by APM. Fix: keep "no rule rests on" for the PMBOK Guide, ISO 21502 and ISO 31000 only, and say PRINCE2 is reached through secondary sources (APM's quotation and prince2.wiki), which the escalation and internal/external rules use.
- `rationale.md`, fourth paragraph: "each team dependency roughly halves the chance of on-time completion; it names no study, and gives only the direction of the effect, never a figure" states the figure the research forbids. research.md and the claim's `trust.basis` for `each-dependency-halves-on-time-chance` (trust 5, refuted by the second check) say it is usable "only as the direction of the effect, never as a figure", and "roughly halves" is a figure. The clause "gives only the direction of the effect" also puts the research's limit on the model, which does give a figure. Fix: state the direction only, e.g. "A practitioner teaching model, reported second-hand and naming no study, holds that each added team dependency lowers the chance of on-time completion; the research uses it for that direction only."
- `rules.md`, bundled rules (behavioral-requirements must-not-bundle-behaviors-into-one-requirement; guideline-formatting one-requirement-per-rule): each of these rules joins two separately testable behaviours, so one can pass while the other fails: `dependency-owner-agreed-on-both-sides` (an agreed owner; the dependency confirmed and tracked in the other side's log), `dependency-has-need-by-date` (a need-by date is carried; the date is agreed with the source), `track-dependency-availability-and-status` (status tracked for the dependency's whole life; dependencies reviewed at regular points), `report-dependency-changes` (dependencies in the standard status reports; changes pushed to the people affected, already two SHOULDs in one bullet), `record-blocker-reason-and-duration` (a reason; a count of days blocked), `analyse-resolved-blockers` (resolved blocker records kept; clustered by cause), and `at-risk-dependency-logged-as-risk` (acknowledged as a risk with a management plan; reviewed for its effect on milestones). Fix: split each into one rule per behaviour, keeping the prior name on one half (names are fixed) and naming the other half freshly, each with its own citation and its own line in `a-build-must-establish.md` and its strength list in `a-complete-review-must-establish.md`.
- `rules.md`, `record-blocker-reason-and-duration` and `analyse-resolved-blockers`, against sibling `task-breakdown` (cross-recipe-consistency; cookbook-compliance must-not-contradict-applicable-guidelines): both guidelines rule on the same blocked-work-item practice from the same Leopold and Magennis source at different strengths. Counting the days blocked is SHOULD here but recording the block's dates is MAY in `task-breakdown`'s `blocker-records-dates`; keeping resolved blockers is MAY here (bundled with clustering) but SHOULD in `task-breakdown`'s `keep-resolved-blockers`. A team keeping both guidelines gets two answers for one blocked task. Fix (this topic's part): scope these two rules to the blocked dependency record rather than "a blocked work item", or align their strengths with `task-breakdown` where the research allows it (research.md gives `record-blocker-reason-and-duration` "MAY to SHOULD"), and point to `task-breakdown` for blocked tasks. Any change to `task-breakdown` is that sibling's, for the orchestrator to route.
- `artifact.json`, frontmatter `related` and `tags`: `related` is `[]`, although sibling guidelines this text overlaps already exist: `risk-tracking` (`a55182ef-3144-407c-b64a-6377f37f5c63`), whose risk register `at-risk-dependency-logged-as-risk` and the rationale's risk-register question turn on, and `task-breakdown` (`f264cc0b-45d3-4593-a437-7371610c5a8a`), which rules on blocked tasks, blocked-by links and blocker reasons that `flag-at-risk-or-blocked-dependencies`, `blocked-dependency-linked-to-affected-work` and `record-blocker-reason-and-duration` also cover. Criterion 6 asks for `related` to match the new guideline. `tags` also breaks the family vocabulary (cross-recipe-consistency must-use-family-tag-vocabulary): every sibling (`decision-records`, `issue-tracking`, `risk-tracking`, `task-breakdown`) tags itself with its own topic slug, and this one has `dependencies` but not `dependency-tracking`. Fix: add both uuids to `related` and add the tag `dependency-tracking`. Whether those siblings add this guideline to their own `related` is theirs.

## Checked

- All 13 verdict rules (3 `supported`, 2 `unsupported`, 8 `new`) are named rules in `rules.md` under their fixed names; the five added rules (`stale-status-is-a-signal`, `report-dependency-changes`, `analyse-resolved-blockers`, `coordinate-directly-with-the-other-team`, `rescope-to-remove-difficult-dependency`) are new names, which is allowed. No `supported` or `new` verdict is left without a rule.
- Every rule ends with exactly one `(claim: …)` or `(claims: …)` citation, nothing after it; every cited id is a claim in research.json and is named by some verdict. The only verdict-named claim cited by no rule is `each-dependency-halves-on-time-chance` (trust 5, refuted), used only in the rationale.
- Strength against refuted claims: the four refuted claims are cited only by `dependency-owner-agreed-on-both-sides` (SHOULD), `stale-status-is-a-signal` (SHOULD), `reduce-dependencies-before-tracking` (SHOULD) and `rescope-to-remove-difficult-dependency` (MAY); none carries MUST. No claim was in the "citation dropped" list.
- The second-check corrections reach the text: `dependency-owner-agreed-on-both-sides` says "the other project or team", not the "providing" side; `rescope-to-remove-difficult-dependency` keeps APM's "In extreme circumstances" at MAY, and `reduce-dependencies-before-tracking` rests on team organisation (LeSS, Team Topologies, DORA), not on "trade solutions"; the Linear tool note uses only the supported staleness part (health icon, grey when overdue).
- The other rules sit at the SHOULD or MAY the research gives: research.md calls the guidance "consistently SHOULD-level" with no mandatory field; `coordinate-directly-with-the-other-team` (LeSS only) is MAY; `escalate-blocked-dependency-before-milestone` follows the research's new-practice wording ("through a named forum or by exception") and its three named forums are each from a cited claim.
- Owner list: `dependency-has-type-and-status` and `blocked-dependency-linked-to-affected-work` keep their prior text word for word after the listed lead-in "A dependency record MUST keep this true:", each citing its `-prior` claim. None of the five open questions is settled: no status vocabulary is fixed beyond a blocked value the sources all show, "type" is left undefined, no escalation trigger time is set, the at-risk rule says "acknowledged as a source of risk" without naming the risk register, and `rationale.md` lists all of them as the owner's, including whether the two MUST checks stay.
- `a-build-must-establish.md` has exactly one line per named rule (18), each naming a rule; `cookr roles check` is ok (18 rules, no findings, four skills compiled). `a-complete-review-must-establish.md` lists each rule once at its own strength (2 MUST, 13 SHOULD, 3 MAY).
- Structure follows gf-roled-parts: intro, Rules, how-to, Examples, What a reviewer looks for, A complete review must establish, A build must establish, Rationale, References, then Change History last; the how-to, examples, rationale and references each say they are informative, and each Rules subsection has three to six rules.
- The intro gives a summary, a scope (delivery dependencies, excluding software dependencies, milestone ordering and record linking, which go to topics that have no guideline or uuid yet, so a freeform mention is the only form available) and a conformance statement, and holds no rule beyond restating them.
- Frontmatter: `summary` is 134 characters, one line, and describes the new text; `platforms` is `[]`, matching research ("no bearing" on Apple, Android or Windows) and every sibling; `references` matches the 25 sources in research.json and `references.md`; the id is in `cookbook/index.json`. Version, modified and history are left for `cookr bump`.
- The how-to and tool comparison match the claims (APM statement form, GitHub single-select and date fields, Linear orange/red flags, Jira's Flagged/Impediment field, Jira Plans' red off-track dependencies, RAID log fields) and the research's "How they compare", including that no tracker gives a dependency its own owner, date or status and that the health values apply to projects.
- The rationale explains the SHOULD defaults (behavioral-requirements must-explain-rationale-for-should-requirements) and matches the research's limitations (PMBOK, ISO 21502, ISO 31000 unreadable; Scrum Guide has no dependency record; Kanban Guide's "must" on active management), apart from the two rationale findings above.

## Lint

/lint-artifact (v2.0.1) on `cookbook/guidelines/planning/project-management/dependency-tracking`, run with this checkout's cookr against the compiled doc, plus `cookr validate` and a citation script:

```
Type: guideline | Compliance: tbd/compliance/artifact-formatting/guideline-formatting.md

[PASS] FM-01: frontmatter block present
[PASS] FM-02: id is a valid UUID (3f978ba7-c8c1-4b53-8fda-12e5a6966b75)
[PASS] FM-03: cookbook/index.json has the entry (path guidelines/planning/project-management/dependency-tracking, rdid adc.guideline.planning.project-management.dependency-tracking); no domain field
[PASS] FM-04: type is guideline
[PASS] FM-05: version 1.0.0 is valid semver
[PASS] FM-06: all gf-frontmatter-complete fields present
[PASS] FM-07: license is MIT
[PASS] FM-08: copyright is "2026 Mike Fullerton"
[PASS] FM-09: created and modified are 2026-11-24
[PASS] FM-10: summary non-empty, over 10 characters
[PASS] FM-11: H1 matches title
[PASS] FM-11a: depends-on, related, ingredients empty; cookr validate reports no link errors for this artifact
[PASS] FM-12: Change History has one row
[PASS] FM-13: no TODO, TBD, FIXME or placeholder text
[PASS] GF-01: summary statement follows the H1
[PASS] GF-02: structured guidance present
[PASS] GF-03: all 18 rules use MUST, SHOULD or MAY
[PASS] GF-04: no Compliance section, none required
[PASS] gf-triggers-field: triggers: [] present
[PASS] gf-roled-parts: every part has a role; build bar has 18 lines, one per rule
[PASS] gf-named-rules: every rules bullet is a uniquely named rule with an RFC 2119 keyword
[PASS] gf-research-folder: research.json has 32 claims and 13 verdicts; research.md has the four headings in order
[PASS] gf-rule-cites-research: every cited claim id is in research.json and has a verdict
[WARN] owner-decides (cookr validate): dependency-has-type-and-status cites dependency-has-type-and-status-prior; blocked-dependency-linked-to-affected-work cites blocked-dependency-linked-to-affected-work-prior (unsupported prior claims; the owner list keeps them, and the rationale leaves the decision to the owner)

Outside this artifact (not counted): cookr validate fails on sibling project-record-linking/research/research.md ("no YAML frontmatter block found").

=== LINT SUMMARY ===
Artifact: dependency-tracking
Type: guideline
Pass: 24 | Warn: 1 | Fail: 0

RESULT: CLEAN — artifact passes all checks.
```

lint: clean

verdict: fail
