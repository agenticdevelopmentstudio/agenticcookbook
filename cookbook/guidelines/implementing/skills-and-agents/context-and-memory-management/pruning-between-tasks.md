
- On switching to an unrelated task, the agent **SHOULD** reset context so prior files and tool output do not bias the new work.
- After repeated failed correction attempts on one problem, the agent **SHOULD** clear the polluted context and restart from a sharper prompt rather than layering more corrections — failed approaches in-window degrade subsequent reasoning.

> Note: larger context windows (forecast to keep growing) raise the threshold at which curation becomes urgent, but do not remove the degradation-with-fill effect. Treat a bigger window as more headroom, not a license to stop curating — this is a durable property, not a vendor-specific number.

