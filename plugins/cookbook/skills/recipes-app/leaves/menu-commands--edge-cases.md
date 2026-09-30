<!-- leaf: recipes-app/menu-commands--edge-cases · source: recipes/app/menu-commands.md -->

# Menu Commands

**Rules** (cite as `recipes-app/menu-commands--edge-cases#<slug>`):

- `permissions-denied` MUST — If the app lacks read permission on the selected directory, the validation step MUST fail gracefully with an error …
- `nsopenpanel-cancelled` MUST — If the user clicks Cancel in the NSOpenPanel, the command MUST silently abort with no error or side effect.
- `nssavepanel-cancelled` MUST — If the user clicks Cancel in the NSSavePanel, the command MUST silently abort with no error or side effect.
- `rapid-repeated-invocation` MUST — If the user presses Cmd-N multiple times quickly, the command MUST NOT open multiple NSOpenPanels simultaneously. The …
- `selected-directory-is-a-symlink` SHOULD — The command SHOULD resolve the symlink to its canonical path before checking for .git and existing packages, to avoid …
- `project-directory-on-a-network-volume` SHOULD — File operations (validation, package creation) MAY be slower. The command SHOULD NOT block the main thread during I/O. …
- `extremely-long-directory-name` MUST — The package filename ({dirname}.{ext}) inherits the directory name. If the resulting path exceeds filesystem limits, …
- `multiple-screens-spaces` SHOULD — NSOpenPanel and NSSavePanel SHOULD appear on the same screen as the app's key window. This is default system behavior.
- `sandboxed-app` MUST — If the app is sandboxed, the NSOpenPanel and NSSavePanel provide security-scoped URLs. The command MUST call …

## Edge Cases

- **No window focused**: Global commands (New Project, New Workspace) remain enabled. Per-window commands (New Session) are disabled via `@FocusedObject` returning nil. This is the expected state at app launch before any document is opened.
- **Directory without .git**: Validation fails with a clear error alert. The user is not prevented from dismissing the alert and retrying with a different directory.
- **Duplicate project package**: If `{dir}/{dirname}.{ext}` already exists, the existing package is opened. This prevents creating multiple packages for the same project directory.
- **Permissions denied**: If the app lacks read permission on the selected directory, the validation step MUST fail gracefully with an error alert (e.g., "Cannot access the selected folder. Check Finder permissions."). If write permission is denied when creating a package, the creation step MUST fail with an error alert.
- **NSOpenPanel cancelled**: If the user clicks Cancel in the NSOpenPanel, the command MUST silently abort with no error or side effect.
- **NSSavePanel cancelled**: If the user clicks Cancel in the NSSavePanel, the command MUST silently abort with no error or side effect.
- **Rapid repeated invocation**: If the user presses Cmd-N multiple times quickly, the command MUST NOT open multiple NSOpenPanels simultaneously. The panel is modal, so subsequent invocations are blocked until the current panel is dismissed.
- **Selected directory is a symlink**: The command SHOULD resolve the symlink to its canonical path before checking for `.git` and existing packages, to avoid creating duplicate packages for symlinked directories.
- **Project directory on a network volume**: File operations (validation, package creation) MAY be slower. The command SHOULD NOT block the main thread during I/O. Asynchronous execution with appropriate UI feedback is RECOMMENDED.
- **Extremely long directory name**: The package filename (`{dirname}.{ext}`) inherits the directory name. If the resulting path exceeds filesystem limits, the creation MUST fail with an error alert rather than silently truncating.
- **Workspace window focused when pressing Cmd-Shift-N**: The @FocusedObject for project state is nil (workspace windows do not provide project state), so the menu item is disabled.
- **Multiple screens / spaces**: NSOpenPanel and NSSavePanel SHOULD appear on the same screen as the app's key window. This is default system behavior.
- **Sandboxed app**: If the app is sandboxed, the NSOpenPanel and NSSavePanel provide security-scoped URLs. The command MUST call `startAccessingSecurityScopedResource()` before accessing the selected URL and `stopAccessingSecurityScopedResource()` when done.
