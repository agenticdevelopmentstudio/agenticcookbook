# Write brief: project-record-linking

Today is 2026-11-24.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/project-record-linking (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/project-record-linking/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/project-record-linking/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/project-record-linking/owner-list.md.
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
- record-has-unique-stable-id: new (claims: pg-prince2-unique-identifiers, bp-ids-never-reused, ks-jira-key-names-target)
- id-never-reused-or-renamed: new (claims: bp-ids-never-reused, bp-identifier-carries-no-status, pg-moved-records-keep-old-names)
- link-names-target-by-id: new (claims: ks-github-autolink-backlink, ks-jira-key-names-target, ks-backlinks-computed)
- typed-links-with-both-readings: new (claims: ks-jira-typed-links-two-descriptions, ks-gitlab-bidirectional-links, ks-linear-relations, ks-backlinks-computed)
- two-way-link-recorded-once-shown-both-ways: new (claims: ks-two-way-link-recorded-once, ks-github-autolink-backlink, ks-github-dependencies-both-directions, ks-gitlab-bidirectional-links, ks-linear-relations, ks-adr-tools-reverse-link, ks-backlinks-computed, bp-bidirectional-traceability)
- close-or-supersede-never-delete: new (claims: pg-deleted-record-breaks-links, ks-linear-relations, bp-supersede-and-link-both)
- superseding-record-links-both-ways: new (claims: bp-supersede-and-link-both, ks-adr-tools-reverse-link, ev-supersede-not-edit-debated, ev-unrecorded-decisions-contradicted)
- blocked-record-names-its-blocker: new (claims: pg-github-single-source-and-blockers, ks-github-dependencies-both-directions, ks-linear-relations, ks-gitlab-bidirectional-links)
- child-record-carries-parent-link: new (claims: ks-github-sub-issues-and-milestones, ks-github-closing-keywords)
- realised-risk-links-to-its-issue: new (claims: bp-risk-realised-links-issue, pg-prince2-integrated-register)
- link-instead-of-copy: new (claims: pg-github-single-source-and-blockers)
- check-links-for-dangling-targets: new (claims: ks-dangling-link-checks, ks-suspect-links, pg-deleted-record-breaks-links, ev-missing-links-impede)
- report-unlinked-records: new (claims: ks-dangling-link-checks, ks-traceability-matrix, ev-missing-links-impede)

Second-check corrections, refuted (criteria 3 applies to these claims):
- ks-two-way-link-recorded-once: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST
- bp-bidirectional-traceability: refuted (quote-found yes, supports-claim partly); trust 55 -> 35; a rule citing it cannot carry MUST
- ev-missing-links-impede: refuted (quote-found yes, supports-claim partly); trust 52 -> 32; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
- ks-jira-typed-links-two-descriptions: dropped 1 citation(s) lacking the quote; independence single -> single

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

none

## Open questions

- Whether a two-way link is written in both records' files or written once and its reverse computed by the checker; the trackers compute the reverse, file-based records must choose.
- What identifier scheme project records use: one prefix per record type (R-1, D-1, I-1) or one global sequence; the sources require only uniqueness and no reuse.
- Whether a link to an unknown identifier fails the check (as Doorstop's error does) or only warns (as Sphinx-Needs does by default).
- Whether a link whose target is closed or superseded is reported at all, and if so at what level; Linear keeps it as Related, Doorstop warns when a child links to an inactive parent.
- Whether every record must be linked to at least one other record (an orphan check), or only the record types whose host topics require a link.
- Whether accepted decision records are immutable (Microsoft Learn, Nygard) or may take dated amendments (Henderson's teams found mutability worked better).
- Whether a realised risk keeps its record and links forward to the new issue (the 'realised, see I-01' convention) or is moved to the issue register as PRINCE2 summaries describe.
