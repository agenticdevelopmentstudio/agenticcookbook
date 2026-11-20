
- `must-use-built-in-frameworks-first`: whether a platform built-in framework was used before any custom implementation
- `should-note-native-controls-used`: whether each generated component notes which native controls it uses and why
- `should-ask-when-native-fit-is-ambiguous`: whether the user was asked before proceeding wherever it was ambiguous that a native control fits
- `should-search-sdk-before-custom-control`: whether the platform SDK was searched for an existing control before a custom one was written
- `should-customize-near-fit-native-controls`: whether native controls that almost fit were customized rather than replaced from scratch
- `should-justify-third-party-ui-dependencies`: whether each third-party UI dependency is justified by a concrete gap the platform SDK cannot fill
- `must-not-reimplement-standard-winui3-controls`: No custom reimplementations of standard WinUI 3 controls;
- `should-use-windows-app-sdk-for-system-integration`: system APIs used for file access, notifications, and background tasks;
- `should-document-native-control-deviations`: deviations from native controls documented with rationale
