
| Stage | Enforce deterministically | Confirm with human |
|-------|---------------------------|--------------------|
| Input | injection/topic/safety filter | no |
| Tool call | allow-list, scope, caps | high-impact / irreversible only |
| Output | schema, PII/secret, moderation | no |

> Privacy and PII handling here is engineering guidance, not legal advice; confirm obligations with counsel. Heavy controls (managed moderation services, dedicated policy engines, sidecar enforcement) are adopt-when-measured-need-justifies per YAGNI — start with in-process deterministic checks.

