# Write brief: issue-tracking

Today is 2026-11-24.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/issue-tracking (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/issue-tracking/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/issue-tracking/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/issue-tracking/owner-list.md.
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
- identify-assess-severity-and-triage: supported (claims: triage-identifies-categorizes-prioritizes, severity-describes-impact, triage-sets-severity-on-every-defect, linear-triage-inbox)
- link-issues-to-findings: unsupported (claims: link-issues-to-findings-prior, link-related-records)
- track-resolution-status: supported (claims: status-tracks-to-resolution, scrum-impediments-removed, kanban-active-management)
- escalate-critical-issues: supported (claims: escalate-critical-full-attention, critical-notifies-beyond-assignee)
- issue-has-severity-and-status: contradicted (claims: issue-has-severity-and-status-prior, triage-sets-severity-on-every-defect, github-no-default-severity, jira-priority-conflates-severity, linear-priority-five-levels)
- critical-issue-owned-or-escalated: supported (claims: escalate-critical-full-attention, critical-notifies-beyond-assignee, issue-has-one-owner)
- resolved-issue-references-resolution: supported (claims: record-resolution, resolution-reason-from-fixed-set, link-fix-to-issue, jira-resolution-field-unresolved)
- defect-has-severity-every-issue-has-status: new (claims: triage-sets-severity-on-every-defect, status-tracks-to-resolution)
- severity-kept-apart-from-priority: new (claims: severity-separate-from-priority, mozilla-bugzilla-severity-priority-fields, google-issue-tracker-priority-and-severity, jira-priority-conflates-severity)
- define-issue-severity-levels: new (claims: severity-levels-defined, regression-not-severity)
- severity-change-needs-rationale: new (claims: severity-change-needs-rationale)
- severity-set-by-assessor-not-reporter: new (claims: priority-inflation)
- escalation-path-documented: new (claims: escalation-procedure-documented)
- escalate-unresolved-after-time-limit: new (claims: escalate-unresolved-after-time)
- triage-has-a-named-owner: new (claims: triage-has-named-owner)
- triage-new-issues-promptly: new (claims: triage-within-time-bound, untriaged-is-visible)
- every-issue-has-one-owner: new (claims: issue-has-one-owner)
- record-resolution-reason: new (claims: resolution-reason-from-fixed-set, itil-known-error)
- link-fix-change-to-issue: new (claims: link-fix-to-issue)
- close-duplicates-linking-canonical: new (claims: close-duplicates-link-canonical, duplicates-refiled)
- close-unplanned-work-definitively: new (claims: close-not-planned-definitively)
- verify-resolution-before-close: new (claims: verify-resolution)
- keep-closed-issues-as-history: new (claims: keep-closed-as-history)
- communicate-resolution-to-stakeholders: new (claims: communicate-resolution)
- issue-records-minimum-fields: new (claims: issue-log-minimum-fields, spolsky-three-things)
- keep-priority-scale-small: new (claims: avoid-extra-fields, linear-priority-five-levels)
- one-tracker-everyone-uses: new (claims: bug-database-everyone-uses, pmbok-issue-log)
- issue-covers-more-than-defects: new (claims: prince2-issue-broad, pmbok-issue-log)
- flag-stale-issues: new (claims: stale-issues-flagged, kanban-active-management)

Second-check corrections, refuted (criteria 3 applies to these claims):
- google-issue-tracker-priority-and-severity: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST
- link-fix-to-issue: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST
- duplicates-refiled: refuted (quote-found yes, supports-claim partly); trust 50 -> 30; a rule citing it cannot carry MUST
- spolsky-three-things: refuted (quote-found yes, supports-claim partly); trust 50 -> 30; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
none

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **link-issues-to-findings** — verdict `unsupported` (claims: link-issues-to-findings-prior, link-related-records). Prior text, kept word for word: "link issues to specialist findings when applicable" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Trackers let an issue reference related issues, pull requests, incidents and changes; none of the sources links issues to review findings as such.
- **issue-has-severity-and-status** — verdict `contradicted` (claims: issue-has-severity-and-status-prior, triage-sets-severity-on-every-defect, github-no-default-severity, jira-priority-conflates-severity, linear-priority-five-levels). Prior text, kept word for word: "Every issue has severity and status" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Mozilla counts a defect as triaged only once it has a severity, so that no critical issue is missed; tasks and enhancements may carry a severity of N/A.
  - against: GitHub ships default labels (bug, duplicate, wontfix and others) but no severity or priority; teams add them as labels or a project single-select field.
  - against: Jira ships priority but no severity field; its default priority descriptions read as severity.
  - against: Linear offers a fixed five-value priority (No priority to Urgent), no severity field, and deliberately no custom priorities.

## Open questions

- Which severity scale the cookbook adopts: Mozilla's four levels (S1 Catastrophic to S4 Small/Trivial) or Atlassian's three (Critical, Major, Minor), or another.
- Whether tasks and enhancements carry a severity, or only defects (Mozilla allows N/A for tasks and enhancements).
- The escalation time limit for an unresolved critical issue, and who it escalates to (Mozilla assigns S1 within 2 business days and notifies Release Management; Linear's example is a 24 hour SLA for Urgent).
- Whether the reporter (or a named verifier) must confirm a fix before the issue is closed, or the fixer may close it.
- Whether the rule to link issues to specialist findings stays, since no source covers specialist findings; the general linking convention is project-record-linking's.
- Whether priority stays optional beside severity (Mozilla makes it optional) or is required.
