# Research: risk-tracking

Researched 2026-11-24 at base commit `f0dd450`. Machine-readable record: `research.json`.

**Summary.** All five listed rules hold at SHOULD strength. ISO 31000, PRINCE2 and the Orange Book all have a team identify risks early and from anyone. They record each risk in a register whose entries carry an author (the raiser), a status and a reference to the product the risk concerns. They evaluate each risk to decide whether it needs action now or is kept under watch, and they review the register on a planned basis so nothing goes stale.

The topic is missing these rules:

- a single named owner for each risk, with an actionee for the response
- a set review cadence: stage boundaries, or a fixed interval such as monthly
- response triage across avoid, reduce, transfer, share, accept, contingent plans and escalation, chosen by weighing cost against tolerance
- escalation of risks that exceed tolerance
- a risk description written as cause, event and effect
- simple scoring
- keeping risks in the team's tracker
- the hand-over to issue-tracking once a risk has happened

None of the trackers (GitHub, Jira, Linear) ships a dedicated risk record. Teams build one from custom issue types and fields, or use a project health flag.

Apple, Android and Windows have no bearing on this topic.

**Verdicts and the strength the sources support.**

- **risk-identification-and-attention-flagging**: supported at SHOULD (`iso-identify-risks-whatever-their-source`, `prince2-capture-risks-when-identified`, `scrum-daily-identifies-impediments`, `linear-health-at-risk`, `orange-book-timely-escalation`, `nao-escalation-criteria-immediate-action`). ISO 31000 and PRINCE2 use "should" and "recommends".
- **distinguish-immediate-action-from-monitoring**: supported at SHOULD (`iso-evaluation-decides-action`, `prince2-reduce-is-action-now`, `prince2-contingent-plans-wait`, `pmbok8-contingent-responses-on-trigger`, `prince2-proximity-field`, `nao-escalation-criteria-immediate-action`). Act-now and plan-but-wait are named, distinct options in PRINCE2 and PMBOK 8, and ISO 31000's evaluation step makes that decision.
- **link-concerns-to-related-elements**: supported at SHOULD for what the risk record itself carries, namely the product it refers to (`prince2-risk-refers-to-product`, `orange-book-register-holds-owners-and-links`, `prince2-register-formats`). How the link is made belongs to project-record-linking.
- **concern-has-status-and-raiser**: supported at SHOULD, as a check the register passes (`prince2-risk-author-field`, `prince2-risk-status-field`, `prince2-register-records-status-and-history`, `prince2-status-shows-action-taken`, `ilx-current-status`). PRINCE2 introduces both fields with "the following should be recorded". The raiser field rests on PRINCE2 alone, while status is corroborated.
- **no-concern-open-without-review**: supported at SHOULD (`iso-monitoring-planned-with-responsibilities`, `iso-untreatable-risk-kept-under-review`, `orange-book-regularly-reviewed`, `orange-book-continuous-monitoring`, `nao-registers-up-to-date`, `prince2-review-register-at-progress-reviews`, `ilx-static-records`, `kanban-review-active-items-age`, `linear-overdue-updates-flagged`, `pmbok8-monitoring-never-stops`).
- **risk-has-single-named-owner**: new, SHOULD (`prince2-single-risk-owner`, `prince2-owner-and-actionee-agreed`, `roam-single-owner`, `atlassian-risk-register-components`, `nao-lack-of-ownership`, `nao-clarity-of-ownership-complex-risks`, `ilx-lack-of-accountability`, `orange-book-first-line-ownership`).
- **risk-response-has-an-actionee**: new, SHOULD (`prince2-risk-actionee`, `iso-treatment-plan-names-responsible-and-timing`, `ilx-owner-and-actionee`, `pmbok8-unassigned-response-is-a-wish`).
- **risk-review-cadence**: new, SHOULD, with the interval left to the team (`prince2-risk-timing-set-in-approach`, `prince2-review-register-at-progress-reviews`, `iso-monitoring-planned-with-responsibilities`, `orange-book-risk-in-normal-management-flow`, `atlassian-regular-risk-meeting`, `nao-monthly-review-example`, `ilx-static-records`, `kanban-review-active-items-age`). No source sets one interval as a standard.
- **risk-response-triage**: new, SHOULD (`iso-treatment-options`, `iso-select-treatment-by-cost-benefit`, `prince2-reduce-is-action-now`, `prince2-contingent-plans-wait`, `prince2-accept-not-beyond-tolerance`, `pmbok8-threat-responses-include-escalation`, `roam-four-categories`).
- **escalate-risks-beyond-tolerance**: new, SHOULD (`orange-book-timely-escalation`, `nao-escalation-criteria-immediate-action`, `prince2-escalate-when-tolerance-threatened`, `prince2-accept-not-beyond-tolerance`, `nao-monthly-review-example`).
- **risk-becomes-issue-when-it-happens**: new, SHOULD (`prince2-issue-is-event-that-happened`, `atlassian-raid-issues-need-immediate-attention`, `pmbok8-issue-already-happened`, `orange-book-contingency-if-risks-crystallise`). This rule hands the risk to issue-tracking and rules nothing about issue severity.
- **describe-risk-as-cause-event-effect**: new, SHOULD (`prince2-risk-description-cause-event-effect`, `ilx-vague-or-duplicated-risks`).
- **keep-risk-scoring-simple**: new, MAY. It rests on a vendor guide and a training provider's opinion, with no study behind it (`atlassian-probability-times-impact`, `ilx-overly-complex-scoring`).
- **track-risks-in-the-team-tracker**: new, MAY. PRINCE2 lists a tool entry as one format among several, and the trackers offer custom types and fields rather than a risk record (`prince2-register-formats`, `github-custom-issue-types`, `github-custom-issue-fields`, `linear-health-at-risk`, `iso-record-and-report-outcomes`, `scrum-controls-risk-by-iteration`).

