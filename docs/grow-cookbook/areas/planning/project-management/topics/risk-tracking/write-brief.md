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

## Round 1 findings

Verdict: fail. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

- R1.1: `rules.md`, bundled rules (behavioral-requirements must-not-bundle-behaviors-into-one-requirement; guideline-formatting one-requirement-per-rule): each of these rules joins two or more behaviours that can each be tested on its own, so one part can pass while another fails:
    - `risk-identification-and-attention-flagging`: identify risks whatever their source; surface new risks and impediments as they appear; record each one as soon as it is identified, whoever raised it.
    - `distinguish-immediate-action-from-monitoring`: evaluate each risk as needing action now or being watched; record its proximity (already two SHOULDs in one bullet).
    - `link-concerns-to-related-elements`: a unique identifier; the product or process it concerns (two SHOULDs).
    - `concern-has-status-and-raiser`: the raiser is named; a status is carried; the status history is kept (two SHOULDs plus the history clause).
    - `risk-review-cadence`: reviews are planned, with responsibility defined, inside the normal management flow; the register is checked for new or revised risks at each review (two SHOULDs).
    - `owner-most-capable-and-not-overloaded`: the owner is the person most capable; no one holds too many risks (two SHOULDs).
    - `risk-response-triage`: the response comes from a defined set of options; it is chosen by weighing benefit against cost (the build line checks the two separately).
    - `escalate-risks-beyond-tolerance`: escalation criteria are agreed; a risk beyond tolerance is escalated rather than accepted (two SHOULDs).
    - `describe-risk-as-cause-event-effect`: the description gives cause, event and effect; no entry duplicates another (the build line checks the two separately).
    Fix: split each into one rule per behaviour. The prior rule name stays on one half, because verdict names are fixed, and the other half gets a fresh name. Each new rule carries its own citation (the claims that support that half), its own line in `a-build-must-establish.md`, and an entry in the SHOULD list of `a-complete-review-must-establish.md`.
- R1.2: `rules.md`, the list as a whole (guideline-formatting keep-rule-lists-short; template/sibling structure): the 17 rules are one flat list, but a list SHOULD have no more than seven items where possible. The siblings group their rules under `###` subsections (`issue-tracking` has "Recording issues" and "Triage"; `dependency-tracking` has three to six rules per subsection). Fix: group the rules, including the new ones from the split above, under `###` subsections of seven or fewer. Possible groups are recording a risk, ownership, review, response and escalation, and tooling.
- R1.3: `rules.md`, `risk-becomes-issue-when-it-happens`, "SHOULD leave the risk register": this rests on the part of the claims that the second check refuted. `pmbok8-issue-already-happened` is refuted because "the source never says an issue no longer belongs in the risk register". `orange-book-contingency-if-risks-crystallise` is refuted because Principle D9 "does not say that crystallising is the point where something stops being a risk". `prince2-issue-is-event-that-happened` and `atlassian-raid-issues-need-immediate-attention` define an issue and set it apart from a risk, but neither says the risk leaves the register. The wording also contradicts the guideline itself in three places:
    - `concern-has-status-and-raiser` keeps each risk's status (active or closed) and its history in the register.
    - `keeping-a-risk-register.md` step 7 says to "close the risk and raise an issue".
    - The build-bar line says "is closed and raised as an issue".
    Fix: "A risk whose event has happened SHOULD be closed in the risk register and raised as an issue, which needs management action now." Add `prince2-risk-status-field` (active or closed; named by the `concern-has-status-and-raiser` verdict) to its citation.
