
**Decision**: Escalate to SIGKILL after a fixed timeout rather than waiting indefinitely.
**Rationale**: A hung child must never keep the app from quitting; five seconds balances graceful exit against responsiveness.
**Approved**: pending

