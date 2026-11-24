I wrote both research files and they pass validation (the exact validate command printed `Research passed.`). All five listed rules are supported at SHOULD strength, and the research adds nine `new` verdicts.

**Files:**
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/risk-tracking/research/research.json`
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/risk-tracking/research/research.md`

**Claims per question (61 in total):**

| Question | Claims |
|---|---|
| best-practices | 15 |
| known-solutions | 22 |
| platform-guidelines | 12 |
| experts-view | 12 |

**Verdicts:**
- risk-identification-and-attention-flagging: supported (SHOULD). Claims: iso-identify-risks-whatever-their-source, prince2-capture-risks-when-identified, scrum-daily-identifies-impediments, linear-health-at-risk, orange-book-timely-escalation, nao-escalation-criteria-immediate-action
- distinguish-immediate-action-from-monitoring: supported (SHOULD). Claims: iso-evaluation-decides-action, prince2-reduce-is-action-now, prince2-contingent-plans-wait, pmbok8-contingent-responses-on-trigger, prince2-proximity-field, nao-escalation-criteria-immediate-action
- link-concerns-to-related-elements: supported (SHOULD; only what the risk record itself carries). Claims: prince2-risk-refers-to-product, orange-book-register-holds-owners-and-links, prince2-register-formats
- concern-has-status-and-raiser: supported (SHOULD). Claims: prince2-risk-author-field, prince2-risk-status-field, prince2-register-records-status-and-history, prince2-status-shows-action-taken, ilx-current-status
- no-concern-open-without-review: supported (SHOULD). Claims: iso-monitoring-planned-with-responsibilities, iso-untreatable-risk-kept-under-review, orange-book-regularly-reviewed, orange-book-continuous-monitoring, nao-registers-up-to-date, prince2-review-register-at-progress-reviews, ilx-static-records, kanban-review-active-items-age, linear-overdue-updates-flagged, pmbok8-monitoring-never-stops
- risk-has-single-named-owner: new (SHOULD). Claims: prince2-single-risk-owner, prince2-owner-and-actionee-agreed, roam-single-owner, atlassian-risk-register-components, nao-lack-of-ownership, nao-clarity-of-ownership-complex-risks, ilx-lack-of-accountability, orange-book-first-line-ownership
- risk-response-has-an-actionee: new (SHOULD). Claims: prince2-risk-actionee, iso-treatment-plan-names-responsible-and-timing, ilx-owner-and-actionee, pmbok8-unassigned-response-is-a-wish
- risk-review-cadence: new (SHOULD; the team sets the interval). Claims: prince2-risk-timing-set-in-approach, prince2-review-register-at-progress-reviews, iso-monitoring-planned-with-responsibilities, orange-book-risk-in-normal-management-flow, atlassian-regular-risk-meeting, nao-monthly-review-example, ilx-static-records, kanban-review-active-items-age
- risk-response-triage: new (SHOULD). Claims: iso-treatment-options, iso-select-treatment-by-cost-benefit, prince2-reduce-is-action-now, prince2-contingent-plans-wait, prince2-accept-not-beyond-tolerance, pmbok8-threat-responses-include-escalation, roam-four-categories
- escalate-risks-beyond-tolerance: new (SHOULD). Claims: orange-book-timely-escalation, nao-escalation-criteria-immediate-action, prince2-escalate-when-tolerance-threatened, prince2-accept-not-beyond-tolerance, nao-monthly-review-example
- risk-becomes-issue-when-it-happens: new (SHOULD). Claims: prince2-issue-is-event-that-happened, atlassian-raid-issues-need-immediate-attention, pmbok8-issue-already-happened, orange-book-contingency-if-risks-crystallise
- describe-risk-as-cause-event-effect: new (SHOULD). Claims: prince2-risk-description-cause-event-effect, ilx-vague-or-duplicated-risks
- keep-risk-scoring-simple: new (MAY). Claims: atlassian-probability-times-impact, ilx-overly-complex-scoring
- track-risks-in-the-team-tracker: new (MAY). Claims: prince2-register-formats, github-custom-issue-types, github-custom-issue-fields, linear-health-at-risk, iso-record-and-report-outcomes, scrum-controls-risk-by-iteration

No rule came out unsupported or contradicted, so there are no `-prior` claims.

**Where the evidence is weaker:**
- Every claim is marked `single`. No two independent publishers used the same quoted words, so corroboration comes from several claims under the same verdict.
- I read ISO 31000 and PRINCE2 from copies hosted on university sites, because the publishers' own sites refused the fetch. Each trust basis says so.
- The PMBOK 8 text is paywalled. It is covered by PMI's public errata and a secondary Substack summary; I checked the Substack quotes against the page with curl.
- These sources could not be fetched and are recorded as limitations: the SAFe site, axelos.com, Jira Align's documentation and ISO 21502. LeSS is not cited.
- No metric or study was found, so no claim takes the Statistical bar.

I deleted the scratch files I had created.
