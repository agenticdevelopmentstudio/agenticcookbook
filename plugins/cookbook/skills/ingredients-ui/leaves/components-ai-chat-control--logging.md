<!-- leaf: ingredients-ui/components-ai-chat-control--logging · source: ingredients/ui/components/ai-chat-control.md -->

# AI Chat Control

**Rules** (cite as `ingredients-ui/components-ai-chat-control--logging#<slug>`):

- `critical-logging-rule` MUST — Message content (user prompts and AI responses) MUST NEVER appear in log output at any level.

## Logging

Subsystem: `{{bundle_id}}` | Category: `AIChatControl`

| Event | Level | Message |
|-------|-------|---------|
| Message sent | debug | `AIChatControl: message sent to "{{provider}}" model "{{model}}"` |
| Response received | debug | `AIChatControl: response received ({{duration}}ms, {{token_count}} chars)` |
| Request failed | debug | `AIChatControl: request failed: {{error}}` |
| History cleared | debug | `AIChatControl: history cleared ({{count}} messages)` |
| AI disabled | debug | `AIChatControl: send blocked — AI features disabled` |
| No API key | debug | `AIChatControl: send blocked — no API key configured` |

**Critical logging rule**: Message content (user prompts and AI responses) MUST NEVER appear in log output at any level.
