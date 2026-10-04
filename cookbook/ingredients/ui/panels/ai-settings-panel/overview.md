
A settings panel for configuring AI/LLM provider integration. Appears as a category within the settings window (see `settings-window.md`). This spec covers both the settings UI and the provider interface pattern.

The panel follows the interface-first pattern (Rules 17-19): settings are stored locally, the actual AI provider is injected via protocol/interface. The settings panel configures which provider, model, and credentials to use. The application consumes AI capabilities exclusively through the `AIProvider` protocol — the settings panel is the configuration surface, not the integration point.

This is BOTH a settings UI spec AND an interface design for AI integration. The UI configures preferences; the interface abstracts the provider. They are decoupled by design — the panel writes configuration, and the provider factory reads it to construct the active provider.

