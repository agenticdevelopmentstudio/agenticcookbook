
- `should-name-essential-complexity-first`: That set is the real work; everything else is overhead to minimize.
- `must-not-treat-boundary-as-precise-classifier`, `should-use-boundary-to-guide-attention`: It is fuzzy and observer-dependent — what is accidental at one altitude (a language's verbosity) can feel essential at another (a hard latency budget).
- `must-not-drop-essential-cases`: Dropping essential cases is hiding complexity, not removing it, and it resurfaces as bugs.
- `should-isolate-essential-core`: This advances `simplicity` and `design-for-deletion`.
- `should-route-accidental-work-to-agents`: LLM coding agents are the strongest tool yet against **accidental** complexity: they emit boilerplate, glue, scaffolding, and syntax fast and cheaply.
- `must-keep-essential-decisions-human-owned`: Agents **cannot** reduce **essential** complexity — they can restate it, but the irreducible domain decisions still require human judgment.
- `should-treat-ai-eliminates-complexity-as-a-claim`: Brooks's argument that no single tool yields an order-of-magnitude gain against the essential part remains the durable, contested-by-some baseline; cheaper accidental-complexity reduction does not refute it.
- `should-spend-saved-time-on-decomposition`: Practical consequence: as accidental cost falls, the **design bottleneck shifts toward managing essential complexity**.
