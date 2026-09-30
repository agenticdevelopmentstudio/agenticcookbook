<!-- leaf: ingredients-ui/components-collapsible-pane-header--test-vectors · source: ingredients/ui/components/collapsible-pane-header.md -->

# Collapsible Pane Header

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pane-001 | tap-toggles-pane | Tap header when expanded | Pane collapses with animation |
| pane-002 | tap-toggles-pane | Tap header when collapsed | Pane expands with animation |
| pane-003 | chevron-animation | Toggle pane | Chevron animates between down↔right |
| pane-004 | header-always-visible | Collapse pane | Header still visible, pane content hidden |
| pane-005 | persist-collapse-state | Collapse pane, restart app | Pane opens collapsed |
| pane-006 | keyboard-toggle | Focus header with keyboard, press Return | Pane toggles |
