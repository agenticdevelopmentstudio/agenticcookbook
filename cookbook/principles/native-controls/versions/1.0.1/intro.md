
# Prefer native controls and libraries

Always use the platform's built-in frameworks before custom implementations. Swift Concurrency over raw threads. Room/SwiftData over raw SQLite. Fetch API over custom HTTP.

When generating a component, explicitly note which native controls are being used and why. If there is ambiguity about whether a native control fits, ask the user before proceeding.

- Search the platform SDK for an existing control before writing a custom one
- When a native control almost fits, customize it rather than replacing it with a from-scratch implementation
- Justify every third-party UI dependency with a concrete gap the platform SDK cannot fill

