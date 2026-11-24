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
