---
id: 5358bc26-ea8f-4dd0-94d1-22dc1c6ad291
title: "Never overwrite a user's files"
domain: agenticdevelopercookbook://guidelines/implementing/skills-and-agents/never-clobber-user-files
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "A shipped skill, command or agent file must never replace a user's file of the same name; installs must namespace what they ship or check for an existing file first."
platforms:
  - macos
  - linux
  - windows
tags:
  - skills
  - commands
  - install
  - shared-resources
  - namespacing
depends-on:
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/authoring-skills-and-rules
related:
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/skill-structure-reference
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/agent-structure-reference
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/rule-structure-reference
  - agenticdevelopercookbook://guidelines/implementing/code-quality/shell-scripts
  - agenticdevelopercookbook://guidelines/reviewing/skills-and-agents/never-clobber-user-files
  - agenticdevelopercookbook://principles/idempotency
  - agenticdevelopercookbook://principles/explicit-over-implicit
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - skill-authoring
  - configuration
---

# Never overwrite a user's files

Skills, commands, agents and rules are installed into directories the user also writes to. Those directories are shared resources: the user may already have a file with the same name, and an install that replaces it destroys work the user cannot get back. This applies whichever tool reads the directory.

## Rules

- An install or update MUST NOT overwrite, truncate or delete a file it did not create. A file of the same name that is not yours is the user's.
- Namespace everything you ship. Use a name that carries your project or team prefix (`acme-review`, not `review`), or a directory that is yours (`acme/review/SKILL.md`), so a collision with a user's own name is unlikely.
- Check before you write. If the target exists, compare it to what you would write. If it is identical, do nothing. If it is a file you installed earlier (see the marker below), update it. If it is anything else, leave it, report the conflict by name, and stop for that file.
- Mark what you install. Put a recognizable marker in each file (a frontmatter field or a comment naming the package and version) or keep a manifest of installed paths, so an update and an uninstall touch only your files.
- Never fix a collision by renaming the user's file or by removing it. Rename or skip your own.
- Uninstall removes only files recorded as yours, and only if they still match what you wrote. A file the user has edited is left in place and reported.
- Do the check in the installer, not in the shipped file. A skill must not rely on being the only one with its name.
- Make installs idempotent: running one twice leaves the same files and reports no conflict with itself.

## Collisions in names that merge

- Some directories merge entries from several levels (project over user over built-in). A shipped file that shares a name with a user's file in another level may silently shadow or be shadowed. Choose names that are unlikely to repeat across levels, and document the shadowing in the install report.

## Reporting

- Print one line per skipped file: the path, why it was skipped, and what the user can do (rename theirs, or install with your own prefix).
- Exit with a non-zero status when any file was skipped for a conflict, so automation notices.

## Why this matters

An overwritten command or skill is the worst kind of install bug: it succeeds, looks fine, and later the user finds their own work gone or replaced by something that behaves differently. The rules cost one existence check and a prefix, and make installs safe to repeat.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
