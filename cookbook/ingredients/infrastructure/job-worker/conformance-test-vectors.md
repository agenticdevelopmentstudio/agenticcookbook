
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| job-worker-001 | poll-claim, run-handler, complete-on-success | Queue contains one job of a supported type with a valid payload | Node claims the job, the handler executes, node calls complete with the handler's result, job moves to done state on the backend |
| job-worker-002 | run-handler, fail-with-backoff, loop-continuity | The handler throws an unrecoverable error | Node calls fail with `retryable: true`; loop continues; next poll iteration proceeds normally |
| job-worker-003 | unknown-type-fail | Queue contains a job whose type has no registered handler | Node immediately calls fail with `retryable: false`; job goes to dead-letter; loop continues |
| job-worker-004 | lease-heartbeat, complete-on-success | Handler takes longer than one heartbeat interval (e.g., 40s call on a 30s lease) | At least one heartbeat is sent before the complete call; the lease remains valid throughout; complete succeeds |
| job-worker-005 | idempotency | Same job is claimed twice (simulated lease expiry mid-run); handler completes on the second claim | Backend result is identical to the first completion; no duplicate side effects are created |
| job-worker-006 | poll-claim, loop-continuity, poll-interval | Backend queue is empty | Claim returns zero jobs; no complete or fail calls are made; loop waits the poll interval and polls again |
| job-worker-007 | lost-lease-abort | Heartbeat response returns lease-invalid (e.g., 409 Conflict) mid-handler | Node cancels handler execution, does NOT call complete or fail, logs lease loss, continues loop |
| job-worker-008 | handler-timeout, fail-with-backoff | Handler exceeds its configured timeout | Invocation is treated as a handler error; node calls fail with `retryable: true` |
| job-worker-009 | heartbeat-stop-on-terminal | Handler completes and node calls complete | No heartbeat is sent after the terminal call |
| job-worker-010 | supported-types-static | Backend holds jobs of types the node does not list in its configuration | Node's claim request names only its configured types; those jobs are never claimed |

