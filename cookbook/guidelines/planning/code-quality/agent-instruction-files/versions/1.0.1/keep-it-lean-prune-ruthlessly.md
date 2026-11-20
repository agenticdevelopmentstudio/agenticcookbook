
- The file **MUST** stay concise and high-signal. A widely-reported failure mode is that bloated, stale instruction files get partially ignored and can degrade task success — keep durable, load-bearing instructions only.
- Note this is a practitioner heuristic, not a settled empirical result; the durable principle is signal-to-noise, so you **SHOULD** delete instructions that are obsolete, obvious, or contradicted by the code.
- Every instruction **SHOULD** be specific and verifiable (a command, a path, a named rule) rather than vague aspiration ("write clean code").
- You **SHOULD** review the file whenever build/test commands or project structure change, treating it as code that rots.

