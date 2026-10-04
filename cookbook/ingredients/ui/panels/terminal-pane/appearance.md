
### Terminal pane layout

```
┌───────────────┬────────────────────────────────────┐
│ Sessions  [+] │                                    │
├───────────────┤                                    │
│               │                                    │
│ ● Session 1   │  user@host ~ %                     │
│   ~/projects  │  ls -la                            │
│   main        │  total 42                          │
│   zsh         │  drwxr-xr-x  5 user staff  160 ...│
│               │  -rw-r--r--  1 user staff  230 ...│
│ ○ Session 2   │                                    │
│   ~/docs      │                                    │
│   bash        │                                    │
│               │                                    │
│               │                                    │
│               │                                    │
└───────────────┴────────────────────────────────────┘
```

### Session row detail

```
┌───────────────────┐
│ ● Session 1       │  ← dot color + name
│  📁 ~/projects    │  ← metadata-line: working directory (middle-truncated)
│  🌿 main          │  ← metadata-line: git branch
│  ⬛ zsh           │  ← metadata-line: foreground process
└───────────────────┘
```

### Empty state

```
┌────────────────────────────────────────────────────┐
│                                                    │
│                                                    │
│                   ⬛                               │
│         No active terminal session                 │
│     Click + to open a new terminal session         │
│              [New Session]                         │
│                                                    │
│                                                    │
└────────────────────────────────────────────────────┘
```

- **Sidebar width**: 180–220pt, resizable
- **Session row spacing**: 4pt between dot/name line and metadata lines
- **Metadata lines**: Use metadata-line component (12pt secondary icon + caption text)
- **Dot color**: 8pt filled circle, leading the session name
- **Terminal background**: Determined by active color profile
- **Terminal font**: Determined by active color profile (monospaced)

