
- Code MUST call a Windows program from WSL by its full name including `.exe` (`explorer.exe`, `powershell.exe`). Interop and the appending of Windows `PATH` entries are on by default and can be turned off in `[interop]` (`enabled`, `appendWindowsPath`); a script MUST check that the program exists instead of assuming it.
- Code MUST detect WSL before using Windows-only commands and MUST NOT run them from plain Linux.
- Code MUST NOT assume a networking mode. The Windows host and the distribution may or may not share `localhost`, so the address MUST be configurable.

