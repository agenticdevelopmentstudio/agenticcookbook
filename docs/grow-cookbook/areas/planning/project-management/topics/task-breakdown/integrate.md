# Integrate: task-breakdown

## For the owner

Rules standing as they were until you decide each (`cookr validate` owner-decides):

- rule 'task-has-assignee-and-priority' cites 'task-has-assignee-and-priority-prior', which the research rules contradicted
- rule 'task-milestone-must-exist' cites 'task-milestone-must-exist-prior', which the research rules unsupported
- rule 'blocked-task-references-blocker' cites 'blocked-task-references-blocker-prior', which the research rules unsupported

Open questions from the owner list:

- Whether 'every todo has an assignee' should become 'every started todo has exactly one assignee', leaving unstarted todos unassigned as Cohn and Scrum.org advise, or stay a check on every todo as a projectteam convention; the owner decides.
- Whether 'priority' is kept as a per-task field (as Linear and Jira offer) or replaced by backlog order (as the Scrum Guide has it), and whether 'no priority' is an allowed value.
- Whether 'no todo is assigned to a nonexistent milestone' is kept as a house referential-integrity check; no external source states it, though trackers only offer existing milestones to pick.
- Which task-size limit the guideline states: one day or less (Scrum Guide), hours to a couple of days with a week as too big (DORA), 2 to 16 hours (Spolsky), or 80 hours (WBS heuristic); the sources agree on 'small' but not on one number.
- Whether a blocker must name a tracked item (a blocked-by link) or may name an outside cause in text (a vendor, a missing decision), and whether its start date is required.
- Whether every task must link to a milestone, or only tasks in a project that uses milestones; the sources describe milestones as optional grouping.

- from the phase 3 code review (claude-code-review/f4): `task-has-assignee-and-priority` (MUST) requires an assignee and a priority on every todo, while `started-task-has-one-owner` assigns an owner only once work begins and `backlog-is-kept-ordered` allows order instead of a priority field; the rule also uses "todo", which the guideline never defines beside "task". The review suggests limiting the MUST to started work and allowing backlog order as the priority, or lowering it to SHOULD.
- from the phase 3 code review (claude-code-review/f8): the name `break-down-assign-and-prioritize-tasks` promises assigning and prioritising, but the rule only breaks work down. It is a prior rule, whose name the grow-cookbook procedure keeps fixed, so the rename is the owner's; the review suggests renaming it to match its text. (Its text no longer names another rule; that part was fixed.)

## Lossless

New topic, no base text (`cookr roles lossless`: not in the base commit).

## Validate

`cookr validate` passed; its owner-decides rows are listed under For the owner. Bumped 1.0.0 → 1.0.1; /add-artifact approved it (no lint failures; warning: the Task wording and Blocked tasks subsections hold 8 rules each).

integrated: 2026-11-24
