
**UI-stub implementation**: The initial implementation from scratching-post is UI-only — settings are stored via `@AppStorage` but no actual AI provider calls are wired up. The `AIProvider` protocol, concrete provider implementations (Claude, OpenAI, Local), connection testing, and dynamic model fetching are all spec-only requirements awaiting implementation. The settings UI is functional and persists values, but the values are not consumed by any AI integration code yet.

