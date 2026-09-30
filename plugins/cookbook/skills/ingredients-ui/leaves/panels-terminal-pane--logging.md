<!-- leaf: ingredients-ui/panels-terminal-pane--logging · source: ingredients/ui/panels/terminal-pane.md -->

# Terminal Pane

## Logging

Subsystem: `{{bundle_id}}` | Category: `TerminalPane`

| Event | Level | Message |
|-------|-------|---------|
| Session created | debug | `TerminalPane: session created "{{name}}" ({{id}}) with shell {{shell}}` |
| Session selected | debug | `TerminalPane: session selected "{{name}}" ({{id}})` |
| Session removed | debug | `TerminalPane: session removed "{{name}}" ({{id}})` |
| Session terminated | debug | `TerminalPane: session "{{name}}" ({{id}}) shell exited with code {{code}}` |
| All sessions terminated | debug | `TerminalPane: all sessions terminated (window closing)` |
| Working directory changed | debug | `TerminalPane: session "{{name}}" directory changed to "{{path}}"` |
| Git branch detected | debug | `TerminalPane: session "{{name}}" git branch: "{{branch}}"` |
| Git branch detection timeout | debug | `TerminalPane: session "{{name}}" git branch detection timed out for "{{path}}"` |
| Git branch stale result | debug | `TerminalPane: session "{{name}}" discarding stale git branch result` |
| Foreground process changed | debug | `TerminalPane: session "{{name}}" foreground process: "{{process}}"` |
| OSC 7 received | debug | `TerminalPane: session "{{name}}" OSC 7: "{{url}}"` |
| OSC 2 received | debug | `TerminalPane: session "{{name}}" OSC 2: "{{title}}"` |
| OSC 7770 received | debug | `TerminalPane: session "{{name}}" OSC 7770: "{{payload}}"` |
| OSC 7770 malformed | debug | `TerminalPane: session "{{name}}" ignoring malformed OSC 7770: "{{payload}}"` |
| Profile applied | debug | `TerminalPane: applied profile "{{profileName}}" to session "{{name}}"` |
| Terminal reparented | debug | `TerminalPane: reparented terminal view to session "{{name}}" ({{id}})` |
| Shell fallback | warning | `TerminalPane: configured shell "{{shell}}" not found, falling back to /bin/zsh` |
| PTY allocation failed | error | `TerminalPane: failed to allocate PTY for session "{{name}}": {{error}}` |
| Session renamed | debug | `TerminalPane: session "{{id}}" renamed from "{{oldName}}" to "{{newName}}"` |
| Empty state displayed | debug | `TerminalPane: no sessions, showing empty state` |
| Auto-open triggered | debug | `TerminalPane: autoOpenTerminal enabled, creating initial session` |
