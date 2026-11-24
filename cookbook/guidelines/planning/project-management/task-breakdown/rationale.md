
*This section is informative.*

The method owners agree on the shape of a breakdown. The Scrum Guide has refinement break items into smaller, more precise ones with a description, order and size, and has the Developers who do the work size it and own their plan. The NASA WBS Handbook defines all of a project's work as a product-oriented structure and ties responsibility to it through a Responsibility Assignment Matrix. PRINCE2 hands work to a team as a work package. GitHub's sub-issues, Jira's links and Linear's estimates are the trackers' forms of the same practice.

Small tasks rest on heuristics, not studies. DORA and Spolsky independently give hours to a couple of days, with a week as too big; the Scrum Guide says decomposition into items of one day or less is often done; SAFe and INVEST bound stories at an iteration; the WBS 80-hour rule bounds a work package, which is coarser than a task. The sources agree on "small" but not on one number, so the size rules are SHOULDs, and the number the guideline settles on is an open question for the owner.

Wording rules come from Wake's SMART tasks, Linear's method and GTD's next action, and the done test from the Scrum Guide's Definition of Done, the Kanban Guide's definition of when an item is started and finished, and Atlassian's acceptance criteria. One owner per piece of work comes from Linear and GitLab's DRIs; Cohn and Scrum.org advise choosing the owner when the work begins. GitHub allows up to ten assignees, so single ownership is a team practice, not a tool constraint.

The vertical-slice, 100%-rule and GTD claims were each found by the second check to support their claim only in part, so the rules citing them hold at SHOULD. The 100% rule and the 80-hour rule come from Wikipedia's summary of the PMI standard, and PRINCE2 from the PRINCE2 wiki, because the primary texts could not be fetched.

Three rules are kept word for word from the projectteam's checks for the owner to decide: `task-has-assignee-and-priority`, `blocked-task-references-blocker` and `task-milestone-must-exist`. The research contradicts the first as a check on every todo (assignment is advised when work begins, Scrum orders the backlog rather than labelling priority, and Linear allows "No priority"), and finds no source stating the other two; trackers only offer existing milestones to pick. The owner's open questions are whether an assignee is required only on started work, whether priority is a field or backlog order, whether the milestone-exists check stays, which size limit to state, whether a blocker has to be a tracked item or may be an outside cause, and whether every task links to a milestone or only tasks in projects that use milestones.

Ordering thin end-to-end slices belongs to [adc.principle.steel-thread-first](cookbook:b224ef56-65f5-45fd-8842-767b20df6736), and writing the spec before code to [adc.guideline.planning.code-quality.spec-driven-development](cookbook:138eed2b-6b13-40ac-8c99-1f7860420b42).

