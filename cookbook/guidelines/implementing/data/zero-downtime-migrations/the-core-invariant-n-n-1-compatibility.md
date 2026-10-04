
During a rolling deploy, both the old app version (N-1) and the new one (N) run against the *same* schema simultaneously.

- Each migration step **MUST** be compatible with the app version currently running against it — both N-1 and N must function after the step is applied.
- A schema change and the code that depends on it **MUST NOT** ship in the same atomic step. The schema goes first (additive), code follows, cleanup goes last.
- Destructive changes (drop column, rename, narrow a type, add NOT NULL) **MUST** be deferred to the contract phase, after no running code references the old shape.

