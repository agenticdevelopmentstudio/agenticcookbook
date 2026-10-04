
The agent acts on the harness's stdout/stderr, so error messages are part of the interface.

- Failures **SHOULD** state what was expected, what was observed, and the location (file:line) — not just a stack trace or a bare assertion.
- Each failure **SHOULD** name a concrete next step ("rename `x` to `y`", "add a test for the logged-out case"), because an actionable message turns into a correct edit; a vague one turns into a guess.
- Output **SHOULD** be concise; dumping thousands of lines floods the agent's context and degrades subsequent reasoning.

