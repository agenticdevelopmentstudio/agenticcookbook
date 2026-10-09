---
id: cfa4b119-d10a-4c2a-b90d-f003717792a7
title: "Never overwrite a user's files"
domain: agenticdevelopercookbook://guidelines/reviewing/skills-and-agents/never-clobber-user-files
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Review installers and shipped skills, commands and agents for namespacing, existence checks, ownership markers and safe uninstall."
platforms:
  - macos
  - linux
  - windows
tags:
  - skills
  - commands
  - install
  - review
  - shared-resources
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/skills-and-agents/never-clobber-user-files
  - agenticdevelopercookbook://guidelines/reviewing/skills-and-agents/skill-checklist
  - agenticdevelopercookbook://guidelines/reviewing/skills-and-agents/agent-checklist
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - code-review
  - pre-commit
---

# Never overwrite a user's files

Review installers and the files they ship against [Never overwrite a user's files](agenticdevelopercookbook://guidelines/implementing/skills-and-agents/never-clobber-user-files).

## Writes

- Every write to a shared directory is preceded by an existence check.
- A same-name file that the installer did not create is skipped and reported, never replaced, truncated or deleted.
- Identical content is a no-op, and a second run reports nothing new.

## Names

- Shipped names carry a project or team prefix, or live in a directory that belongs to the package.
- A name does not duplicate a common built-in name.

## Ownership

- Each installed file carries a marker or is listed in a manifest.
- Update and uninstall touch only marked or listed files, and only when they still match what was written.

## Reporting

- Skipped files are listed by path with a reason, and the exit status is non-zero when any conflict was skipped.

## Why this matters

The bug is invisible on a clean test machine, where no user file exists to collide with. Review has to ask the question the test machine cannot.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
