<!-- leaf: recipes-app/lifecycle--states · source: recipes/app/lifecycle.md -->

# App Lifecycle

## States

| State | Behavior |
|-------|----------|
| Cold launch, mode = newWindow | App opens default window immediately |
| Cold launch, mode = restoreSession, saved URLs exist | App opens each saved document in order |
| Cold launch, mode = restoreSession, no saved URLs | App falls back to newWindow behavior |
| Cold launch, mode = nothing | App activates with no windows; only menu bar and dock icon visible |
| App becoming active (already running) | No automatic window creation; user activates existing windows |
| App quitting, documents open | URL list saved to persistence, child processes terminated |
| App quitting, no documents open | Empty URL list saved (clears previous restore list), child processes terminated |
| System logout/restart | Same as app quitting; session restore list saved normally |
| Force quit / crash | Saved URL list from previous clean quit preserved; no new save occurs |
