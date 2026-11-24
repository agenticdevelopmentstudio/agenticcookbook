
# Project Record Linking

Give every project record an identifier that is unique, never reused and free of anything that changes, such as status, and make every link name its target by that identifier. Give each link a type that reads correctly from both ends, show a two-way relationship on both records, and close or supersede a record instead of deleting it, linking a superseding record and the one it replaces to each other. Check the links for targets that do not exist.

This guideline covers the linking convention shared by a delivery team's project records: risks, decisions, dependencies, issues, milestones and tasks. It covers how a record is identified, how a link names its target, what type a link carries, which record carries which link, and how the links are checked. The fields that belong to one kind of record stay with that record's own guideline: decision supersession with decision records, issue resolution with issue tracking, blocked milestones with milestone scheduling, task blockers with task breakdown, and the risk and dependency fields with risk tracking and dependency tracking. Requirements traceability for safety-critical work is outside it.

Following this guideline means keeping each SHOULD rule below, or stating why a record departs from it; a MAY rule is an option the team can take or leave. No rule here is a MUST.

