
- **button-role**: The control MUST be a `<button>` element (not a link or div).
- **aria-label-descriptive**: The `aria-label` MUST describe the current mode and what clicking will do. Examples:
  - Auto mode: `"Theme: Auto (currently dark). Click to switch to dark."`
  - Dark mode: `"Theme: Dark. Click to switch to light."`
  - Light mode: `"Theme: Light. Click to switch to auto."`
- **tooltip-descriptive**: The `title` attribute MUST describe the current state:
  - Auto: `"Following system (dark)"` or `"Following system (light)"`
  - Dark: `"Dark mode — click for light"`
  - Light: `"Light mode — click for auto"`
- **no-color-only**: The mode MUST NOT be conveyed by color alone. The icon shape (sun vs moon) and the presence/absence of the badge indicator distinguish the three modes.
- **focus-ring**: The button MUST show a visible focus ring when focused via keyboard (`focus-visible`). Use the site's accent color for the ring.

