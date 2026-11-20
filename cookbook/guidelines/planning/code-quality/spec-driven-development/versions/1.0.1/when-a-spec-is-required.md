
- A non-trivial change **MUST** start from a written spec before code is generated. "Non-trivial" means: the approach is uncertain, the change touches multiple files, or the agent is unfamiliar with the code being modified.
- If you can describe the diff in one sentence (a typo, a log line, a rename), you **SHOULD** skip the spec and do the work directly. Right-size the ceremony to the change.
- Planning and implementation **SHOULD** run in distinct phases so research context does not bleed into and bias execution.

