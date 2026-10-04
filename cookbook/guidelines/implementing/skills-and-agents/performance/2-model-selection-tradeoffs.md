
When a subtask is simple enough for a smaller model, consider downgrading. But measure — don't assume.

### The Decision Framework

Before selecting a smaller model for a subtask, verify three things:

1. **Token efficiency**: Does the smaller model actually use fewer tokens? Some smaller models compensate for lower capability with more verbose output, more retries, or more tool calls. If the smaller model uses the same or more tokens than the larger model, the downgrade is pure cost with no benefit.

2. **Latency**: Does the smaller model complete the subtask faster? If the smaller model needs multiple attempts or produces output that requires correction, the wall-clock time may be worse.

3. **Correctness**: Can the smaller model do the job reliably? A task that looks simple may have edge cases the smaller model mishandles, requiring human intervention or a retry with the larger model.

### When Downgrading Makes Sense

- Template filling with clear structure and no ambiguity
- Simple extraction from well-formatted input (parsing JSON, reading frontmatter)
- Formatting tasks with explicit rules (markdown cleanup, import sorting)
- Classification with a small, well-defined set of categories

### When to Stay on the Larger Model

- Any task involving reasoning about code behavior or architecture
- Tasks where a wrong answer costs more than the token savings
- Tasks that chain — where the output feeds into another model call and errors compound

### When It's Unclear

Ask the user. Present the tradeoff: "This subtask could run on a smaller model — it's a simple extraction. But if it gets it wrong, we'd retry on the larger model anyway. Want me to try the smaller model or just use the current one?" Do not silently downgrade.

