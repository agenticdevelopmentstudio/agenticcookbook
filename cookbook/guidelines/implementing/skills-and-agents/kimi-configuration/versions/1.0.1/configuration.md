
- Project-level configuration overrides global configuration, and startup parameters such as `--system-prompt` override both.
- The environment variables `KIMI_API_KEY`, `KIMI_BASE_URL`, `KIMI_MODEL` and `KIMI_MAX_TOKENS` take precedence over the configuration file. The API key MUST stay in the environment and MUST NOT appear in a checked-in file.
- The older command-line tool manages MCP servers with `kimi mcp add`, `list`, `remove` and `auth`, and accepts a `--mcp-config-file` whose top-level key is `mcpServers`.

