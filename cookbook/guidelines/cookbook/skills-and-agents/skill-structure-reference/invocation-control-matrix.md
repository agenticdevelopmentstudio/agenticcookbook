
| `disable-model-invocation` | `user-invocable` | Behavior |
|---------------------------|-----------------|----------|
| `false` (default) | `true` (default) | Auto-invoked by Claude + available as `/command` |
| `true` | `true` | Only via `/command` — never auto-invoked |
| `false` | `false` | Auto-invoked as background knowledge — not in menu |
| `true` | `false` | Never invoked — effectively disabled |

