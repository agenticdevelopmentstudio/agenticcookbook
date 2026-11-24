
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| `apn-001` | `poll-claim`, `run-handler`, `complete-on-success` | Backend queue contains one `categorize_and_tag` job with `{ "title": "How to prune roses", "body": "..." }` | Node claims the job, handler executes, node calls complete with `{ category, tags, confidence? }`, job moves to done state on backend |
| `apn-002` | `run-handler`, `fail-with-backoff`, `loop-continuity` | Handler for `categorize_and_tag` throws an unrecoverable error | Node calls fail with `retryable: true`; loop continues; next poll iteration proceeds normally |
| `apn-003` | `unknown-type-fail` | Backend queue contains a job with `type: "transcribe_audio"` and node has no handler for that type | Node immediately calls fail with `retryable: false`; job goes to dead-letter; loop continues |
| `apn-004` | `lease-heartbeat`, `complete-on-success` | Handler takes longer than one heartbeat interval (e.g., 40s LLM call on a 30s lease) | At least one heartbeat is sent before the complete call; job lease remains valid throughout; complete succeeds |
| `apn-005` | `idempotency`, `idempotent-end-to-end` | Same job is claimed twice (simulated lease expiry mid-run); handler completes on the second claim | Backend result is identical to first completion; no duplicate category or tag entries created |
| `apn-006` | `poll-claim`, `loop-continuity` | Backend queue is empty | Claim returns zero jobs; no complete/fail calls made; loop waits the poll interval and polls again |
| `apn-007` | `lost-lease-abort` | Heartbeat response returns lease-invalid (e.g. 409 Conflict) mid-handler | Node cancels handler execution, does NOT call complete or fail, logs lease loss, continues loop |
| `apn-008` | `backend-failure-is-job-failure`, `inject-llm-backend` | Stub LLM backend returns a result missing `category` | Handler fails; node calls fail with `retryable: true`; no complete call is made |
| `apn-009` | `register-handler-at-startup` | Start the node with the handler registry populated | The claim request lists exactly `categorize_and_tag` as the supported type |

