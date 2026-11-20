
- `must-verify-bulk-operations`: every operation touching more than 5 files has a recorded verification pass before completion
- `must-not-complete-with-stale-references`: the last verification pass before completion returned zero stale references
- `must-grep-for-stale-references`: a repo-wide grep for every old name, path and identifier finds none left in source, docs, configuration, indexes, skills, rules or test fixtures
- `should-verify-cross-reference-integrity`: every file referencing a renamed or moved entity points at its new name or path, or the work says why not
- `should-confirm-completeness`: the list of changed files matches the list of intended files, or the work says why not
- `should-verify-after-bulk-changes`: every rename, migration, restructuring and multi-file convention update has its verification pass, or the work says why not
- `should-verify-each-repo-independently`: each repo of a cross-repo operation has its own verification pass, or the work says why not
- `should-run-cross-repo-check`: every shared identifier resolves in each repo that references it, or the work says why not
