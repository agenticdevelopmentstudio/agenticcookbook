# Review: project-record-linking

## Findings

- `rules.md` against sibling guidelines: some links this guideline makes a SHOULD or a MAY are required at a different strength by the sibling guideline for that kind of record, and nothing says which one governs. `intro.md` says each kind's own fields "stay with that record's own guideline". The rules still cover supersession, blockers and part-of links for every record, so the overlap is in the rules themselves. Under cookbook-compliance (must-not-contradict-applicable-guidelines, must-be-at-least-as-strict-as-guideline-musts, must-satisfy-all-applicable-guidelines-together) and behavioral-requirements (must-use-keywords-with-defined-semantics), a reader of both guidelines gets a waivable and an absolute version of the same behaviour. All the instances:
  1. `superseding-record-links-both-ways` (SHOULD: the superseding record links to the one it replaces, and the replaced one is marked superseded) against decision-records `acknowledge-contradicted-decisions` (MUST: "a new record that names the earlier decision, and the earlier record is marked superseded"). The same overlap shows in `close-or-supersede-never-delete`'s "marked superseded".
  2. `blocked-record-names-its-blocker` (SHOULD) against task-breakdown `blocked-task-references-blocker` (MUST: "blocked todos reference a specific blocker"), dependency-tracking `blocked-dependency-linked-to-affected-work` (MUST) and milestone-scheduling `blocked-milestone-has-issue-or-concern` (MUST).
  3. `child-record-carries-parent-link` (MAY) against task-breakdown `link-tasks-to-milestones` (SHOULD: each task linked to its milestone) and issue-tracking `link-fix-change-to-issue` (SHOULD: the fixing change linked to the issue). The research and `rationale.md` make this MAY about which end carries the link ("only GitHub documents which end carries it"). The rule text, "MAY carry the link to the larger record", reads as making the link itself optional.

  Fix: keep every strength, since the research supports nothing above SHOULD. Add one sentence to `intro.md`: where a kind of record's own guideline requires one of these links at a stronger level, that guideline governs for that kind, and this guideline is the baseline for the others. Name the four MUST rules above with in-text links (see the next finding). Reword `child-record-carries-parent-link` so the option is the end, not the link. For example: "Where a record is part of a larger one, such as a sub-issue under its parent issue, work under a milestone, or the change that resolves an issue, the link between them MAY be carried on the smaller record. (claims: ks-github-sub-issues-and-milestones, ks-github-closing-keywords)". Change its `a-build-must-establish.md` line to match ("where used, the link between a part record and the record it is part of is carried on the part record").
- `intro.md` (second paragraph) and `linking-project-records.md` (step 5): sibling guidelines are named by freeform description. The intro has "decision supersession with decision records, issue resolution with issue tracking, blocked milestones with milestone scheduling, task blockers with task breakdown, and the risk and dependency fields with risk tracking and dependency tracking", and step 5 has "is a question for decision records". All six siblings exist and are in `related`. cross-recipe-consistency (must-reference-siblings-by-uuid, must-format-cross-references-consistently) asks for in-text `[rdid](cookbook:uuid)` links, the form decision-records uses for datastore-selection. Fix: write each one as its link: `[adc.guideline.planning.project-management.decision-records](cookbook:2b7a1593-48e0-4bbe-8e14-0df7a863628d)`, `…issue-tracking](cookbook:f77eeffe-2699-4028-9195-4bfc23c75e91)`, `…milestone-scheduling](cookbook:023d4c91-d797-4e82-880c-a4ad7906a54a)`, `…task-breakdown](cookbook:f264cc0b-45d3-4593-a437-7371610c5a8a)`, `…risk-tracking](cookbook:a55182ef-3144-407c-b64a-6377f37f5c63)` and `…dependency-tracking](cookbook:3f978ba7-c8c1-4b53-8fda-12e5a6966b75)`, each with the full `adc.guideline.planning.project-management.` rdid. Uses of "decision records" for the kind of record, such as in `rationale.md`, are not part of this finding.

## Checked

