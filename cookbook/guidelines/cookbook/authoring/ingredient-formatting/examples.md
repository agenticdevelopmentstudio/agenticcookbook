
A States table for a toggle that can be hovered and selected:

```markdown
| State | Appearance change |
|-------|-------------------|
| Default | Track grey, thumb left |
| Hover | Track one step darker |
| Pressed | Thumb grows 10% |
| Selected | Track accent color, thumb right |
| Disabled | 40% opacity, no hover or press |
| Focused | 2pt focus ring outside the track |
```

Conformance test vectors with all three outcomes for one requirement:

```markdown
| ID | Requirements | Input | Expected |
|----|--------------|-------|----------|
| toggle-001 | must-announce-state | A screen reader focuses the toggle while it is on | "On" is announced: passed |
| toggle-002 | must-announce-state | The toggle announces nothing when focused | failed |
| toggle-003 | must-announce-state | The toggle is hidden from the accessibility tree by its container | inapplicable |
```

A Feature Flags section, in the template's table, each flag with its key and its default:

```markdown
| Flag Key | Default | Description |
|----------|---------|-------------|
| `{{app_prefix}}.component_name` | `true` | Enables this component |
```

A Privacy section for a component that collects nothing:

```markdown
## Privacy

- **Data collected**: None
- **Storage**: None
- **Transmission**: No data leaves the device
- **Retention**: None
- **Encryption in transit**: Not applicable: nothing is transmitted
```

Event names that Firebase Analytics accepts:

```markdown
| Event | Properties | When |
|-------|------------|------|
| `toggle_viewed` | `{}` | Component appears on screen |
| `toggle_changed` | `{ value: boolean }` | User changes the toggle |
```

A Design Decisions entry with its status:

```markdown
- **Decision**: The toggle animates its thumb over 150 ms. **Rationale**: Matches the platform switch. **Approved**: pending
```

