
This section is informative: it shows one way to keep the rules, not a required method.

1. Give each record its identifier when it is created, and never hand that identifier to another record. Decision logs number records sequentially and never reuse a number (Nygard, MADR); Jira keys are a project prefix, a hyphen and a number, such as ABC-123. Which scheme the project's records use, one prefix per record type or one sequence for all, is left open here: the sources ask only that identifiers be unique and not reused.
2. Keep status, owner and other changing facts in the record's fields, never in its identifier. W3C's advice for web addresses is the model: documents change status, so an address that names a status breaks.
3. Write each link with its type and the target's identifier: "D-4 supersedes D-2", "T-12 is blocked by DEP-3". A tracker turns a reference by number or key into a link: GitHub converts #26, and Jira links a commit whose message holds the key.
4. Make a two-way relationship visible from both records. GitLab's linked items are bi-directional and are removed from both items together; Jira stores one link with an outward and an inward description; GitHub writes a backlink by default and exposes blocked-by and blocking from both ends; Sphinx-Needs stores the link on the source item and computes the back link; adr-tools writes the reverse link into the existing record. For records kept as files, whether both files hold the link or one file holds it and a checker computes the reverse is left open here.
5. When a record is finished with, close it or mark it superseded; do not delete it. A deleted GitHub issue's address shows page-not-found and nobody is notified, while Linear keeps a resolved blocker linked as Related. Whether an accepted decision record may still take dated amendments is a question for [adc.guideline.planning.project-management.decision-records](cookbook:2b7a1593-48e0-4bbe-8e14-0df7a863628d), and is not settled here.
6. Run a link check, by tool or by hand, whenever records are added, moved or closed. Doorstop and Sphinx-Needs check links by default: both flag a link to an unknown identifier, and Doorstop also reports links to inactive items, items with no links, and cycles. IBM's lifecycle tools mark a link suspect when either end changes. Whether a link to an unknown identifier fails the check or only warns, whether a link to a closed or superseded record is reported at all, and which records must have at least one link, are left open here.
7. To see every link at once, a traceability matrix lists records against records; it becomes large and confusing as the project grows, so a check that lists only the problems scales better.

How the tools compare:

- **GitHub** links by number with an automatic backlink, records blocked-by and blocking dependencies with a Blocked icon, nests sub-issues under a parent, and closes an issue when a change that names it with a closing keyword is merged. A transferred issue's old address redirects; a deleted one is gone.
- **Jira** names each item by its key, gives each link type an outward and an inward description (relates to, duplicates, blocks, clones by default), and reserves and redirects a moved item's old keys.
- **Linear** shows Blocked by on one issue and Blocks on the other, turns a mention into a related link, and moves the relation to Related once the blocker is resolved.
- **GitLab** keeps linked items as bi-directional relationships (relates to, blocks, is blocked by) and asks for confirmation before a blocked item is closed.
- **Doorstop and Sphinx-Needs** keep items as files, check their links by default, and, in Sphinx-Needs, compute back links with separate incoming and outgoing wording.

