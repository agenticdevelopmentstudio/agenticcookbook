
- **must-use-built-in-frameworks-first**: MUST use the platform's built-in frameworks before custom implementations: Swift Concurrency over raw threads, Room/SwiftData over raw SQLite, Fetch API over custom HTTP.
- **should-note-native-controls-used**: When generating a component, SHOULD explicitly note which native controls are being used and why.
- **should-ask-when-native-fit-is-ambiguous**: If there is ambiguity about whether a native control fits, SHOULD ask the user before proceeding.
- **should-search-sdk-before-custom-control**: SHOULD search the platform SDK for an existing control before writing a custom one.
- **should-customize-near-fit-native-controls**: When a native control almost fits, SHOULD customize it rather than replacing it with a from-scratch implementation.
- **should-justify-third-party-ui-dependencies**: SHOULD justify every third-party UI dependency with a concrete gap the platform SDK cannot fill.
