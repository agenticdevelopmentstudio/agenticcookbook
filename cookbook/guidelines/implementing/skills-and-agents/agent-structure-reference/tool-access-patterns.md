
- **Unrestricted**: Omit both `tools` and `disallowedTools` — agent has access to all tools
- **Allowlist**: Set `tools` to a specific list — agent can ONLY use those tools
- **Denylist**: Set `disallowedTools` — agent can use everything EXCEPT those tools
- `tools` and `disallowedTools` MUST NOT be used together (mutually exclusive)

