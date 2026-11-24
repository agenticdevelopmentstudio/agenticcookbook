
- **LLM backend returns invalid schema**: the handler MUST fail the job with `retryable: true` rather than passing a malformed result to complete (backend-failure-is-job-failure).
- **Startup with empty handler registry**: the node MUST log a warning and start normally; it will claim no jobs (no supported types), poll an empty result, and idle.
- **Large batch with mixed types**: the node SHOULD process jobs in the batch concurrently up to a configurable concurrency limit, with each job's heartbeat running independently.
- **Backend slower than the lease**: a long LLM call that outlasts one heartbeat interval relies on the job worker's heartbeat running independently of the handler, so the lease stays valid while inference runs.
- **Component-level cases**: network partition during complete, heartbeat firing after a terminal call, and clock skew are specified in the job-worker ingredient's edge cases; they apply to this composition unchanged.
- **Old node, new backend**: a node that sends no `jobTypes` gets only `categorize_and_tag` from the legacy rule, so it never claims a step it would kill as an unknown type.
- **Acting token outlives the lease**: if the lease is lost mid-loop the next `/mcp` call is refused; the handler MUST treat that like a lost lease (lost-lease-abort) and call neither complete nor fail.
- **Script writes huge stdout**: the handler caps captured stdout at 4 MiB and stderr at 64 KiB, and fails the step without retry when stdout exceeds its cap rather than holding it all in memory; a rerun of the same source on the same inputs would overflow again (step-script-handler).
- **Claude Code not signed in**: the CLI exits non-zero or prints an error result; the step fails as retryable with the CLI's message, and the node keeps running.
