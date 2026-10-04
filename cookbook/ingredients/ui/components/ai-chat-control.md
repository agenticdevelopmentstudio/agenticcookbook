---
id: f9f12465-9f73-40ef-b9f6-d124090781f5
title: "AI Chat Control"
domain: agenticdevelopercookbook://ingredients/ui/components/ai-chat-control
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-04-05
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Compact inline chat control for multi-turn AI conversation with scrollable history and multi-provider support"
platforms:
  - ios
  - kotlin
  - macos
  - swift
  - typescript
  - web
  - windows
tags:
  - ai-chat-control
  - component
  - ui
depends-on: []
related:
  - ingredient.ui.panel.ai-settings-panel
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
---

# AI Chat Control

## Overview

A compact, inline chat control for conversing with a configured AI provider. Supports multi-turn conversation with scrollable message history, text input, and asynchronous response handling. Designed for embedding in settings panels, sidebars, or inspector views. A full-size variant for standalone windows can compose this control with additional chrome (toolbar, model picker, conversation management).

This spec covers the chat control only — provider configuration (API key, model, endpoint) is managed externally via the AI settings panel (see `ingredient.ui.panel.ai-settings-panel`).

## Terminology

| Term | Definition |
|------|-----------|
| Message | A single unit of conversation: user input, assistant response, or error |
| Conversation | An ordered sequence of messages in a single chat session |
| Provider | The AI backend that generates responses (Anthropic, OpenAI, Google, Custom) |
| Typing indicator | Animated placeholder shown while waiting for an AI response |
| Mini variant | Fixed-height version for embedding in panels (~200pt) |
| Full variant | Flexible-height version for standalone windows (future) |

## Behavioral Requirements

### Conversation

- **ordered-message-history**: The control MUST maintain an ordered list of messages representing the full conversation history.
- **message-roles**: Messages MUST have one of three roles: `user`, `assistant`, or `error`.
- **vertical-scroll**: The message area MUST scroll vertically when content exceeds the visible area.
- **auto-scroll-new-message**: The control MUST auto-scroll to the newest message when a new message is appended.
- **auto-scroll-typing-indicator**: The control MUST auto-scroll to the typing indicator when it appears.
- **scroll-animation-timing**: Auto-scroll animation duration MUST be 0.2 seconds with ease-out timing.

### Input

- **text-input-field**: The control MUST display a text input field at the bottom.
- **enter-key-submit**: Pressing Enter/Return in the text field MUST submit the message (same as tapping the send button).
- **send-button-display**: A send button MUST be displayed to the right of the text field.
- **send-button-disabled-empty**: The send button MUST be disabled when the input field is empty (after trimming whitespace).
- **clear-input-after-send**: After sending, the input field MUST be cleared immediately.
- **block-send-while-loading**: The control MUST NOT allow sending while a response is in progress (loading state).

### API Integration

- **send-full-history**: The control MUST send the full conversation history (excluding error messages) with each request, enabling multi-turn conversation.
- **multi-provider-support**: The control MUST support all providers defined in `ai-settings-panel.md` provider-picker-options: Anthropic, OpenAI, Google (Gemini), and Custom (OpenAI-compatible).
- **secure-key-retrieval**: API keys MUST be read from platform secure storage (Keychain / EncryptedSharedPreferences / HttpOnly cookies) at request time. Keys MUST NOT be cached in the view model or held in memory longer than the request.
- **max-response-tokens**: The maximum response length MUST be 256 tokens for the mini variant. Implementations MAY make this configurable for the full variant.
- **request-timeout**: Request timeout MUST be 30 seconds.
- **check-ai-enabled**: The control MUST check whether AI features are enabled (via the `ai-settings-panel.md` enable toggle) before sending. If disabled, an error message MUST be displayed: "AI features are disabled — enable them above."
- **no-api-key-error**: If no API key is configured, an error message MUST be displayed: "No API key configured."

### Error Handling

