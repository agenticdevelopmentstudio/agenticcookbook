
Subsystem: `{{bundle_id}}` | Category: `LLMBackend`

| Event | Level | Message |
|-------|-------|---------|
| Backend selected | info | `LLMBackend: using {{kind}} backend` |
| Inference started | debug | `LLMBackend: request started for job {{jobId}}` |
| Inference completed | debug | `LLMBackend: request completed in {{duration}}s` |
| Output failed validation | warning | `LLMBackend: output for job {{jobId}} failed schema validation: {{error}}` |
| Backend error | error | `LLMBackend: backend failed: {{error}}` |

