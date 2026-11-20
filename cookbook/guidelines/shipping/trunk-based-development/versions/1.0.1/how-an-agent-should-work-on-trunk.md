
1. **Branch small.** Cut a short-lived branch from current `main` for one logical change.
2. **Keep work shippable.** If the change is partial, gate the new behavior behind a feature flag (default off). Add code paths that are inert until the flag is enabled.
3. **Commit atomically.** One logical change per commit (see atomic-commits), running the build and tests before each commit.
4. **Rebase, don't drift.** Before opening or updating a PR, the agent SHOULD rebase the branch onto the latest `main` so the diff reflects current trunk.
5. **Merge fast.** Open the PR, get checks green, and merge within a day. Prefer squash merges to keep trunk history linear and each merge a single revertible unit.
6. **Don't sit on it.** The agent MUST NOT accumulate days of work on a branch "until it's complete." Land enabling-but-disabled increments instead.