**Open questions.**

- **Review cadence:** which one the rule names. PRINCE2 ties formal review to stage ends and progress reviews, the NAO example is monthly, and the Kanban Guide allows continuous or fixed-interval review.
- **Response vocabulary:** which one the cookbook adopts. The candidates are ISO 31000's treatment options, PRINCE2's response types, PMBOK 8's responses (which include escalate), and the ROAM categories.
- **Opportunities:** whether positive risks are in scope.
- **Actionee:** whether the rule requires a separate actionee beside the owner.
- **Tracker mapping:** which one the cookbook recommends. The options are a custom Risk issue type with fields, a RAID log, or a project health flag.

**Limitations.**

- **Third-party copies:** ISO 31000 was read from a copy hosted by a university, and PRINCE2 2017 from a copy on a university mirror; neither came from its publisher.
- **PMBOK 8:** the core text is paywalled. It is covered only by PMI's errata and a secondary Substack summary.
- **Not fetched or not cited:**
  - ISO 21502 was not fetched.
  - The SAFe site, axelos.com and Jira Align's documentation could not be fetched, so ROAM is cited from the Open Practice Library.
  - LeSS was not cited.
- **No metric found:** no study measures how review cadence affects register outcomes, so no claim takes the Statistical bar.

## Best practices

- **Identify every risk:** identify all risks to the objectives, whether or not their sources are under the team's control. (claim: `iso-identify-risks-whatever-their-source`)
  > The organization should identify risks, whether or not their sources are under its control.
- **Evaluate each risk to decide on action:** compare each risk against the agreed criteria. The outcome is to do nothing further, treat it, analyse it further, keep existing controls, or reconsider objectives. This is the decision between acting now and watching. (claim: `iso-evaluation-decides-action`)
  > Risk evaluation involves comparing the results of the risk analysis with the established risk criteria to determine where additional action is required.
- **Treatment options:** avoid the risk, take it on for an opportunity, remove its source, change its likelihood or consequences, share it, or retain it by informed decision. (claim: `iso-treatment-options`)
  > Options for treating risk may involve one or more of the following: — avoiding the risk by deciding not to start or continue with the activity that gives rise to the risk; — taking or increasing the risk in order to pursue an opportunity; — removing the risk source; — changing the likelihood; — changing the consequences; — sharing the risk (e.g. through contracts, buying insurance); — retaining the risk by informed decision.
- **Choose a treatment by weighing cost:** weigh what a treatment gains against its cost, effort and disadvantages. (claim: `iso-select-treatment-by-cost-benefit`)
  > Selecting the most appropriate risk treatment option(s) involves balancing the potential benefits derived in relation to the achievement of the objectives against costs, effort or disadvantages of implementation.
- **Keep untreatable risks open:** a risk that no treatment adequately reduces stays recorded and under ongoing review. (claim: `iso-untreatable-risk-kept-under-review`)
  > If there are no treatment options available or if treatment options do not sufficiently modify the risk, the risk should be recorded and kept under ongoing review.
- **Plan the reviews:** monitoring and periodic review are planned, with responsibilities clearly defined. (claim: `iso-monitoring-planned-with-responsibilities`)
  > Ongoing monitoring and periodic review of the risk management process and its outcomes should be a planned part of the risk management process, with responsibilities clearly defined.
