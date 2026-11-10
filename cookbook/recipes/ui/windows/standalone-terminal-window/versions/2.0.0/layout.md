
```
 WindowGroup(id: "terminal")  [min 600×400, frame "terminal-window"]
┌──────────────┬─────────────────────────────────────────┐
│ Terminal     │ Terminal Pane view                      │
│ Window Shell:│ (colors/font from active Color Profile) │
│ Sessions [+] │                                         │
│  ● Session 1 │  user@host ~ %                          │
│  ○ Session 2 │                                         │
└──────────────┴─────────────────────────────────────────┘
```

The shell supplies the split and session manager; the terminal-pane ingredient fills both halves; the color profile styles the terminal view.

### Composed states

| State | Behavior |
|-------|----------|
| Profile changed | Colors/font applied to terminal view without reparenting |
| Profile deleted while in use | Falls back to Solarized Dark (per color-profile fallback-to-default) |

