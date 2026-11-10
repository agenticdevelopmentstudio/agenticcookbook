
| State | Source | Consumer | Direction | Mechanism |
|---|---|---|---|---|
| Startup behavior mode | Settings (via settings-keys) | Startup Behavior, Session Restore | one-way | Resolved once at launch |
| Restore URL list | Open document windows at quit | Session Restore on next launch | one-way | Atomic write to platform persistence |
| Child process handles | Subsystems that spawn processes | Child Process Cleanup | one-way | Registered when spawned; cleaned at quit |
| Untitled-window decision | Startup Behavior mode and relaunch state | App delegate | one-way | `applicationShouldOpenUntitledFile` result |

