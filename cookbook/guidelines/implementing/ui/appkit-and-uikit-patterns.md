---
id: 8aa22a6b-2328-4a2d-8fe3-53c339390808
title: "AppKit and UIKit patterns"
domain: agenticdevelopercookbook://guidelines/implementing/ui/appkit-and-uikit-patterns
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Work with the responder chain, delegates, the main thread and the view-controller and window lifecycle instead of around them, and opt in to state restoration deliberately."
platforms:
  - ios
  - macos
languages:
  - swift
  - objective-c
tags:
  - appkit
  - uikit
  - responder-chain
  - delegates
  - lifecycle
  - state-restoration
depends-on:
  - agenticdevelopercookbook://guidelines/implementing/platform-integration/prefer-explicit-apple-apis
related:
  - agenticdevelopercookbook://guidelines/implementing/concurrency/swift6-strict-concurrency
  - agenticdevelopercookbook://guidelines/implementing/language/swift
  - agenticdevelopercookbook://guidelines/implementing/language/objective-c
  - agenticdevelopercookbook://guidelines/reviewing/ui/appkit-and-uikit-patterns
references:
  - https://developer.apple.com/documentation/uikit/using-responders-and-the-responder-chain-to-handle-events
  - https://developer.apple.com/documentation/uikit/uiviewcontroller
  - https://developer.apple.com/documentation/appkit/nsviewcontroller
  - https://developer.apple.com/documentation/uikit/preserving-your-app-s-ui-across-launches
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - ui-implementation
  - platform-integration
---

# AppKit and UIKit patterns

[Use AppKit and UIKit, not SwiftUI](agenticdevelopercookbook://guidelines/implementing/platform-integration/prefer-explicit-apple-apis) chooses the frameworks. This guideline covers how to use them: the patterns that every AppKit and UIKit screen depends on, and the mistakes that follow from fighting them.

## Responder chain

- Events and action messages travel a chain of responders. A view that does not handle an event passes it to its superview; a view controller sits in the chain between its root view and that view's superview; the window and then the application object come after.
- A control whose target is `nil` sends its action up the chain until an object implements the method. Use that for commands that belong to whoever is frontmost (copy, delete, undo), and set an explicit target for commands that belong to one object.
- Implement an action on the object that owns the behavior, usually the view controller, not on a distant object reached through a stored reference.
- To insert an object into the chain, override `nextResponder` and return it. Do this sparingly; the default chain is what users and the system expect.
- A gesture recognizer sees touches before its view does. If it fails to recognize them, the view gets them.

## Delegates and data sources

- Delegate and data-source properties are `weak` (or `unowned(unsafe)` on old APIs) so the owner does not keep its delegate alive and the delegate does not keep its owner alive.
- Define a delegate as a protocol with narrow, named callbacks. Optional methods are acceptable in Objective-C protocols; in Swift prefer a small required protocol plus default extension methods.
- A delegate callback is a notification that something happened or a request for a decision. Do not use it to move large state between objects; pass a value or use a closure for a single reply.

## Main thread

- Touch views, windows, layers that back views, and view-controller state only on the main thread. Mark UI-facing types `@MainActor` and follow [Adopt Swift 6 strict concurrency incrementally](agenticdevelopercookbook://guidelines/implementing/concurrency/swift6-strict-concurrency).
- Do slow work (disk, network, decoding, image processing) off the main thread and hop back only to apply the result.
- Do not block the main thread waiting for another queue or task.

## View controller and window lifecycle

- A view controller loads its view lazily. Accessing `view` the first time creates it, so do one-time setup in the load callbacks and never touch `view` in an initializer.
- Put work that must happen every time the view appears in the appear and disappear callbacks, and pair setup with teardown (observers, timers, notification registrations) in the matching pair of callbacks.
- On macOS (10.10 and later) `NSViewController` offers the same style of lifecycle methods, and its actions take part in the responder chain, so keep window content in view controllers and keep `NSWindowController` for window-level concerns.
- Containment is explicit: add a child view controller, add its view, then tell the child it moved to its parent, and reverse the steps to remove it.

## State restoration

- State restoration is opt-in. On iOS, the app delegate implements the secure save and restore callbacks (`application(_:shouldSaveSecureApplicationState:)` and `application(_:shouldRestoreSecureApplicationState:)`), assigns restoration identifiers to the view controllers to preserve, and encodes only the data needed to rebuild each one.
- Save identifiers and small values, not model objects. Rebuild the screen from the model on restore.
- Version the saved state and refuse to restore from an incompatible version, then fall back to the normal launch UI.

## Why this matters

AppKit and UIKit already solve routing, ownership of callbacks, threading and lifecycle. Code that uses those mechanisms is short and behaves like the rest of the platform; code that works around them (global references for actions, strong delegates, UI work on background queues) is where retain cycles, crashes and missed teardown come from.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
