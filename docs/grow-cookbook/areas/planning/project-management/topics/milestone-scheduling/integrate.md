# Integrate: milestone-scheduling

## For the owner

Rules standing as they were until you decide each (`cookr validate` owner-decides):

- rule 'milestone-has-status-and-target-date' cites 'milestone-has-status-and-target-date-prior', which the research rules unsupported
- rule 'blocked-milestone-has-issue-or-concern' cites 'blocked-milestone-has-issue-or-concern-prior', which the research rules unsupported

Open questions from the owner list:

- Whether the two unsupported Verify rules (milestone-has-status-and-target-date, blocked-milestone-has-issue-or-concern) are kept as must-hold checks by house policy or restated at the SHOULD strength the sources support; the owner decides.
- Whether 'target date' in milestone-has-status-and-target-date means a fixed committed date or a forecast computed from logic: GAO says baseline and status schedules should not carry hard date constraints, so a policy that every milestone carries a fixed date conflicts with logic-driven scheduling unless the date is a baseline target.
- Whether the at-risk case joins the blocked case in one rule (every blocked or at-risk milestone names its issue or risk) or stays a separate rule; the brief's research question asks for both, the listed rule names only blocked.
- Which status vocabulary the cookbook names: Linear uses On track / At risk / Off track, GitHub Projects uses On track / At risk among others, Jira uses a Flagged = Impediment field; the owner decides whether to fix a vocabulary or leave it to the tracker.
- Whether the cookbook names a schedule update cadence; GAO ties cadence to duration, complexity and risk and gives only an example (track weekly when reporting monthly), so any fixed cadence is a policy choice.
- Whether 'fix the date, flex the scope' (Shape Up, Scrum's fixed-length Sprint) is stated as an option beside critical-path scheduling or left out; the sources present it as a method choice, not a universal practice.

## Lossless

New topic, no base text (`cookr roles lossless`: not in the base commit).

## Validate

`cookr validate` passed; its owner-decides rows are listed under For the owner. Bumped 1.0.0 → 1.0.1; /add-artifact approved it (lint clean, 37 rules).

integrated: 2026-11-24
