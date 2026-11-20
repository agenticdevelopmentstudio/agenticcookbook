
Every token spent is time and money. Every model call that could have been a shell script is wasted latency. Every rule line loaded on every turn that's only needed once per session is compounding waste. This guideline establishes three principles for building Claude Code extensions that are fast and token-efficient.

- `should-use-shell-scripts-for-deterministic-work`: Shell scripts are faster, cheaper, and deterministic — they produce the same result every time without consuming model tokens.
- `should-load-only-what-the-current-step-needs`: This is the single highest-leverage optimization for Claude Code extensions.

### The Cost Model

Files in `.claude/rules/` and CLAUDE.md are injected into the system prompt on **every turn** — every user message, every tool call, every response. In a 50-turn conversation, a 10KB rule file consumes ~500KB of context. This cost is invisible and compounding.

Content loaded via tool calls (reading files, invoking skills) is paid once at the point of use. This makes on-demand loading dramatically cheaper for anything not needed on every turn.

### Real-World Impact

The agenticdevelopercookbook's own rules went from 381 lines / 17,689 bytes per turn to 10 lines / 358 bytes per turn — a 97% reduction — by applying progressive disclosure. The behavioral constraints were preserved; only the delivery mechanism changed.

