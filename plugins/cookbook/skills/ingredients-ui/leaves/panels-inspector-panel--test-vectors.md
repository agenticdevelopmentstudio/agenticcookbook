<!-- leaf: ingredients-ui/panels-inspector-panel--test-vectors · source: ingredients/ui/panels/inspector-panel.md -->

# Inspector Panel

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| inspector-001 | slide-in-right | Toggle inspector on | Panel slides in from the right side |
| inspector-002 | fixed-width-250 | Measure panel width | Panel width is 250pt |
| inspector-003 | toolbar-toggle-button | Click toolbar inspector button | Panel visibility toggles |
| inspector-004 | persist-visibility | Show inspector, quit app, relaunch | Inspector is visible on relaunch |
| inspector-005 | persist-visibility | Hide inspector, quit app, relaunch | Inspector is hidden on relaunch |
| inspector-006 | form-metadata-display, uttype-file-type | Select a Markdown file (README.md) | Name shows "README.md", Type shows "Markdown" or UTType description |
| inspector-007 | size-files-only, byte-count-format | Select a 4,200-byte file | Size row shows "4.2 KB" (or locale-appropriate equivalent) |
| inspector-008 | size-files-only | Select a directory | Size row is not displayed |
| inspector-009 | date-format-medium | Select a file modified on 2026-03-25 at 14:30 | Modified shows "Mar 25, 2026 at 2:30 PM" (or locale equivalent) |
| inspector-010 | git-status-indicator, hide-clean-git-status | Select a modified file in a git repo | Git Status row shows orange "M" badge with label "Modified" |
| inspector-011 | hide-clean-git-status | Select a clean/committed file in a git repo | Git Status row is not displayed |
| inspector-012 | hide-clean-git-status | Select a file in a non-git project | Git Status row is not displayed |
| inspector-013 | empty-state-display | No file selected, inspector visible | Empty state shows icon and "Select a file to inspect" |
| inspector-014 | selectable-path-text | Select a file, attempt to select the path text | Path text is selectable and copyable |
| inspector-015 | path-caption-truncate | Select a file with a very long path | Path truncates in the middle with ellipsis |
| inspector-016 | grouped-form-style | Inspect form style | Form uses grouped style |
| inspector-017 | toggle-accessible-label, toggle-state-announce | Enable VoiceOver, activate toolbar toggle | Button announces "Toggle Inspector" and state |
| inspector-018 | keyboard-navigable | Press Tab repeatedly while inspector is open | Focus moves through metadata rows and toggle button |
