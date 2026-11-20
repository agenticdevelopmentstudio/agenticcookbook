
A server offers three primitives.

| Primitive | Control model | Use for |
|-----------|---------------|---------|
| **Resource** | App/user-driven | Read-only context the host or user attaches (files, records, docs). No side effects. |
| **Prompt** | User-invoked | Templated, user-triggered workflows (slash commands, canned interactions). |
| **Tool** | Model-driven | Actions and side effects the model decides to invoke (queries, API calls, writes). |
