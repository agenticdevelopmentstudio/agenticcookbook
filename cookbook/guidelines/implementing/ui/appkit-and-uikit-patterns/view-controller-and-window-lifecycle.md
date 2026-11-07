
- A view controller loads its view lazily. Accessing `view` the first time creates it, so one-time setup MUST go in the load callbacks and an initializer MUST NOT touch `view`.
- Work that must happen every time the view appears MUST go in the appear and disappear callbacks, and setup MUST be paired with teardown (observers, timers, notification registrations) in the matching pair of callbacks.
- On macOS (10.10 and later) `NSViewController` offers the same style of lifecycle methods, and its actions take part in the responder chain, so window content SHOULD live in view controllers and `NSWindowController` SHOULD be kept for window-level concerns.
- Containment is explicit: code MUST add a child view controller, add its view, then tell the child it moved to its parent, and reverse the steps to remove it.

