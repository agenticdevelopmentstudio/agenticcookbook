
Subsystem: `{{bundle_id}}` | Category: `CategorizeAndTag`

| Event | Level | Message |
|-------|-------|---------|
| Handler started | debug | `CategorizeAndTag: job {{jobId}} started` |
| Handler succeeded | info | `CategorizeAndTag: job {{jobId}} categorized as "{{category}}" with {{tagCount}} tags` |
| Duplicate result skipped | debug | `CategorizeAndTag: job {{jobId}} already has a result, skipping writes` |
| Handler failed | warning | `CategorizeAndTag: job {{jobId}} failed: {{error}}` |

