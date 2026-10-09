
- The help-center page on customization names the global configuration `~/.kimi/config.toml` (TOML or JSON), editable with the `/config` command, and a global `~/.kimi/AGENTS.md`.
- The skills documentation names the user skills directory under `$KIMI_CODE_HOME/skills/`, which defaults to `~/.kimi-code/skills/`.
- The archived `kimi-cli` project stores its data in `~/.kimi/`.
- Do not assume one. Check which directory the installed version uses, and let scripts that touch these paths accept an override rather than hardcoding either.

