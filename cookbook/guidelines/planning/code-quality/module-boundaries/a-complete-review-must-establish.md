
- `should-treat-each-declared-target-as-candidate`: whether every independently declared build target or package is a candidate, regardless of size
- `may-merge-trivial-wrappers`: whether any merged wrapper target holds only re-exports with no logic of its own
- `should-flag-large-monolithic-targets`: whether every 200+ file target is flagged for secondary analysis
- `should-group-test-targets-with-main-target`: whether test targets follow their main target
- `should-not-separate-test-targets`: whether a test target got its own scope group without testing multiple main targets
- `should-exclude-vendor-directories`: whether vendor and third-party directories are excluded
- `should-note-shared-directories`: whether `core`, `common`, `shared` and `util` directories are noted
- `should-not-auto-split-shared-directories`: whether such directories were split automatically
