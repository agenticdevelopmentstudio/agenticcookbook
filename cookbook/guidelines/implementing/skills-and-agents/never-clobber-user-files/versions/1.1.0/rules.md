
- **must-not-overwrite-files-it-did-not-create**: An install or update MUST NOT overwrite, truncate or delete a file it did not create. A file of the same name that is not yours is the user's.
- **should-namespace-everything-shipped**: Everything you ship SHOULD be namespaced. Use a name that carries your project or team prefix (`acme-review`, not `review`), or a directory that is yours (`acme/review/SKILL.md`), so a collision with a user's own name is unlikely.
- **should-not-duplicate-a-built-in-name**: A shipped name SHOULD NOT duplicate a common built-in name.
- **should-check-before-writing**: An installer SHOULD check before it writes. If the target exists, compare it to what you would write. If it is identical, do nothing. If it is a file you installed earlier (see the marker below), update it. If it is anything else, leave it, report the conflict by name, and stop for that file.
- **should-mark-what-is-installed**: An installer SHOULD mark what it installs. Put a recognizable marker in each file (a frontmatter field or a comment naming the package and version) or keep a manifest of installed paths, so an update and an uninstall touch only your files.
- **must-not-rename-or-remove-the-users-file**: A collision MUST NOT be fixed by renaming the user's file or by removing it. Rename or skip your own.
- **should-uninstall-only-own-unchanged-files**: Uninstall SHOULD remove only files recorded as yours, and only if they still match what you wrote. A file the user has edited is left in place and reported.
- **should-check-in-the-installer**: The check SHOULD be done in the installer, not in the shipped file.
- **must-not-rely-on-a-unique-name**: A skill MUST NOT rely on being the only one with its name.
- **should-make-installs-idempotent**: Installs SHOULD be idempotent: running one twice leaves the same files and reports no conflict with itself.
- **should-choose-names-unlikely-to-repeat-across-levels**: Shipped files SHOULD have names that are unlikely to repeat across levels.
- **should-document-shadowing-in-the-install-report**: The install report SHOULD document the shadowing.
- **should-print-one-line-per-skipped-file**: An installer SHOULD print one line per skipped file: the path, why it was skipped, and what the user can do (rename theirs, or install with your own prefix).
- **should-exit-non-zero-on-a-skipped-conflict**: An installer SHOULD exit with a non-zero status when any file was skipped for a conflict, so automation notices.

