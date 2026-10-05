
### Window structure

- **hsplit-sidebar-terminal**: The window MUST use an HSplitView with two sections: session list sidebar (left) and terminal view (right).
- **sidebar-width-range**: The session list sidebar MUST have a width between 150pt and 200pt.

### Session management

- **own-session-manager**: The window MUST create its own `SessionManager` instance as a `@StateObject`. This instance MUST be independent from any project window's session manager.
- **auto-create-default**: On window appear (`onAppear`), if the session manager contains no sessions, a default session MUST be created automatically by calling `addSession()`.
- **terminate-on-close**: On window close, all sessions MUST be terminated by calling `terminateAll()` on the session manager.
- **focused-object-dispatch**: The session manager MUST be provided as `.focusedObject()` so that menu commands (New Session, Close Session, etc.) can dispatch to the correct window's session manager.

### Relationship to project window

- **independent-sessions**: Each standalone terminal window MUST have its own `SessionManager` instance. Sessions MUST NOT be shared between standalone terminal windows or between standalone terminal windows and project windows.

