# Write brief: risk-tracking

Today is 2026-11-24.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/risk-tracking (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/risk-tracking/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/risk-tracking/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/risk-tracking/owner-list.md.
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
- risk-identification-and-attention-flagging: supported (claims: iso-identify-risks-whatever-their-source, prince2-capture-risks-when-identified, scrum-daily-identifies-impediments, linear-health-at-risk, orange-book-timely-escalation, nao-escalation-criteria-immediate-action)
- distinguish-immediate-action-from-monitoring: supported (claims: iso-evaluation-decides-action, prince2-reduce-is-action-now, prince2-contingent-plans-wait, pmbok8-contingent-responses-on-trigger, prince2-proximity-field, nao-escalation-criteria-immediate-action)
- link-concerns-to-related-elements: supported (claims: prince2-risk-refers-to-product, orange-book-register-holds-owners-and-links, prince2-register-formats)
- concern-has-status-and-raiser: supported (claims: prince2-risk-author-field, prince2-risk-status-field, prince2-register-records-status-and-history, prince2-status-shows-action-taken, ilx-current-status)
- no-concern-open-without-review: supported (claims: iso-monitoring-planned-with-responsibilities, iso-untreatable-risk-kept-under-review, orange-book-regularly-reviewed, orange-book-continuous-monitoring, nao-registers-up-to-date, prince2-review-register-at-progress-reviews, ilx-static-records, kanban-review-active-items-age, linear-overdue-updates-flagged, pmbok8-monitoring-never-stops)
- risk-has-single-named-owner: new (claims: prince2-single-risk-owner, prince2-owner-and-actionee-agreed, roam-single-owner, atlassian-risk-register-components, nao-lack-of-ownership, nao-clarity-of-ownership-complex-risks, ilx-lack-of-accountability, orange-book-first-line-ownership)
- risk-response-has-an-actionee: new (claims: prince2-risk-actionee, iso-treatment-plan-names-responsible-and-timing, ilx-owner-and-actionee, pmbok8-unassigned-response-is-a-wish)
- risk-review-cadence: new (claims: prince2-risk-timing-set-in-approach, prince2-review-register-at-progress-reviews, iso-monitoring-planned-with-responsibilities, orange-book-risk-in-normal-management-flow, atlassian-regular-risk-meeting, nao-monthly-review-example, ilx-static-records, kanban-review-active-items-age)
- risk-response-triage: new (claims: iso-treatment-options, iso-select-treatment-by-cost-benefit, prince2-reduce-is-action-now, prince2-contingent-plans-wait, prince2-accept-not-beyond-tolerance, pmbok8-threat-responses-include-escalation, roam-four-categories)
- escalate-risks-beyond-tolerance: new (claims: orange-book-timely-escalation, nao-escalation-criteria-immediate-action, prince2-escalate-when-tolerance-threatened, prince2-accept-not-beyond-tolerance, nao-monthly-review-example)
- risk-becomes-issue-when-it-happens: new (claims: prince2-issue-is-event-that-happened, atlassian-raid-issues-need-immediate-attention, pmbok8-issue-already-happened, orange-book-contingency-if-risks-crystallise)
- describe-risk-as-cause-event-effect: new (claims: prince2-risk-description-cause-event-effect, ilx-vague-or-duplicated-risks)
- keep-risk-scoring-simple: new (claims: atlassian-probability-times-impact, ilx-overly-complex-scoring)
- track-risks-in-the-team-tracker: new (claims: prince2-register-formats, github-custom-issue-types, github-custom-issue-fields, linear-health-at-risk, iso-record-and-report-outcomes, scrum-controls-risk-by-iteration)

Second-check corrections, refuted (criteria 3 applies to these claims):
- prince2-owner-and-actionee-agreed: refuted (quote-found yes, supports-claim partly); trust 72 -> 52; a rule citing it cannot carry MUST
- roam-single-owner: refuted (quote-found yes, supports-claim partly); trust 54 -> 34; a rule citing it cannot carry MUST
- atlassian-risk-register-components: refuted (quote-found yes, supports-claim partly); trust 60 -> 40; a rule citing it cannot carry MUST
- nao-clarity-of-ownership-complex-risks: refuted (quote-found yes, supports-claim partly); trust 68 -> 48; a rule citing it cannot carry MUST
- iso-treatment-plan-names-responsible-and-timing: refuted (quote-found yes, supports-claim partly); trust 74 -> 54; a rule citing it cannot carry MUST
- pmbok8-unassigned-response-is-a-wish: refuted (quote-found yes, supports-claim partly); trust 44 -> 24; a rule citing it cannot carry MUST
- kanban-review-active-items-age: refuted (quote-found yes, supports-claim partly); trust 68 -> 48; a rule citing it cannot carry MUST
- prince2-contingent-plans-wait: refuted (quote-found yes, supports-claim partly); trust 76 -> 56; a rule citing it cannot carry MUST
- roam-four-categories: refuted (quote-found yes, supports-claim partly); trust 50 -> 30; a rule citing it cannot carry MUST
- pmbok8-issue-already-happened: refuted (quote-found yes, supports-claim partly); trust 48 -> 28; a rule citing it cannot carry MUST
- orange-book-contingency-if-risks-crystallise: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST
- prince2-register-formats: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST
- github-custom-issue-types: refuted (quote-found yes, supports-claim partly); trust 72 -> 52; a rule citing it cannot carry MUST
- linear-health-at-risk: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST
- scrum-controls-risk-by-iteration: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
none

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

none

## Open questions

- Which review cadence the rule names: PRINCE2 ties formal review to stage ends and progress reviews, the NAO example is monthly, and the Kanban Guide allows continuous or fixed-interval review; the owner decides whether the rule names one interval or requires the team to set one.
- Which response vocabulary the cookbook adopts: ISO 31000's treatment options, PRINCE2's avoid, reduce, transfer, share, accept and prepare contingent plans, PMBOK 8's mitigate, avoid, transfer, accept and escalate, or the ROAM categories (resolved, owned, accepted, mitigated).
- Whether opportunities (positive risks) are in this topic's scope: ISO 31000, PRINCE2 and PMBOK 8 all treat them alongside threats, while the listed rules speak only of concerns.
- Whether the rule requires a separate actionee beside the owner, as PRINCE2 does, or lets one person hold both, which PRINCE2 says is common.
- Which tracker mapping the cookbook recommends for a small team: a custom 'Risk' issue type with fields in GitHub or Jira, a RAID log document, or a project health flag such as Linear's 'At risk', which marks a project but is not a per-risk record.
