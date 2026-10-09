
- An install or update MUST NOT overwrite, truncate or delete a file it did not create. A file of the same name that is not yours is the user's.
- Namespace everything you ship. Use a name that carries your project or team prefix (`acme-review`, not `review`), or a directory that is yours (`acme/review/SKILL.md`), so a collision with a user's own name is unlikely.
- Check before you write. If the target exists, compare it to what you would write. If it is identical, do nothing. If it is a file you installed earlier (see the marker below), update it. If it is anything else, leave it, report the conflict by name, and stop for that file.
- Mark what you install. Put a recognizable marker in each file (a frontmatter field or a comment naming the package and version) or keep a manifest of installed paths, so an update and an uninstall touch only your files.
- Never fix a collision by renaming the user's file or by removing it. Rename or skip your own.
- Uninstall removes only files recorded as yours, and only if they still match what you wrote. A file the user has edited is left in place and reported.
- Do the check in the installer, not in the shipped file. A skill must not rely on being the only one with its name.
- Make installs idempotent: running one twice leaves the same files and reports no conflict with itself.

