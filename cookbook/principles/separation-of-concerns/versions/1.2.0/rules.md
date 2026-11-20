
- **should-have-one-reason-to-change**: A module SHOULD have one reason to change. This applies at every scale: functions, modules, services, teams.
- **should-split-when-description-needs-and**: SHOULD describe each module's responsibility in one sentence without using "and" — if you cannot, split it.
- **should-separate-ui-logic-and-data**: SHOULD keep UI rendering, business logic, and data access in separate layers that can change independently.
- **should-treat-cross-feature-edits-as-coupling**: When a change to one feature forces edits in an unrelated feature, SHOULD treat it as a coupling defect.
- **should-co-locate-by-reason-to-read**: Counterweight — locality of behavior: SHOULD separate by *reason to change*, but co-locate by *reason to read*; choose per case rather than maximizing either.
