
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| settings-001 | single-instance-enforce | Open settings window, trigger shortcut again | Window count remains 1, existing window is key/front |
| settings-002 | no-auto-reopen | Open settings, quit app, relaunch | Settings window is not visible after relaunch |
| settings-003 | persist-frame-position | Open settings, resize to 600×500 at (100,200), close, reopen | Window opens at 600×500 at (100,200) |
| settings-004 | immediate-apply | Toggle a boolean setting | Setting value in persistence layer matches new state immediately |
| settings-005 | sidebar-category-list | Open settings window | First category in list is selected, content panel shows its settings |
| settings-006 | category-content-update | Select second category | Content panel updates to show second category's settings |
| settings-007 | resizable-min-size | Attempt to resize window below 500×400 | Window does not shrink below minimum |
| settings-008 | keyboard-sidebar-nav | Focus sidebar, press Down arrow | Selection moves to next category |
| settings-009 | tab-focus-transfer | Press Tab from sidebar | Focus moves to first control in content panel |

