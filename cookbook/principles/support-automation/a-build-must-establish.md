
- `should-expose-capabilities-through-automation`: the application's capabilities are exposed through automation interfaces, not just interactive UI, or the work says why not
- `should-use-platform-automation-frameworks`: core actions are exposed through the platform's automation frameworks (AppIntents, AppActions, UI Automation, APIs) wherever it provides them, or the work says why not
- `should-treat-accessibility-tree-as-backbone`: automation is driven through the accessibility tree and every control is present in it, or the work says why not
- `should-design-composable-commands`: operations are discrete, composable commands invokable programmatically, or the work says why not
- `should-provide-non-interactive-entry-points`: non-interactive entry points (CLI, URL schemes, intent filters) let workflows and tools drive the app without a human in the loop, or the work says why not
- `should-wrap-deterministic-operations-in-scripts`: every deterministic operation is wrapped in a shell script that can be invoked directly
- `should-allow-chaining-without-confirmation`: every skill can be chained without human confirmation at each step
- `should-emit-machine-parseable-output`: every output is machine-parseable, not just human-readable
