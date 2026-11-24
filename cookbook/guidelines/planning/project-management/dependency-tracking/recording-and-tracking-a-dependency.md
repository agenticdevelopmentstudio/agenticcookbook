
This section is informative: it shows one way to keep the rules, not a required method.

1. In planning, ask the other teams, stakeholders and partners what the work waits on; they know of hidden dependencies. SAFe's PI Planning does this for a whole release train, and its planning board shows feature delivery dates against their dependencies. Capture the dependencies other projects raise on the team as well.
2. Write each dependency as a statement, in the APM form: "We are dependent on X to deliver Y on date Z in order for us to deliver AA". Agree the date with X, including whether X has the resources to meet it.
3. Record the dependency in one place the team already reads: a RAID log, which keeps risks, assumptions, issues and dependencies in one list, or the tracker's blocked-by and blocking links. APM's guidance also documents the dependency's source and specification, and has the two sides sign off an agreement of commitments and responsibility.
4. Give it an owner, and send it to the owner of the other project or team so it is confirmed there and appears in their dependency log too.
5. Set its status from the team's preset list. A tracker's single-select field holds such a list, and a date field holds the need-by date. GitHub recommends automating updates so the project stays current.
6. Review the dependencies at the meetings the team already holds: status meetings, steering reviews, sprint planning, the Daily Scrum. The sources name no cadence.
7. When one is blocked, flag it where the team will see it, note why, and count the days it stays blocked. When it cannot be cleared locally, take it to the forum the method names, or straight to the other team. Keep the note once the block is cleared.

How the tools compare:

- **GitHub Issues** links issues as blocked by and blocking, and shows a Blocked icon on project boards and the Issues page.
- **Linear** shows blockers with an orange flag and blocked work with a red flag in the issue sidebar, and moves the relation to Related once the blocker is resolved. A project's health icon shows a missed update, and turns grey when the project stays overdue.
- **Jira** marks a blocked item with the Flagged field, whose one value is Impediment, visible to everyone in the space, with an optional comment. Jira Plans treats work-item links as Blocks dependencies, draws an off-track dependency in red on its dependencies view and program board, calculating off-track from the schedule, and can show only the off-track ones.
- **A RAID log** records an owner, a due date and a status for each entry by hand, but links nothing.
- No tracker gives a dependency its own owner, need-by date or status; these come from the item's or the project's fields. Linear's and GitHub's health values (On track, At risk, Off track) apply to projects, not to single dependencies.

