
When context approaches its limit, harnesses summarize older history (compaction). Summaries discard detail, so anything not explicitly preserved can vanish silently.

- Before a compaction is likely, the agent **MUST** ensure the **list of modified files** and the **test/run/build commands** are recorded somewhere durable (a memory file or compaction directive), so they survive the summary.
- The agent **SHOULD** assume compaction loses specifics: exact line numbers, intermediate reasoning, and raw tool output are not guaranteed to persist.
- Where the harness supports it, the agent **SHOULD** declare compaction-preservation directives (e.g. "when compacting, always keep the full modified-file list and test commands").

