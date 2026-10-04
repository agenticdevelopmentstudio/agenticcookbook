
- **High-frequency logging**: Logging in tight loops (e.g., per-frame rendering) SHOULD use debug level so it is automatically suppressed in release. If logging cannot be avoided, consider rate-limiting or sampling.
- **Sensitive data**: Log messages MUST NOT contain passwords, tokens, or PII. Use `privacy: .private` on Apple (os.Logger interpolation) or redact explicitly on other platforms.
- **Module boundaries**: In a multi-module project, each module MAY define its own `Log` enum, but all MUST share the same subsystem string so filtering by subsystem captures everything.
- **Thread safety**: Platform logging APIs (os.Logger, android.util.Log, console) are thread-safe. The centralized type's static properties are initialized once and are read-only, so no synchronization is needed.
- **Logger initialization cost**: On Apple, `os.Logger` is lightweight. Static `let` properties ensure each logger is created exactly once.

