<!-- leaf: ingredients/infrastructure-window-frame-persistence--states · source: ingredients/infrastructure/window-frame-persistence.md -->

# Window Frame Persistence

## States

| State | Behavior |
|-------|----------|
| Window appears | Autosave name applied, previous frame restored if saved |
| Window moved/resized | Frame auto-saved by AppKit (no manual intervention needed) |
| Window closed | `onClose` callback fired, observers cleaned up |
| No saved frame | Window uses default layout |
