
| Name | Ingredient | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Startup Behavior | [adc.ingredient.app.startup-behavior](cookbook:ee72734e-2cff-41be-9d1a-813b64aa0fd2) | Resolves the startup mode and controls untitled-window creation | Yes | Default `restoreSession` |
| Session Restore | [adc.ingredient.app.session-restore](cookbook:a7c4168e-2f0a-40bb-b38f-0f81ad6a9cf0) | Saves and reopens document URLs | Yes | Active when mode is `restoreSession` |
| Child Process Cleanup | [adc.ingredient.app.child-process-cleanup](cookbook:5546b9ad-b8b4-4973-817e-b3bc4f090618) | Terminates child processes on quit | Yes | Timeout 5 seconds |
| Settings Keys | [adc.ingredient.infrastructure.settings-keys](cookbook:39676af7-b0b9-48f2-8056-f0c8e8754ffc) | Central keys for the startup mode and restore list | Yes | Keys in a constants enum or struct |
| Logging | [adc.ingredient.infrastructure.logging](cookbook:7c2049c7-89d9-4135-b657-dbd03cdd19a0) | Logger for lifecycle events | Yes | Category `AppLifecycle` |

