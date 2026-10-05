
- **immediate-apply**: Setting changes MUST take effect immediately when the user interacts with the control. There MUST NOT be an "Apply" or "Save" button.
- **sidebar-category-list**: The sidebar MUST display a vertical list of category names. The first category MUST be selected by default.
- **category-content-update**: Selecting a category MUST update the content panel to show that category's settings.
- **content-vertical-scroll**: The content panel MUST scroll vertically if its content exceeds the panel height.
- **abstract-persistence**: Settings MUST be read from and written to a persistence layer. The storage backend SHOULD be abstracted behind an interface so it can be swapped without changing consumers. Common backends:
  - macOS/iOS: `UserDefaults` / `@AppStorage` (default), or SQLite for apps that need migration-safe structured storage
  - Windows: Registry or app config file
  - Web/Electron: `localStorage` or `electron-store`
  - Note: apps MAY migrate from one backend to another (e.g., UserDefaults → SQLite) — see the `settings-keys` ingredient for key preservation during migration
- **form-section-layout**: The content panel SHOULD use `Form` with `Section` blocks for grouping related settings with clear section headers.

