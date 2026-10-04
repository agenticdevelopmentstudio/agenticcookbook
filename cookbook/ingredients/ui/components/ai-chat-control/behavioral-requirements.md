
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

