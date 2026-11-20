
- User settings live in `~/.codex/config.toml`. The Codex home directory defaults to `~/.codex` and can be moved with the `CODEX_HOME` environment variable.
- Project settings live in `.codex/config.toml` inside the repository. Codex loads a project's file only when the project is trusted, so a setting that must apply on every machine MUST NOT depend on an untrusted checkout.
- Precedence, strongest first: command-line flags and `--config` overrides, project configuration (the closest file wins), a named profile file (`~/.codex/<name>.config.toml`, selected with `--profile`), the user file, cloud-managed defaults, `/etc/codex/config.toml`, and the built-in defaults.
- Typical keys are `model`, `approval_policy` (for example `"on-request"`) and `sandbox_mode` (for example `"workspace-write"`). You MUST check a key against the configuration reference before using it, and MUST NOT copy keys from another tool.
- A checked-in `config.toml` MUST NOT contain secrets.