- R1.4: `rules.md`, `flag-project-at-risk`, "alongside a record for each risk rather than in place of one", and its `a-build-must-establish.md` line, "beside its per-risk records": none of the cited claims supports the clause. `linear-health-at-risk` was refuted on exactly the per-risk part ("Nothing in the quote or the page supports 'no per-risk record type'"), and its quote supports only the project-level health indicator. The clause also decides part of the owner's open question on tracker mapping, which lists "a project health flag such as Linear's 'At risk'" as one candidate mapping for a small team, because it rules that flag out as the mapping. Fix: end the rule at the indicator: "A team MAY mark a project its risks threaten with a health indicator such as on track, at risk or off track. (claim: linear-health-at-risk)". Make the build line read "where used, a threatened project carries a health indicator". The other rules already ask for a record for each risk, so nothing is lost.
- R1.5: `artifact.json` `related` and `intro.md`, the scope paragraph (criterion 6; cross-recipe-consistency must-reference-siblings-by-uuid): `related` is `[]`, but the text hands every risk that has happened to issue tracking, and sibling guidelines it overlaps already exist:
    - `issue-tracking` (`f77eeffe-2699-4028-9195-4bfc23c75e91`, in `cookbook/index.json`). Its own intro sends "risks that have not happened" to this topic.
    - `dependency-tracking` (`3f978ba7-c8c1-4b53-8fda-12e5a6966b75`). Its `at-risk-dependency-logged-as-risk` rule feeds this register, and its round-1 review already asked that guideline to add this one to its `related`.
    The intro also names issue tracking in free prose, not by link. Fix: add both UUIDs to `related`, and in the intro link issue tracking as `[adc.guideline.planning.project-management.issue-tracking](cookbook:f77eeffe-2699-4028-9195-4bfc23c75e91)`, the form `issue-tracking`'s intro uses for its existing siblings. `project-record-linking` has no guideline yet, so it stays a topic mention.

Lint failed (`lint: fail 1`): fix each lint error in the draft. The review's `## Lint` section:

````
I ran /lint-artifact (v2.0.1, using this checkout's cookr) on the compiled guideline. Result: Pass 21, Warn 0, Fail 1, RESULT: NOT CLEAN.

- PASS: FM-01, FM-02, FM-04 to FM-13 (frontmatter, UUID, type, semver, required fields, MIT license, copyright, dates, summary, H1 matching the title, links, Change History, no placeholders); GF-01 to GF-04; gf-triggers-field; gf-roled-parts (17 build-bar lines, one per rule); gf-named-rules; gf-research-folder; gf-rule-cites-research (every cited claim exists and has a verdict).
- FAIL: FM-03, index entry matches folder. `cookbook/index.json` has no entry for `a55182ef-3144-407c-b64a-6377f37f5c63` and no `risk-tracking` path. Fix: run `cookr update`, which adds the entry. The sibling `milestone-scheduling` is unindexed in the same way.
- `cookr validate` shows nothing for this artifact. It fails only on `project-record-linking/research/research.md` (no frontmatter) and on cookbook-wide index drift.

lint: fail 1
````

## Round 2 findings

Verdict: fail. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

- R2.1: `a-build-must-establish.md`, build lines that ask for more than their rule (behavioral-requirements, source-fidelity: a build check must test the rule at the strength and scope it states, no more). Two lines changed this round have this problem:
    - `risk-identification-and-attention-flagging`: "the register includes risks whose sources lie outside the team's control." The rule, like `iso-identify-risks-whatever-their-source` ("should identify risks, whether or not their sources are under its control"), asks that identification not stop at what the team controls. It does not say such risks must exist. A project with no external-source risks keeps the rule but fails this line. Fix: "risk identification covered sources outside the team's control as well as those within it."
    - `agree-escalation-criteria`: "escalation criteria are agreed and written down." The rule and its claims (`orange-book-timely-escalation` "based on agreed criteria"; `nao-escalation-criteria-immediate-action` "clear criteria for escalating risks") ask for agreed, clear criteria. Neither the rule nor its claims says the criteria are written down. Fix: "clear escalation criteria are agreed."

Disputes so far (disputes.md):

- lint-FM-03: the missing `cookbook/index.json` entry for `a55182ef-3144-407c-b64a-6377f37f5c63` is not in the draft and cannot be fixed there; the fix the lint names, `cookr update`, edits the index, which the guideline author must not touch (guideline-author "Touch indexes ... That is the cookbook's file-management job"), so it belongs to the integration stage, as for the unindexed sibling `milestone-scheduling`

## Round 3 findings

Verdict: pass. Fix each finding, or dispute it in disputes.md (`- <id>: <why, citing the claim or rule>`); a disputed finding is not obeyed.

none