- **inline-error-display**: API errors MUST be displayed as error-role messages in the conversation, not as alerts or dialogs.
- **recoverable-after-error**: After an error, the user MUST be able to continue sending messages (the control does not enter a stuck state).
- **extract-provider-error**: HTTP error responses MUST extract the provider's error message from the response body (e.g., `json.error.message`) and display it. If parsing fails, display "HTTP {statusCode}".

### History Management

- **clear-history-action**: A "Clear" action MUST be available to reset the conversation history.
- **clear-removes-all**: Clearing history MUST remove all messages (user, assistant, and error).
- **ephemeral-history**: Conversation history MUST NOT be persisted across app launches. It is ephemeral, in-memory only.

## Appearance

### Mini variant layout

```
┌──────────────────────────────────────┐
│  User message              ▐ accent  │  ← right-aligned
│  ▌ secondary  Assistant message      │  ← left-aligned
│  ▌ red        Error message          │  ← left-aligned
│  ▌ ...                               │  ← typing indicator
├──────────────────────────────────────┤
│  [Message...                   ] [➤] │  ← input row
└──────────────────────────────────────┘
```

### Container
- **Corner radius**: 8pt
- **Border**: 1pt, system quaternary color
- **Background**: system background at 0.5 opacity
- **Mini variant height**: 200pt (fixed, not resizable)

### Message bubbles
- **Font**: System font, 12pt
- **Horizontal padding**: 8pt
- **Vertical padding**: 5pt
- **Corner radius**: 6pt
- **Text selection**: Enabled
- **Minimum spacer**: 40pt on the opposite side (prevents full-width bubbles)

| Role | Background | Foreground | Alignment |
|------|-----------|-----------|-----------|
| User | Accent color, 15% opacity | Primary | Right-aligned |
| Assistant | Secondary color, 10% opacity | Primary | Left-aligned |
| Error | Red, 10% opacity | Red | Left-aligned |

### Message area
- **Vertical spacing** between messages: 8pt
- **Padding**: 8pt all sides

### Input row
- **Font**: System font, 12pt, plain style (no border)
- **Placeholder**: "Message..."
- **HStack spacing**: 6pt
- **Horizontal padding**: 8pt
- **Vertical padding**: 6pt

### Send button
- **Icon**: arrow.up.circle.fill (SF Symbols) / equivalent per platform
- **Size**: 16pt
- **Color**: System tint/accent
- **Style**: Plain (no button chrome)

### Typing indicator
- **Animation**: Cycling dots (1→2→3→1), 0.4 second interval
- **Font**: System monospaced, 12pt
- **Color**: Secondary
- **Background**: Secondary color, 10% opacity
- **Corner radius**: 6pt
- **Alignment**: Left-aligned (same as assistant messages)

## States

| State | Behavior |
|-------|----------|
| Empty | No messages; message area is blank; input field active |
| Conversing | Messages visible; input field active; send button enabled when text present |
| Loading | Typing indicator visible; send button replaced with spinner; input field active but send disabled |
| Error displayed | Error message visible in red; input field active; user can continue chatting |
| AI disabled | Sending blocked; error message shown if attempted |
| No API key | Sending blocked; error message shown if attempted |

## Accessibility

