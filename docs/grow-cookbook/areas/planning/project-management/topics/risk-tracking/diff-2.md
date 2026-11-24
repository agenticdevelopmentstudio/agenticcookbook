--- draft-1.md
+++ draft.md
@@ -10,7 +10,7 @@
 author: Mike Fullerton
 copyright: 2026 Mike Fullerton
 license: MIT
-summary: "Keeping a project risk register: identify and record risks early, give each one owner, status and response, review on a plan, escalate, hand over issues."
+summary: "Keeping a project risk register: record each risk early, with one owner, a status and a response; review on a plan, escalate, and close it into an issue."
 platforms: []
 tags:
   - risk-tracking
@@ -18,7 +18,9 @@
   - project-management
   - escalation
 depends-on: []
-related: []
+related:
+  - f77eeffe-2699-4028-9195-4bfc23c75e91
+  - 3f978ba7-c8c1-4b53-8fda-12e5a6966b75
 references:
   - https://fenix.tecnico.ulisboa.pt/downloadFile/1970943312401590/Norma_ISO_31000_EN.pdf
   - https://www.gov.uk/government/publications/orange-book/the-orange-book-management-of-risk-principles-and-concepts
@@ -42,39 +44,69 @@
 
 # Risk Tracking
 
-Identify a project's risks early, from anyone, and record each one in a register as soon as it is seen: described as cause, event and effect, with its raiser, its status, the product it concerns and one named owner. Decide for each risk whether it needs action now or is watched, choose its response by weighing cost against benefit, review the register on a planned cadence so no open risk goes stale, escalate what exceeds tolerance, and hand a risk that has happened to issue tracking.
-
-This guideline covers how a delivery team identifies, records, owns, reviews, responds to and closes project risks and open concerns, in a risk register, a RAID log or the team's tracker. It does not cover issues: a risk that has happened is handed to issue tracking, which rules issue severity and triage. How a risk record links to milestones, tasks and other project records belongs to project record linking; only what a risk record itself carries is this guideline's. Technical risks of one practice, such as backup and recovery or feature flags, belong to their own guidelines. Following it means keeping each SHOULD rule below or stating why a register departs from it; the MAY rules are options.
+Identify a project's risks early, from anyone, and record each one in a register as soon as it is seen: described as cause, event and effect, with its raiser, its status, the product it concerns and one named owner. Decide for each risk whether it needs action now or is watched, choose its response by weighing cost against benefit, review the register on a planned cadence so no open risk goes stale, escalate what exceeds tolerance, and close a risk that has happened into an issue.
+
+This guideline covers how a delivery team identifies, records, owns, reviews, responds to and closes project risks and open concerns, in a risk register, a RAID log or the team's tracker. It does not cover issues: a risk that has happened is raised as an issue under [adc.guideline.planning.project-management.issue-tracking](cookbook:f77eeffe-2699-4028-9195-4bfc23c75e91), which covers issue severity and triage. A dependency at risk reaches this register from [adc.guideline.planning.project-management.dependency-tracking](cookbook:3f978ba7-c8c1-4b53-8fda-12e5a6966b75). How a risk record links to milestones, tasks and other project records belongs to the `project-record-linking` topic; only what a risk record itself carries is this guideline's. Technical risks of one practice, such as backup and recovery or feature flags, belong to their own guidelines. Following it means keeping each SHOULD rule below or stating why a register departs from it; the MAY rules are options.
 
 ## Rules
 
