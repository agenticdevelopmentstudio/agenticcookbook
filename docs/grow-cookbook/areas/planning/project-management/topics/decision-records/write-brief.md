# Write brief: decision-records

Today is 2026-11-24.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/decision-records (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/decision-records/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/decision-records/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/decision-records/owner-list.md.
cookr, this checkout's own (never an installed one): PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook <command>

Review criteria. Stage 4 reviews against exactly these, and the author writes to them:

1. Every guideline in /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/recipe-quality/:
   behavioral-requirements, completeness, cookbook-compliance,
   cross-recipe-consistency, source-fidelity and template-conformance.
2. Source fidelity means fidelity to the research:
   - every rule follows from the claims it cites, at the strength it states;
   - no claim with a `supported` or `new` verdict is left without a rule;
   - every rule ends with its citation, and every cited claim exists.
3. The strength rule: each rule is at the strength of the weakest claim it
   cites. A claim the second check refuted (listed under "Second-check
   corrections, refuted" in the write brief; its `trust.basis` says "Second
   check … refuted") cannot carry MUST. A claim that only lost a citation
   whose source lacked the quote (listed under "citation dropped") is still
   supported, and its strength is unchanged.
4. A rule's citations are authoritative. A verdict's `claims` list is stage
   2's record of the old rule: nobody compares it with the rule's citations,
   and research is not edited after stage 2. A rule may cite any claim of
   research.json that some verdict names. Prior rule names (the names the
   verdicts key on) are fixed; new rules may be named and renamed freely.
5. The owner list (owner-list.md): a prior rule listed there keeps its prior
   text word for word, citing `<rule>-prior`. Only its wording is exempt from
   review, nothing else. Where the prior text has no RFC keyword, one lead-in
   in front of it carries the keyword the old text implied ("In TypeScript,
   the panel MUST be reached this way:"); owner-list.md lists the lead-in, and
   it is the one change accepted. An open question listed there is the
   owner's: the text does not settle it, and it is never a finding.
6. Frontmatter: the author updates `summary` (160 characters or fewer,
   describing the new text), `tags`, `platforms` and `related` to match the
   new guideline. `version`, `modified` and Change History are left for stage
   5's `cookr bump`: a stale version, modified date or history is never a
   finding.
7. One topic at a time: a finding about a sibling topic's guideline names the
   sibling, and the orchestrator routes it there; it is not this topic's to
   fix.

Write one roled guideline, as a single markdown doc with frontmatter, that:
- keeps every rule whose verdict is `supported`, reworded only where the
  research says it is wrong or unclear, at the strength of its weakest cited
  claim;
- adds a named rule for every `new` verdict, at the strength of its weakest
  cited claim;
- leaves every rule on the owner list below worded exactly as its prior
  text, citing its `<rule-name>-prior` claim: `(claim: <rule-name>-prior)`.
  Where the prior text has no MUST, SHOULD or MAY, put one lead-in in front of
  it carrying the keyword the old text implied, and keep the text after it
  word for word;
- settles none of the open questions on the owner list;
- follows /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/guideline-formatting/rules.md,
  gf-roled-parts and gf-named-rules: an intro; a `## Rules` section of
  named rules `- **kebab-name**: … MUST|SHOULD|MAY …`; how-to and example
  sections; `## What a reviewer looks for`;
  `## A complete review must establish`; `## A build must establish`;
  `## Rationale`; `## References`; `## Change History`;
- gives `## A build must establish` exactly one line per named rule,
  `` - `rule-name`: … ``, and no line naming anything that is not a named
  rule of `## Rules` (`cookr roles check` refuses a rule with no line and a
  line naming no rule);
- cites research exactly as `cookr validate` enforces it: every named rule
  ends with one citation, `(claim: <id>)` or `(claims: <id>, <id>)`, with
  nothing after it, not even a full stop; only one citation per rule;
  every id is a claim `id` in research.json that some verdict names
  (gf-rule-cites-research);
- updates `summary` (160 characters or fewer), `tags`, `platforms` and `related` to match the new text, and leaves `version`, `modified` and Change History to stage 5's `cookr bump`.

Edit only the draft. Never edit research, the owner list or another topic.
A finding you think is wrong is disputed, not obeyed: see the round sections
below, when there are any.

Verdicts:
- record-decisions-with-full-context: supported (claims: record-context-of-decision, record-rationale-justification, record-consequences-good-and-bad)
- capture-rationale-alternatives-and-decider: supported (claims: record-rationale-justification, record-alternatives-considered, record-who-decided)
- decisions-findable-and-linked: supported (claims: store-openly-findable, store-with-the-code, link-decisions-to-work, github-issue-pr-linking)
- decision-has-rationale-and-decider: supported (claims: record-rationale-justification, record-who-decided, zimmermann-identify-decision-makers)
- alternatives-are-recorded: supported (claims: record-alternatives-considered, proposal-processes-record-alternatives, zimmermann-dummy-alternative-and-sprint)
- acknowledge-contradicted-decisions: supported (claims: supersede-and-link, records-prevent-relitigation, cloud-providers-agree-on-supersession, gds-way-supersede-must)
- supersede-never-edit-accepted-records: new (claims: accepted-records-immutable, adr-tools-supersede-command, clarifications-may-amend)
- supersession-links-both-ways: new (claims: supersede-and-link, supersession-header-fields, gds-way-supersede-must)
- record-status-lifecycle: new (claims: status-lifecycle)
- record-decision-date: new (claims: record-decision-date)
- record-consequences-good-and-bad: new (claims: record-consequences-good-and-bad, zimmermann-anti-patterns)
- one-decision-per-short-record: new (claims: one-decision-short-record, zimmermann-mega-adr)
- record-significant-decisions-only: new (claims: record-significant-decisions)
- record-rejected-proposals: new (claims: record-rejected-decisions)
- record-confidence-level: new (claims: record-confidence-level)
- backfill-undocumented-decisions: new (claims: backfill-undocumented)
- no-dummy-alternatives: new (claims: zimmermann-dummy-alternative-and-sprint)

Second-check corrections, refuted (criteria 3 applies to these claims):
- adr-tools-supersede-command: refuted (quote-found yes, supports-claim partly); trust 72 -> 52; a rule citing it cannot carry MUST
- clarifications-may-amend: refuted (quote-found yes, supports-claim partly); trust 68 -> 48; a rule citing it cannot carry MUST
- supersession-header-fields: refuted (quote-found yes, supports-claim partly); trust 86 -> 66; a rule citing it cannot carry MUST
- gds-way-supersede-must: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST
- backfill-undocumented: refuted (quote-found yes, supports-claim partly); trust 72 -> 52; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
none

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

none

## Open questions

- Whether naming the decider is a MUST or a SHOULD: MADR marks decision-makers optional and Nygard's template has no decider field, while PEP-Delegate, DACI and GOV.UK always name one; the owner sets the strength.
- Whether alternatives are required on every record, or only where two or more options were real: Nygard and GOV.UK omit the section, Google Cloud ties ADRs to 'two or more engineering options', MADR's minimal template keeps it.
- Whether a clarification may edit an accepted record in place (GDS Way allows it before implementation; Henderson's collection prefers dated amendments) or every change must be a new superseding record (Microsoft, AWS, Fowler).
- Where records live: in the code repository (Nygard, Fowler, GDS, Thoughtworks, log4brains) or a wiki readable by non-developers (Google Cloud notes both; Atlassian's decision log); or the repository with a mirrored wiki.
- Which template to standardise on: Nygard's, MADR, or Y-statements; Zimmermann advises choosing one and sticking to it.
- Whether 'deprecated' is a status distinct from 'superseded' (Nygard and MADR list both) and whether superseded records may ever be deleted (Zimmermann mentions deleting; Nygard and Microsoft keep them).
- Whether sequential numbering is required (Nygard, Fowler, adr-tools) or avoided to dodge merge conflicts (log4brains).

## Round 1 findings

Verdict: fail. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

- R1.1: `rules.md`, `supersession-links-both-ways` against `acknowledge-contradicted-decisions`: two behaviours are required twice, at two strengths. (1) Marking the earlier record superseded is a MUST in `acknowledge-contradicted-decisions` ("the earlier record is marked superseded") and a SHOULD in `supersession-links-both-ways` ("the superseded record SHOULD be marked superseded with a link to its replacement"). (2) The new record naming the record it replaces is a MUST in `acknowledge-contradicted-decisions` ("a new record that names the earlier decision") and a SHOULD in `supersession-links-both-ways` ("the new record SHOULD name the record it replaces"). Under cookbook-compliance (must-not-contradict) and behavioral-requirements (must-use-keywords-with-defined-semantics), one behaviour cannot be both absolute and waivable. The two build-bar lines and the review-focus sentence repeat the overlap. Fix: cut `supersession-links-both-ways` down to the one thing it adds, the link from the superseded record's mark to its replacement. For example: "When one record supersedes another, the superseded record's status SHOULD link to the record that replaces it. (claims: supersede-and-link, supersession-header-fields, gds-way-supersede-must)". It stays SHOULD, because it cites two refuted claims. Narrow its `a-build-must-establish.md` line to match ("each superseded record's status links to its replacement").
- R1.2: `a-build-must-establish.md`, `backfill-undocumented-decisions`: the line "where a log was started for an existing system, known past decisions were recorded where their data was available" turns a MAY rule into an obligation the build must meet. The other MAY rule's line is written "where used" (`record-confidence-level`), and the review bar files backfill under "noted where it was used". Fix: make the line conditional on use, e.g. "where used, past decisions recorded retroactively are ones whose data was available".
- R1.3: `intro.md`, first paragraph: "A later decision that changes an earlier one never edits or silently contradicts it" and "the two link to each other" state as absolutes what the rules hold at lower strength. Not editing an accepted record is SHOULD NOT (`supersede-never-edit-accepted-records`). It cannot carry MUST, because it cites the refuted `adr-tools-supersede-command` and `clarifications-may-amend`. Two-way linking is SHOULD (`supersession-links-both-ways`). Only the "silently contradicts" part is MUST. Fix: keep "never silently contradicts" and soften the rest so it matches the rules, e.g. "...is a new record rather than an edit, it marks the old one superseded, and the two should link to each other".
- R1.4: `intro.md`, second paragraph: "such as datastore selection" mentions a cookbook artifact by a freeform description. cross-recipe-consistency (must-reference-siblings-by-uuid, must-format-cross-references-consistently) asks for an in-text `[rdid](cookbook:uuid)` link, which is the form sibling `task-breakdown` uses in its rationale. The artifact is already in `related`. Fix: write it as `[adc.guideline.planning.data.datastore-selection](cookbook:6a653107-929d-418e-865d-636373a27b02)`. The other mention there, "project record linking", has no guideline or uuid yet, so a freeform mention is the only form available and is not part of this finding.
- R1.5: Lint FM-03: `cookbook/index.json` has no entry for id `2b7a1593-48e0-4bbe-8e14-0df7a863628d` (expected rdid `adc.guideline.planning.project-management.decision-records`). template-conformance must-have-index-entry-and-matching-rdid fails for the same reason, and `cookr validate` reports index drift for `guidelines/INDEX.md`. Fix: run `cookr update`, using this checkout's cookr, to add the index entry and regenerate the index.

Lint failed (`lint: fail 1`): fix each lint error in the draft. The review's `## Lint` section:

````
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
````
