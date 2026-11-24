
| Name | Ingredient | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Job worker | [adc.ingredient.infrastructure.job-worker](cookbook:22fbf585-c5a3-425a-94f1-ba9b570ebfde) | Owns the poll-claim loop, lease heartbeat, handler dispatch table, result reporting, and the idempotency contract | Yes | Supported job types, batch size, poll interval (default 5 seconds), per-handler timeout, concurrency limit |
| LLM backend | [adc.ingredient.infrastructure.llm-backend](cookbook:597e9cd0-453a-42b8-a464-8ba8d31a6efc) | Executes each handler's inference step with schema-constrained output through a configured provider | Yes | Backend kind (OpenAI-compatible HTTP endpoint or CLI subprocess) and endpoint, selected by environment variable or config file |
| Categorize and tag handler | [adc.ingredient.infrastructure.categorize-and-tag-handler](cookbook:7c0b4381-0a41-4d8c-8b90-1614038b1a94) | The concrete handler registered for the `categorize_and_tag` job type | Yes, except in machine mode | Registered in the job worker's dispatch table at startup on a node not in machine mode; receives the LLM backend by injection |

The TypeScript node also has three components that are not ingredients yet. They are specified in this recipe's Integration Requirements:

- **`jobs.step.ai` handler**: one model call, with an optional `/mcp` tool loop under the claim's acting token (`step-ai-handler`, `step-ai-tool-loop`).
- **`jobs.step.script` handler**: runs a step's script as a subprocess, on a machine only, with `AI_NODE_ALLOW_SCRIPTS=1`; the Python interpreter is `AI_NODE_PYTHON` (`step-script-handler`).
- **Claude Code provider**: an LLM backend kind that runs the Claude Code CLI with pinned flags, on a machine only. It is configured by `AI_NODE_CLAUDE_CODE_BIN` (default `claude`) and `AI_NODE_CLAUDE_CODE_TIMEOUT_MS` (default 300,000), and the step's model is passed as a checked `--model` (`claude-code-provider`).

