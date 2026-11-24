--- draft-1.md
+++ draft.md
@@ -51,9 +51,9 @@
 
 # Decision Records
 
-Record each significant decision once, in a short record that states its context, the decision, why it was made, the options that lost, who decided, when, its status and all its consequences, and keep the record where everyone it affects can find it. A later decision that changes an earlier one never edits or silently contradicts it: it is a new record that marks the old one superseded, and the two link to each other.
-
-This guideline covers how any delivery team writes, stores, links and supersedes a project or architecture decision record. It does not cover which technical option to choose: a guideline that requires one decision to be recorded, such as datastore selection, says what to record, and this one says how. Linking between project records in general belongs to project record linking; only the links between a decision and the decisions it supersedes are this guideline's. Following it means keeping every MUST rule below and keeping each SHOULD rule or stating why a record departs from it.
+Record each significant decision once, in a short record that states its context, the decision, why it was made, the options that lost, who decided, when, its status and all its consequences, and keep the record where everyone it affects can find it. A later decision that changes an earlier one never silently contradicts it: it is a new record rather than an edit, it marks the old one superseded, and the old record's status should link to its replacement.
+
+This guideline covers how any delivery team writes, stores, links and supersedes a project or architecture decision record. It does not cover which technical option to choose: a guideline that requires one decision to be recorded, such as [adc.guideline.planning.data.datastore-selection](cookbook:6a653107-929d-418e-865d-636373a27b02), says what to record, and this one says how. Linking between project records in general belongs to project record linking; only the links between a decision and the decisions it supersedes are this guideline's. Following it means keeping every MUST rule below and keeping each SHOULD rule or stating why a record departs from it.
 
 ## Rules
 
@@ -73,7 +73,7 @@
 - **decision-links-to-its-work**: A decision record SHOULD be linked to the work it affects: the issues that carry it out and the code review that checks changes against it. (claims: link-decisions-to-work, github-issue-pr-linking)
 - **acknowledge-contradicted-decisions**: A decision that changes or reverses an earlier recorded decision MUST acknowledge the change: it is written as a new record that names the earlier decision, and the earlier record is marked superseded, so no decision contradicts an earlier one unknowingly. (claims: supersede-and-link, records-prevent-relitigation, cloud-providers-agree-on-supersession)
 - **supersede-never-edit-accepted-records**: An accepted decision record SHOULD NOT be edited to change its decision; a changed decision is proposed as a new record that, once accepted, supersedes the old one, whose status alone is updated to point to it. (claims: accepted-records-immutable, adr-tools-supersede-command, clarifications-may-amend)
-- **supersession-links-both-ways**: When one record supersedes another, the superseded record SHOULD be marked superseded with a link to its replacement, and the new record SHOULD name the record it replaces. (claims: supersede-and-link, supersession-header-fields, gds-way-supersede-must)
+- **supersession-links-both-ways**: When one record supersedes another, the superseded record's status SHOULD link to the record that replaces it. (claims: supersede-and-link, supersession-header-fields, gds-way-supersede-must)
 - **backfill-undocumented-decisions**: When a decision log is started for an existing system, decisions already made but never written down MAY be recorded retroactively, where the data on them is available. (claim: backfill-undocumented)
 
 ## Writing a decision record
@@ -132,7 +132,7 @@
 
 ## What a reviewer looks for
 
-Checks that every significant decision has a record, and that each record states its context, the decision, its rationale and all its consequences, the costs included. Checks that a record names its decider, carries a date and a status, lists the options that lost with why, and lists no made-up option. Checks that each record holds one decision and stays short, that rejected proposals are recorded with their reason, and that the log is stored openly with history and linked to the work. Above all, checks that no decision contradicts an earlier one without a new record that names it, that no accepted record was edited to change its decision, and that superseded and superseding records link to each other.
+Checks that every significant decision has a record, and that each record states its context, the decision, its rationale and all its consequences, the costs included. Checks that a record names its decider, carries a date and a status, lists the options that lost with why, and lists no made-up option. Checks that each record holds one decision and stays short, that rejected proposals are recorded with their reason, and that the log is stored openly with history and linked to the work. Above all, checks that no decision contradicts an earlier one without a new record that names it, that no accepted record was edited to change its decision, and that each superseded record's status links to its replacement.
 
 ## A complete review must establish
 
@@ -158,8 +158,8 @@
 - `decision-links-to-its-work`: each record links to the issues and code review that carry it out.
 - `acknowledge-contradicted-decisions`: no decision changes an earlier one without a new record naming it and the earlier record marked superseded.
 - `supersede-never-edit-accepted-records`: no accepted record was edited to change its decision.
-- `supersession-links-both-ways`: each superseded record links to its replacement, and each replacement names what it replaces.
-- `backfill-undocumented-decisions`: where a log was started for an existing system, known past decisions were recorded where their data was available.
+- `supersession-links-both-ways`: each superseded record's status links to its replacement.
+- `backfill-undocumented-decisions`: where used, past decisions recorded retroactively are ones whose data was available.
 
 ## Rationale
 
