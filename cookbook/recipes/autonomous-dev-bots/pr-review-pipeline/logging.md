
Subsystem: `pr-review-pipeline` | Category: `Pipeline`

| Event | Level | Message |
|-------|-------|---------|
| Pipeline started | info | `Pipeline: started for PR #{{pr_number}} on {{repo}}` |
| Phase completed | info | `Pipeline: phase {{phase}} completed — {{result}}` |
| Phase short-circuited | info | `Pipeline: skipping phase {{phase}} — prior phase rejected` |
| Fix bot committed | info | `Pipeline: fix bot pushed commit {{sha}} for PR #{{pr_number}}` |
| Rate limit hit | warning | `Pipeline: GitHub API rate limited — retrying in {{seconds}}s` |
| Pipeline failed | error | `Pipeline: failed for PR #{{pr_number}} — {{error}}` |

