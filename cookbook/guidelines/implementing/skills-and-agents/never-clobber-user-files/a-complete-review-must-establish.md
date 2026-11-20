
- `must-not-overwrite-files-it-did-not-create`: whether any install or update can overwrite, truncate or delete a file it did not create
- `should-namespace-everything-shipped`: whether every shipped name carries a project or team prefix or lives in the package's own directory
- `should-not-duplicate-a-built-in-name`: whether any shipped name duplicates a common built-in name
- `should-check-before-writing`: whether every write to a shared directory is preceded by an existence check that compares, updates, or skips and reports
- `should-mark-what-is-installed`: whether every installed file carries a marker or is listed in a manifest
- `must-not-rename-or-remove-the-users-file`: whether any collision is fixed by renaming or removing the user's file
- `should-uninstall-only-own-unchanged-files`: whether uninstall removes only recorded files that still match what was written
- `should-check-in-the-installer`: whether the collision check is in the installer rather than the shipped file
- `must-not-rely-on-a-unique-name`: whether any skill relies on being the only one with its name
- `should-make-installs-idempotent`: whether a second install leaves the same files and reports no conflict with itself
- `should-choose-names-unlikely-to-repeat-across-levels`: whether shipped names are unlikely to repeat across levels
- `should-document-shadowing-in-the-install-report`: whether the install report documents shadowing
- `should-print-one-line-per-skipped-file`: whether each skipped file gets one line with its path, the reason and what the user can do
- `should-exit-non-zero-on-a-skipped-conflict`: whether the installer exits non-zero when any file was skipped for a conflict