- **Record and report outcomes:** document and report the outcomes of risk management. (claim: `iso-record-and-report-outcomes`)
  > The risk management process and its outcomes should be documented and reported through appropriate mechanisms.
- **Name who acts, and when:** a treatment plan names who is accountable and responsible for it, and when its actions start and finish. (claim: `iso-treatment-plan-names-responsible-and-timing`)
  > those who are accountable and responsible for approving and implementing the plan;
- **Review regularly, because risks change:** the Orange Book has the recorded outcome of each risk evaluation reviewed and revised regularly. (claim: `orange-book-regularly-reviewed`)
  > It should be regularly reviewed and revised based on the dynamic nature and level of the risks faced.
- **Monitor continuously:** continuous monitoring shows how the risk profile is changing. (claim: `orange-book-continuous-monitoring`)
  > Ongoing and continuous monitoring should support understanding of whether and how the risk profile is changing
- **Make risk part of normal management:** consider risk regularly in the normal flow of management information. (claim: `orange-book-risk-in-normal-management-flow`)
  > Risk should be considered regularly as part of the normal flow of management information about the organisation’s activities
- **Escalate on agreed criteria:** escalate risks in good time against agreed criteria. (claim: `orange-book-timely-escalation`)
  > including the timely escalation of risks, as necessary, based on agreed criteria.
- **Prepare for a risk that happens:** have contingency and incident arrangements ready for when a risk crystallises, the point at which it is no longer a risk but an event. (claim: `orange-book-contingency-if-risks-crystallise`)
  > contingency, containment, crisis, incident and continuity management arrangements should be developed and communicated to support resilience and recovery if risks crystallise.
- **Management owns its risks:** management in the first line holds primary ownership of its risks. (claim: `orange-book-first-line-ownership`)
  > Under the ‘first line role’, management have primary ownership, responsibility and accountability for identifying, assessing and managing risks.
- **The register links risks to what they concern:** risk registers already hold each risk's owners and its links to the business processes it concerns. (claim: `orange-book-register-holds-owners-and-links`)
  > Existing risk and control information (including owners and links to business processes etc) should already have been captured in risk registers and other documents and this should be useful when planning assurance work

## Known solutions

**The PRINCE2 risk register** is the most fully specified register.

- **Who raises a risk, and when:** anyone may raise a risk, and it goes in the register as soon as it is identified. (claim: `prince2-capture-risks-when-identified`)
  > Any member of the project, corporate or programme management, the customer, or other stakeholder may raise an issue or risk. PRINCE2 recommends that risks are captured in the risk register as soon as they are identified.
- **Status and history:** the register keeps each risk's status and history. (claim: `prince2-register-records-status-and-history`)
  > A risk register provides a record of identified risks relating to the project, including their status and history.
- **Author:** each entry records its author, the person who raised it. (claim: `prince2-risk-author-field`)
  > Risk author The person who raised the risk
- **Status values:** an entry's status is active or closed. (claim: `prince2-risk-status-field`)
  > Risk status Typically described in terms of whether the risk is active or closed
- **Status shows action:** the register's quality criteria require the status to show whether action has been taken. (claim: `prince2-status-shows-action-taken`)
  > The status indicates whether action has been taken.
- **Identity and product:** each risk is uniquely identified and names the product it refers to. (claim: `prince2-risk-refers-to-product`)
  > Risks are uniquely identified, including information about which product they refer to.
- **Description:** describe a risk as its cause, the event, and the effect. (claim: `prince2-risk-description-cause-event-effect`)
  > Risk description Describes the risk in terms of the cause, event (threat or opportunity) and effect (in words of the impact)
- **Proximity:** record how soon the event is expected. (claim: `prince2-proximity-field`)
  > Proximity This would typically state how close to the present time the risk event is anticipated to happen (e.g. imminent, within the management stage, within the project, beyond the project).
- **One owner:** each risk has exactly one owner. (claim: `prince2-single-risk-owner`)
  > Risk owner The person responsible for managing the risk (there should be only one risk owner per risk)
- **Who the owner should be:** the owner is the person most able to manage the risk, and no one holds too many. (claim: `prince2-owner-and-actionee-agreed`)
  > The risk owner should be the person most capable of managing the risk. Allocating too many risks to any one individual should be avoided.
- **Actionee:** an actionee carries out the response and may or may not be the owner. (claim: `prince2-risk-actionee`)
  > Risk actionee The person(s) who will implement the action(s) described in the risk response. This may or may not be the same person as the risk owner.
- **Reduce acts now:** reducing a risk means acting now. (claim: `prince2-reduce-is-action-now`)
  > This option involves definite action now to change the probability and/or the impact of the risk.
