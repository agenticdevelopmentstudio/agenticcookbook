
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pw-003 | collapsible-pane-headers | Inspect editor and terminal sections | Each preceded by a collapsible pane header |
| pw-015 | persist-window-frame, sha256-autosave-id | Open project, move window, close, reopen | Window restores at saved position; autosave name is SHA256 of project path |
| pw-016 | sync-status-overlay | Trigger directory sync | Status bar overlay appears at bottom of file tree panel |
| pw-017 | load-initial-start-watch | Open a project window | `loadInitial` and `startWatching` called on appear |
| pw-018 | auto-open-terminal | Open project with auto-open-terminal enabled | Terminal pane opens automatically |
| pw-019 | terminate-on-close | Close the project window | `terminateAll` and `stopWatching` called |
| pw-023 | header-collapse-drives-detail-area, collapsible-pane-headers | Collapse the terminal pane header | Terminal collapses, editor fills the detail area, terminal header remains visible |
| pw-024 | layout-hosts-panel-ingredients, delegate-inspector | Select a file in the file tree, then toggle the inspector on | Inspector slides in and shows metadata for the selected file |
| pw-025 | settings-keys-central, persist-window-frame | Open two projects, resize one window and toggle panels in it | The other window's frame, proportions and visibility are unchanged |

