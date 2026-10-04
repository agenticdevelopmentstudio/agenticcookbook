
- You **SHOULD** explicitly document which behaviors are guaranteed and state the rest as **non-guarantees** (e.g., "iteration order is unspecified and may change").
- You **SHOULD** make unpromised behavior visibly unstable so consumers cannot quietly couple to it — deliberately randomize ordering, jitter timing, or vary error text where feasible (the "chaos" tactic Go and Abseil use for map iteration).
- You **SHOULD** version the interface and change unspecified behavior early and often, before a de facto contract forms.
- When you must change a relied-upon behavior, you **SHOULD** deprecate with discipline: announce, provide a migration path, and allow a window — do not break silently.
- You **MUST NOT** assume an undocumented behavior is safe to change just because the docs never promised it; with enough consumers, someone depends on it.

