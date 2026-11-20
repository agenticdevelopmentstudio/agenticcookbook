
Review installers and the files they ship against the rules above.

- `must-not-overwrite-files-it-did-not-create`: A same-name file that the installer did not create is skipped and reported, never replaced, truncated or deleted.
- `should-namespace-everything-shipped`: Shipped names carry a project or team prefix, or live in a directory that belongs to the package.
- `should-not-duplicate-a-built-in-name`: A name does not duplicate a common built-in name.
- `should-check-before-writing`: Every write to a shared directory is preceded by an existence check.
- `should-mark-what-is-installed`: Each installed file carries a marker or is listed in a manifest.
- `must-not-rename-or-remove-the-users-file`: a collision handled by renaming or removing the user's file rather than renaming or skipping the shipped one.
- `should-uninstall-only-own-unchanged-files`: Update and uninstall touch only marked or listed files, and only when they still match what was written.
- `should-check-in-the-installer`: a collision check placed in the shipped file instead of the installer.
- `must-not-rely-on-a-unique-name`: a skill whose behavior depends on no other skill having its name.
- `should-make-installs-idempotent`: Identical content is a no-op, and a second run reports nothing new.
- `should-choose-names-unlikely-to-repeat-across-levels`: a shipped name likely to repeat a name at another level of a merging directory.
- `should-document-shadowing-in-the-install-report`: an install report that does not mention shadowing across levels.
- `should-print-one-line-per-skipped-file`: Skipped files are listed by path with a reason, and the exit status is non-zero when any conflict was skipped.
- `should-exit-non-zero-on-a-skipped-conflict`: an installer that exits zero after skipping a file for a conflict.