-- **risk-identification-and-attention-flagging**: A team SHOULD identify the risks to its objectives, whether or not their sources are under its control, surface new risks and impediments as they appear, and record each risk in the register as soon as it is identified, whoever on the project or among its stakeholders raised it. (claims: iso-identify-risks-whatever-their-source, prince2-capture-risks-when-identified, scrum-daily-identifies-impediments)
-- **distinguish-immediate-action-from-monitoring**: A team SHOULD evaluate each risk against its agreed risk criteria to decide whether it needs definite action now or is watched, with any plan for it prepared now and carried out only if its trigger condition occurs, and SHOULD record how soon the risk event is expected to happen. (claims: iso-evaluation-decides-action, prince2-reduce-is-action-now, prince2-contingent-plans-wait, pmbok8-contingent-responses-on-trigger, prince2-proximity-field)
-- **link-concerns-to-related-elements**: Each risk record SHOULD be uniquely identified and SHOULD name the product or business process it concerns. (claims: prince2-risk-refers-to-product, orange-book-register-holds-owners-and-links)
-- **concern-has-status-and-raiser**: Each risk record SHOULD name its author, the person who raised it, and SHOULD carry a status that shows whether the risk is active or closed and whether its response actions are complete, ongoing or pending, with the register keeping that status's history. (claims: prince2-risk-author-field, prince2-risk-status-field, prince2-status-shows-action-taken, prince2-register-records-status-and-history, ilx-current-status)
-- **no-concern-open-without-review**: An open risk SHOULD NOT sit unreviewed: each one, a risk that no treatment can sufficiently reduce included, SHOULD be kept under ongoing review and revised as it changes, so the register stays up to date. (claims: iso-untreatable-risk-kept-under-review, orange-book-regularly-reviewed, orange-book-continuous-monitoring, nao-registers-up-to-date, pmbok8-monitoring-never-stops)
+### Recording a risk
+
+- **risk-identification-and-attention-flagging**: A team SHOULD identify the risks to its objectives, whether or not their sources are under its control. (claim: iso-identify-risks-whatever-their-source)
+- **surface-new-risks-continually**: A team SHOULD keep looking for new risks and impediments throughout the project, such as at its daily meeting. (claims: scrum-daily-identifies-impediments, pmbok8-monitoring-never-stops)
+- **record-risk-when-identified**: Each risk SHOULD be entered in the register as soon as it is identified, whoever on the project or among its stakeholders raised it. (claim: prince2-capture-risks-when-identified)
+- **describe-risk-as-cause-event-effect**: Each risk SHOULD be described in terms of its cause, the event that may happen and its effect. (claim: prince2-risk-description-cause-event-effect)
+- **no-duplicate-risk-entries**: Each risk entry SHOULD be specific and distinct from every other entry, not repeated in slightly different forms. (claim: ilx-vague-or-duplicated-risks)
+- **risk-uniquely-identified**: Each risk record SHOULD carry an identifier unique in the register. (claim: prince2-risk-refers-to-product)
+- **link-concerns-to-related-elements**: Each risk record SHOULD name the product or business process it concerns. (claims: prince2-risk-refers-to-product, orange-book-register-holds-owners-and-links)
+
+### Status and history
+
+- **concern-has-status-and-raiser**: Each risk record SHOULD name its author, the person who raised it. (claim: prince2-risk-author-field)
+- **risk-has-active-or-closed-status**: Each risk record SHOULD carry a status that shows whether the risk is active or closed. (claim: prince2-risk-status-field)
+- **status-shows-response-progress**: Each risk's status SHOULD show whether its response actions are complete, ongoing or pending. (claims: prince2-status-shows-action-taken, ilx-current-status)
+- **keep-risk-status-history**: The register SHOULD keep the history of each risk's status. (claim: prince2-register-records-status-and-history)
+- **record-risk-proximity**: Each risk record SHOULD state how soon its event is expected to happen, such as imminent, within the stage, within the project or beyond it. (claim: prince2-proximity-field)
+
+### Ownership
+
+- **risk-has-single-named-owner**: Each risk SHOULD have exactly one named owner, responsible for its management and escalation, a complex risk that spans parts of the organisation or delivery partners included. (claims: prince2-single-risk-owner, roam-single-owner, atlassian-risk-register-components, nao-lack-of-ownership, nao-clarity-of-ownership-complex-risks, ilx-lack-of-accountability, orange-book-first-line-ownership)
+- **owner-most-capable-of-managing**: A risk's owner SHOULD be the person most capable of managing it. (claim: prince2-owner-and-actionee-agreed)
+- **no-owner-holds-too-many-risks**: A team SHOULD NOT allocate too many risks to any one person. (claim: prince2-owner-and-actionee-agreed)
+- **risk-response-has-an-actionee**: Each risk response SHOULD name its actionee, the person or people who will carry it out. (claims: prince2-risk-actionee, iso-treatment-plan-names-responsible-and-timing, ilx-owner-and-actionee, pmbok8-unassigned-response-is-a-wish)
+
+### Review
+
+- **no-concern-open-without-review**: Each open risk, a risk that no treatment can sufficiently reduce included, SHOULD be kept under ongoing review and revised as it changes. (claims: iso-untreatable-risk-kept-under-review, orange-book-regularly-reviewed, orange-book-continuous-monitoring, pmbok8-monitoring-never-stops)
+- **keep-register-up-to-date**: The risk register SHOULD be kept up to date. (claim: nao-registers-up-to-date)
+- **risk-review-cadence**: A team SHOULD plan when its risks are formally reviewed, with responsibility for the review clearly defined and the review built into its normal management flow, such as stage boundaries, progress reviews or team reviews. (claims: prince2-risk-timing-set-in-approach, iso-monitoring-planned-with-responsibilities, orange-book-risk-in-normal-management-flow, atlassian-regular-risk-meeting, nao-monthly-review-example, ilx-static-records, kanban-review-active-items-age)
+- **check-register-at-each-review**: At each planned review, a team SHOULD check the register for new or revised risks. (claim: prince2-review-register-at-progress-reviews)
 - **flag-overdue-risk-reviews**: A tracker MAY mark a record that is overdue for its update, so a stale entry is visible. (claim: linear-overdue-updates-flagged)
