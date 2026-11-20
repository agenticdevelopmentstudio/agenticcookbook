
- `must-not-overwrite-files-it-did-not-create`: an install or update over a same-name user file leaves that file unchanged
- `should-namespace-everything-shipped`: every shipped name has the project or team prefix or sits in the package's own directory
- `should-not-duplicate-a-built-in-name`: no shipped name equals a common built-in name
- `should-check-before-writing`: every write to a shared directory follows an existence check: identical is skipped, an earlier install is updated, anything else is left and reported
- `should-mark-what-is-installed`: every installed file has a marker or a manifest entry
- `must-not-rename-or-remove-the-users-file`: no code path renames or removes a user's file to resolve a collision
- `should-uninstall-only-own-unchanged-files`: uninstall removes only recorded files that still match, and leaves and reports an edited one
- `should-check-in-the-installer`: the collision check lives in the installer
- `must-not-rely-on-a-unique-name`: no skill depends on being the only one with its name
- `should-make-installs-idempotent`: running the install twice leaves the same files and reports no conflict with itself
- `should-choose-names-unlikely-to-repeat-across-levels`: shipped names are distinct from names at the other levels of a merging directory
- `should-document-shadowing-in-the-install-report`: the install report states any shadowing
- `should-print-one-line-per-skipped-file`: each skipped file prints one line with path, reason and the user's options
- `should-exit-non-zero-on-a-skipped-conflict`: the exit status is non-zero when any file was skipped for a conflict

