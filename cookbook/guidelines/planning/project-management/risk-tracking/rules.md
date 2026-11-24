
### Recording a risk

- **risk-identification-and-attention-flagging**: A team SHOULD identify the risks to its objectives, whether or not their sources are under its control. (claim: iso-identify-risks-whatever-their-source)
- **surface-new-risks-continually**: A team SHOULD keep looking for new risks and impediments throughout the project, such as at its daily meeting. (claims: scrum-daily-identifies-impediments, pmbok8-monitoring-never-stops)
- **record-risk-when-identified**: Each risk SHOULD be entered in the register as soon as it is identified, whoever on the project or among its stakeholders raised it. (claim: prince2-capture-risks-when-identified)
- **describe-risk-as-cause-event-effect**: Each risk SHOULD be described in terms of its cause, the event that may happen and its effect. (claim: prince2-risk-description-cause-event-effect)
- **no-duplicate-risk-entries**: Each risk entry SHOULD be specific and distinct from every other entry, not repeated in slightly different forms. (claim: ilx-vague-or-duplicated-risks)
- **risk-uniquely-identified**: Each risk record SHOULD carry an identifier unique in the register. (claim: prince2-risk-refers-to-product)
- **link-concerns-to-related-elements**: Each risk record SHOULD name the product or business process it concerns. (claims: prince2-risk-refers-to-product, orange-book-register-holds-owners-and-links)

### Status and history

- **concern-has-status-and-raiser**: Each risk record SHOULD name its author, the person who raised it. (claim: prince2-risk-author-field)
- **risk-has-active-or-closed-status**: Each risk record SHOULD carry a status that shows whether the risk is active or closed. (claim: prince2-risk-status-field)
- **status-shows-response-progress**: Each risk's status SHOULD show whether its response actions are complete, ongoing or pending. (claims: prince2-status-shows-action-taken, ilx-current-status)
- **keep-risk-status-history**: The register SHOULD keep the history of each risk's status. (claim: prince2-register-records-status-and-history)
- **record-risk-proximity**: Each risk record SHOULD state how soon its event is expected to happen, such as imminent, within the stage, within the project or beyond it. (claim: prince2-proximity-field)

### Ownership

- **risk-has-single-named-owner**: Each risk SHOULD have exactly one named owner, responsible for its management and escalation, a complex risk that spans parts of the organisation or delivery partners included. (claims: prince2-single-risk-owner, roam-single-owner, atlassian-risk-register-components, nao-lack-of-ownership, nao-clarity-of-ownership-complex-risks, ilx-lack-of-accountability, orange-book-first-line-ownership)
- **owner-most-capable-of-managing**: A risk's owner SHOULD be the person most capable of managing it. (claim: prince2-owner-and-actionee-agreed)
- **no-owner-holds-too-many-risks**: A team SHOULD NOT allocate too many risks to any one person. (claim: prince2-owner-and-actionee-agreed)
- **risk-response-has-an-actionee**: Each risk response SHOULD name its actionee, the person or people who will carry it out. (claims: prince2-risk-actionee, iso-treatment-plan-names-responsible-and-timing, ilx-owner-and-actionee, pmbok8-unassigned-response-is-a-wish)

### Review

- **no-concern-open-without-review**: Each open risk, a risk that no treatment can sufficiently reduce included, SHOULD be kept under ongoing review and revised as it changes. (claims: iso-untreatable-risk-kept-under-review, orange-book-regularly-reviewed, orange-book-continuous-monitoring, pmbok8-monitoring-never-stops)
- **keep-register-up-to-date**: The risk register SHOULD be kept up to date. (claim: nao-registers-up-to-date)
- **risk-review-cadence**: A team SHOULD plan when its risks are formally reviewed, with responsibility for the review clearly defined and the review built into its normal management flow, such as stage boundaries, progress reviews or team reviews. (claims: prince2-risk-timing-set-in-approach, iso-monitoring-planned-with-responsibilities, orange-book-risk-in-normal-management-flow, atlassian-regular-risk-meeting, nao-monthly-review-example, ilx-static-records, kanban-review-active-items-age)
- **check-register-at-each-review**: At each planned review, a team SHOULD check the register for new or revised risks. (claim: prince2-review-register-at-progress-reviews)
- **flag-overdue-risk-reviews**: A tracker MAY mark a record that is overdue for its update, so a stale entry is visible. (claim: linear-overdue-updates-flagged)

### Response and escalation

- **distinguish-immediate-action-from-monitoring**: A team SHOULD evaluate each risk against its agreed risk criteria to decide whether it needs definite action now or is watched, with any plan for a watched risk prepared now and carried out only if its trigger condition occurs. (claims: iso-evaluation-decides-action, prince2-reduce-is-action-now, prince2-contingent-plans-wait, pmbok8-contingent-responses-on-trigger)
- **risk-response-triage**: A team SHOULD choose each risk's response from a defined set of response options, such as avoiding, reducing, sharing or retaining the risk, preparing a contingent plan, or escalating it. (claims: iso-treatment-options, prince2-reduce-is-action-now, prince2-contingent-plans-wait, pmbok8-threat-responses-include-escalation, roam-four-categories)
- **weigh-response-cost-against-benefit**: A team SHOULD choose a risk's response by weighing what it gains toward the objectives against its cost, effort and disadvantages. (claim: iso-select-treatment-by-cost-benefit)
- **agree-escalation-criteria**: A team SHOULD agree clear criteria for when a risk is escalated. (claims: orange-book-timely-escalation, nao-escalation-criteria-immediate-action)
- **escalate-risks-beyond-tolerance**: A risk whose exposure exceeds or threatens the agreed tolerance SHOULD be escalated in good time rather than accepted. (claims: orange-book-timely-escalation, nao-escalation-criteria-immediate-action, prince2-escalate-when-tolerance-threatened, prince2-accept-not-beyond-tolerance, nao-monthly-review-example)
- **risk-becomes-issue-when-it-happens**: A risk whose event has happened SHOULD be closed in the risk register and raised as an issue, which needs management action now. (claims: prince2-issue-is-event-that-happened, atlassian-raid-issues-need-immediate-attention, pmbok8-issue-already-happened, orange-book-contingency-if-risks-crystallise, prince2-risk-status-field)

### Tooling

- **keep-risk-scoring-simple**: A team MAY score each risk simply, as its probability multiplied by its impact, rather than with a scoring model that needs excessive interpretation. (claims: atlassian-probability-times-impact, ilx-overly-complex-scoring)
- **track-risks-in-the-team-tracker**: A team MAY keep its risk register in the tracker it already works in, as a custom issue type with structured fields such as impact or priority, or as part of an integrated log of risks, actions, decisions, assumptions and issues. (claims: prince2-register-formats, github-custom-issue-types, github-custom-issue-fields, iso-record-and-report-outcomes)
- **flag-project-at-risk**: A team MAY mark a project its risks threaten with a health indicator such as on track, at risk or off track. (claim: linear-health-at-risk)