-- **risk-review-cadence**: A team SHOULD plan when its risks are formally reviewed, with responsibility for the review clearly defined and the review built into its normal management flow, such as stage boundaries, progress reviews or team reviews, and SHOULD check the register at each review for new or revised risks. (claims: prince2-risk-timing-set-in-approach, prince2-review-register-at-progress-reviews, iso-monitoring-planned-with-responsibilities, orange-book-risk-in-normal-management-flow, atlassian-regular-risk-meeting, nao-monthly-review-example, ilx-static-records, kanban-review-active-items-age)
-- **risk-has-single-named-owner**: Each risk SHOULD have exactly one named owner, responsible for its management and escalation, a complex risk that spans parts of the organisation or delivery partners included. (claims: prince2-single-risk-owner, roam-single-owner, atlassian-risk-register-components, nao-lack-of-ownership, nao-clarity-of-ownership-complex-risks, ilx-lack-of-accountability, orange-book-first-line-ownership)
-- **owner-most-capable-and-not-overloaded**: A risk's owner SHOULD be the person most capable of managing it, and no one person SHOULD be allocated too many risks. (claim: prince2-owner-and-actionee-agreed)
-- **risk-response-has-an-actionee**: Each risk response SHOULD name its actionee, the person or people who will carry it out, who may or may not be the risk's owner. (claims: prince2-risk-actionee, iso-treatment-plan-names-responsible-and-timing, ilx-owner-and-actionee, pmbok8-unassigned-response-is-a-wish)
-- **risk-response-triage**: A team SHOULD choose each risk's response from a defined set of response options, such as avoiding, reducing, sharing or retaining the risk, preparing a contingent plan, or escalating it, by weighing what the response gains against its cost, effort and disadvantages. (claims: iso-treatment-options, iso-select-treatment-by-cost-benefit, prince2-reduce-is-action-now, prince2-contingent-plans-wait, pmbok8-threat-responses-include-escalation, roam-four-categories)
-- **escalate-risks-beyond-tolerance**: A team SHOULD agree clear criteria for escalating a risk, and a risk whose exposure exceeds or threatens the agreed tolerance SHOULD be escalated in good time rather than accepted. (claims: orange-book-timely-escalation, nao-escalation-criteria-immediate-action, prince2-escalate-when-tolerance-threatened, prince2-accept-not-beyond-tolerance, nao-monthly-review-example)
-- **risk-becomes-issue-when-it-happens**: A risk whose event has happened SHOULD leave the risk register and be raised as an issue, which needs management action now. (claims: prince2-issue-is-event-that-happened, atlassian-raid-issues-need-immediate-attention, pmbok8-issue-already-happened, orange-book-contingency-if-risks-crystallise)
-- **describe-risk-as-cause-event-effect**: Each risk SHOULD be described in terms of its cause, the event that may happen and its effect, specific and distinct from every other entry rather than repeated in slightly different forms. (claims: prince2-risk-description-cause-event-effect, ilx-vague-or-duplicated-risks)
+
+### Response and escalation
+
+- **distinguish-immediate-action-from-monitoring**: A team SHOULD evaluate each risk against its agreed risk criteria to decide whether it needs definite action now or is watched, with any plan for a watched risk prepared now and carried out only if its trigger condition occurs. (claims: iso-evaluation-decides-action, prince2-reduce-is-action-now, prince2-contingent-plans-wait, pmbok8-contingent-responses-on-trigger)
+- **risk-response-triage**: A team SHOULD choose each risk's response from a defined set of response options, such as avoiding, reducing, sharing or retaining the risk, preparing a contingent plan, or escalating it. (claims: iso-treatment-options, prince2-reduce-is-action-now, prince2-contingent-plans-wait, pmbok8-threat-responses-include-escalation, roam-four-categories)
+- **weigh-response-cost-against-benefit**: A team SHOULD choose a risk's response by weighing what it gains toward the objectives against its cost, effort and disadvantages. (claim: iso-select-treatment-by-cost-benefit)
+- **agree-escalation-criteria**: A team SHOULD agree clear criteria for when a risk is escalated. (claims: orange-book-timely-escalation, nao-escalation-criteria-immediate-action)
+- **escalate-risks-beyond-tolerance**: A risk whose exposure exceeds or threatens the agreed tolerance SHOULD be escalated in good time rather than accepted. (claims: orange-book-timely-escalation, nao-escalation-criteria-immediate-action, prince2-escalate-when-tolerance-threatened, prince2-accept-not-beyond-tolerance, nao-monthly-review-example)
+- **risk-becomes-issue-when-it-happens**: A risk whose event has happened SHOULD be closed in the risk register and raised as an issue, which needs management action now. (claims: prince2-issue-is-event-that-happened, atlassian-raid-issues-need-immediate-attention, pmbok8-issue-already-happened, orange-book-contingency-if-risks-crystallise, prince2-risk-status-field)
+
+### Tooling
+
 - **keep-risk-scoring-simple**: A team MAY score each risk simply, as its probability multiplied by its impact, rather than with a scoring model that needs excessive interpretation. (claims: atlassian-probability-times-impact, ilx-overly-complex-scoring)
 - **track-risks-in-the-team-tracker**: A team MAY keep its risk register in the tracker it already works in, as a custom issue type with structured fields such as impact or priority, or as part of an integrated log of risks, actions, decisions, assumptions and issues. (claims: prince2-register-formats, github-custom-issue-types, github-custom-issue-fields, iso-record-and-report-outcomes)
