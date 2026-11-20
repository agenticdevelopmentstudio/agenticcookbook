
- `must-use-built-in-frameworks-first`: the platform's built-in frameworks are used before any custom implementation (Swift Concurrency, Room/SwiftData, Fetch API)
- `should-note-native-controls-used`: each generated component notes which native controls it uses and why, or the work says why not
- `should-ask-when-native-fit-is-ambiguous`: the user was asked before proceeding wherever it was ambiguous that a native control fits, or the work says why not
- `should-search-sdk-before-custom-control`: the platform SDK was searched for an existing control before each custom one was written, or the work says why not
- `should-customize-near-fit-native-controls`: every native control that almost fit was customized rather than replaced from scratch, or the work says why not
- `should-justify-third-party-ui-dependencies`: every third-party UI dependency names a concrete gap the platform SDK cannot fill, or the work says why not
- `must-not-reimplement-standard-winui3-controls`: no standard WinUI 3 control the build needs is custom-reimplemented
- `should-use-windows-app-sdk-for-system-integration`: Windows system integration (file access, notifications, background tasks) uses Windows App SDK APIs, or the build says why not
- `should-document-native-control-deviations`: each deviation from a native control is documented with its rationale
