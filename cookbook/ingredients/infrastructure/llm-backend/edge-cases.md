
- **LLM backend returns invalid schema**: The handler MUST fail the job with `retryable: true` rather than passing a malformed result to complete (invalid-output-fails-retryable).
- **Model without native structured-output support**: Fall back to a JSON-object response mode with the schema injected into the system prompt, and still validate the output before returning.
- **CLI backend exits non-zero**: The handler treats this as a handler error and fails the job as retryable.
- **Unknown backend kind in configuration**: Startup MUST fail with a clear configuration error rather than choosing a default provider.

