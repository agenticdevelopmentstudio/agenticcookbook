
- **Data collected**: Message content (user prompts and AI responses), provider and model identifiers, error messages.
- **Sensitive data**: User prompts may contain sensitive content. API keys are transient (read from secure storage, used for one request, not retained).
- **Storage**: Conversation history is in-memory only (ephemeral-history). Not persisted to disk, database, or any storage layer.
- **Transmission**: Messages are sent to the configured AI provider endpoint over TLS/HTTPS. They are not sent to analytics, crash reporting, or any other service. Message content MUST NOT appear in log output.
- **Retention**: Conversation exists only for the lifetime of the control instance. Destroyed on navigation away or app termination.

