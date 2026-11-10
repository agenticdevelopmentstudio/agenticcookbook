
```
 App menu > Settings...  (platform shortcut)
        |
        v
┌──────────────────────────────────────────────┐
│ Settings                         (min 500×400)│
├────────────┬─────────────────────────────────┤
│ Sidebar    │  Content panel                  │
│ General    │  Setting Label         [control]│
│ Appearance │  Setting Label         [control]│
│ Advanced   │  Setting Label         [control]│
├────────────┴─────────────────────────────────┤
```

The sidebar and content panel are the Settings Category Browser; the title bar, frame, and instance behavior belong to the window. The sidebar and content layout variants are defined by the browser's Appearance section.

### Composed states

| State | Behavior |
|-------|----------|
| No window open | Menu item and keyboard shortcut are enabled |
| Window open, shortcut triggered | Existing window brought to front (single-instance-enforce) |
| Window resized | Frame saved automatically for next open (persist-frame-position) |
| App quit with window open | Window does not reopen on next launch (no-auto-reopen) |

