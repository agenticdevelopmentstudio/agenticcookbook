# planning/project-management: area plan

The project-management practices a delivery team keeps its plan in: the
risks it watches, the decisions it records, the dependencies it waits on, the
issues it triages, the milestones it schedules and the tasks it breaks the
work into. projectteam's six `project/` specialities (concerns, decisions,
dependencies, issues, schedule, todos) are grounded in this area by owner
ruling (2026-11-21: "projectteam is grounded in the cookbook: a researched
project-management area"). Every topic is new: the cookbook has no
project-management area. projectteam's speciality text, its `.dev-team-project/`
paths and its artifact formats are inputs to check against research, never a
source of rules, and the team-specific parts stay in projectteam.

## Topics

| Topic | Path | Survivor | Copies | Specialities | Research type |
|---|---|---|---|---|---|
| risk-tracking | `cookbook/guidelines/planning/project-management/risk-tracking` (new; input: projectteam `specialities/project/concerns.md`) | itself (new) | none | none | How-to / troubleshooting (intent Do; domain project risk management; method standards bodies and practitioner sources) |
| decision-records | `cookbook/guidelines/planning/project-management/decision-records` (new; input: projectteam `specialities/project/decisions.md`) | itself (new) | none | none | How-to / troubleshooting (intent Do; domain software decision documentation; method practitioner sources and published templates) |
| dependency-tracking | `cookbook/guidelines/planning/project-management/dependency-tracking` (new; input: projectteam `specialities/project/dependencies.md`) | itself (new) | none | none | How-to / troubleshooting (intent Do; domain cross-team delivery dependencies; method standards bodies and practitioner sources) |
| issue-tracking | `cookbook/guidelines/planning/project-management/issue-tracking` (new; input: projectteam `specialities/project/issues.md`) | itself (new) | none | none | How-to / troubleshooting (intent Do; domain issue triage and resolution; method standards bodies, tool documentation and practitioner sources) |
| milestone-scheduling | `cookbook/guidelines/planning/project-management/milestone-scheduling` (new; input: projectteam `specialities/project/schedule.md`) | itself (new) | none | none | How-to / troubleshooting (intent Do; domain project scheduling; method standards bodies and practitioner sources) |
| task-breakdown | `cookbook/guidelines/planning/project-management/task-breakdown` (new; input: projectteam `specialities/project/todos.md`) | itself (new) | none | none | How-to / troubleshooting (intent Do; domain work decomposition and task assignment; method standards bodies and practitioner sources) |
| project-record-linking | `cookbook/guidelines/planning/project-management/project-record-linking` (new, by owner ruling 2026-11-24; input: the cross-references each of projectteam's six `specialities/project/` files requires) | itself (new) | none | none | How-to / troubleshooting (intent Do; domain traceability between project records; method standards bodies, tool documentation and practitioner sources) |

No topic has a copy, so nothing folds in this area. Each topic was added to
the worklist as `new: true`, `kind: "new"`, `devteam: "authored"`, in the
`planning/project-management` batch; `project-record-linking` joined it on
the owner's ruling of 2026-11-24 that cross-artifact linking is its own topic.

The topic names are the practices, not projectteam's file names: a
"concern" is a risk or an open worry, so the topic is `risk-tracking`; a
"todo" is a task, so the topic is `task-breakdown`; the "schedule" speciality
is milestones and their sequencing, so the topic is `milestone-scheduling`.

## Gaps

The area has no speciality: `run_gaps.py` reports `why_empty` "area has no
speciality", and `reference.json` is `[]`. No speciality text is measured, no
new topic claims a speciality, and the worklist's `building` list is empty, so
"Building specialities not yet measured" has nothing to list. The gaps of this
area are the **Missing subjects** below, judged by hand against what
projectteam's six specialities ask a worker to do and verify.

No R9 measure is owed or possible: every topic is `kind: new` and the area has
no reference. Candidate survivors were chosen from a whole-cookbook search
(G87): `grep -ril` over `cookbook/` for risk register, RAID log, risk owner,
decision record, ADR, architecture decision, milestone, critical path, work
breakdown, WBS, issue tracker, issue tracking, triage and severity, plus
every folder under `cookbook/guidelines/planning/`. The hits weighed:
`planning/data/datastore-selection` (ADR), `planning/data/cqrs-and-event-sourcing`
and `planning/networking/api-style-selection` (decision wording),
`shipping/incident-response` (severity tiers, triage),
`reviewing/security/vulnerability-prioritization` (triage),
`planning/code-quality/spec-driven-development` (planning before tasks),
`planning/code-quality/system-dependencies` and
`implementing/security/dependency-security` (the word "dependency"),
`implementing/code-quality/use-roadmaplib` (roadmap operations) and
`principles/steel-thread-first` (slicing). No hit names a risk register, a
milestone schedule, a work breakdown or an issue tracker. The ones that touch
a proposed topic are listed under **Overlaps**.

## Missing subjects

1. **Risk review cadence**: projectteam requires that no concern stay open indefinitely without review, and no artifact says how often an open risk is reviewed, by whom, or when it is closed.
2. **Risk response triage**: projectteam asks a worker to tell a concern needing immediate action from one to monitor; no artifact names the response options (avoid, mitigate, transfer, accept, monitor) or how one is chosen.
3. **Decision supersession**: projectteam requires that a decision not contradict an earlier one without acknowledging it; no artifact says how a decision record is superseded, amended or deprecated.
4. **Blocked dependency flagging**: projectteam flags dependencies that are at risk or blocked and affect milestones; no artifact says how a dependency's status is kept, who owns it, or when it is escalated.
5. **Issue severity levels**: projectteam assigns each issue a severity; no artifact outside incident response defines severity levels for project issues, or separates severity from priority.
6. **Issue escalation path**: projectteam escalates critical issues; no artifact says when and to whom a project issue is escalated.
7. **Issue resolution traceability**: projectteam requires a resolved issue to reference its resolution; no artifact says what a closed issue records.
8. **Milestone cycle detection**: projectteam's dependency chains between milestones must hold no cycles; no artifact says how a milestone plan is checked for cycles or its critical path found.
9. **Blocked milestone accounting**: projectteam allows no milestone to be blocked without an issue or concern explaining it; no artifact ties a milestone's status to the records that explain it.
10. **Actionable task wording**: projectteam requires each task to be specific and actionable, with an owner and a priority; no artifact says what makes a task actionable or how large it may be.
11. **Task blocker naming**: projectteam requires a blocked task to name its blocker; no artifact says how a blocked task records what it waits on.
12. **Cross-artifact linking**: projectteam links concerns, decisions, issues and tasks to milestones and findings; no artifact says how project records reference each other so each is findable from the others.

## Overlaps

`copy_check.py` finds no copy to fold and no move in this area. The overlaps
below are existing topics whose rules touch part of a proposed topic, from the
whole-cookbook search (see **Gaps**). None holds the ground of a proposed
topic, so every topic stays `new`; each cites the artifact it touches rather
than restating it.

- **decision-records** and `cookbook/guidelines/planning/data/datastore-selection`: "whether the chosen store and its one-line justification are recorded in an ADR or the plan" (`must-record-the-store-and-its-justification`). The survivor requires one decision to be recorded; decision-records rules how any decision record is written, found and superseded. Partial overlap: kept `new`, and datastore-selection's rule is the kind of record decision-records describes.
- **decision-records** and `cookbook/guidelines/planning/networking/api-style-selection` and `cookbook/guidelines/planning/data/cqrs-and-event-sourcing`: both rule one technical choice and mention recording it; neither rules the record. Checked; no shared rule.
- **issue-tracking** and `cookbook/guidelines/shipping/incident-response`: "Run production incidents with defined command roles and severity tiers". The survivor's severity tiers are for production incidents; issue-tracking rules project issues found in planning and delivery. Partial overlap on severity: kept `new`, citing incident-response's tiers where an issue is a production incident.
- **issue-tracking** and `cookbook/guidelines/reviewing/security/vulnerability-prioritization`: "Triage CVEs by exploitability ... not raw CVSS". Triage of security findings only. Checked; issue-tracking cites it for security issues.
- **task-breakdown** and `cookbook/guidelines/planning/code-quality/spec-driven-development`: "write a self-contained spec before code, separating planning from execution and ending with a verification step". The survivor rules an agent's spec before code; task-breakdown rules how the planned work is split into owned, actionable tasks. Partial overlap: kept `new`, citing spec-driven-development.
- **task-breakdown** and `cookbook/principles/steel-thread-first`: "Build the thinnest end-to-end slice through every boundary before breadth". A principle for ordering slices; task-breakdown cites it for slicing and does not restate it.
- **dependency-tracking** and `cookbook/guidelines/planning/code-quality/system-dependencies` and `cookbook/guidelines/implementing/security/dependency-security`: both rule software dependencies (libraries, OS frameworks), not delivery dependencies between teams, tasks and milestones. No shared ground beyond the word; listed so the owner sees it was checked.
- **milestone-scheduling** and `cookbook/guidelines/implementing/code-quality/use-roadmaplib`: rules a library's use for roadmap files, not how milestones are scheduled. Checked; no overlap.
- **risk-tracking**: no artifact rules project risk; the "risk" hits (backup-and-recovery, feature-flags, authorization and others) rule technical risks of one practice. No overlap.

copy_check.py planning/project-management: copies 0; identical 0; moved 0; unreadable 0; twin_differs 0; differ_uncarried none; result caed47f1ecdb

## Proposed topics

| Topic | Action | Artifact | Why |
|---|---|---|---|
| risk-tracking | new | `cookbook/guidelines/planning/project-management/risk-tracking` | No artifact rules a project risk register, its review or its responses; grounds projectteam's concerns speciality. |
| decision-records | new | `cookbook/guidelines/planning/project-management/decision-records` | No artifact rules how a decision is recorded, found or superseded; `datastore-selection` only requires one record. |
| dependency-tracking | new | `cookbook/guidelines/planning/project-management/dependency-tracking` | No artifact rules delivery dependencies between teams, tasks and milestones; the "dependency" guidelines rule software libraries. |
| issue-tracking | new | `cookbook/guidelines/planning/project-management/issue-tracking` | No artifact rules project issue triage, severity and resolution; `incident-response` covers production incidents only. |
| milestone-scheduling | new | `cookbook/guidelines/planning/project-management/milestone-scheduling` | No artifact rules milestones, their sequencing or a critical path. |
| task-breakdown | new | `cookbook/guidelines/planning/project-management/task-breakdown` | No artifact rules how work is split into owned, actionable tasks; `spec-driven-development` stops at the spec. |
| project-record-linking | new | `cookbook/guidelines/planning/project-management/project-record-linking` | No artifact rules how risks, decisions, dependencies, issues, milestones and tasks reference each other; its own topic by owner ruling (2026-11-24). Last in order: it cites the six record topics. |

## Research questions

Every topic's question 3 (*Platform guidelines*) means the method owners and
standards bodies the topic touches (PMI's PMBOK Guide, ISO 21502, ISO 31000,
AXELOS PRINCE2, the Scrum Guide, the Kanban Guide), and the published guidance
of the issue trackers teams use (GitHub Issues and Projects, Jira, Linear).

### risk-tracking (new)

1. Best practice: how should a delivery team identify, record and monitor project risks and open concerns: a risk register's fields (description, likelihood, impact, owner, status, raiser), its review, and when a risk becomes an issue?
2. Known solutions: how do RAID logs, risk registers, probability-impact matrices and the risk features of GitHub Projects, Jira and Linear compare for a small software team, and which fields does each keep?
3. Platform guidelines: what do ISO 31000, the PMBOK Guide's risk performance domain and PRINCE2's risk theme say about recording, owning, reviewing and closing a risk?
4. The expert's view: what do delivery leads and risk practitioners say teams get wrong with risk registers (stale entries, no owner, risks never closed, issues logged as risks), and what to do instead?
5. **Risk review cadence**: find how often standards and practitioners review open risks, who reviews them and what closes one, and state the review rule a register follows so no risk stays open without review.
6. **Risk response triage**: find the response options standards name (avoid, mitigate, transfer, accept, escalate, monitor) and how one is chosen, and state how a worker decides that a risk needs action now or is monitored.

### decision-records (new)

1. Best practice: how should a team record a decision: its context, the alternatives weighed, the rationale, who decided and when, and where the record lives so it can be found?
2. Known solutions: how do Michael Nygard's ADR, MADR, Y-statements, RFC processes and decision logs in issue trackers compare, and what tools (adr-tools, log4brains) keep them?
3. Platform guidelines: what do the published ADR guidance of AWS, Microsoft (Azure Well-Architected), Google Cloud and the UK Government Digital Service say about recording and governing decisions?
4. The expert's view: what do architects and practitioners say teams get wrong with decision records (no alternatives, written after the fact, never read, never superseded), and what to do instead?
5. **Decision supersession**: find how ADR practice marks a decision superseded, amended or deprecated, and state how a new decision that contradicts an earlier one acknowledges and links it.

### dependency-tracking (new)

1. Best practice: how should a delivery team map and track its dependencies on other teams, vendors, tasks and decisions: internal versus external, each with a type, an owner, a status and a need-by date?
2. Known solutions: how do dependency boards, SAFe's program board, RAID logs and the dependency links of Jira, Linear and GitHub Projects compare for tracking delivery dependencies?
3. Platform guidelines: what do the PMBOK Guide's schedule and stakeholder guidance, PRINCE2 and the scaled-agile frameworks (SAFe, LeSS) say about recording and managing dependencies between teams?
4. The expert's view: what do delivery leads say teams get wrong with dependencies (found late, no owner on the other side, status never updated), and what to do instead?
5. **Blocked dependency flagging**: find how teams mark a dependency at risk or blocked and escalate it before it delays a milestone, and state the status values a dependency carries and when a blocked one is escalated.

### issue-tracking (new)

1. Best practice: how should a team identify, triage and track project issues to resolution: what an issue records, who triages it, and how it links to the findings that raised it?
2. Known solutions: how do the triage workflows and fields of GitHub Issues, Jira and Linear compare (labels, severity, priority, states), and how does issue triage differ from incident and vulnerability triage?
3. Platform guidelines: what do the PMBOK Guide's issue log, ITIL 4's problem management and the issue-tracker vendors' own triage guides say about severity, priority and resolution?
4. The expert's view: what do triage practitioners say teams get wrong with issue trackers (everything critical, severity confused with priority, issues closed with no resolution), and what to do instead?
5. **Issue severity levels**: find the severity scales standards and trackers use and how severity differs from priority, and state the severity levels a project issue carries and what each means.
6. **Issue escalation path**: find when and to whom practitioners escalate an issue, and state the escalation rule for a critical issue.
7. **Issue resolution traceability**: find what a closed issue records in tracker practice (the resolution, the change or decision that resolved it), and state what a resolved issue references.

### milestone-scheduling (new)

1. Best practice: how should a team set milestones, sequence the work between them, set target dates and keep the schedule current?
2. Known solutions: how do milestone plans, roadmaps, Gantt charts, critical path method and rolling-wave planning compare for a software team, and which do GitHub milestones, Jira and Linear cycles support?
3. Platform guidelines: what do the PMBOK Guide's schedule guidance, ISO 21502 and the Scrum and Kanban Guides say about milestones, dates and forecasting?
4. The expert's view: what do delivery leads say teams get wrong with schedules (dates without dependencies, no buffer, milestones blocked with no reason recorded), and what to do instead?
5. **Milestone cycle detection**: find how scheduling practice and tools detect cycles in a dependency chain and find the critical path, and state how a milestone plan is checked so its chains hold no cycle.
6. **Blocked milestone accounting**: find how practitioners tie a milestone's status to the risks and issues that explain it, and state the rule that every blocked or at-risk milestone names the issue or risk that blocks it.

### task-breakdown (new)

1. Best practice: how should work be broken into tasks: the size of a task, one owner, a priority, acceptance criteria, and the link from each task to its milestone?
2. Known solutions: how do work breakdown structures, user story splitting, INVEST, task checklists and the task fields of GitHub Issues, Jira and Linear compare?
3. Platform guidelines: what do the PMBOK Guide's WBS guidance, the Scrum Guide's sprint backlog and the Kanban Guide's work items say about breaking down and assigning work?
4. The expert's view: what do practitioners say teams get wrong with task lists (vague tasks, tasks too large, no owner, blocked tasks that never say why), and what to do instead?
5. **Actionable task wording**: find what practitioners require of an actionable task (a verb and an object, a done condition, a size limit), and state what a task's text says and how large a task may be.
6. **Task blocker naming**: find how trackers and practitioners record what a blocked task waits on, and state how a blocked task names its blocker.

### project-record-linking (new)

1. Best practice: how should a delivery team link its project records (risks, decisions, dependencies, issues, milestones, tasks) to each other and to the findings that raised them: which record carries each link, which links are two-way, and how a record is identified so a link stays valid when the record moves or closes?
2. Known solutions: how do RAID logs, traceability matrices, ADR links, and the linked-issue, sub-issue, relation and dependency fields of GitHub Issues and Projects, Jira and Linear compare for keeping links between records findable?
3. Platform guidelines: what do the PMBOK Guide, ISO 21502, PRINCE2's registers and logs, and the trackers' own documentation say about cross-referencing risks, issues, decisions and the plan?
4. The expert's view: what do delivery leads and traceability practitioners say teams get wrong with links between records (one-way links, links to closed or deleted records, records findable from none of the others), and what to do instead?
5. **Cross-artifact linking**: find how practitioners and trackers keep each project record findable from the records it touches, and state which links each record type carries (a blocked milestone to its issue or risk, a task to its milestone and blocker, a superseding decision to the one it supersedes, a resolved issue to its resolution), how a link names its target, and how links are checked for dangling targets. The record-specific fields stay at their hosts (**Decision supersession**, **Issue resolution traceability**, **Blocked milestone accounting**, **Task blocker naming**); this topic rules the linking convention they share.

## Owner questions

1. Research bar for every topic (risk-tracking, decision-records, dependency-tracking, issue-tracking, milestone-scheduling, task-breakdown): no escalation is proposed. Each topic stays at the *How-to / troubleshooting* bar; any metric claim (a review cadence or a task size backed by a study) takes the *Statistical* bar. Answered 2026-11-24: the owner approved the plan as it stands, research bars as proposed, no escalation.
2. **Cross-artifact linking**: answered 2026-11-24 by owner ruling: it is its own `new` topic in this area, `project-record-linking`, which hosts it (**Research questions**, *project-record-linking*, question 5). It no longer sits under `### No host`.
3. The area path: the topics go under a new `cookbook/guidelines/planning/project-management/`, beside `planning/code-quality` and the other planning areas. Answered 2026-11-24: the owner approved the path.
4. Research bar for project-record-linking: no escalation; *How-to / troubleshooting*, any metric claim taking the *Statistical* bar. Answered 2026-11-24: set by the owner's ruling and approval, no escalation.

## Step-4 re-check

### On 1.4.48

Short path: the area has no speciality (`why_empty` "area has no
speciality"), so re-run checklist items 4 to 6 are skipped and item 5 owes no
R9.

First check (`stage_status.py --first-check`, `A/first-check.txt`), run on the
saved reports after the plan was first written:

- unmeasured.py planning/project-management: check unchanged; changes 0; new_keys 0; stale_reference 0; result a7c23a7e7fca
- run_gaps.py --check planning/project-management: changed, exit 1; would_clear 0; failed 0; unplaced 0; stale_reference 0; r9_stale 0; verdict_changes 0; counted_rows 0; counted_rows_differ 0; changes 1; gap_total_rows 0; measured_total 0; missing_subjects 12; not_compared 0; counted_with_prior_verdict 0; counted_never_judged 0; stated 0 -> measured 0 (+0: counted_with_prior_verdict 0, counted_never_judged 0, verdict_changes 0); hints on (flag); report d9913d428d0d260eeb7378fa0ce0b8df15d42ab1
- stage_status.py planning/project-management: next plan; plan_sections 0; stale_reference 0; r9_stale 0; stale_copy_check 0; host_check 1; cite_moved 0; stale_verdicts 0; result 603240ea750f

First check's `new_keys` 0, `changes` 1, `cleared` 0. The one change is this
plan's own: `missing_subjects` went from 0 to 12 (the **Missing subjects**
above). `host_check` held the area at plan on one tie: the subject then named "Task blocker recording" shared "record" with decision-records and "task" with task-breakdown. It was renamed **Task blocker naming**, which shares a word with task-breakdown only. Step 1.3 was re-run (`run_gaps.py --hints`), which saved the report again.

Hand-off check, after the plan's final edit:

- unmeasured.py planning/project-management: check unchanged; changes 0; new_keys 0; stale_reference 0; result a7c23a7e7fca
- run_gaps.py --check planning/project-management: unchanged, exit 0; would_clear 0; failed 0; unplaced 0; stale_reference 0; r9_stale 0; verdict_changes 0; counted_rows 0; counted_rows_differ 0; changes 0; gap_total_rows 0; measured_total 0; missing_subjects 12; not_compared 0; counted_with_prior_verdict 0; counted_never_judged 0; stated 0 -> measured 0 (+0: counted_with_prior_verdict 0, counted_never_judged 0, verdict_changes 0); hints on (flag); report 3549796163980e5e4fa6770f5e6e2996557e90b7
- run_gaps.py --check-homes planning/project-management: `check_homes` [], exit 0
- run_gaps.py --check-verdicts planning/project-management: `check_verdicts` [], exit 0
- copy_check.py planning/project-management: copies 0; identical 0; moved 0; unreadable 0; twin_differs 0; differ_uncarried none; result caed47f1ecdb
- stage_status.py planning/project-management: next approve; plan_sections 0; stale_reference 0; r9_stale 0; stale_copy_check 0; host_check 0; cite_moved 0; stale_verdicts 0; result 0785eeb62840

This plan cites no other area plan, so no plan hash is recorded.

### On 1.4.48, after the owner's ruling (2026-11-24)

The owner ruled that cross-artifact linking is its own topic,
`project-record-linking`, and approved the plan as it stands (the path,
research bars as proposed, no escalation). The plan added the topic to
**Topics**, **Proposed topics** (last, since it cites the six record topics)
and **Research questions**, moved **Cross-artifact linking** from `### No host`
to its question 5 (it shares `linking` with the topic's folder name), and
marked every Owner question answered. The record-specific links stay at their
hosts (**Decision supersession**, **Issue resolution traceability**,
**Blocked milestone accounting**, **Task blocker naming**): each shares a
specific word only with its own topic, so moving one would trip `host_check`.
The worklist batch gained `project-record-linking` (`new: true`, `kind: "new"`,
`devteam: "authored"`).

The first `unmeasured.py --check` after the edit changed (exit 1, `changes` 1):
`new_topics` added `guidelines/planning/project-management/project-record-linking`,
the worklist row above. `A/unmeasured.json` was rewritten with
`write_on_success.py`. Hand-off check, after the plan's final edit:

- unmeasured.py planning/project-management: check unchanged; changes 0; new_keys 0; stale_reference 0; result a7c23a7e7fca
- run_gaps.py --check planning/project-management: unchanged, exit 0; would_clear 0; failed 0; unplaced 0; stale_reference 0; r9_stale 0; verdict_changes 0; counted_rows 0; counted_rows_differ 0; changes 0; gap_total_rows 0; measured_total 0; missing_subjects 12; not_compared 0; counted_with_prior_verdict 0; counted_never_judged 0; stated 0 -> measured 0 (+0: counted_with_prior_verdict 0, counted_never_judged 0, verdict_changes 0); hints on (flag); report 3549796163980e5e4fa6770f5e6e2996557e90b7
- run_gaps.py --check-homes planning/project-management: `check_homes` [], exit 0
- run_gaps.py --check-verdicts planning/project-management: `check_verdicts` [], exit 0
- copy_check.py planning/project-management: copies 0; identical 0; moved 0; unreadable 0; twin_differs 0; differ_uncarried none; result caed47f1ecdb
- stage_status.py planning/project-management: next approve; plan_sections 0; stale_reference 0; r9_stale 0; stale_copy_check 0; host_check 0; cite_moved 0; stale_verdicts 0; result 0785eeb62840

This plan cites no other area plan, so no plan hash is recorded.
