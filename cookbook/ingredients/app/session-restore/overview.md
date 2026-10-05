
Saves the list of open document URLs on quit and reopens them on the next launch. On restore, saved URLs are filtered to registered document types, validated against the file system, deduplicated, and opened in their original order; if nothing valid remains the app falls back to opening a new window. Writes are atomic so a crash never corrupts the list.

### Terminology

| Term | Definition |
|------|-----------|
| Session restore | The process of reopening previously open documents or windows from a saved URL list |

