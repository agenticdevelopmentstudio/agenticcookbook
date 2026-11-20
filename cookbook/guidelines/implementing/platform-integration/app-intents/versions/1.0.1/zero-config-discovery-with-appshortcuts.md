
`AppShortcutsProvider` registers shortcuts that work the moment the app is installed — no user setup required.

- Conform one type to `AppShortcutsProvider` and return `AppShortcut` values from the `appShortcuts` builder.
- Each `AppShortcut` **MUST** supply `phrases` containing `\(.applicationName)` so Siri can resolve the invocation.
- High-value actions **SHOULD** ship as `AppShortcut`s so users get voice and Spotlight access with no configuration.

