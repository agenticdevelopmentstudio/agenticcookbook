---
type: ingredient
status: accepted
---

## Overview

Chat composer component fixture.

## Behavioral Requirements

Chat composer accepts text input.

## Appearance

Chat composer has input field and send button.

## States

Chat composer has default and active states.

## Accessibility

Chat composer is voice-accessible.

## Conformance Test Vectors

Chat composer passes input tests.

## Edge Cases

Chat composer handles multiline text.

## Configuration

Chat composer accepts placeholder text.

## Platform Notes

- **SwiftUI**: Use `TextField` and `Button`.
- **Compose**: `TextField` and `Button`.
- **React/Web**: `packages/ui/chat-composer.tsx`.
- **AppKit / UIKit**: `NSTextField` and `NSButton`.
- **WinUI 3**:

## Design Decisions

Chat composer uses primary color for send button.
