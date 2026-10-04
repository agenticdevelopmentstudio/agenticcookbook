
A model's output is attacker-influenceable data, not a trusted command. Apply the same egress controls you would to a raw HTTP request body.

- You **MUST** sanitize, encode, or parameterize model output before it crosses any trust boundary:
  - **Shell** — never pass output to `exec`/`system`/a shell string. Use argument arrays; **MUST NOT** interpolate into a command line.
  - **SQL** — use parameterized queries / prepared statements; never string-concatenate model output into SQL.
  - **HTML/DOM** — context-aware output encoding; **MUST NOT** inject into `innerHTML` or render as raw markup without sanitization.
  - **Tool arguments** — validate and type-check against a schema before any tool call (see input-validation guideline).
- You **MUST** validate structured output (JSON, function-call args) against a strict schema and reject on mismatch — fail fast rather than coerce.
- You **MUST NOT** treat output as proof of an action; verify side effects out-of-band.

