
- A view controller loads its view lazily. Accessing `view` the first time creates it, so do one-time setup in the load callbacks and never touch `view` in an initializer.
- Put work that must happen every time the view appears in the appear and disappear callbacks, and pair setup with teardown (observers, timers, notification registrations) in the matching pair of callbacks.
- On macOS (10.10 and later) `NSViewController` offers the same style of lifecycle methods, and its actions take part in the responder chain, so keep window content in view controllers and keep `NSWindowController` for window-level concerns.
- Containment is explicit: add a child view controller, add its view, then tell the child it moved to its parent, and reverse the steps to remove it.

