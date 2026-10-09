
- Call a Windows program from WSL by its full name including `.exe` (`explorer.exe`, `powershell.exe`). Interop and the appending of Windows `PATH` entries are on by default and can be turned off in `[interop]` (`enabled`, `appendWindowsPath`); a script must check that the program exists instead of assuming it.
- Detect WSL before using Windows-only commands; do not run them from plain Linux.
- Do not assume a networking mode. The Windows host and the distribution may or may not share `localhost`, so make the address configurable.

