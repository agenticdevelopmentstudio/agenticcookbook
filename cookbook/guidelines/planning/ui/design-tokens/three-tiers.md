
Use three layers so values change in one place and intent stays stable:

| Tier | Holds | Example | May code reference it? |
|------|-------|---------|------------------------|
| Primitive (global) | Raw, context-free values | `color.blue.600 = #2563EB` | No |
| Semantic (alias) | Intent, references a primitive | `color.action.primary → color.blue.600` | Yes |
| Component | Per-component intent | `button.bg.default → color.action.primary` | Yes |

- Components and application code **MUST** reference semantic or component tokens only; they **MUST NOT** reference primitives directly.
- Semantic and component tokens **MUST** be aliases (DTCG `{token.path}` references), not duplicated literals, so a primitive change cascades automatically.
- Tier count **SHOULD** stay at three; add a component tier only when a real second consumer exists (YAGNI) — a flat alias layer is enough for a single app.

