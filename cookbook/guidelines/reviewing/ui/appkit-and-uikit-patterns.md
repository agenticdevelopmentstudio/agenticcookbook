---
id: a48af237-db64-40ae-9574-e579c107de83
title: "AppKit and UIKit patterns"
domain: agenticdevelopercookbook://guidelines/reviewing/ui/appkit-and-uikit-patterns
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Review AppKit and UIKit code for responder-chain use, weak delegates, main-thread discipline, paired lifecycle setup and teardown, and deliberate state restoration."
platforms:
  - ios
  - macos
languages:
  - swift
  - objective-c
tags:
  - appkit
  - uikit
  - review
  - lifecycle
  - responder-chain
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/ui/appkit-and-uikit-patterns
  - agenticdevelopercookbook://guidelines/reviewing/platform-integration/prefer-explicit-apple-apis
references:
  - https://developer.apple.com/documentation/uikit/using-responders-and-the-responder-chain-to-handle-events
  - https://developer.apple.com/documentation/uikit/preserving-your-app-s-ui-across-launches
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - code-review
---

# AppKit and UIKit patterns

Review changed AppKit and UIKit code against [AppKit and UIKit patterns](agenticdevelopercookbook://guidelines/implementing/ui/appkit-and-uikit-patterns).

## Responder chain

- Actions that belong to the frontmost object use a `nil` target and are implemented on a responder in the chain. Actions that belong to one object name that object.
- No action reaches its handler through a global or a stored back-reference when the chain would deliver it.
- A `nextResponder` override has a stated reason.

## Delegates

- Every delegate and data-source property is `weak`. Flag a strong one unless a comment explains the ownership.
- Delegate protocols are narrow. No callback carries mutable shared state.

## Main thread

- Every call that touches a view, window or view-controller state is on the main thread or in a `@MainActor` context.
- No `DispatchQueue.main.sync` from code that may already be on the main thread, and no blocking wait on another queue from the main thread.
- Slow work runs off the main thread, and only the result is applied on it.

## Lifecycle

- One-time setup is in the load callbacks; per-appearance work is in the appear callbacks; nothing reads `view` in an initializer.
- Every observer, timer or registration added in one callback is removed in its counterpart.
- Child view controllers are added and removed with the full containment sequence.
- On macOS, window content lives in a view controller, not in the window controller.

## State restoration

- Restoration identifiers are assigned only to view controllers that should be restored. Saved data is identifiers and small values.
- Saved state carries a version, and an old version falls back to the normal launch UI.

## Why this matters

These are the defects that pass a quick test and fail in the field: a delegate that leaks a screen, a callback on the wrong thread, an observer that is never removed. A fixed checklist finds them without running the app.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
