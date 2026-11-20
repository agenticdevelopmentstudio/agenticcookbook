
- You **SHOULD** name the essential complexity of a module *before* writing code: what are the irreducible rules, states, and interactions? That set is the real work; everything else is overhead to minimize.
- You **MUST NOT** treat the boundary as a precise classifier. It is fuzzy and observer-dependent — what is accidental at one altitude (a language's verbosity) can feel essential at another (a hard latency budget). Use it to guide attention, not to mechanically sort lines of code.
- You **SHOULD** delete or generate-away accidental complexity aggressively (better abstractions, code generation, fewer moving parts) but **MUST NOT** "simplify" by dropping essential cases — that is hiding complexity, not removing it, and it resurfaces as bugs.
- When the two are entangled, you **SHOULD** refactor to isolate the essential core behind a thin layer so the accidental parts can change or be regenerated independently. This advances `simplicity` and `design-for-deletion`.

