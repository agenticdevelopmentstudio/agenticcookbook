# Review: task-breakdown

## Findings

- `rules.md` **work-package-within-eighty-hours** and **work-package-within-one-reporting-period**, plus their echoes, in text that changed this round (source fidelity against `wbs-eighty-hour-heuristic`, and behavioral-requirements must-be-independently-testable: the bars must test what the rule says). The claim says WBS heuristics cap a work package "at about 80 hours". It is a rule of thumb with no study behind it (its trust basis). The split in this round dropped "about", so the rule and its echoes now state a hard 80-hour line that the claim does not give. The echoes in the review bar, review focus and how-to also dropped the rule's WBS scope ("In a work breakdown structure", "where a WBS is used"; the previous draft said "WBS work package"). As a result they apply the 80-hour and reporting-period limits, and the add-up check, to every work package. Every instance: `rules.md` work-package-within-eighty-hours ("no more than 80 hours of effort"); `a-build-must-establish.md` work-package-within-eighty-hours ("80 hours of effort or less"); `a-complete-review-must-establish.md` line 2 ("each work package's activities add up to its work", no WBS scope) and line 4 ("every work package is within 80 hours and one reporting period"); `what-a-reviewer-looks-for.md` line 2 ("a work package whose activities do not add up to its work", no WBS scope) and line 5 ("a work package over 80 hours or one reporting period"); `breaking-work-into-tasks.md` step 4 ("work packages within 80 hours and one reporting period"). Fix: restore "about 80 hours" in the rule and in every 80-hour echo. Restore the WBS scope ("in a work breakdown structure" or "WBS work package") on the review-bar, review-focus and how-to lines that name work packages.

## Checked

- Every claim cited in `rules.md` exists in research.json, and every claim that any verdict names is cited by at least one rule.
- None of the five claims refuted by the second check (`decompose-to-one-day-or-less`, `trackers-record-blocked-by-links`, `waiting-for-names-whom`, `split-vertically-not-by-layer`, `wbs-hundred-percent-rule`) is cited by a MUST rule. Every rule citing them is SHOULD.
- The three owner-listed rules keep their prior text word for word, each behind its listed lead-in, and each cites its `-prior` claim.
- The prior rule names (break-down-assign-and-prioritize-tasks, tasks-specific-and-actionable, link-tasks-to-milestones, identify-blocked-tasks-and-blockers and the owner-listed three) are kept. Each new split rule cites a claim that supports it: `task-states-its-outcome` from `task-specific-enough-to-understand`, `task-serves-its-story` from `smart-task-time-boxed`, `mark-blocked-tasks` from `trackers-record-blocked-by-links`, `jira-flag-with-reason` and `waiting-for-names-whom`, `remove-identified-blockers` from `kanban-unblock-blocked-work` and `daily-scrum-identifies-impediments`, and `work-has-a-responsible-owner` from `nasa-ram-assigns-responsibility` and `prince2-work-package-assigns-products`.
- Every rule has exactly one build-bar line, under its own name.
- The open questions in owner-list.md are left to the owner: the rationale lists all six, and no informative part settles them.
- The summary is 157 characters and describes the new text. Tags, platforms and related still fit.
- Rationale paragraph 4 now names all five refuted claims and the rules that cite each one, and that matches `rules.md`.

## Rulings

- R1.1: fixed — link-tasks-to-milestones is scoped to "where a project uses milestones". The build-bar, review-bar, review-focus, intro and how-to step 7 lines all carry the same scope.
- R1.2: fixed — blocker-links-the-blocking-item is scoped to a blocked task that "waits on a tracked item" and says nothing about outside causes. The build-bar, review-bar ("where that is a tracked item"), review-focus, handling-a-blocked-task step 3 and intro lines carry the same scope.
- R1.3: fixed — how-to step 6 now gives each todo an assignee and a priority, and step 8 no longer tells the reader to leave tasks unassigned. The worked example carries `Assignee:` and `Priority:` lines. The open question stays with the owner.
- R1.4: fixed — the out-of-scope clause is gone from the build bar, review bar, review focus and how-to step 1. Both blocked-marking lines now carry "where the tracker allows it".
- R1.5: fixed — each compound rule is split into one behaviour per rule, each with its own citation and build-bar line: break-down / work-has-a-responsible-owner; tasks-specific-and-actionable / task-states-its-outcome / task-serves-its-story / task-title-states-the-task; task-names-visible-action / task-has-done-test; identify / mark-blocked-tasks / remove-identified-blockers; work-package-within-eighty-hours / work-package-within-one-reporting-period. The ordering clause is dropped, because backlog-is-kept-ordered covers it.
- R1.6: fixed — split-large-estimates now reads "a week or more", "nor too detailed" is gone, and the title rule no longer says "short".
- R1.7: fixed — rationale paragraph 4 names all five refuted claims and the rules that cite each one.

## Lint

/lint-artifact on `cookbook/guidelines/planning/project-management/task-breakdown` (cookr run as instructed): Pass 18, Warn 0, Fail 0, RESULT: CLEAN. `cookr validate` passed. It listed the three owner-decides items (task-has-assignee-and-priority, task-milestone-must-exist, blocked-task-references-blocker), which are open owner decisions and not lint failures.

lint: clean

verdict: fail
