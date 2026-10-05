
- **llm-backend-selectable**: The node MUST support selecting which LLM backend executes a handler's inference step via configuration (e.g., an environment variable or config file), with no code changes required to switch. Supported backend kinds include at minimum: an OpenAI-compatible HTTP API endpoint (local model server or hosted), and a CLI-based inference tool invoked as a subprocess.
- **structured-output**: Handlers that invoke the LLM MUST request schema-constrained (structured) output from the backend rather than parsing free-form text. The output schema MUST be defined per handler and validated before the handler returns its result.
- **backend-injected**: The backend MUST be supplied to handlers as an injected dependency so handler code never names a provider and can be exercised with a stub backend.
- **invalid-output-fails-retryable**: If the backend returns output that does not validate against the handler's schema, the handler MUST fail the job as retryable rather than passing a malformed result onward.

