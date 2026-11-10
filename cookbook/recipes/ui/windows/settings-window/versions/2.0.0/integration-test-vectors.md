
| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| settings-001 | single-instance-enforce | Open settings window, trigger shortcut again | Window count remains 1, existing window is key/front |
| settings-002 | no-auto-reopen | Open settings, quit app, relaunch | Settings window is not visible after relaunch |
| settings-003 | persist-frame-position | Open settings, resize to 600×500 at (100,200), close, reopen | Window opens at 600×500 at (100,200) |
| settings-007 | resizable-min-size | Attempt to resize window below 500×400 | Window does not shrink below minimum |
| settings-010 | log-window-events, single-instance-enforce | Trigger the shortcut while the window is open | Log contains `SettingsWindow: already open, brought to front` |
| settings-011 | keys-through-registry, immediate-apply | Toggle a setting | The value is written under the key declared in the settings-keys registry |
| settings-012 | browser-fills-window | Inspect the open window | No Apply or Save control is present anywhere in the window |