- **Contingent plans wait:** a contingent plan is prepared now and acted on later. (claim: `prince2-contingent-plans-wait`)
  > This option involves preparing plans now, but not taking action now.
- **Acceptance has a limit:** do not accept a risk once its exposure is beyond tolerance. (claim: `prince2-accept-not-beyond-tolerance`)
  > This option would not be appropriate if the risk exposure exceeded the risk tolerance threshold for the organizational activity in question.
- **Escalate at progress reviews:** escalate when tolerances are threatened. (claim: `prince2-escalate-when-tolerance-threatened`)
  > escalate issues and risks (section 17.4.7) if tolerances are threatened
- **Review at progress reviews:** each progress review checks the register for new or revised risks. (claim: `prince2-review-register-at-progress-reviews`)
  > check the risk register for any new or revised risks and assess their impact on the business case, stage plan or project plan
- **Review timing is set up front:** the risk management approach sets when formal risk management happens, for example at stage ends. (claim: `prince2-risk-timing-set-in-approach`)
  > Timing of risk management activities States when formal risk management activities are to be undertaken (e.g. at the end of management stages)
- **Formats, including a RAID-style log:** the register can be a tool entry or part of an integrated register of risks, actions, decisions, assumptions, issues and lessons. (claim: `prince2-register-formats`)
  > a part of an integrated project register for all risks, actions, decisions, assumptions, issues, lessons, etc.
- **Issue versus risk:** an issue is an event that has happened, which is where a risk stops and issue-tracking takes over. (claim: `prince2-issue-is-event-that-happened`)
  > A relevant event that has happened, was not planned, and requires management action.

**PMBOK 8** has two points on responses.

- **Contingent responses wait for a trigger:** contingent responses run only when a trigger condition occurs. (claim: `pmbok8-contingent-responses-on-trigger`)
  > Contingent response strategies. These risk strategies are intentionally designed for implementation only if one or more specific trigger conditions occur.
- **Escalation is a response:** a secondary summary of PMBOK 8 lists escalation among the threat responses. (claim: `pmbok8-threat-responses-include-escalation`)
  > For threats: You can use mitigation, avoidance, transference, acceptance, or escalation.

**ROAM**, used in SAFe program planning, sorts risks into four categories and prefers a single owner.

- **Four categories:** resolved, owned, accepted and mitigated. (claim: `roam-four-categories`)
  > ROAM Boards are a simple visualization for categorizing project or program risks into four categories:
- **A single owner:** one owner keeps track of the work. (claim: `roam-single-owner`)
  > A single owner is preferred to limit the chance that no one keeps track of the work.

## Platform guidelines

The platforms for this topic are the method owners and the trackers. Apple, Android and Windows have no bearing on it.

- **Scrum: risk is controlled by iterating:** the Scrum Guide controls risk through iteration and short Sprints, and prescribes no risk register. (claim: `scrum-controls-risk-by-iteration`)
  > Scrum employs an iterative, incremental approach to optimize predictability and to control risk.
- **Scrum: impediments surface daily:** the Daily Scrum surfaces impediments every day. (claim: `scrum-daily-identifies-impediments`)
  > Daily Scrums improve communications, identify impediments, promote quick decision-making, and consequently eliminate the need for other meetings.
- **Kanban: no item ages unreviewed:** team members review active items regularly, either continuously or at set intervals, so work does not age unnecessarily. (claim: `kanban-review-active-items-age`)
  > A common practice is for Kanban system members to review the active items regularly. This review can occur continuously, at regular intervals, or through a combination of both.
- **Linear: risk is a project health flag:** Linear marks risk at project level through an update's health indicator and has no per-risk record. (claim: `linear-health-at-risk`)
  > Select a health indicator— On track, At risk, or Off track —to represent the current state of the Initiative or Project.
- **Linear: reminders go to one owner:** update reminders go only to the project lead or initiative owner. (claim: `linear-update-reminders-to-owner`)
  > Reminders are sent for active Initiatives and Projects with statuses in the In Progress category, and only to the Initiative owner or project lead.
- **Linear: stale status is visible:** projects that are overdue for an update are marked as such. (claim: `linear-overdue-updates-flagged`)
  > When project update reminders are enabled, in-progress projects that are overdue for updates will reflect this for easier monitoring.
- **GitHub: no built-in risk type:** GitHub ships no risk type, but an organisation can define its own issue types, up to 25. (claim: `github-custom-issue-types`)
  > The default types are task, bug, and feature.
- **GitHub: custom fields:** issue fields add structured metadata such as impact or priority, so a risk issue can carry them. (claim: `github-custom-issue-fields`)
  > Issue fields let you add structured metadata to issues across your repositories. Instead of relying on labels or free-text workarounds, you can create fields like priority, effort, impact, or any custom category your team needs.