-- **flag-project-at-risk**: A team MAY mark a project its risks threaten with a health indicator such as on track, at risk or off track, alongside a record for each risk rather than in place of one. (claim: linear-health-at-risk)
+- **flag-project-at-risk**: A team MAY mark a project its risks threaten with a health indicator such as on track, at risk or off track. (claim: linear-health-at-risk)
 
 ## Keeping a risk register
 
 This section is informative: it shows one way to keep the rules, not a required method.
 
 1. Choose where the register lives. A small team can define a Risk issue type in GitHub (which ships task, bug and feature and allows up to 25 organisation types) or Jira, with fields for impact, probability, proximity, owner and actionee. PRINCE2 also allows a separate register, a tool entry, or one part of an integrated register of risks, actions, decisions, assumptions, issues and lessons, the shape a RAID log takes. Linear's project health indicator marks a project, not a single risk.
-2. When anyone spots a risk, at a Daily Scrum, a review or in passing, add it at once. Write the description as cause, event and effect, check that it is not an existing entry in other words, and record the raiser, the product it concerns and how soon the event is expected (imminent, within the stage, within the project or beyond it).
-3. Agree its owner, the one person most capable of managing it, and the actionee who will carry out the response.
-4. Evaluate it against the team's criteria. Score it simply if the team scores at all; Atlassian's register uses probability times impact. Then choose a response: reduce it now, prepare a contingent plan that waits for its trigger, avoid, share or retain it, or escalate it if its exposure exceeds tolerance.
-5. Set the status: active or closed, and whether the response actions are complete, ongoing or pending.
+2. When anyone spots a risk, at a Daily Scrum, a review or in passing, add it at once with its own identifier. Write the description as cause, event and effect, check that it is not an existing entry in other words, and record the raiser, the product it concerns and how soon the event is expected (imminent, within the stage, within the project or beyond it).
+3. Agree its owner, the one person most capable of managing it, checking that person does not already hold too many risks, and name the actionee who will carry out the response.
+4. Evaluate it against the team's criteria. Score it simply if the team scores at all; Atlassian's register uses probability times impact. Then choose a response, weighing its benefit against its cost: reduce it now, prepare a contingent plan that waits for its trigger, avoid, share or retain it, or escalate it if its exposure exceeds tolerance under the team's escalation criteria.
+5. Set the status: active or closed, and whether the response actions are complete, ongoing or pending. Keep earlier statuses as the risk's history.
 6. At each planned review, a stage end, a progress review, a regular risk meeting or a fixed interval the team has set, walk every open risk, update its status and exposure, add new risks, escalate those beyond tolerance, and close what no longer applies.
 7. When a risk's event happens, close the risk and raise an issue for it, carrying its owner and its contingency plan across.
 
