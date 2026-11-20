
- **fail-closed-backstop** — after redaction you MUST re-scan the serialized output and hard-fail
  the emit or build if any pattern survives. A filter that silently misses is worse than none,
  because the output *looks* safe.
- **defense-in-depth** — layer independent gates (surface reduction → structural drop → prose
  substitution → assertion) so one layer's miss is caught by the next.
- **golden-tests** — keep a known-leaky fixture and assert end-to-end that nothing survives.
  Freeze real edge cases as regression tests — e.g. a `git@github.com:` SSH remote that looks
  email-shaped but must be kept, or a `~/tool` path that must not be redacted like a home path.

