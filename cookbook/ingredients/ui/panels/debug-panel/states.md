
| State | Behavior |
|-------|----------|
| Debug build, panel closed | Gesture/shortcut is active, panel is not visible |
| Debug build, panel open | Modal/overlay showing, app still visible beneath |
| Release build | Panel code is not compiled, gesture has no effect |
| Flag overridden | Flag row shows "override" badge, value reflects override |
| Flag reset | Override cleared, value returns to default/remote |
| Environment switched | All service URLs update, services reconnect |

