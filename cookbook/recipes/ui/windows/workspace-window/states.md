
| State | Behavior |
|-------|----------|
| No entries | Sidebar shows empty sections, detail pane shows welcome empty state with add buttons (welcome-empty-state) |
| Entries present, none selected | Sidebar lists entries, detail pane shows welcome empty state (welcome-empty-state) |
| Entry selected | Sidebar highlights selection, detail pane shows entry detail (detail-pane-metadata) |
| Directory entry expanded | DisclosureGroup open, discovered projects listed (directory-disclosure-group) |
| Directory entry collapsed | DisclosureGroup closed, discovered projects hidden |
| Syncing | SyncProgressBar visible at sidebar bottom (sync-progress-indicator), `isSyncing` true |
| Sync complete | SyncProgressBar hidden, discovered projects up to date |
| Project opened | Project window opens via NSDocumentController, workspace window remains |
| Entry removed | Entry disappears from sidebar, coordinator stopped (if directory), document updated |
| Entry added | Entry appears in sidebar, coordinator started (if directory), document updated |
| Self-referential add rejected | Add operation silently rejected, warning logged (prevent-self-referential) |
| Entry type migrated | Entry with incorrect type auto-corrected on load (auto-correct-entry-type) |

