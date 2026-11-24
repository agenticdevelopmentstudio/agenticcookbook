# Write brief: milestone-scheduling

Today is 2026-11-24.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/milestone-scheduling (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/milestone-scheduling/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/milestone-scheduling/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/planning/project-management/topics/milestone-scheduling/owner-list.md.
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
- define-and-sequence-milestones: supported (claims: sequence-with-logic, milestones-are-zero-duration-key-events, github-milestones-due-date-progress, github-projects-roadmap-dates, github-define-blocked-by-and-one-target-date, linear-milestones-optional-date, linear-project-dependencies, jira-plan-dependencies, safe-planning-board-milestones)
- identify-at-risk-or-blocked-milestones: supported (claims: status-reveals-late-work, jira-off-track-warnings, jira-flag-impediment, linear-project-health-updates, github-status-updates, github-issue-dependencies, kanban-unblock-and-age, scrum-impediments)
- milestone-has-status-and-target-date: unsupported (claims: milestone-has-status-and-target-date-prior, schedule-narrative-explains-changes, baseline-and-variance, github-status-updates, linear-milestones-optional-date, github-milestones-due-date-progress)
- milestone-chains-have-no-cycles: supported (claims: assess-network-for-circular-logic, ms-project-refuses-circular-dependency, topological-order-iff-acyclic, jira-cyclic-links-detected-after)
- blocked-milestone-has-issue-or-concern: unsupported (claims: blocked-milestone-has-issue-or-concern-prior, github-issue-dependencies, jira-flag-impediment, prince2-issue-includes-concern, schedule-narrative-explains-changes, linear-project-health-updates)
- milestone-marks-a-key-event: new (claims: milestones-are-zero-duration-key-events, standard-milestones-documented-with-criteria, too-many-milestones-mask-work)
- link-milestones-by-logic-not-fixed-dates: new (claims: sequence-with-logic, missing-logic-justified, avoid-hard-date-constraints, hard-constraints-defeat-cpm)
- check-chains-by-topological-sort: new (claims: topological-order-iff-acyclic, assess-network-for-circular-logic, ms-project-refuses-circular-dependency, jira-cyclic-links-detected-after)
- identify-the-critical-path: new (claims: critical-path-is-longest-path, critical-path-is-dag-longest-path, critical-path-vs-critical-chain)
- status-against-a-status-date: new (claims: status-date-separates-actual-from-remaining, update-regularly-track-finer-than-report, status-date-not-view-date, linear-project-health-updates)
- hold-explicit-schedule-contingency: new (claims: schedule-contingency-is-explicit, risk-margin-not-padding, schedule-risk-analysis-sizes-contingency, critical-path-vs-critical-chain)
- keep-a-baseline-and-report-variance: new (claims: baseline-and-variance)
- explain-every-milestone-date-change: new (claims: schedule-narrative-explains-changes, avoid-hard-date-constraints)
- at-risk-milestone-names-its-risk: new (claims: linear-project-health-updates, github-status-updates, prince2-issue-includes-concern, schedule-risk-analysis-sizes-contingency, schedule-narrative-explains-changes)
- forecast-dates-from-history-as-ranges: new (claims: kanban-sle-forecast, scrum-forecasting-practices, evidence-based-scheduling, commit-after-cone-narrows, schedules-are-halfhearted)
- fix-the-date-flex-the-scope: new (claims: fixed-time-variable-scope, scrum-sprint-fixed-length, scrum-product-goal-target, linear-cycles-not-releases)
- commit-near-term-forecast-later: new (claims: safe-roadmap-commit-near-forecast-far, commit-after-cone-narrows)

Second-check corrections, refuted (criteria 3 applies to these claims):
- standard-milestones-documented-with-criteria: refuted (quote-found yes, supports-claim partly); trust 62 -> 42; a rule citing it cannot carry MUST
- sequence-with-logic: refuted (quote-found yes, supports-claim partly); trust 86 -> 66; a rule citing it cannot carry MUST
- hard-constraints-defeat-cpm: refuted (quote-found yes, supports-claim partly); trust 74 -> 54; a rule citing it cannot carry MUST
- ms-project-refuses-circular-dependency: refuted (quote-found yes, supports-claim partly); trust 84 -> 64; a rule citing it cannot carry MUST
- critical-path-vs-critical-chain: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST
- status-date-not-view-date: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST
- schedule-risk-analysis-sizes-contingency: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST
- github-status-updates: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST
- evidence-based-scheduling: refuted (quote-found yes, supports-claim partly); trust 62 -> 42; a rule citing it cannot carry MUST
- schedules-are-halfhearted: refuted (quote-found yes, supports-claim partly); trust 45 -> 25; a rule citing it cannot carry MUST
- scrum-product-goal-target: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST
- linear-cycles-not-releases: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
none

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **milestone-has-status-and-target-date** — verdict `unsupported` (claims: milestone-has-status-and-target-date-prior, schedule-narrative-explains-changes, baseline-and-variance, github-status-updates, linear-milestones-optional-date, github-milestones-due-date-progress). Prior text, kept word for word: "Every milestone has a status and target date" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Each status update should carry a narrative giving the status of key milestone dates and explaining any change in them.
  - against: A baseline schedule is kept under change control and the current forecast is monitored against it to reveal milestone variance and its downstream effect.
  - against: GitHub Projects status updates record a status such as On track or At risk, start and target dates, and a message.
  - against: Linear project milestones divide a project into stages with completion percentages; a target date on a milestone is optional.
  - against: GitHub milestones group a repository's issues and pull requests and show a due date and a completion percentage.
- **blocked-milestone-has-issue-or-concern** — verdict `unsupported` (claims: blocked-milestone-has-issue-or-concern-prior, github-issue-dependencies, jira-flag-impediment, prince2-issue-includes-concern, schedule-narrative-explains-changes, linear-project-health-updates). Prior text, kept word for word: "no milestone is blocked without a corresponding issue or concern" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: GitHub issue dependencies record which issue blocks which, and a blocked issue is marked as blocked by naming the issue it depends on.
  - against: Jira lets a work item be flagged as blocked (Flagged = Impediment) and optionally takes a comment when the flag is added or removed.
  - against: PRINCE2 7 defines an issue as anything that could affect the project, covering problems and concerns as well as opportunities.
  - against: Each status update should carry a narrative giving the status of key milestone dates and explaining any change in them.
  - against: Linear project updates carry a health indicator (On track, At risk, Off track) and a description of status, challenges and next steps, with reminders on a chosen cadence.

## Open questions

- Whether the two unsupported Verify rules (milestone-has-status-and-target-date, blocked-milestone-has-issue-or-concern) are kept as must-hold checks by house policy or restated at the SHOULD strength the sources support; the owner decides.
- Whether 'target date' in milestone-has-status-and-target-date means a fixed committed date or a forecast computed from logic: GAO says baseline and status schedules should not carry hard date constraints, so a policy that every milestone carries a fixed date conflicts with logic-driven scheduling unless the date is a baseline target.
- Whether the at-risk case joins the blocked case in one rule (every blocked or at-risk milestone names its issue or risk) or stays a separate rule; the brief's research question asks for both, the listed rule names only blocked.
- Which status vocabulary the cookbook names: Linear uses On track / At risk / Off track, GitHub Projects uses On track / At risk among others, Jira uses a Flagged = Impediment field; the owner decides whether to fix a vocabulary or leave it to the tracker.
- Whether the cookbook names a schedule update cadence; GAO ties cadence to duration, complexity and risk and gives only an example (track weekly when reporting monthly), so any fixed cadence is a policy choice.
- Whether 'fix the date, flex the scope' (Shape Up, Scrum's fixed-length Sprint) is stated as an option beside critical-path scheduling or left out; the sources present it as a method choice, not a universal practice.

## Round 1 findings

Verdict: fail. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

- R1.1: `rules.md`, `define-and-sequence-milestones` against `milestone-has-status-and-target-date`: the same behaviours are required twice, at two strengths. `define-and-sequence-milestones` says Planning SHOULD "give each a target date" and "track each one's status". The owner-listed `milestone-has-status-and-target-date` holds "Every milestone has a status and target date" at MUST. Under behavioral-requirements (must-use-keywords-with-defined-semantics) and cookbook-compliance (must-not-contradict), one behaviour cannot be both absolute and waivable. This is the same class of finding decision-records R1.1 raised. The rule also bundles five behaviours into one sentence: define, sequence, date, record the chains, and track status and progress (behavioral-requirements must-not-bundle-behaviors-into-one-requirement). The overlap shows up again in `a-build-must-establish.md` (the `define-and-sequence-milestones` line), in the first bullet of `what-a-reviewer-looks-for.md` ("not defined, sequenced, dated or tracked") and in the first bullet of `a-complete-review-must-establish.md` ("sequenced, dated and tracked"). Fix: keep the rule's fixed name, but cut it to define the milestones, put them in sequence and record the dependency chains between them (same citations). Drop the target date and the status from it; they belong to the owner-listed rule, and their strength is the owner's open question. Move progress tracking into a new SHOULD rule, e.g. `track-milestone-progress`: "Each milestone's progress SHOULD be tracked, for example as the completion of the work linked to it (claims: github-milestones-due-date-progress, linear-milestones-optional-date)". Give it a build-bar line, then narrow the build-bar, review-focus and review-bar wording to match.
- R1.2: `rules.md`, `justify-missing-logic` and `justify-unavoidable-hard-constraints` (these are the only two instances): both are SHOULD, but each cites a claim that states the requirement as "must", and neither claim was refuted. `missing-logic-justified` (trust 74, second check confirmed) quotes GAO: "any activity that is missing predecessor or successor logic must be clearly justified in the schedule documentation". `avoid-hard-date-constraints` (trust 74) quotes GAO: "If a hard constraint cannot be avoided, it must be used judiciously and must be fully justified by referring to some controlling event outside the schedule". The second check notes that the quote "matches the claim's scope and strength". Under criterion 3, each rule sits at the strength of the weakest claim it cites, so these two are understated. Both rules are conditional on a departure (a missing link, an unavoidable constraint), so MUST does not make the underlying SHOULD rules absolute. I checked every other rule for an unrefuted "must" claim cited at SHOULD and found none. `sequence-with-logic` quotes "must be logically sequenced", but it is refuted and cannot carry MUST. Fix: raise both rules to MUST: "...MUST be justified in the schedule documentation" and "...MUST be justified in the schedule's basis document by the event outside the schedule that controls it". Then update `rationale.md` paragraphs 1 and 2. They currently say "the rules carry its practice at SHOULD" and "The cycle rule is the one MUST"; they should name the two justification MUSTs too.
- R1.3: `examples.md`, the sentence after the Python block: the cycle message it shows, `cycle in milestone chain: start -> launch -> beta -> api-freeze -> start`, is not what the code prints. I added `depends_on["start"] = {"launch"}` and ran the example under Python 3 with several `PYTHONHASHSEED` values. Every run printed `cycle in milestone chain: api-freeze -> docs-ready -> launch -> start -> api-freeze`. graphlib lists the cycle in successor order, each node followed by one that depends on it. The example shows dependency (predecessor) order, which graphlib never prints, and it names `beta` where graphlib names `docs-ready`. The hedge "(the order the error lists varies)" does not cover a reversed direction. This is a factual error against `topological-order-iff-acyclic`, which says graphlib reports the cycle. Fix: replace it with the real output, `cycle in milestone chain: api-freeze -> docs-ready -> launch -> start -> api-freeze`. Then change the parenthetical to say graphlib lists each milestone followed by one that depends on it, starting from whichever node it reaches first.
- R1.4: `artifact.json` `related`, `intro.md` paragraph 2 and `rationale.md` last paragraph: the guideline hands parts of its scope to two indexed siblings, but it names them only by freeform description ("Delivery dependencies on other teams, tasks and their blockers ... are covered by their own guidelines"; "belong to the dependency-tracking guideline, tasks and their blockers to the task-breakdown guideline"). `related` is `[]`. The two siblings are dependency-tracking (`3f978ba7-c8c1-4b53-8fda-12e5a6966b75`) and task-breakdown (`f264cc0b-45d3-4593-a437-7371610c5a8a`). cross-recipe-consistency (must-reference-siblings-by-uuid, must-format-cross-references-consistently) and criterion 6 (`related` matches the new text) both apply, as in decision-records R1.4. Fix: add both UUIDs to `related`. In `rationale.md`, write them as `[adc.guideline.planning.project-management.dependency-tracking](cookbook:3f978ba7-c8c1-4b53-8fda-12e5a6966b75)` and `[adc.guideline.planning.project-management.task-breakdown](cookbook:f264cc0b-45d3-4593-a437-7371610c5a8a)`, and link the intro's mentions the same way. The project-record-linking mention stays freeform, because that topic has no artifact or UUID yet.
