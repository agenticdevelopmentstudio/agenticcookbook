
A server offers three primitives. Pick by purpose, not convenience.

| Primitive | Control model | Use for |
|-----------|---------------|---------|
| **Resource** | App/user-driven | Read-only context the host or user attaches (files, records, docs). No side effects. |
| **Prompt** | User-invoked | Templated, user-triggered workflows (slash commands, canned interactions). |
| **Tool** | Model-driven | Actions and side effects the model decides to invoke (queries, API calls, writes). |

- You **SHOULD** prefer a **resource** for anything read-only that the user or host selects as context.
- You **SHOULD** prefer a **prompt** for workflows a human explicitly invokes.
- You **SHOULD** model **tools** for operations the model chooses autonomously — and only those.
- Do not expose read-only context as a tool merely because tools are easier to wire up; that puts routing load on the model and invites accidental invocation.

