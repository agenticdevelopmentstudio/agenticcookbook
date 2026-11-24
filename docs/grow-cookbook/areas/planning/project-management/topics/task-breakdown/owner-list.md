# Owner list: task-breakdown

For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **task-has-assignee-and-priority** — verdict `contradicted` (claims: task-has-assignee-and-priority-prior, assign-when-work-begins, developers-own-the-sprint-backlog, backlog-is-ordered, linear-priority-levels). Prior text, kept word for word: "Every todo has an assignee and priority" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied. lead-in: "Each todo MUST pass this check:" (the one change the reviewer accepts)
  - against: Experts advise against assigning every task up front at planning: each person claims their first task and then chooses the next as work progresses, so assignment happens close to when work begins.
  - against: In Scrum the Sprint Backlog, including its breakdown into work, is a plan by and for the Developers, who are accountable for creating it.
  - against: The Scrum Guide orders the Product Backlog, with the Product Owner accountable for that order, rather than assigning each item a priority label.
  - against: Linear offers a fixed five-value priority, including 'No priority', so a tracker's priority field may be left unset.
- **blocked-task-references-blocker** — verdict `unsupported` (claims: blocked-task-references-blocker-prior, trackers-record-blocked-by-links, jira-flag-with-reason, blocker-note-states-reason-and-dates). Prior text, kept word for word: "blocked todos reference a specific blocker" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied. lead-in: "A blocked todo MUST pass this check:" (the one change the reviewer accepts)
  - against: GitHub, Jira and Linear each record a blocker as a 'blocked by' / 'blocks' link from the blocked item to the item it waits on, and mark blocked items visibly.
  - against: Jira marks a blocked item with a flag (stored as 'Impediment') and lets the user add a comment giving the reason when flagging or unflagging it.
  - against: Practitioners record each blocker on the blocked item with a brief reason that names its cause, and its start and resolved dates or days blocked, then keep resolved blockers to cluster them for improvement.
- **task-milestone-must-exist** — verdict `unsupported` (claims: task-milestone-must-exist-prior, github-milestones-group-issues). Prior text, kept word for word: "no todo is assigned to a nonexistent milestone" It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied. lead-in: "A todo's milestone MUST pass this check:" (the one change the reviewer accepts)
  - against: GitHub milestones group issues to track their progress; an issue is associated with a milestone chosen from the repository's existing milestones.

## Open questions

- Whether 'every todo has an assignee' should become 'every started todo has exactly one assignee', leaving unstarted todos unassigned as Cohn and Scrum.org advise, or stay a check on every todo as a projectteam convention; the owner decides.
- Whether 'priority' is kept as a per-task field (as Linear and Jira offer) or replaced by backlog order (as the Scrum Guide has it), and whether 'no priority' is an allowed value.
- Whether 'no todo is assigned to a nonexistent milestone' is kept as a house referential-integrity check; no external source states it, though trackers only offer existing milestones to pick.
- Which task-size limit the guideline states: one day or less (Scrum Guide), hours to a couple of days with a week as too big (DORA), 2 to 16 hours (Spolsky), or 80 hours (WBS heuristic); the sources agree on 'small' but not on one number.
- Whether a blocker must name a tracked item (a blocked-by link) or may name an outside cause in text (a vendor, a missing decision), and whether its start date is required.
- Whether every task must link to a milestone, or only tasks in a project that uses milestones; the sources describe milestones as optional grouping.
