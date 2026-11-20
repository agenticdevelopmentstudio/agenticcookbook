
- Cross-session continuity (plans, conventions, in-progress task state) **MUST** live in a persistent file the agent re-reads at session start, since the context window does not persist between sessions.
- Memory files **MUST** stay concise and high-signal. An overstuffed memory file dilutes attention and causes the agent to ignore the rules that matter — keep only what changes behavior, and prune regularly.
- The agent **MUST NOT** duplicate information the model can cheaply re-derive (e.g. file contents, standard conventions) into memory; store only what cannot be inferred.

