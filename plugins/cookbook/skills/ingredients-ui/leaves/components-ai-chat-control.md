<!-- leaf: ingredients-ui/components-ai-chat-control · source: ingredients/ui/components/ai-chat-control.md -->

**Rules** (cite as `ingredients-ui/components-ai-chat-control#<slug>`):

- `ordered-message-history` MUST
- `message-roles` MUST
- `vertical-scroll` MUST
- `auto-scroll-new-message` MUST
- `auto-scroll-typing-indicator` MUST
- `scroll-animation-timing` MUST
- `text-input-field` MUST
- `enter-key-submit` MUST
- `send-button-display` MUST
- `send-button-disabled-empty` MUST
- `clear-input-after-send` MUST
- `block-send-while-loading` MUST
- `send-full-history` MUST
- `multi-provider-support` MUST
- `secure-key-retrieval` MUST
- `max-response-tokens` MUST
- `request-timeout` MUST
- `check-ai-enabled` MUST
- `no-api-key-error` MUST
- `inline-error-display` MUST
- `recoverable-after-error` MUST
- `extract-provider-error` MUST
- `clear-history-action` MUST
- `clear-removes-all` MUST
- `ephemeral-history` MUST
- `message-a11y-label` MUST
- `error-screen-reader` MUST
- `send-button-a11y-label` MUST
- `send-disabled-announce` MUST
- `typing-a11y-label` MUST
- `keyboard-tab-order` MUST
- `transmission` MUST — Messages are sent to the configured AI provider endpoint over TLS/HTTPS. They are not sent to analytics, crash …

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

## Accessibility

- **message-a11y-label**: Each message bubble MUST have an accessibility label that includes the role and content (e.g., "You said: Hello", "Assistant said: Hi there").
- **error-screen-reader**: Error messages MUST be announced by screen readers when they appear.
- **send-button-a11y-label**: The send button MUST have an accessibility label: "Send message".
- **send-disabled-announce**: The send button MUST announce its disabled state when the input is empty.
- **typing-a11y-label**: The typing indicator MUST have an accessibility label: "Waiting for response".
- **keyboard-tab-order**: The input field MUST be keyboard-focusable. Tab order: input field → send button.
- **minimum-tap-target**: Minimum tap target for the send button: 44x44pt (iOS), 48x48dp (Android).

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