- All 13 verdict rules (every one `new`) are named rules in `rules.md` under their fixed names. The author added `identifier-carries-no-status` and `mark-changed-links-suspect`, which is allowed for new rules. Both cite claims a verdict names: `bp-identifier-carries-no-status` (named by `id-never-reused-or-renamed`) and `ks-suspect-links` (named by `check-links-for-dangling-targets`).
- A script over `rules.md` and research.json confirmed that each of the 15 rules ends with exactly one `(claim: …)` or `(claims: …)` citation with nothing after it, and that every cited id exists in research.json and is named by some verdict. Every claim a verdict names is cited by at least one rule. `pg-scrum-guide-leaves-attributes` is named by no verdict and appears only in the rationale. `cookr validate` passes ("Every researched artifact's rules cite its research") and reports nothing for this artifact.
- Strengths match research.md's verdicts: SHOULD or SHOULD NOT for the ten SHOULD verdicts and the added `identifier-carries-no-status`, and MAY for `child-record-carries-parent-link`, `realised-risk-links-to-its-issue`, `report-unlinked-records` and the added `mark-changed-links-suspect` (a single vendor source, trust 62). No rule carries MUST, which matches research.md: "The strongest strength they support is SHOULD."
- Refuted claims: `ks-two-way-link-recorded-once` and `bp-bidirectional-traceability` are cited only by `two-way-link-recorded-once-shown-both-ways` (SHOULD). `ev-missing-links-impede` is cited only by `check-links-for-dangling-targets` (SHOULD) and `report-unlinked-records` (MAY). None carries MUST. The citation-dropped claim `ks-jira-typed-links-two-descriptions` stays at full strength in `typed-links-with-both-readings` (SHOULD).
- The second check's caveats are reflected. The two-way rule says "one relationship that is shown from both records", not "recorded once", so it doesn't claim the storage behaviour the check refuted. `rationale.md` calls the bidirectional-traceability definition requirements-only and the missing-links evidence one case. `rationale.md` and `references.md` describe the PRINCE2 sources as trainer summaries.
- Each rule follows from its cited claims. Some examples: `id-never-reused-or-renamed` from Nygard/MADR and the Jira and GitHub redirects; `close-or-supersede-never-delete` from GitHub's page-not-found on deletion and Linear's Related; `link-instead-of-copy` from GitHub's single source of truth; `realised-risk-links-to-its-issue` keeps the secondary-source MAY.
- Owner list: there are no prior rules to keep word for word. None of the seven open questions is settled. The how-to leaves open whether links are stored in both files or computed, the identifier scheme, fail versus warn, whether links to closed records are reported, and which records need a link. Step 5 leaves decision amendments to decision records. `realised-risk-links-to-its-issue` says only that the two MAY be linked, and the examples are labelled as illustrations, not a required format. `rationale.md` lists all seven as the owner's.
- `a-build-must-establish.md` has exactly one line per named rule (15), each naming a rule, and the four MAY lines read "where used". `cookr roles check` is ok: 15 rules, no findings, and the builder, build-verifier, reviewer and review-verifier skills compiled. `a-complete-review-must-establish.md` puts each of the 15 rules in exactly one list (11 SHOULD, 4 MAY), matching the rules.
- `what-a-reviewer-looks-for.md` covers each of the 11 SHOULD rules and nothing beyond the rules.
- Structure follows gf-roled-parts: intro, Rules, how-to, Examples, What a reviewer looks for, A complete review must establish, A build must establish, Rationale, References, then Change History last. The how-to, examples, rationale and references each say they are informative. The intro's "No rule here is a MUST" is accurate.
- The rationale explains why each SHOULD can be departed from (behavioral-requirements must-explain-rationale-for-should-requirements), and the research's limitations are carried over: the paywalled standards, Kanban, SAFe and LeSS not researched, no study of dangling-link frequency.
- Frontmatter: `summary` is 151 characters, one line, and describes the new text. `tags` include `project-management`, the tag the siblings share. `platforms` is `[]`, matching research ("Apple, Android and Windows have no bearing"). `related` lists the six project-management siblings, and each UUID resolves in `cookbook/index.json`. `references` matches `references.md` and the sources in research. The artifact is in `cookbook/index.json` (id `23e55c7c-…`) and in `guidelines/INDEX.md`.
- The examples follow the rules: supersession is linked both ways with the old record marked, the blocked link is shown from both ends with each end's reading, the realised risk is linked to its issue, and the link-check output reports a dangling link and an unlinked record.

## Lint

/lint-artifact on `cookbook/guidelines/planning/project-management/project-record-linking`, run with this checkout's cookr. It compiled the folder and ran `cookr validate`, which passed:

```
Type: guideline | Compliance: tbd/compliance/artifact-formatting/guideline-formatting.md

[PASS] FM-01, FM-02, FM-04 to FM-12, FM-13
[PASS] FM-03: index.json entry for the id has path guidelines/planning/project-management/project-record-linking and rdid adc.guideline.planning.project-management.project-record-linking; no domain field
[PASS] FM-11a: cookr validate reports no unresolved links
[PASS] GF-01: summary statement follows the H1
[PASS] GF-02: rules are structured bullets under subsections
[PASS] GF-03: every rule uses SHOULD, SHOULD NOT or MAY
[PASS] GF-04: no ## Compliance section, optional here
[PASS] gf-frontmatter-complete, gf-type-field, gf-title-heading, gf-change-history
[PASS] gf-triggers-field: triggers present and empty, which is allowed
[PASS] gf-roled-parts: rules, review-focus, review-bar and build-bar present; build-bar has exactly one line per each of the 15 named rules
[PASS] gf-named-rules: all 15 rules are kebab-named bullets with RFC 2119 keywords
[PASS] gf-research-folder: research.json and research.md exist with the four question headings
[PASS] gf-rule-cites-research: each rule ends with one (claim: …)/(claims: …) citation, and every id resolves
[WARN] cookr validate printed owner-decides warnings for other guidelines in the tree (e.g. task-milestone-m…, blocked-task-ref…); none for this one

=== LINT SUMMARY ===
Artifact: project-record-linking
Type: guideline
Pass: 29 | Warn: 1 | Fail: 0
RESULT: CLEAN — artifact passes all checks.
```

The lint could not run its own version check, because the skill loaded from another worktree. The one WARN is about sibling guidelines and is not an error.

lint: clean

verdict: fail
