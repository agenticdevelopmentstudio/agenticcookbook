
- **tap-toggles-pane**: Tapping anywhere on the header MUST toggle the associated pane's visibility.
- **chevron-animation**: The disclosure chevron MUST animate between collapsed (pointing right) and expanded (pointing down) states.
- **collapse-expand-animation**: The pane collapse/expand MUST animate with an ease-in-out curve (~0.2s duration).
- **display-title**: The header MUST display a title.
- **optional-leading-icon**: The header MAY display an icon to the left of the title (e.g., a file icon for an editor pane header).
- **optional-subtitle**: The header MAY display a subtitle or secondary label to the right of the title (e.g., a filename).
- **header-always-visible**: The header MUST remain visible when the pane is collapsed — it is the mechanism to re-expand.
- **persist-collapse-state**: The collapsed/expanded state MUST be persisted per-pane so it survives app restart.

