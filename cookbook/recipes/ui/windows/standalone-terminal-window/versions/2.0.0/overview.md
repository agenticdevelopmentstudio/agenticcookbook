
The primary window for non-project terminal use. A `WindowGroup(id: "terminal")` scene hosts the Terminal Window Shell (session sidebar and terminal view with its own independent session manager), applies the active color profile, persists its frame under the autosave name `"terminal-window"`, and enforces a 600x400pt minimum size. It shares the terminal-pane ingredient with the project window's embedded terminal but shares no sessions with it.

