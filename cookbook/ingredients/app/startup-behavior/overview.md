
The configurable action an app takes when it first becomes active after launch, and the control of automatic untitled-window creation that goes with it. Three modes are supported: open the default window, restore the previous session, or launch silently with no window. The mode is a user setting stored through the platform's standard persistence layer under a centralized key and defaults to restoring the session. This ingredient decides what to do at launch; reopening documents is the Session Restore ingredient.

### Terminology

| Term | Definition |
|------|-----------|
| Startup behavior | The configurable action the app takes when it first becomes active after launch |
| Untitled file | A new, unsaved document window that macOS may open automatically on launch |

