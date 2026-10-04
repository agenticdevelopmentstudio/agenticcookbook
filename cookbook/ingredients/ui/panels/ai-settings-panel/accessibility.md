
- **control-a11y-labels**: All form controls MUST have accessible labels matching their visible labels (e.g., "Enable AI Features", "Provider", "API Key", "Model").
- **status-a11y-label**: The connection status indicator MUST have an accessibility label that includes both the status and any error message (e.g., "Connection status: Disconnected. Authentication failed.").
- **status-not-color-only**: The status dot MUST NOT rely solely on color to convey state. The text label ("Connected", "Disconnected", "Not tested") MUST always be displayed alongside the dot.
- **secure-field-announce**: The secure API key field MUST be announced as a secure text field by screen readers.
- **disabled-state-announce**: When controls are disabled (AI features off), screen readers MUST announce them as disabled/dimmed.
- **keyboard-tab-order**: The panel MUST be fully keyboard-navigable. Tab order MUST follow the visual layout top to bottom: Enable toggle, Provider picker, API Key field, Model picker, Custom model field, Endpoint fields (if visible), Test Connection button.
- **test-loading-announce**: The Test Connection button MUST announce its loading state to screen readers when a test is in progress (e.g., "Test Connection, testing...").

### Auto-enable behavior

- **auto-enable-on-key-entry**: When the user enters a new API key, the "Enable AI Features" toggle MUST be automatically set to `true` (on). The user MAY subsequently disable it manually.

### Quick Chat

- **inline-chat-control**: The panel MUST include an inline chat control (see `ingredient.ui.component.ai-chat-control`) at the bottom of the panel, below all configuration fields. This allows the user to verify the configuration by sending a real message.
- **chat-respects-toggle**: The chat control MUST respect the "Enable AI Features" toggle — when AI features are disabled, sending messages MUST be blocked with an inline error message.

