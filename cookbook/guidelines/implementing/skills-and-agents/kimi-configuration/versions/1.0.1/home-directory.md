
- The help-center page on customization names the global configuration `~/.kimi/config.toml` (TOML or JSON), editable with the `/config` command, and a global `~/.kimi/AGENTS.md`.
- The skills documentation names the user skills directory under `$KIMI_CODE_HOME/skills/`, which defaults to `~/.kimi-code/skills/`.
- The archived `kimi-cli` project stores its data in `~/.kimi/`.
- Code MUST NOT assume one. It MUST check which directory the installed version uses, and scripts that touch these paths SHOULD accept an override rather than hardcoding either.

