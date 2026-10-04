
| Term | Definition |
|------|-----------|
| Provider | An AI/LLM service backend (e.g., Anthropic, OpenAI, a local model server) |
| Model | A specific model offered by a provider (e.g., claude-sonnet-4-6, gpt-4o) |
| API key | A secret credential used to authenticate with a provider's API |
| Endpoint | The base URL for a provider's API |
| Connection status | The result of a test call to the configured provider: connected, disconnected, or untested |
| Secure storage | Platform-specific credential storage (Keychain, EncryptedSharedPreferences, HttpOnly cookies) — NOT UserDefaults, SharedPreferences, or localStorage |

