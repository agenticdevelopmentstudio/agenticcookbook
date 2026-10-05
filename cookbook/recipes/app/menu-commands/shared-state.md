
| State | Source | Consumer | Direction | Mechanism |
|---|---|---|---|---|
| Focused window state | Focused window (`.focusedObject()`) | Creation Menu Commands | one-way | `@FocusedObject` read at the command level |
| Selected directory or save location | File picker | Document Creation Flow | one-way | Picker result passed to validation or package creation |
| Created document | Document Creation Flow | Document controller | one-way | Opened via `NSDocumentController.shared.openDocument(withContentsOf:display:)` |
| Flow in progress | Document Creation Flow | Creation Menu Commands | one-way | Commands that start a flow are non-reentrant while a flow runs |

