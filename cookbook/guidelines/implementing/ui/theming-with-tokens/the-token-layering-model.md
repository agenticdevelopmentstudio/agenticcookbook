
Keep three tiers so themes only rebind the middle one:

| Tier | Example | Themed? |
|------|---------|---------|
| **Primitive** (raw scale) | `blue-600 = #2563EB` | No — a fixed palette |
| **Semantic** (role) | `color.text.primary`, `color.surface.raised` | Yes — each theme maps it to a primitive |
| **Component** (optional) | `button.primary.background` | Aliases a semantic token |

- Components **MUST** consume only semantic (or component) tokens, never primitives or hard-coded
  literals. This is what makes theming automatic.
- Each theme **SHOULD** be authored as a value set that rebinds every semantic token — same keys,
  different primitive references. Light, dark, and high-contrast are sibling sets, not branches in code.

