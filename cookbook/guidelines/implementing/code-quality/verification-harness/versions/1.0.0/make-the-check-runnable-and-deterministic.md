
- The harness **MUST** be a single command (or short script) the agent can invoke and that returns a machine-readable signal: a process exit code, a test summary, a diff against a fixture, or a screenshot compared to a target.
- The check **MUST** be deterministic: the same input produces the same pass/fail. Flaky, time-, or network-dependent checks **MUST NOT** gate completion — they teach the agent to retry randomly or suppress the signal.
- The agent **MUST** show evidence (the command run and its output), not assert success. Reviewing evidence is faster than re-running the check.
- Wire the command into the project so the agent can discover it (e.g., a documented `verify`/`lint`/`test` entry point referenced in agent-readable docs).

