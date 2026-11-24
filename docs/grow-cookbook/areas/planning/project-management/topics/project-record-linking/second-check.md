## pg-prince2-unique-identifiers
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: The issue-register page holds the first half of the quote and the ILX risk-register post holds the second half, each word for word. Both are trainer summaries, not the AXELOS manual itself.

## bp-ids-never-reused
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: Nygard says "ADRs will be numbered sequentially and monotonically. Numbers will not be reused." MADR says "`NNNN` is a consecutive number".

## ks-jira-key-names-target
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page also says the key can go in the branch name or the pull request title, which covers the claim's branch and pull request.

## bp-identifier-carries-no-status
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page also says "Keep the status out of the name," which backs the claim directly.

## pg-moved-records-keep-old-names
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: The Atlassian article covers the reserved keys and the ALPHA-1 to BETA-5 redirect. GitHub says "The original URL redirects to the new issue's URL."

## ks-github-autolink-backlink
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page lists the #26 and owner/repo#26 forms and says "By default, references generate a backlink."

## ks-backlinks-computed
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page says "A link type's back links are computed on every need" and lists separate `incoming` and `outgoing` texts. That a link is stored once on the source is implied, not stated.

## ks-jira-typed-links-two-descriptions
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: lacks-quote
- result: confirmed
- note: The Server admin page holds the whole quote, including the four default link types. The Cloud "link issues" page names link types but does not call them defaults and has none of the quote.
- correction: dropped 1 citation(s) lacking the quote; independence single -> single

## ks-gitlab-bidirectional-links
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page lists the types "Relates to", "Blocks" and "Is blocked by", says removal clears both items, and says closing a blocked item asks for confirmation.

## ks-linear-relations
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: All four sentences appear word for word.

## ks-two-way-link-recorded-once
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- result: refuted
- note: The sources say links are bi-directional, that Jira shows one link as inward on the other issue, and that GitHub "will automatically generate another link". None says a link is "recorded once", and GitHub's backlink is a second link with no wording of its own, so "across trackers… each side with its own wording" goes beyond what they say.
- correction: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST

## ks-github-dependencies-both-directions
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: The REST page has the endpoints "List dependencies an issue is blocked by" and "List dependencies an issue is blocking".

## ks-adr-tools-reverse-link
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Both help-text sentences for `-s` and `-l` appear word for word in `src/adr-new`.

## bp-bidirectional-traceability
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The definition is of requirements traceability: following "the life of a requirement" forwards and backwards. The claim widens it to traceability of any item.
- correction: refuted (quote-found yes, supports-claim partly); trust 55 -> 35; a rule citing it cannot carry MUST

## pg-deleted-record-breaks-links
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page says admins "can permanently delete an issue", collaborators get no notification, and the URL shows a page-not-found message.

## bp-supersede-and-link-both
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: Microsoft holds the append-only and supersede-and-link sentences. Nygard holds the deprecated-or-superseded sentence and also says "keep the old one around, but mark it as superseded."

## ev-supersede-not-edit-debated
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The repo adds "We insert the new info the existing ADR, with a date stamp…", which backs the claim's "dated amendments".

## ev-unrecorded-decisions-contradicted
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The sentence appears word for word under "Workload documentation repository".

## pg-github-single-source-and-blockers
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: All three sentences appear word for word.

## ks-github-sub-issues-and-milestones
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: The milestone page shows open and closed counts. For parents, the sub-issues page only says "Parent issues and sub-issue progress is also available in your projects," so parent-side progress is implied rather than stated outright.

## ks-github-closing-keywords
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: For a closing keyword in a commit message, the page says the issue closes when the commit is merged into the default branch.

## bp-risk-realised-links-issue
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: PRINCE2 wiki says "A risk becomes an issue once it materializes." The second page gives the "realised → see I-01" convention, but it is a single course site, not a PRINCE2 source.

## pg-prince2-integrated-register
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: The risk-register page lists the integrated project register as one of several possible formats, which matches "may". The issue-register page ties linking an issue report to a risk to using a shared spreadsheet or tool, not to an integrated register.

## ks-dangling-link-checks
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: In Doorstop, an unknown UID and an inactive parent link are errors, and a missing link and a cycle are warnings, all shown in a default run. Sphinx-Needs warns on an unknown outgoing link unless `allow_dead_links` is set.

## ks-suspect-links
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The page is IBM ELM 7.0.3 link-validity documentation, and it applies to projects enabled for configurations.

## ev-missing-links-impede
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The abstract reports one case, at a single telecom company, where links were missing. It says traceability is "often assumed to exist", not that links are "often missing", and it does not say gaps are found only when someone needs them.
- correction: refuted (quote-found yes, supports-claim partly); trust 52 -> 32; a rule citing it cannot carry MUST

## ks-traceability-matrix
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The full sentence is "However, in industry, projects often consist of thousands of artifacts: the tables could become very large and confusing."
