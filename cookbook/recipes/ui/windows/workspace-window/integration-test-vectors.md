
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| ws-001 | hsplit-sidebar-detail | Open a workspace window | HSplitView renders with sidebar (left) and detail pane (right) |
| ws-002 | persist-window-frame | Open workspace, move window to (100, 200), close, reopen | Window appears at (100, 200) |
| ws-003 | sidebar-default-30pct | Open workspace, do not adjust sidebar | Sidebar occupies approximately 30% of window width |
| ws-004 | sidebar-default-30pct | Adjust sidebar proportion to 0.4, close workspace, reopen | Sidebar proportion restored to 0.4 |
| ws-032 | edits-flow-to-document, prevent-duplicate-entry | Use the welcome-state "Add Directory" button to add a path that already exists | Add is rejected by the document; sidebar does not change |
| ws-033 | browser-bound-to-document, auto-discover-projects | A new `.catnip-proj` appears in a watched directory | `onDiscoveryChanged` updates the document and the sidebar shows the new discovered project |
| ws-034 | sidebar-proportion-via-document | Drag the divider, close and reopen the workspace | Proportion is restored from the document's `settings` table |
| ws-035 | frame-key-from-path, window-events-logged | Open two different workspaces and move each window | Each window restores to its own frame; logs show distinct autosave names |

