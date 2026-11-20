
Rules in `.claude/rules/` are injected into the system prompt on **every turn** — not just at session start. Every byte costs context on every user message, tool call, and response. These checks flag common sources of per-turn waste.
