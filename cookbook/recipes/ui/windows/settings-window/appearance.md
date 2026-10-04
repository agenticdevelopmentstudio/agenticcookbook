
```
┌──────────────────────────────────────────────┐
│ Settings                                     │
├────────────┬─────────────────────────────────┤
│            │                                 │
│ General    │  Setting Label         [control]│
│ Appearance │  Setting Label         [control]│
│ Advanced   │  Setting Label         [control]│
│            │                                 │
│            │                                 │
│            │                                 │
│            │                                 │
├────────────┴─────────────────────────────────┤
```

- **Layout variant — Sidebar** (default, for 4+ categories): Horizontal split view — sidebar on left, content panel on right
- **Layout variant — Tab bar** (for fewer categories or per platform convention): Horizontal tab bar at top, content panel below. Use when there are fewer than 5 categories or when the platform convention prefers tabs (e.g., macOS System Settings pre-Ventura). This is a **Design Decision** — document which variant is chosen.
- **Sidebar width**: Fixed or narrow resizable range (150–220pt)
- **Sidebar selection**: Platform-native selection highlight
- **Content layout**: Labeled rows — label on left, control on right. Group related settings with section headers.
- **Controls**: Native controls only — toggles, dropdowns/pickers, sliders, text fields, steppers
- **Category icons**: Optional — whether to show icons alongside category names is a **Design Decision** that MUST be approved by the user

