
| State | Behavior |
|-------|----------|
| No window open | Menu item and keyboard shortcut are enabled |
| Window open, shortcut triggered | Existing window brought to front (single-instance-enforce) |
| Category selected | Content panel updates to show that category's settings (category-content-update) |
| Window resized | Frame saved automatically for next open (persist-frame-position) |
| App quit with window open | Window does not reopen on next launch (no-auto-reopen) |
| Setting changed | Change persisted and applied immediately (immediate-apply) |