- **message-a11y-label**: Each message bubble MUST have an accessibility label that includes the role and content (e.g., "You said: Hello", "Assistant said: Hi there").
- **error-screen-reader**: Error messages MUST be announced by screen readers when they appear.
- **send-button-a11y-label**: The send button MUST have an accessibility label: "Send message".
- **send-disabled-announce**: The send button MUST announce its disabled state when the input is empty.
- **typing-a11y-label**: The typing indicator MUST have an accessibility label: "Waiting for response".
- **keyboard-tab-order**: The input field MUST be keyboard-focusable. Tab order: input field → send button.
- **minimum-tap-target**: Minimum tap target for the send button: 44x44pt (iOS), 48x48dp (Android).

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| chat-001 | ordered-message-history | Send "Hello", receive response, send "How are you?" | Three messages in order: user, assistant, user |
| chat-002 | vertical-scroll | Send enough messages to overflow visible area | Message area scrolls; earlier messages accessible by scrolling up |
| chat-003 | auto-scroll-new-message, auto-scroll-typing-indicator, scroll-animation-timing | Send a message | View auto-scrolls to new message with 0.2s ease-out animation |
| chat-004 | enter-key-submit | Type "Hello" and press Enter | Message sent; input cleared |
| chat-005 | send-button-disabled-empty | Input field is empty, observe send button | Send button is disabled |
| chat-006 | send-button-disabled-empty | Input field contains only whitespace | Send button is disabled |
| chat-007 | block-send-while-loading | Send message while response is in progress | Second send is blocked |
| chat-008 | send-full-history | Send "Hello", receive response, send "What did I just say?" | Second request includes both previous messages in history |
| chat-009 | secure-key-retrieval | Send message, inspect memory after response | API key is not retained in view model properties |
| chat-010 | check-ai-enabled | Disable AI features, send message | Error: "AI features are disabled — enable them above" |
| chat-011 | no-api-key-error | No API key configured, send message | Error: "No API key configured" |
| chat-012 | inline-error-display | Send message with invalid API key | Error message displayed inline, not as alert |
| chat-013 | recoverable-after-error | Receive an error, then send another message | Second message sends successfully (not stuck) |
| chat-014 | extract-provider-error | Send message, server returns 401 with `{"error":{"message":"invalid key"}}` | Error shows "invalid key", not "HTTP 401" |
| chat-015 | clear-history-action, clear-removes-all | Send messages, then clear history | All messages removed; message area is empty |
| chat-016 | ephemeral-history | Send messages, quit app, relaunch | Chat history is empty after relaunch |

## Edge Cases

- **Extremely long response**: Message bubble wraps text; does not truncate. Scroll area accommodates.
- **Extremely long input**: Text field accepts input without truncation. Long messages display correctly in bubble.
- **Rapid send attempts**: Only the first send is accepted while loading; subsequent attempts are ignored (block-send-while-loading).
- **Network timeout**: After 30 seconds, display timeout error message. User can retry.
- **Provider returns empty response**: Display "(Empty response)" as assistant message.
- **Provider returns malformed JSON**: Display "(Unable to parse response)" as assistant message.
- **Concurrent provider change**: If the user changes provider while a request is in flight, the in-flight response is still displayed. The next request uses the new provider.
- **Keychain unavailable**: Display error "No API key configured" (same as missing key).

## Configuration

This ingredient has no configurable options.

## Deep Linking

| Platform | URL Pattern | Behavior |
|----------|-------------|----------|
| Apple | `{{app_scheme}}://settings/ai#chat` | Opens AI settings and scrolls to Quick Chat section |

## Localization

| String Key | Default (en) | Context |
|-----------|-------------|---------|
| `ai_chat.placeholder` | Message... | Input field placeholder |
| `ai_chat.send` | Send message | Send button accessibility label |
| `ai_chat.typing` | Waiting for response | Typing indicator accessibility label |
| `ai_chat.clear` | Clear | Clear history button label |
| `ai_chat.error.disabled` | AI features are disabled — enable them above | AI toggle is off |
| `ai_chat.error.no_key` | No API key configured | No key in secure storage |
| `ai_chat.error.empty_response` | (Empty response) | Provider returned no content |
| `ai_chat.error.parse_failed` | (Unable to parse response) | Response JSON malformed |

## Accessibility Options

| Option | Behavior |
|--------|----------|
| Reduce Motion | Auto-scroll is instant (no animation); typing indicator uses static "..." instead of cycling dots |
| Reduce Transparency | Container background uses opaque fill instead of 0.5 opacity |
| Increase Contrast | Message bubble backgrounds use higher opacity (user: 25%, assistant: 20%, error: 20%) |
| Differentiate Without Color | Error messages include a leading "Error:" prefix in addition to red color |
| VoiceOver / TalkBack | Messages announced with role prefix; typing indicator announced; send state announced |
| Bold Text | Message text and input field respond to system bold text setting |

## Feature Flags

