
# Separation of concerns

A module should have one reason to change. If describing what a module does requires "and," consider splitting. This applies at every scale: functions, modules, services, teams.

- Describe each module's responsibility in one sentence without using "and" — if you cannot, split it
- Keep UI rendering, business logic, and data access in separate layers that can change independently
- When a change to one feature forces edits in an unrelated feature, treat it as a coupling defect
- Counterweight — locality of behavior: separate by *reason to change*, but co-locate by *reason to read*. If splitting a concern scatters one feature's behavior across many files so you must hop between them to follow it, that fragmentation is its own cost. Separation and locality pull in opposite directions; choose per case rather than maximizing either.