- **Atlassian (Jira): register components:** a risk register has a knowledgeable owner for each risk, who keeps the entry current. (claim: `atlassian-risk-register-components`)
  > Risk ownership : Assign a knowledgeable owner responsible for the overall risk, including the response plan.
- **Atlassian (Jira): regular risk meetings:** review the register in project reviews and also in a separate, regular risk meeting. (claim: `atlassian-regular-risk-meeting`)
  > The project review meeting should include reviewing the risk register, but having a separate and regular risk register meeting is good practice.
- **Atlassian (Jira): scoring:** a risk's score is its probability multiplied by its impact. (claim: `atlassian-probability-times-impact`)
  > Finally, calculate the risk score by multiplying the probability by the impact.
- **Atlassian (Jira): RAID log:** a RAID log separates risks, which are hypothetical, from issues, which are already affecting the project and need immediate attention. (claim: `atlassian-raid-issues-need-immediate-attention`)
  > Unlike risks, issues require immediate attention because they are already impacting the project.

## The expert's view

- **Missing ownership:** practitioners name the lack of accountability, and so of ownership, as a reason risks go unmanaged. (claim: `nao-lack-of-ownership`)
  > Leaders and practitioners suggested that one of the reasons is the lack of accountability for risks, resulting in a lack of ownership to take actions.
- **Ownership of risks that span teams:** ownership must be clearest for complex risks that cross parts of the organisation or involve delivery partners. (claim: `nao-clarity-of-ownership-complex-risks`)
  > It is particularly important to have clarity of ownership for complex risks that involve different aspects of the organisation or other delivery partners.
- **Stale registers:** keep the register up to date and focused on the risks that matter most. (claim: `nao-registers-up-to-date`)
  > Risk registers are central to reporting and communicating risks in government – they need to be up to date and reflect the risks of most importance to the organisation.
- **Unclear escalation:** clear criteria tell people when a risk is above tolerance and needs immediate action. (claim: `nao-escalation-criteria-immediate-action`)
  > Having clear criteria for escalating risks improves transparency and makes it easier for individuals to know when to escalate risks that are above tolerance and require immediate action.
- **A cadence in use:** one government body updates its central register monthly after a review with each workstream lead. This is an example from one organisation, not a standard. (claim: `nao-monthly-review-example`)
  > The central risk register is updated monthly following risk reviews with each workstream lead where ongoing risks are discussed, and risks which exceed tolerance levels are flagged for escalation with senior leaders.
- **Owner versus actionee:** the owner is accountable for the risk being managed, and the actionee carries out the response. (claim: `ilx-owner-and-actionee`)
  > Owner and actionee: The owner is accountable for ensuring the risk is managed; the actionee is responsible for carrying out the agreed response
- **What status should show:** whether the response actions are complete, ongoing or pending, and whether the risk exposure has changed. (claim: `ilx-current-status`)
  > Current status: Shows whether the response actions are complete, ongoing, or pending, and whether the risk exposure has changed
- **Static records:** build reviews into stage boundaries, board meetings or team reviews. (claim: `ilx-static-records`)
  > Static records: Reviews should be built into stage boundaries, project board meetings, or team reviews
- **Nobody responsible:** each risk needs someone responsible for managing and escalating it. (claim: `ilx-lack-of-accountability`)
  > Lack of accountability: Each risk must have someone responsible for its management and escalation
- **Vague or duplicated entries:** make each risk specific and distinct. (claim: `ilx-vague-or-duplicated-risks`)
  > Vague or duplicated risks: Ambiguous entries make it hard to assess ownership or action, so, risks should be specific and distinct, not repeated in slightly different forms
- **Over-complex scoring:** keep scoring simple, or the register stops being kept up. (claim: `ilx-overly-complex-scoring`)
  > Overly complex scoring systems: If the scoring model requires excessive interpretation, it’s less likely to be maintained consistently, so keep it simple to encourage engagement
- **Unassigned responses:** a response that nobody is assigned to, or that has no resources, is not a response. (claim: `pmbok8-unassigned-response-is-a-wish`)
  > A response that exists in a document but never gets assigned or resourced is not a response. It is just a wish.
- **Issues logged as risks:** an issue has already happened, so it leaves the risk register for issue handling. (claim: `pmbok8-issue-already-happened`)
  > An issue is something that has already happened.
- **Monitoring that stops:** keep tracking existing risks, look for new ones, and check whether responses worked. (claim: `pmbok8-monitoring-never-stops`)
  > Monitoring never stops. You track existing risks and hunt for new ones.
