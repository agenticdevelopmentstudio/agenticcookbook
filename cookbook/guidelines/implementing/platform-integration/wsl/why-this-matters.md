
WSL hides the boundary until it costs you: a build that takes ten times longer on a mounted drive, a script that breaks on a carriage return, a file that exists twice on Windows. Knowing where the boundary is, and converting across it with the platform's own tools, avoids all of these.

Boundary bugs rarely appear on the author's machine. A checklist aimed at the boundary catches them in review.

- `linux-files-in-linux-fs`: Cross-boundary access is slower, which shows up in builds, package installs and file watchers.
