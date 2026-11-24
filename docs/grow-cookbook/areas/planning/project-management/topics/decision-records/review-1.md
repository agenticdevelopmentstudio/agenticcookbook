# Review: decision-records

## Findings

- `rules.md`, `supersession-links-both-ways` against `acknowledge-contradicted-decisions`: two behaviours are required twice, at two strengths. (1) Marking the earlier record superseded is a MUST in `acknowledge-contradicted-decisions` ("the earlier record is marked superseded") and a SHOULD in `supersession-links-both-ways` ("the superseded record SHOULD be marked superseded with a link to its replacement"). (2) The new record naming the record it replaces is a MUST in `acknowledge-contradicted-decisions` ("a new record that names the earlier decision") and a SHOULD in `supersession-links-both-ways` ("the new record SHOULD name the record it replaces"). Under cookbook-compliance (must-not-contradict) and behavioral-requirements (must-use-keywords-with-defined-semantics), one behaviour cannot be both absolute and waivable. The two build-bar lines and the review-focus sentence repeat the overlap. Fix: cut `supersession-links-both-ways` down to the one thing it adds, the link from the superseded record's mark to its replacement. For example: "When one record supersedes another, the superseded record's status SHOULD link to the record that replaces it. (claims: supersede-and-link, supersession-header-fields, gds-way-supersede-must)". It stays SHOULD, because it cites two refuted claims. Narrow its `a-build-must-establish.md` line to match ("each superseded record's status links to its replacement").
- `a-build-must-establish.md`, `backfill-undocumented-decisions`: the line "where a log was started for an existing system, known past decisions were recorded where their data was available" turns a MAY rule into an obligation the build must meet. The other MAY rule's line is written "where used" (`record-confidence-level`), and the review bar files backfill under "noted where it was used". Fix: make the line conditional on use, e.g. "where used, past decisions recorded retroactively are ones whose data was available".
- `intro.md`, first paragraph: "A later decision that changes an earlier one never edits or silently contradicts it" and "the two link to each other" state as absolutes what the rules hold at lower strength. Not editing an accepted record is SHOULD NOT (`supersede-never-edit-accepted-records`). It cannot carry MUST, because it cites the refuted `adr-tools-supersede-command` and `clarifications-may-amend`. Two-way linking is SHOULD (`supersession-links-both-ways`). Only the "silently contradicts" part is MUST. Fix: keep "never silently contradicts" and soften the rest so it matches the rules, e.g. "...is a new record rather than an edit, it marks the old one superseded, and the two should link to each other".
- `intro.md`, second paragraph: "such as datastore selection" mentions a cookbook artifact by a freeform description. cross-recipe-consistency (must-reference-siblings-by-uuid, must-format-cross-references-consistently) asks for an in-text `[rdid](cookbook:uuid)` link, which is the form sibling `task-breakdown` uses in its rationale. The artifact is already in `related`. Fix: write it as `[adc.guideline.planning.data.datastore-selection](cookbook:6a653107-929d-418e-865d-636373a27b02)`. The other mention there, "project record linking", has no guideline or uuid yet, so a freeform mention is the only form available and is not part of this finding.
- Lint FM-03: `cookbook/index.json` has no entry for id `2b7a1593-48e0-4bbe-8e14-0df7a863628d` (expected rdid `adc.guideline.planning.project-management.decision-records`). template-conformance must-have-index-entry-and-matching-rdid fails for the same reason, and `cookr validate` reports index drift for `guidelines/INDEX.md`. Fix: run `cookr update`, using this checkout's cookr, to add the index entry and regenerate the index.

## Checked

