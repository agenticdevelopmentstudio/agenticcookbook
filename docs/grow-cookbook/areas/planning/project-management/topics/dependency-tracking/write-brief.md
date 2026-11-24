# Write brief: dependency-tracking

Today is 2026-11-24.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/dependency-tracking (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/dependency-tracking/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/dependency-tracking/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/dependency-tracking/owner-list.md.
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
- map-internal-and-external-dependencies: supported (claims: internal-and-external-dependency-classes, raid-log-tracks-dependencies-with-risks, cluster-blockers-internal-external, identify-dependencies-in-planning-with-others)
- track-dependency-availability-and-status: supported (claims: raid-entry-owner-due-date-status, review-dependencies-regularly, document-dependency-type-source-timeline, kanban-guide-unblock-and-review, tracker-health-on-track-at-risk-off-track)
- flag-at-risk-or-blocked-dependencies: supported (claims: github-issue-dependencies-blocked-icon, linear-blocked-by-flags, jira-flag-impediment, jira-plans-off-track-dependencies, leopold-red-blocker-sticker-days-blocked)
- dependency-has-type-and-status: unsupported (claims: dependency-has-type-and-status-prior, document-dependency-type-source-timeline, raid-entry-owner-due-date-status)
- blocked-dependency-linked-to-affected-work: unsupported (claims: blocked-dependency-linked-to-affected-work-prior, github-projects-define-blockers-and-fields, github-issue-dependencies-blocked-icon, jira-plans-off-track-dependencies, at-risk-dependency-entered-as-risk)
- dependency-owner-agreed-on-both-sides: new (claims: owner-agreed-and-confirmed-by-other-side, raid-entry-owner-due-date-status, apm-common-difficulties, document-dependency-type-source-timeline)
- dependency-has-need-by-date: new (claims: dependency-statement-with-need-by-date, raid-entry-owner-due-date-status, apm-common-difficulties)
- dependency-status-values: new (claims: tracker-health-on-track-at-risk-off-track, raid-entry-owner-due-date-status, linear-blocked-by-flags, jira-plans-off-track-dependencies, linear-update-reminders-and-staleness, stale-log-loses-value)
- escalate-blocked-dependency-before-milestone: new (claims: safe-art-sync-escalation-point, prince2-manage-by-exception, scrum-guide-impediments, less-just-talk-and-scouts, communicate-dependency-changes)
- at-risk-dependency-logged-as-risk: new (claims: at-risk-dependency-entered-as-risk, apm-common-difficulties)
- reduce-dependencies-before-tracking: new (claims: rescope-to-remove-dependencies, less-minimise-dependencies-feature-teams, each-dependency-halves-on-time-chance)
- record-blocker-reason-and-duration: new (claims: leopold-red-blocker-sticker-days-blocked, jira-flag-impediment, cluster-blockers-internal-external)
- identify-dependencies-during-planning: new (claims: identify-dependencies-in-planning-with-others, safe-pi-planning-identifies-dependencies)

Second-check corrections, refuted (criteria 3 applies to these claims):
- owner-agreed-and-confirmed-by-other-side: refuted (quote-found yes, supports-claim partly); trust 65 -> 45; a rule citing it cannot carry MUST
- linear-update-reminders-and-staleness: refuted (quote-found yes, supports-claim partly); trust 82 -> 62; a rule citing it cannot carry MUST
- rescope-to-remove-dependencies: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST
- each-dependency-halves-on-time-chance: refuted (quote-found yes, supports-claim partly); trust 25 -> 5; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
none

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **dependency-has-type-and-status** — verdict `unsupported` (claims: dependency-has-type-and-status-prior, document-dependency-type-source-timeline, raid-entry-owner-due-date-status). Prior text, kept word for word: "Every dependency has a type and status" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Each identified dependency is documented with its type (inward or outward), its source, its specification and its timeline, agreed in a signed-off dependency agreement, and then monitored for its whole life.
  - against: In a RAID log each dependency entry has a designated owner, a due date and a status, and Blocked is one of the statuses a dependency entry takes.
- **blocked-dependency-linked-to-affected-work** — verdict `unsupported` (claims: blocked-dependency-linked-to-affected-work-prior, github-projects-define-blockers-and-fields, github-issue-dependencies-blocked-icon, jira-plans-off-track-dependencies, at-risk-dependency-entered-as-risk). Prior text, kept word for word: "blocked or at-risk dependencies are linked to affected milestones or todos" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: GitHub's guidance for Projects is to define which issues are blocked by or blocking others, track status in a single-select field with preset values and target dates in a date field, and automate updates so the project stays current.
  - against: GitHub Issues records dependencies as 'blocked by' and 'blocking' links between issues, and marks a blocked issue with a Blocked icon on project boards and the Issues page.
  - against: Jira Plans treats work-item links as dependencies (Blocks by default), and its dependencies view and program board show a dependency in red when it is off-track, with filters to list only off-track dependencies.
  - against: A dependency assessed as a risk to the project, or a threat to it such as lateness, is also entered in the risk log or register and reviewed for its effect on milestones.

## Open questions

- Whether the two Verify clauses (every dependency has a type and status; blocked or at-risk dependencies are linked to affected milestones or todos) stay as must-hold checks as a house convention, or are restated at SHOULD, the strength the sources support.
- Which status vocabulary the cookbook adopts for a dependency: the trackers' project-health set (On track, At risk, Off track) plus Blocked and Done, or another set; the sources offer several and none is a standard.
- What 'type' means for a dependency in the cookbook: internal versus external (PRINCE2), internal / intra / external (MSP, Essex), inward versus outward (APM), the PMBOK's mandatory / discretionary, or what the dependency is on (team, vendor, task, decision); the sources use all of these.
- When a blocked or at-risk dependency is escalated: at a fixed review cadence, as soon as its need-by date is forecast to be missed (PRINCE2's manage-by-exception), or at a named forum such as SAFe's ART Sync; the sources give no single trigger.
- Whether a dependency at risk is also entered as a risk (Essex, APM), which would couple this topic to risk-tracking, or stays only in the dependency record.

## Round 1 findings

Verdict: fail. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

- R1.1: `examples.md`, the RAID-log table: the identity-team dependency is marked "Internal", but `map-internal-and-external-dependencies` defines internal as "under the team's control" and external as "beyond it", and the claim it cites (`internal-and-external-dependency-classes`) gives "delivery of a product from another project" as an external dependency. Another team delivering an endpoint is beyond the mobile team's control, so the example contradicts the rule it illustrates. Fix: mark the entry "External", or change the example to a dependency that is under the team's own control.
- R1.2: `rationale.md`, last paragraph: "PRINCE2 was reached only through secondary sources, so no rule rests on them" is untrue. `escalate-blocked-dependency-before-milestone` cites `prince2-manage-by-exception` (prince2.wiki, secondary) and names "the PRINCE2 project board once tolerance is exceeded", and `map-internal-and-external-dependencies` cites `internal-and-external-dependency-classes`, whose internal/external definitions are PRINCE2's as quoted by APM. Fix: keep "no rule rests on" for the PMBOK Guide, ISO 21502 and ISO 31000 only, and say PRINCE2 is reached through secondary sources (APM's quotation and prince2.wiki), which the escalation and internal/external rules use.
- R1.3: `rationale.md`, fourth paragraph: "each team dependency roughly halves the chance of on-time completion; it names no study, and gives only the direction of the effect, never a figure" states the figure the research forbids. research.md and the claim's `trust.basis` for `each-dependency-halves-on-time-chance` (trust 5, refuted by the second check) say it is usable "only as the direction of the effect, never as a figure", and "roughly halves" is a figure. The clause "gives only the direction of the effect" also puts the research's limit on the model, which does give a figure. Fix: state the direction only, e.g. "A practitioner teaching model, reported second-hand and naming no study, holds that each added team dependency lowers the chance of on-time completion; the research uses it for that direction only."
- R1.4: `rules.md`, bundled rules (behavioral-requirements must-not-bundle-behaviors-into-one-requirement; guideline-formatting one-requirement-per-rule): each of these rules joins two separately testable behaviours, so one can pass while the other fails: `dependency-owner-agreed-on-both-sides` (an agreed owner; the dependency confirmed and tracked in the other side's log), `dependency-has-need-by-date` (a need-by date is carried; the date is agreed with the source), `track-dependency-availability-and-status` (status tracked for the dependency's whole life; dependencies reviewed at regular points), `report-dependency-changes` (dependencies in the standard status reports; changes pushed to the people affected, already two SHOULDs in one bullet), `record-blocker-reason-and-duration` (a reason; a count of days blocked), `analyse-resolved-blockers` (resolved blocker records kept; clustered by cause), and `at-risk-dependency-logged-as-risk` (acknowledged as a risk with a management plan; reviewed for its effect on milestones). Fix: split each into one rule per behaviour, keeping the prior name on one half (names are fixed) and naming the other half freshly, each with its own citation and its own line in `a-build-must-establish.md` and its strength list in `a-complete-review-must-establish.md`.
- R1.5: `rules.md`, `record-blocker-reason-and-duration` and `analyse-resolved-blockers`, against sibling `task-breakdown` (cross-recipe-consistency; cookbook-compliance must-not-contradict-applicable-guidelines): both guidelines rule on the same blocked-work-item practice from the same Leopold and Magennis source at different strengths. Counting the days blocked is SHOULD here but recording the block's dates is MAY in `task-breakdown`'s `blocker-records-dates`; keeping resolved blockers is MAY here (bundled with clustering) but SHOULD in `task-breakdown`'s `keep-resolved-blockers`. A team keeping both guidelines gets two answers for one blocked task. Fix (this topic's part): scope these two rules to the blocked dependency record rather than "a blocked work item", or align their strengths with `task-breakdown` where the research allows it (research.md gives `record-blocker-reason-and-duration` "MAY to SHOULD"), and point to `task-breakdown` for blocked tasks. Any change to `task-breakdown` is that sibling's, for the orchestrator to route.
- R1.6: `artifact.json`, frontmatter `related` and `tags`: `related` is `[]`, although sibling guidelines this text overlaps already exist: `risk-tracking` (`a55182ef-3144-407c-b64a-6377f37f5c63`), whose risk register `at-risk-dependency-logged-as-risk` and the rationale's risk-register question turn on, and `task-breakdown` (`f264cc0b-45d3-4593-a437-7371610c5a8a`), which rules on blocked tasks, blocked-by links and blocker reasons that `flag-at-risk-or-blocked-dependencies`, `blocked-dependency-linked-to-affected-work` and `record-blocker-reason-and-duration` also cover. Criterion 6 asks for `related` to match the new guideline. `tags` also breaks the family vocabulary (cross-recipe-consistency must-use-family-tag-vocabulary): every sibling (`decision-records`, `issue-tracking`, `risk-tracking`, `task-breakdown`) tags itself with its own topic slug, and this one has `dependencies` but not `dependency-tracking`. Fix: add both uuids to `related` and add the tag `dependency-tracking`. Whether those siblings add this guideline to their own `related` is theirs.

## Round 2 findings

Verdict: fail. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

- R2.1: `rationale.md`, first paragraph, the sentence added this round: "the count of days blocked rests on the practitioners alone, so it is an option, as recording a blocked task's dates is in task breakdown." The reason it gives for MAY ("rests on the practitioners alone") also fits `keep-resolved-dependency-blockers`. That rule cites only `leopold-red-blocker-sticker-days-blocked` too, whose `trust.basis` corroborates only the reason-with-flag part, yet it is SHOULD. Read with the rules, the rationale gives one reason for two different strengths. This is the only instance in the changed text. Fix: give the reason for each strength on its own terms. For example, say the day count is an option so that it matches `task-breakdown`'s `blocker-records-dates`, and that keeping resolved blockers is a recommendation because Leopold and Magennis say it emphatically ("DON'T THROW THE BLOCKER POST-ITS AWAY!"), which matches `task-breakdown`'s `keep-resolved-blockers`. Or drop "rests on the practitioners alone, so" as the reason.
