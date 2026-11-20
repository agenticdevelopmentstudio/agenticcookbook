
# Support Automation

Applications should expose their capabilities through automation interfaces, not just interactive UI. Automation support is a design constraint — not an afterthought — that improves accessibility, testability, and composability.

- Expose core actions through platform automation frameworks (AppIntents, AppActions, UI Automation, APIs) wherever the platform provides them
- Treat the accessibility tree as the automation backbone — scriptability and assistive technology share the same semantic foundation
- Design operations as discrete, composable commands that can be invoked programmatically, not just through clicks and taps
- Provide non-interactive entry points (CLI, URL schemes, intent filters) so workflows and tools can drive the app without a human in the loop

