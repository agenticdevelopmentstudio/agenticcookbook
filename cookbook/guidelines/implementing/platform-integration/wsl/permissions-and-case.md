
- Linux file permissions on a Windows drive are translated from Windows permissions unless metadata is enabled. A Windows read-only attribute removes write access. With the `metadata` mount option, WSL stores Linux owner, group and mode in NTFS extended attributes, so a `chmod` persists.
- Windows is case-insensitive and Linux is case-sensitive. Per-directory case sensitivity is a flag on NTFS directories, controlled with `fsutil.exe file setCaseSensitiveInfo <path> enable` (and `disable`, `queryCaseSensitiveInfo`). Windows applications may fail in a case-sensitive directory, and directories created by Windows applications are not case-sensitive.
- Directories in the WSL file system are case-sensitive by default.