| Flag Key | Default | Description |
|----------|---------|-------------|
| `{{app_prefix}}.ai_chat` | `true` | Enables the inline chat control |
| `{{app_prefix}}.ai_chat.max_tokens` | `256` | Maximum response tokens for the mini variant |

## Analytics

| Event | Properties | When |
|-------|-----------|------|
| `ai_chat.message_sent` | `{ provider: string, model: string }` | User sends a message |
| `ai_chat.response_received` | `{ provider: string, model: string, duration_ms: int }` | Assistant response received |
| `ai_chat.error` | `{ provider: string, error: string }` | API error or validation error |
| `ai_chat.cleared` | `{ message_count: int }` | User clears conversation |

## Privacy

- **Data collected**: Message content (user prompts and AI responses), provider and model identifiers, error messages.
- **Sensitive data**: User prompts may contain sensitive content. API keys are transient (read from secure storage, used for one request, not retained).
- **Storage**: Conversation history is in-memory only (ephemeral-history). Not persisted to disk, database, or any storage layer.
- **Transmission**: Messages are sent to the configured AI provider endpoint over TLS/HTTPS. They are not sent to analytics, crash reporting, or any other service. Message content MUST NOT appear in log output.
- **Retention**: Conversation exists only for the lifetime of the control instance. Destroyed on navigation away or app termination.

## Logging

Subsystem: `{{bundle_id}}` | Category: `AIChatControl`

| Event | Level | Message |
|-------|-------|---------|
| Message sent | debug | `AIChatControl: message sent to "{{provider}}" model "{{model}}"` |
| Response received | debug | `AIChatControl: response received ({{duration}}ms, {{token_count}} chars)` |
| Request failed | debug | `AIChatControl: request failed: {{error}}` |
| History cleared | debug | `AIChatControl: history cleared ({{count}} messages)` |
| AI disabled | debug | `AIChatControl: send blocked — AI features disabled` |
| No API key | debug | `AIChatControl: send blocked — no API key configured` |

**Critical logging rule**: Message content (user prompts and AI responses) MUST NEVER appear in log output at any level.

## Platform Notes

- **SwiftUI (macOS / iOS / visionOS)**: Use `ScrollViewReader` with `ScrollView` containing `LazyVStack` for the message area. Use `.id()` on each message for scroll targeting. Input field: `TextField` with `.plain` style and `.onSubmit` for Enter key handling. Send button: `Button` with `.plain` style and SF Symbol icon. Typing indicator: `Timer.publish` driving dot count with modulo arithmetic. API calls: `Task.detached(priority: .userInitiated)` with `URLSession.shared.data(for:)`. Update UI via `await MainActor.run {}`. Read API key with `SecItemCopyMatching` at request time.
- **Compose (Android)**: Use `LazyColumn` with `rememberLazyListState()` for auto-scroll. Input: `OutlinedTextField` with `keyboardActions` for Enter. Send button: `IconButton` with Material icon. Typing indicator: `LaunchedEffect` with `delay`. API calls: `viewModelScope.launch(Dispatchers.IO)` with `HttpURLConnection` or OkHttp. Read API key from `EncryptedSharedPreferences` at request time.
- **React / Web**: Use a `div` with `overflow-y: auto` and `scrollIntoView()` for auto-scroll. Input: `<input>` with `onKeyDown` for Enter. Send button: `<button>` with icon. Typing indicator: `setInterval` cycling dot count. API calls: `fetch` with `AbortController` for timeout. API key: retrieve from server-side secure storage via authenticated endpoint.

## Design Decisions

**Mini variant only (v1.0.0)**: The initial spec covers only the mini variant (fixed 200pt height, embedded in settings). The full variant (flexible height, standalone window, conversation management) is deferred to a future version.

**Decision**: No streaming support in v1.0.0.
**Rationale**: Streaming adds complexity (SSE parsing, incremental rendering) without significant benefit at 256 max tokens. The full variant SHOULD add streaming.
**Approved**: pending

**Decision**: Conversation history is ephemeral (not persisted).
**Rationale**: The primary use case is quick verification of AI configuration. Persistent history adds storage and privacy concerns without matching the use case.
**Approved**: pending

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
