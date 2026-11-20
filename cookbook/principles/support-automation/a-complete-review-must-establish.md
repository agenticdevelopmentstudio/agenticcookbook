
- `should-expose-capabilities-through-automation`: whether the application's capabilities are exposed through automation interfaces, not just interactive UI
- `should-use-platform-automation-frameworks`: whether core actions are exposed through the platform's automation frameworks where it provides them
- `should-treat-accessibility-tree-as-backbone`: whether automation rests on the accessibility tree, the semantic foundation it shares with assistive technology
- `should-design-composable-commands`: whether operations are discrete, composable commands that can be invoked programmatically
- `should-provide-non-interactive-entry-points`: whether non-interactive entry points (CLI, URL schemes, intent filters) let workflows and tools drive the app without a human
- `should-provide-non-interactive-entry-points`: Key operations callable non-interactively (no required interactive prompts for automation paths);
- `should-wrap-deterministic-operations-in-scripts`: shell scripts wrap deterministic operations for direct invocation;
- `should-allow-chaining-without-confirmation`: skills can be chained without requiring human confirmation at each step;
- `should-emit-machine-parseable-output`: outputs are machine-parseable (not just human-readable)
