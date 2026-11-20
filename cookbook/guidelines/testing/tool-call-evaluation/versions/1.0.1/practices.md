
- Run each case multiple times; tool selection is non-deterministic, so **SHOULD** report pass rates with trial counts, not a single run.
- Gate releases on the suite and track per-dimension scores over time so a regression in argument correctness is not masked by stable task-completion numbers.
- Keep cases hermetic: stub or record tool responses so the eval measures the agent, not live backend flakiness.

