
- **Profile deleted while in use**: If the active profile is a custom profile that gets deleted while a standalone terminal window is open, the window MUST fall back to Solarized Dark immediately (per color-profile fallback-to-default). Terminal colors update without reparenting.
- **Standalone window and project window open simultaneously**: Both function independently. Changing the active color profile affects all terminal views across both window types (since profile ID is stored in `@AppStorage`, a global setting).
- **Frame persistence for multiple standalone windows**: All standalone terminal windows share the autosave name `"terminal-window"`. This means only one window's frame is persisted. If multiple standalone windows are needed with independent frame persistence, a future revision MAY introduce per-window identifiers.
- **visionOS window placement**: On visionOS, the system manages window placement. Frame persistence (persist-window-frame) is a no-op on visionOS. Minimum size constraints still apply.

