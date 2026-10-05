
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| pw-001 | hsplit-three-panels | Open a project window | HSplitView renders with sessions, file tree, and detail panels |
| pw-002 | vsplit-editor-terminal | Inspect detail panel | VSplitView contains editor (top) and terminal (bottom) |
| pw-004 | inspector-slide-right | Toggle inspector on | Inspector slides in from right |
| pw-005 | proportional-sizing, sessions-default-15pct, filetree-default-20pct | Open window at 1200pt width | Sessions ~180pt (15%), file tree ~240pt (20%), detail fills remainder |
| pw-006 | detail-split-50-50 | Inspect detail panel at 600pt height | Editor ~300pt, terminal ~300pt (50/50 split) |
| pw-007 | persist-layout-proportions, persist-project-settings | Resize sessions panel to 25%, close project, reopen | Sessions panel restores at 25% |
| pw-008 | toggle-sessions-panel, persist-visibility-state | Hide sessions panel, close project, reopen | Sessions panel remains hidden |
| pw-009 | toggle-terminal, persist-visibility-state | Hide terminal pane, close project, reopen | Terminal pane remains hidden, header still visible |
| pw-010 | animate-pane-toggle | Toggle sessions panel visibility | Panel animates in/out with easeInOut(0.2) |
| pw-011 | toolbar-sessions-button | Click sessions toolbar button | Sessions panel toggles visibility |
| pw-012 | toolbar-inspector-button | Click inspector toolbar button | Inspector panel toggles visibility |
| pw-013 | toolbar-gear-button | Click gear toolbar button | Project settings sheet appears |
| pw-014 | folder-header-repo-name | Open project at `/Users/dev/my-repo` | Folder header shows "my-repo" above file tree |
| pw-020 | sessions-toggle-label | Enable VoiceOver, focus sessions toolbar button | Announces "Toggle Sessions Panel" |
| pw-021 | keyboard-region-nav | Press Tab repeatedly through window | Focus moves between sessions, file tree, editor, terminal, toolbar |
| pw-022 | immediate-settings-save | Toggle inspector, immediately force-quit app, relaunch | Inspector state matches last toggle (persisted immediately) |

