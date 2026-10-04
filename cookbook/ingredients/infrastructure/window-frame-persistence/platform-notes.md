
- **SwiftUI (macOS)**: Implement as `NSViewRepresentable`. In `makeNSView`, return an empty `NSView`. In `updateNSView`, dispatch to main queue to access `view.window`, then call `window.setFrameAutosaveName(name)`. Observe `NSWindow.willCloseNotification` for close callback. Attach via `.background(WindowAccessor(name: "...", onClose: { }))`.
- **Other platforms**: Not applicable. iOS, Android, and Web handle window/view positioning differently (iOS has no user-movable windows, Android has activity lifecycle, Web uses CSS/URL state).

