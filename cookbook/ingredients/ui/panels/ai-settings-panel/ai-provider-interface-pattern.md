
### Protocol definition

The `AIProvider` protocol defines the contract for all AI provider implementations. The settings panel configures WHICH provider is active and supplies credentials. Application code consumes AI capabilities exclusively through this interface.

```
AIProvider {
  func complete(prompt: String, options: CompletionOptions) async throws -> String
  func stream(prompt: String, options: CompletionOptions) -> AsyncStream<String>
  var isConfigured: Bool { get }
  var providerName: String { get }
  var supportedModels: [String] { get async }
}

CompletionOptions {
  model: String
  maxTokens: Int?
  temperature: Double?
  systemPrompt: String?
}
```

### Implementations

- **claude-provider-impl**: A `ClaudeProvider` implementation MUST exist for the Anthropic API.
- **openai-provider-impl**: An `OpenAIProvider` implementation MUST exist for the OpenAI API.
- **google-custom-provider-impl**: A `GoogleProvider` implementation MUST exist for the Google Gemini API. A `CustomProvider` implementation MUST exist for OpenAI-compatible endpoints (e.g., Ollama, LM Studio).
- **mock-provider-impl**: A `MockProvider` implementation MUST exist for testing. It MUST return deterministic canned responses and MUST NOT make network calls.
- **runtime-provider-resolution**: The active provider MUST be resolved at runtime based on the settings panel configuration, using a factory or dependency injection container.
- **tls-required**: All providers MUST use TLS/HTTPS for network communication. The `CustomProvider` MAY allow HTTP for `localhost` addresses only.
- **no-cached-keys-in-providers**: Provider implementations MUST NOT store or cache API keys internally. They MUST retrieve credentials from secure storage on each use or accept them via injection at construction time.

