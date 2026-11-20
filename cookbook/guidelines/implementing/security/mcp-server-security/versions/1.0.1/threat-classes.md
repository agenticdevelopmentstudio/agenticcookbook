
| Class | Vector | Core mitigation |
|-------|--------|-----------------|
| Tool poisoning | Malicious instructions embedded in a tool's `description`/schema | Treat descriptions as untrusted content; surface them for human review |
| Output prompt injection | Attacker-controlled data returned in tool **results** | Label tool output as data, not instructions; sanitize/escape before returning |
| Rug-pull (tool redefinition) | Tool changes its behavior/description after initial approval | Bind user approval to a hash of the tool's content |
| Confused deputy | OAuth proxy reuses a static client ID + consent cookie | Per-client consent before forwarding to third-party authz |
| Token passthrough | Server forwards client-supplied tokens downstream | FORBIDDEN; reject tokens not issued for this server |
| Session hijacking | Guessed/stolen session ID impersonates a client | Non-deterministic IDs bound to user identity; never authenticate via session |
| SSRF | Malicious discovery URLs point at internal/metadata hosts | Validate/allowlist OAuth discovery URLs; block private ranges |

