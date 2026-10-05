
| State | Source | Consumer | Direction | Mechanism |
|---|---|---|---|---|
| Setting values | Settings Category Browser controls | Persistence layer, rest of the app | two-way | Written immediately through settings-keys constants |
| Window frame | Window | Window Frame Persistence | two-way | Platform frame autosave |
| Window instance | Window controller | Menu item and shortcut handler | one-way | Existing instance is brought to front instead of creating another |
| Selected category | Settings Category Browser | Content panel | one-way | Not persisted across launches |

