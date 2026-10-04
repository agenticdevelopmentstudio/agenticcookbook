
| Event | Properties | When |
|-------|-----------|------|
| `ai_chat.message_sent` | `{ provider: string, model: string }` | User sends a message |
| `ai_chat.response_received` | `{ provider: string, model: string, duration_ms: int }` | Assistant response received |
| `ai_chat.error` | `{ provider: string, error: string }` | API error or validation error |
| `ai_chat.cleared` | `{ message_count: int }` | User clears conversation |

