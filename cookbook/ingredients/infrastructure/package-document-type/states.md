
| State | Behavior |
|-------|----------|
| New document | Empty model with default values; the first save creates the package directory |
| Open document | Model loaded; changes to `model` trigger auto-save |
| Auto-save in progress | Model property changed; the system snapshots the model and writes the package |
| Session restoration | App launches; previously open document URLs are reopened; any that fail are logged and skipped |

