
Subsystem: `{{bundle_id}}` | Category: `JobWorker`

| Event | Level | Message |
|-------|-------|---------|
| Node started | info | `JobWorker: started with {{handlerCount}} handlers for types {{types}}` |
| Empty registry | warning | `JobWorker: no handlers registered, node will idle` |
| Claim returned jobs | debug | `JobWorker: claimed {{count}} jobs` |
| Claim returned none | debug | `JobWorker: no jobs, waiting {{seconds}}s` |
| Job completed | info | `JobWorker: job {{jobId}} completed in {{duration}}s` |
| Job failed | warning | `JobWorker: job {{jobId}} failed (retryable={{retryable}}): {{error}}` |
| Lease lost | warning | `JobWorker: lease lost for job {{jobId}}, work aborted` |
| Unknown type | error | `JobWorker: no handler for type "{{type}}" (job {{jobId}})` |
| Report retry | warning | `JobWorker: retrying {{endpoint}} for job {{jobId}} after {{error}}` |

