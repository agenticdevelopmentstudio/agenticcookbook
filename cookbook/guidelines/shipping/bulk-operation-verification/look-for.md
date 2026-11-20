
- `must-verify-bulk-operations`: an operation touching more than 5 files shows a verification pass before it is reported complete; one reported done with no pass breaks it
- `must-not-complete-with-stale-references`: the verification pass's result shows zero stale references at the point the operation is marked complete
- `must-grep-for-stale-references`: a repo-wide search for the old names, paths or identifiers was run across source, docs, configuration, indexes, skills, rules and test fixtures
- `should-verify-cross-reference-integrity`: every file referencing a renamed or moved entity was updated, including the common miss points (README and CLAUDE.md, indexes and tables of contents, imports and require paths, skill and rule files, CI/CD configuration, symlinks)
- `should-confirm-completeness`: a list of what was changed was compared against what should have been changed
- `should-verify-after-bulk-changes`: a verification pass followed each rename, cross-directory or cross-repo migration, directory restructuring, or multi-file convention update
- `should-verify-each-repo-independently`: in a cross-repo operation, each repo was verified on its own
- `should-run-cross-repo-check`: in a cross-repo operation, a cross-repo check confirmed each shared identifier resolves in every repo that references it
