
- `must-use-built-in-frameworks-first`: a custom implementation (raw threads, raw SQLite, custom HTTP) where a built-in framework exists
- `should-note-native-controls-used`: a generated component with no note of which native controls it uses and why
- `should-ask-when-native-fit-is-ambiguous`: a custom control built where it was unclear a native one fit, with no question to the user
- `should-search-sdk-before-custom-control`: a custom control that duplicates one the platform SDK already has
- `should-customize-near-fit-native-controls`: a from-scratch implementation replacing a native control that almost fit
- `should-justify-third-party-ui-dependencies`: a third-party UI dependency with no concrete gap in the platform SDK named
