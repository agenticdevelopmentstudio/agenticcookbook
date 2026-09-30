<!-- leaf: ingredients/infrastructure-window-frame-persistence--test-vectors · source: ingredients/infrastructure/window-frame-persistence.md -->

# Window Frame Persistence

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| frame-001 | persist-frame-autosave | Open window, move to (200,300), close, reopen | Window appears at (200,300) |
| frame-002 | persist-frame-autosave | Open window, resize to 800×600, close, reopen | Window appears at 800×600 |
| frame-003 | unique-autosave-name | Open two document windows | Each has unique autosave name, saved independently |
| frame-004 | invisible-background-view | Inspect view hierarchy | No visible NSView from this component |
| frame-005 | on-close-callback | Close window with onClose callback | Callback fires |
