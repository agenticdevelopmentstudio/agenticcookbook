
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| stw-002 | hsplit-sidebar-terminal | Open a standalone terminal window | HSplitView renders with session sidebar (left) and terminal view (right) |
| stw-003 | sidebar-width-range | Inspect session sidebar width | Width is between 150pt and 200pt |
| stw-006 | own-session-manager | Open a standalone terminal window and a project window | Each has its own SessionManager instance; adding a session in one does not affect the other |
| stw-007 | auto-create-default | Open a standalone terminal window for the first time | A default session ("Session 1") is created automatically; terminal shows shell prompt |
| stw-008 | terminate-on-close | Open window with 3 sessions, close window | All 3 PTYs terminated |
| stw-009 | focused-object-dispatch | Open two standalone terminal windows, focus window 1, invoke "New Session" menu | Session created in window 1's session manager only (via focusedObject dispatch) |
| stw-013 | independent-sessions | Open two standalone terminal windows, create sessions in each | Sessions are independent; removing a session in window A does not affect window B |
| stw-014 | auto-create-default | Open window, remove all sessions, no auto-creation on removal | Empty state displayed; auto-creation only happens on initial appear |
| stw-015 | delegate-session-list, delegate-terminal-view | Open window, create multiple sessions, switch between them | Session list displays rows per terminal-pane spec; reparenting preserves scrollback |

