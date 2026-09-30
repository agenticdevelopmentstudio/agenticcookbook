<!-- leaf: ingredients/infrastructure-window-frame-persistence · source: ingredients/infrastructure/window-frame-persistence.md -->

**Rules** (cite as `ingredients/infrastructure-window-frame-persistence#<slug>`):

- `persist-frame-autosave` MUST
- `unique-autosave-name` MUST
- `invisible-background-view` MUST
- `delayed-window-access` MUST
- `on-close-callback` MAY
- `cleanup-observers` MUST
- `default-first-launch` SHOULD

# Window Frame Persistence

## Overview

An invisible view modifier that persists a window's position and size between sessions using the platform's native frame autosave mechanism. Attached as a background modifier to any window's root content. On macOS, accesses the hosting `NSWindow` and calls `setFrameAutosaveName`. Supports a close callback for cleanup.

## Behavioral Requirements

- **persist-frame-autosave**: The component MUST persist the window's frame (origin + size) across app sessions using `NSWindow.setFrameAutosaveName`.
- **unique-autosave-name**: Each window MUST have a unique autosave name. For document windows, this SHOULD be derived from the document's file path (e.g., SHA256 hash prefix).
- **invisible-background-view**: The component MUST NOT be visible — it renders as an empty `NSView` added as a background.
- **delayed-window-access**: The component MUST access the hosting `NSWindow` via the view hierarchy after a brief delay (next main run loop cycle) to ensure the window exists.
- **on-close-callback**: The component MAY accept an `onClose` callback that fires when the window is closed (via `NSWindow.willCloseNotification`).
- **cleanup-observers**: The component MUST clean up notification observers on deinit.
- **default-first-launch**: On first launch (no saved frame), the window SHOULD use its default position/size defined elsewhere.

## Configuration

This ingredient has no configurable options.

## Platform Notes

- **SwiftUI (macOS)**: Implement as `NSViewRepresentable`. In `makeNSView`, return an empty `NSView`. In `updateNSView`, dispatch to main queue to access `view.window`, then call `window.setFrameAutosaveName(name)`. Observe `NSWindow.willCloseNotification` for close callback. Attach via `.background(WindowAccessor(name: "...", onClose: { }))`.
- **Other platforms**: Not applicable. iOS, Android, and Web handle window/view positioning differently (iOS has no user-movable windows, Android has activity lifecycle, Web uses CSS/URL state).
