
- `must-record-modified-files-and-commands-before-compaction`, `should-assume-compaction-loses-specifics`, `should-declare-compaction-preservation-directives`: When context approaches its limit, harnesses summarize older history (compaction). Summaries discard detail, so anything not explicitly preserved can vanish silently.
- `must-keep-memory-files-concise`, `should-keep-only-behavior-changing-memory`, `should-prune-memory-regularly`: An overstuffed memory file dilutes attention and causes the agent to ignore the rules that matter.
- `should-treat-a-bigger-window-as-headroom`: Note: larger context windows (forecast to keep growing) raise the threshold at which curation becomes urgent, but do not remove the degradation-with-fill effect.

