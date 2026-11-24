## triage-sets-severity-on-every-defect
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The Mozilla page defines a triaged defect as one with a Severity other than "--" or N/A, and says tasks and enhancements may take N/A. Both quoted sentences are there; the inline markup only changes the spacing.

## github-no-default-severity
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: The default label table (accessibility, bug, documentation, duplicate, enhancement, good first issue, help wanted, invalid, question, wontfix) has no severity or priority label. The Projects best-practices page gives priority as its example of a single-select field. GitHub's newer "issue fields" feature might weaken "no priority", but neither citation covers it.

## jira-priority-conflates-severity
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page lists default statuses, priorities and resolutions and never uses the word "severity". The priority descriptions ("This problem will block progress", "Trivial problem with little or no impact") describe impact.

## linear-priority-five-levels
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page gives the five values and the reason for having no custom priorities. The word "severity" does not appear anywhere on it.

## status-tracks-to-resolution
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- citation 4: holds-quote
- result: confirmed
- note: Each source holds its fragment. The Google fragment comes from the page's auto-generated "Page Summary" box, not its main text.

## severity-separate-from-priority
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- result: confirmed
- note: Mozilla's 2020 post says "Using Priority alone conflates severity with scheduling" and moves triage onto the Severity field. Atlassian's blog adds a separate "Symptom Severity" field next to priority.

## mozilla-bugzilla-severity-priority-fields
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: The severity guide says the field is displayed alongside priority. The BugFields wiki defines P1, P2 and P5 by release cycle; P3 is Backlog and P4 is reserved for the WPT bot.

## google-issue-tracker-priority-and-severity
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- citation 2: holds-quote
- result: refuted
- note: The quote supports severity and priority as issue fields and a P0–P4 range, but nothing in it says priority is required at creation or that levels are defined by impact and workaround. The cited page does say both, in "required fields... Component, Title, Priority and Type" and in its P0–P4 table, so a fuller quote would back the claim.
- correction: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST

## severity-levels-defined
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: Mozilla's S1–S4 and Atlassian's Critical/Major/Minor are each described by user impact, data loss and whether a workaround exists.

## regression-not-severity
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The sentence appears word for word in the 2020 mozilla.tools.bmo post on the triage process change.

## severity-change-needs-rationale
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It is stated as a requirement ("requires"), right after a note that QA sets the initial severity on bugs it files or reproduces.

## priority-inflation
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: The OpenAlex abstract, rebuilt from its inverted index, holds both sentences. Mozilla's BugFields says severity "should not be set by people filing bugs" and that triagers are expected to set it.

## escalation-procedure-documented
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is from the February 2012 CDC UP Project Management Newsletter. The direct download returned 403, so the PDF was retrieved through WebFetch and its text extracted.

## escalate-unresolved-after-time
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- result: confirmed
- note: CDC leaves the time unspecified ("lengthy period... we may want to specify a time range here"). Linear's default SLA rules and Mozilla's end-of-cycle review of S1/S2 bugs supply the time bounds tied to priority or severity.

## triage-has-named-owner
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- result: confirmed
- note: Mozilla requires a Triage Owner per component, and Linear and Chromium both recommend a rotation.

## triage-within-time-bound
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: Mozilla says "within one week of being created" and also expects a daily quick assessment.

## untriaged-is-visible
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: The Kubernetes `needs-triage` label and Linear's Triage inbox both keep untriaged issues apart.

## issue-has-one-owner
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- result: confirmed
- note: The match is word for word once the inline markup in Joel's text is ignored. CDC's issue-log text elsewhere allows "one or more individuals", which pulls against the one-owner rule.

## resolution-reason-from-fixed-set
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- citation 4: holds-quote
- result: confirmed
- note: Jira lists Done, Won't do, Duplicate and Cannot reproduce. The GitHub REST `state_reason` enum is completed/not_planned/duplicate/reopened/null, Google has the Won't fix variants, and FogBugz has fixed through by design. Only markup differs.

## itil-known-error
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: The Jira page lists "Known error" under "Jira Service Management resolutions".

## link-fix-to-issue
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- result: refuted
- note: The quoted Jira text only covers putting the key in commit messages. The claim's "and pull requests that carry the issue key" isn't in the quote, though the page does say "When you create a pull request, use the key in the pull request title." The GitHub and Jira Service Management parts are supported.
- correction: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST

## close-duplicates-link-canonical
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- citation 4: holds-quote
- result: confirmed
- note: The GitHub REST `duplicate_issue_id` description matches apart from code markup. Linear moves duplicates into a reserved Duplicate status that links to the original.

## duplicates-refiled
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: Chromium uses this line to justify spending triage time on recent issues and letting old ones go. Its point is that important problems resurface as new reports. It does not say triage should expect duplicates and merge them, beyond noting that old issues often "have not been properly duped".
- correction: refuted (quote-found yes, supports-claim partly); trust 50 -> 30; a rule citing it cannot carry MUST

## close-not-planned-definitively
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- result: confirmed
- note: Chromium says to "Be definitive... close the issue out and provide honest and courteous feedback". Linear's Decline action offers an explanatory comment.

## verify-resolution
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- citation 4: holds-quote
- result: confirmed
- note: Each source supports one form of confirmation (reporter, Verifier field, or testing). In Google's tracker "Fixed (Verified)" is a separate status from plain "Fixed", so verification is optional there.

## keep-closed-as-history
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The text appears word for word in the CDC UP newsletter, under its best practices.

## communicate-resolution
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The text appears word for word in the newsletter's list of issue-management activities.

## issue-log-minimum-fields
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: CDC's minimum fields plus its log description (owner, target date) cover the list. Google requires Component, Title, Priority and Type for new issues.

## spolsky-three-things
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote says only that a good report needs "exactly three things" and does not name them. The page names them in the next sentence ("Steps to reproduce, What you expected to see, and What you saw instead"), so a longer quote would support the claim.
- correction: refuted (quote-found yes, supports-claim partly); trust 50 -> 30; a rule citing it cannot carry MUST

## avoid-extra-fields
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: Joel warns against adding fields and Linear warns against finer priorities.

## bug-database-everyone-uses
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: Both sentences are on the page. The first is word for word once the bold markup is ignored.

## pmbok-issue-log
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The CDC newsletter attributes the issue definition to PMBOK, so this is a secondary source. The "all projects, regardless of type or size, should have an issue tracking system or log" line is the CDC's own recommendation, not PMBOK's. A primary PMBOK glossary citation would be stronger.

## prince2-issue-broad
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: All four sentences are on the PeopleCert PRINCE2 7 article.

## stale-issues-flagged
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: The Kubernetes robot adds `lifecycle/stale` after 90 days without activity. The Kanban Guide says to keep items from ageing unnecessarily, using the SLE as a reference.

## kanban-active-management
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The Kanban Guide says "must be managed actively" and lists unblocking work and preventing unnecessary ageing among its forms.