- Every one of the 17 verdict rules (11 `new`, 6 `supported`) is a named rule in `rules.md` under its fixed name. The author added one rule, `decision-links-to-its-work`, which is allowed for a new rule.
- Every claim named by a verdict is cited by at least one rule, so no `supported` or `new` verdict's claims are left without a rule. Every rule's citations name claims that exist in research.json and that some verdict names. `jira-link-types-no-supersedes` and the other context claims appear only in informative sections.
- Every rule ends with exactly one `(claim: …)` or `(claims: …)` citation, with nothing after it. `cookr validate` reports "Every researched artifact's rules cite its research" and flags no frontmatter or link issue for this artifact.
- Strength against refuted claims: the five refuted claims are cited only by `supersede-never-edit-accepted-records` (SHOULD NOT), `supersession-links-both-ways` (SHOULD) and `backfill-undocumented-decisions` (MAY). None of the three carries MUST. No claim was in the "citation dropped" list.
- `acknowledge-contradicted-decisions` MUST: it cites `supersede-and-link` (confirmed; GDS "must be clearly marked"; trust 89), `cloud-providers-agree-on-supersession` (AWS "requires creating a new ADR"; trust 88) and `records-prevent-relitigation` (trust 85). None of these is refuted. The second check refuted `gds-way-supersede-must` only on the heading placement, and that claim is not cited here. So the MUST is within its citations.
- Every other rule sits at the strength research.md gives it: SHOULD for context, rationale, decider, alternatives, consequences, date, status, one-decision, significance, rejected proposals, findability and links; SHOULD NOT for dummy alternatives; MAY for confidence level and backfill. `backfill-undocumented-decisions` keeps Microsoft's "where the data is available" condition, which the second check said the claim had dropped.
- The prior rule names `capture-rationale-alternatives-and-decider`, `decision-has-rationale-and-decider` and `decisions-findable-and-linked` are kept, with their content split across separate rules (rationale, decider, alternatives, links). That avoids bundled requirements, and the names are fixed under criterion 4.
- Owner list: there are no prior rules to keep word for word. None of the seven open questions is settled by the text. The decider and alternatives rules stay at the SHOULD the research supports. Clarification edits are not addressed (the rule covers only changing a decision). Storage says "a store that keeps a history" and picks neither repository nor wiki. The how-to says to pick a template without naming one. Deprecated is reported as MADR's addition. Deletion and numbering are not ruled on. `rationale.md` lists all seven as the owner's.
- Second-check corrections show up in the prose. `rationale.md` says GDS allows a clarification "during implementation", and the how-to cites PEP headers, not RFC headers, for two-way supersession.
- `a-build-must-establish.md` has exactly one line per named rule (18), and each line names a rule. `cookr roles check` is ok, with 18 rules, no findings, and four skills compiled. `a-complete-review-must-establish.md` puts each of the 18 rules in exactly one strength list (1 MUST, 15 SHOULD, 2 MAY), matching the rules.
- Structure follows gf-roled-parts: intro, Rules, how-to, Examples, What a reviewer looks for, A complete review must establish, A build must establish, Rationale, References, then Change History last. The how-to, examples, rationale and references each declare themselves informative.
- Frontmatter: `summary` is 157 characters, one line, and describes the new text. `tags` (decision-records, adr, project-management, supersession) fit the content and share `project-management` with sibling `task-breakdown`. `platforms` is `[]`, matching research ("no bearing" on Apple, Android or Windows) and the sibling. `related` holds datastore-selection, which resolves. Version, modified and history are left for `cookr bump`.
- `references.md` and the `references` frontmatter list the same sources that research.json cites.
- The examples follow the rules: the superseded record is marked under its heading with a link, and the replacement carries status, date, decider, a Supersedes link, considered options with reasons, and good and bad consequences. The Y-statement follows the shape in the `y-statement` claim.
- The rationale's SHOULD explanations meet behavioral-requirements must-explain-rationale-for-should-requirements. Its evidence caveats (no outcome study; the adoption study is context only; PMBOK and the others were unreachable) match research.json's limitations.

## Lint

/lint-artifact (v2.0.1) on `cookbook/guidelines/planning/project-management/decision-records`, run with this checkout's cookr:

```
Type: guideline | Compliance: tbd/compliance/artifact-formatting/guideline-formatting.md

[PASS] FM-01: YAML frontmatter block present
[PASS] FM-02: id is a valid UUID (2b7a1593-48e0-4bbe-8e14-0df7a863628d)
[FAIL] FM-03: Index entry matches folder
       -> cookbook/index.json has no entry for this id and no entry whose path is guidelines/planning/project-management/decision-records. Expected rdid: adc.guideline.planning.project-management.decision-records. Run `cookr update` to add it.
[PASS] FM-04: type is guideline
[PASS] FM-05: version 1.0.0 is valid semver
[PASS] FM-06: all required fields present (approved-by and approved-date are blank, not checked)
[PASS] FM-07: license is MIT
[PASS] FM-08: copyright "2026 Mike Fullerton"
[PASS] FM-09: created and modified are ISO dates
[PASS] FM-10: summary is non-empty
[PASS] FM-11: H1 "Decision Records" matches title
[PASS] FM-11a: links resolve
       -> The only link is related 6a653107-..., which is in the index as datastore-selection. `cookr validate` reports nothing for this artifact.
[PASS] FM-12: Change History section present with one row
[WARN] FM-13: placeholder text
       -> Line 85 of the compiled doc says "Fill in the context, the decision...". It is an instruction step in the how-to, not a placeholder. No TODO, TBD, FIXME or placeholder text was found.
[PASS] GF-01: summary statement follows H1
[PASS] GF-02: structured guidance (rules, how-to, tables, subsections)
[PASS] GF-03: RFC 2119 keywords on every rule
[PASS] GF-04: Compliance section is optional and nothing references it
[PASS] gf-roled-parts: the rules, review-focus, review-bar and build-bar parts are all present with valid roles
[PASS] gf-named-rules: 18 named rules, all names unique, each with an RFC 2119 keyword
[PASS] gf-research-folder: research.json and research.md are present, with the four question headings in order
[PASS] gf-rule-cites-research: every rule ends in a claim citation, and all cited ids exist in research.json
[PASS] gf-triggers-field: `triggers` is present and empty, which is allowed

=== LINT SUMMARY ===
Artifact: decision-records
Type: guideline
Pass: 22 | Warn: 1 | Fail: 1
RESULT: NOT CLEAN — 1 failing check. Fix these before the artifact can be approved.
```

The FM-13 WARN is not an error. `cookr validate` also reports four frontmatter-presence issues, but all four are in sibling topics' research.md files (dependency-tracking, milestone-scheduling, project-record-linking, risk-tracking), not this artifact.

lint: fail 1

verdict: fail
