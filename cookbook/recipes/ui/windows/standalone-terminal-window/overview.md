
A standalone terminal window with a session sidebar and terminal view — distinct from the project window's embedded terminal. This is the primary window for non-project terminal usage. The window uses an HSplitView with a session list on the left and a terminal view on the right, and creates its own independent SessionManager instance. It shares the same terminal-pane spec for terminal behavior (PTY sessions, session list, terminal rendering, profiles) but operates as a completely independent instance with no session sharing between windows.

