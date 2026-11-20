
- `must-verify-bulk-operations`: whether an operation touching more than 5 files had a verification pass before it was considered complete
- `must-not-complete-with-stale-references`: whether the operation was marked complete with any stale reference left
- `must-grep-for-stale-references`: whether the entire repo was grepped for the old names, paths and identifiers
- `should-verify-cross-reference-integrity`: whether every file referencing a renamed or moved entity was updated
- `should-confirm-completeness`: whether what was changed was compared against what should have been changed
- `should-verify-after-bulk-changes`: whether each rename, migration, restructuring or multi-file convention update was followed by a verification pass
- `should-verify-each-repo-independently`: whether each repo of a cross-repo operation was verified independently
- `should-run-cross-repo-check`: whether a cross-repo consistency check was run
