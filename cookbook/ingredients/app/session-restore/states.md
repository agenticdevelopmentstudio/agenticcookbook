
| State | Behavior |
|-------|----------|
| Cold launch, mode = restoreSession, saved URLs exist | App opens each saved document in order |
| Cold launch, mode = restoreSession, no saved URLs | App falls back to newWindow behavior |
| Force quit / crash | Saved URL list from previous clean quit preserved; no new save occurs |

