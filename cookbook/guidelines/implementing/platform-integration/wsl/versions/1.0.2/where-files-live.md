
- Project files that Linux tools work on SHOULD live in the Linux file system (for example `/home/<user>/project`), not under `/mnt/c/...`. Cross-boundary access is slower, which shows up in builds, package installs and file watchers.
- Files that Windows tools work on SHOULD live in the Windows file system. Open a WSL directory from Windows with `explorer.exe .` or through the `\\wsl$` share.
- Code MUST NOT hardcode `/mnt/c`. The automount root is configurable in `/etc/wsl.conf` under `[automount]` (`root`).