@@ -98,6 +130,7 @@
 Probability: 3  Impact: 5  Score: 15
 Response: reduce: migrate to the v3 API this sprint
 Status: active; response ongoing
+Status history: 2026-11-03 active, response pending; 2026-11-10 active, response ongoing
 Next review: sprint review, 2026-11-28
 ```
 
@@ -105,32 +138,45 @@
 
 This section is informative.
 
-Checks that every known risk is in the register, raised as soon as it was seen, and that each entry has a cause, event and effect description distinct from every other entry, a unique identifier, the product it concerns, its raiser, one named owner, an actionee for its response and a status that shows whether it is active or closed and how far its response has got. Checks that each risk was evaluated to act now or watch, that its response was chosen from the team's options by weighing cost against benefit, that no risk beyond tolerance was accepted instead of escalated, and that escalation criteria exist. Checks that the team has a planned review cadence with a named responsibility, that no open risk has gone unreviewed past it, and that a risk whose event happened was moved to issue tracking. Notes whether the team scores risks simply, keeps the register in its tracker, and flags project health or overdue updates.
+Checks that the team looks for risks beyond its own control and keeps surfacing new ones, and that every known risk is in the register, entered as soon as it was seen. Checks that each entry has its own identifier, a cause, event and effect description distinct from every other entry, the product it concerns, its raiser, a status that shows whether it is active or closed and how far its response has got, a kept status history and its proximity. Checks that each risk has one named owner who is the person most capable of managing it, that no one holds too many risks, and that each response names its actionee. Checks that each risk was evaluated to act now or watch, that its response was chosen from the team's options by weighing cost against benefit, that escalation criteria exist, and that no risk beyond tolerance was accepted instead of escalated. Checks that the team has a planned review cadence with a named responsibility, that the register is checked for new or revised risks at each review, that no open risk has gone unreviewed and the register is current, and that a risk whose event happened was closed and raised as an issue. Notes whether the team scores risks simply, keeps the register in its tracker, and flags project health or overdue updates.
 
 ## A complete review must establish
 
-- Each SHOULD rule is kept or its departure is stated: `risk-identification-and-attention-flagging`, `distinguish-immediate-action-from-monitoring`, `link-concerns-to-related-elements`, `concern-has-status-and-raiser`, `no-concern-open-without-review`, `risk-review-cadence`, `risk-has-single-named-owner`, `owner-most-capable-and-not-overloaded`, `risk-response-has-an-actionee`, `risk-response-triage`, `escalate-risks-beyond-tolerance`, `risk-becomes-issue-when-it-happens`, `describe-risk-as-cause-event-effect`.
+- Each SHOULD rule is kept or its departure is stated: `risk-identification-and-attention-flagging`, `surface-new-risks-continually`, `record-risk-when-identified`, `describe-risk-as-cause-event-effect`, `no-duplicate-risk-entries`, `risk-uniquely-identified`, `link-concerns-to-related-elements`, `concern-has-status-and-raiser`, `risk-has-active-or-closed-status`, `status-shows-response-progress`, `keep-risk-status-history`, `record-risk-proximity`, `risk-has-single-named-owner`, `owner-most-capable-of-managing`, `no-owner-holds-too-many-risks`, `risk-response-has-an-actionee`, `no-concern-open-without-review`, `keep-register-up-to-date`, `risk-review-cadence`, `check-register-at-each-review`, `distinguish-immediate-action-from-monitoring`, `risk-response-triage`, `weigh-response-cost-against-benefit`, `agree-escalation-criteria`, `escalate-risks-beyond-tolerance`, `risk-becomes-issue-when-it-happens`.
 - Each MAY rule is noted where it was used: `flag-overdue-risk-reviews`, `keep-risk-scoring-simple`, `track-risks-in-the-team-tracker`, `flag-project-at-risk`.
 
 ## A build must establish
 
-- `risk-identification-and-attention-flagging`: each identified risk is in the register, added when it was identified.
-- `distinguish-immediate-action-from-monitoring`: each risk is marked as needing action now or watched, and records how soon its event is expected.
-- `link-concerns-to-related-elements`: each risk record has a unique identifier and names the product or process it concerns.
-- `concern-has-status-and-raiser`: each risk record names its raiser and carries a status, with the status's history kept.
-- `no-concern-open-without-review`: every open risk has been reviewed and the register is current.
+- `risk-identification-and-attention-flagging`: the register includes risks whose sources lie outside the team's control.
+- `surface-new-risks-continually`: the team has a recurring point, such as its daily meeting, where new risks and impediments are raised.
+- `record-risk-when-identified`: each identified risk is in the register, added when it was identified.
+- `describe-risk-as-cause-event-effect`: each description states cause, event and effect.
+- `no-duplicate-risk-entries`: no entry repeats another in different words.
+- `risk-uniquely-identified`: each risk record has an identifier unique in the register.
+- `link-concerns-to-related-elements`: each risk record names the product or process it concerns.
+- `concern-has-status-and-raiser`: each risk record names its raiser.
+- `risk-has-active-or-closed-status`: each risk record carries an active or closed status.
+- `status-shows-response-progress`: each status shows whether the response actions are complete, ongoing or pending.
+- `keep-risk-status-history`: each risk's earlier statuses are kept.
+- `record-risk-proximity`: each risk record states how soon its event is expected.
+- `risk-has-single-named-owner`: each risk names exactly one owner.
+- `owner-most-capable-of-managing`: each owner is the person most capable of managing the risk.
+- `no-owner-holds-too-many-risks`: no one person holds too many risks.
+- `risk-response-has-an-actionee`: each response names its actionee.
+- `no-concern-open-without-review`: every open risk has been reviewed and revised as it changed.
+- `keep-register-up-to-date`: the register is current.
+- `risk-review-cadence`: the team has a planned review cadence, with responsibility defined, built into its normal management flow.
+- `check-register-at-each-review`: each review checked the register for new or revised risks.
 - `flag-overdue-risk-reviews`: where used, a record overdue for update is marked as such.
-- `risk-review-cadence`: the team has a planned review cadence, with responsibility defined, at which the register is checked.
-- `risk-has-single-named-owner`: each risk names exactly one owner.
-- `owner-most-capable-and-not-overloaded`: each owner is the person most capable of managing the risk, and no one holds too many.
-- `risk-response-has-an-actionee`: each response names its actionee.
-- `risk-response-triage`: each risk's response comes from the team's defined options and was chosen by weighing cost against benefit.
-- `escalate-risks-beyond-tolerance`: escalation criteria are agreed, and every risk beyond tolerance was escalated, not accepted.
+- `distinguish-immediate-action-from-monitoring`: each risk is marked as needing action now or watched.
+- `risk-response-triage`: each risk's response comes from the team's defined options.
+- `weigh-response-cost-against-benefit`: each response was chosen by weighing its benefit against its cost.
+- `agree-escalation-criteria`: escalation criteria are agreed and written down.
+- `escalate-risks-beyond-tolerance`: every risk beyond tolerance was escalated, not accepted.
 - `risk-becomes-issue-when-it-happens`: each risk whose event happened is closed and raised as an issue.
-- `describe-risk-as-cause-event-effect`: each description states cause, event and effect, and no entry duplicates another.
 - `keep-risk-scoring-simple`: where used, scores are probability times impact.
 - `track-risks-in-the-team-tracker`: where used, the register is a custom issue type with fields, or part of an integrated log.
-- `flag-project-at-risk`: where used, a threatened project carries a health indicator beside its per-risk records.
+- `flag-project-at-risk`: where used, a threatened project carries a health indicator.
 
 ## Rationale
 
@@ -138,7 +184,7 @@
 
 A register is only as useful as it is current. The National Audit Office names stale registers and missing ownership among the reasons government risks go unmanaged, and practitioner guidance lists static records, vague or duplicated entries, unclear accountability and over-complex scoring as the common failures. A risk with one owner, a clear description and a planned review is one somebody will act on; a risk with none of these is a line in a document.
 
-The rules are recommendations, not requirements, because the sources state them that way: ISO 31000 uses "should", PRINCE2 "recommends" and lists the register's fields under what "should be recorded", and the Orange Book and NAO give guidance rather than mandates. Several rules rest on PRINCE2 alone, such as the raiser field, and several secondary claims were only partly supported by their quotes on a second check, so none carries more than SHOULD. Scoring and keeping the register in a tracker are options: the scoring rule rests on a vendor guide and a training provider's view with no study behind it, and the trackers offer custom types and fields rather than a risk record. The Scrum Guide prescribes no register at all and controls risk through short iterations, which is why a team using it may keep a lighter register than PRINCE2 describes.
+The rules are recommendations, not requirements, because the sources state them that way: ISO 31000 uses "should", PRINCE2 "recommends" and lists the register's fields under what "should be recorded", and the Orange Book and NAO give guidance rather than mandates. Several rules rest on PRINCE2 alone, such as the raiser, proximity and status-history fields, and several secondary claims were only partly supported by their quotes on a second check, so none carries more than SHOULD. Scoring and keeping the register in a tracker are options: the scoring rule rests on a vendor guide and a training provider's view with no study behind it, and the trackers offer custom types and fields rather than a risk record. The Scrum Guide prescribes no register at all and controls risk through short iterations, which is why a team using it may keep a lighter register than PRINCE2 describes.
 
 Several questions are the owner's and are left open here: which review cadence the rule names, or whether the team sets its own; which response vocabulary the cookbook adopts, ISO 31000's, PRINCE2's, PMBOK 8's or ROAM's; whether opportunities, positive risks, are in this topic's scope; whether a separate actionee is required beside the owner; and which tracker mapping a small team is recommended.
 
