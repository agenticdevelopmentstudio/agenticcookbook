
- LLM coding agents are the strongest tool yet against **accidental** complexity: they emit boilerplate, glue, scaffolding, and syntax fast and cheaply. You **SHOULD** route that work to agents and review it for correctness, not for novelty.
- Agents **cannot** reduce **essential** complexity — they can restate it, but the irreducible domain decisions still require human judgment. You **MUST** keep design review, requirement disambiguation, and invariant definition under human ownership even when an agent writes the code.
- Treat "AI eliminates complexity" as a **forecast/marketing claim, not an established result**. Brooks's argument that no single tool yields an order-of-magnitude gain against the essential part remains the durable, contested-by-some baseline; cheaper accidental-complexity reduction does not refute it.
- Practical consequence: as accidental cost falls, the **design bottleneck shifts toward managing essential complexity**. Spend the time saved on agents harvesting the incidental on sharper problem decomposition, not on shipping more under-specified features (see `yagni`).

