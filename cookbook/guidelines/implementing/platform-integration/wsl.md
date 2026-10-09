---
id: 6aa54d1a-1888-4107-9e8d-1c2f0ef0c320
title: "Windows Subsystem for Linux"
domain: agenticdevelopercookbook://guidelines/implementing/platform-integration/wsl
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Work across the Windows and WSL boundary deliberately: keep Linux-tool projects in the Linux file system, convert paths with wslpath, align line endings, and respect permission, case-sensitivity and interop limits."
platforms:
  - windows
  - linux
tags:
  - wsl
  - windows
  - paths
  - line-endings
  - interop
  - filesystem
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/language/powershell
  - agenticdevelopercookbook://guidelines/implementing/code-quality/shell-scripts
  - agenticdevelopercookbook://guidelines/implementing/code-quality/visual-studio-project-files
  - agenticdevelopercookbook://guidelines/reviewing/platform-integration/wsl
  - agenticdevelopercookbook://principles/explicit-over-implicit
references:
  - https://learn.microsoft.com/en-us/windows/wsl/filesystems
  - https://learn.microsoft.com/en-us/windows/wsl/case-sensitivity
  - https://learn.microsoft.com/en-us/windows/wsl/wsl-config
  - https://learn.microsoft.com/en-us/windows/wsl/file-permissions
  - https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-git
  - https://learn.microsoft.com/en-us/windows/dev-environment/wsl-interop
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - platform-integration
  - configuration
---

# Windows Subsystem for Linux

Code that runs partly in Windows and partly in a WSL distribution crosses a boundary between two file systems, two path syntaxes and two sets of permissions. These rules keep that crossing explicit.

## Where files live

- Keep project files that Linux tools work on in the Linux file system (for example `/home/<user>/project`), not under `/mnt/c/...`. Cross-boundary access is slower, which shows up in builds, package installs and file watchers.
- Files that Windows tools work on live in the Windows file system. Open a WSL directory from Windows with `explorer.exe .` or through the `\\wsl$` share.
- Do not hardcode `/mnt/c`. The automount root is configurable in `/etc/wsl.conf` under `[automount]` (`root`).

## Path conversion

- Convert paths with `wslpath`, never by string replacement. `wslpath "C:\Users\me"` returns the Linux path, `wslpath -w` returns the Windows path (a `\\wsl.localhost\<distro>\...` path for files inside the distribution), and `wslpath -m` returns a `C:/...` form with forward slashes.
- The `\\wsl$` share resolves only while the distribution is running. Start it before relying on the path.

## Line endings

- Use one line-ending convention across Windows, WSL and containers. Set it in `.gitattributes` per file type, not in each developer's global configuration, and keep shell scripts as LF: a script with CRLF endings fails in Linux with confusing errors.
- Install Git in each file system you use it from, and make sure each is configured for the same convention.

## Permissions and case

- Linux file permissions on a Windows drive are translated from Windows permissions unless metadata is enabled. A Windows read-only attribute removes write access. With the `metadata` mount option, WSL stores Linux owner, group and mode in NTFS extended attributes, so a `chmod` persists. Set `uid`, `gid`, `umask`, `fmask` and `dmask` in `[automount] options` when the defaults do not suit.
- Windows is case-insensitive and Linux is case-sensitive. Two files that differ only by case can exist in WSL and collide in Windows. Per-directory case sensitivity is a flag on NTFS directories, controlled with `fsutil.exe file setCaseSensitiveInfo <path> enable` (and `disable`, `queryCaseSensitiveInfo`). Windows applications may fail in a case-sensitive directory, and directories created by Windows applications are not case-sensitive.
- Directories in the WSL file system are case-sensitive by default.

## Interop

- Call a Windows program from WSL by its full name including `.exe` (`explorer.exe`, `powershell.exe`). Interop and the appending of Windows `PATH` entries are on by default and can be turned off in `[interop]` (`enabled`, `appendWindowsPath`); a script must check that the program exists instead of assuming it.
- Detect WSL before using Windows-only commands; do not run them from plain Linux.
- Do not assume a networking mode. The Windows host and the distribution may or may not share `localhost`, so make the address configurable.

## Configuration scope

- `/etc/wsl.conf` configures one distribution. `%UserProfile%\.wslconfig` configures all WSL 2 distributions.
- A change takes effect only after the distribution has stopped. Run `wsl --terminate <distro>` or `wsl --shutdown` and wait for the distribution to exit before restarting it.

## Why this matters

WSL hides the boundary until it costs you: a build that takes ten times longer on a mounted drive, a script that breaks on a carriage return, a file that exists twice on Windows. Knowing where the boundary is, and converting across it with the platform's own tools, avoids all of these.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
