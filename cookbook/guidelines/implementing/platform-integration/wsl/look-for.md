
Review changes that run across Windows and WSL against Windows Subsystem for Linux ([adc.guideline.implementing.platform-integration.wsl](cookbook:6aa54d1a-1888-4107-9e8d-1c2f0ef0c320)).

- `linux-files-in-linux-fs`: Linux-tool project files are not placed under `/mnt/c`, and no path hardcodes the automount root.
- `windows-files-in-windows-fs`: files Windows tools work on kept inside the WSL file system
- `must-not-hardcode-mnt-c`: a literal `/mnt/c` in code or scripts
- `must-convert-with-wslpath`: Paths cross the boundary through `wslpath`, not string substitution.
- `must-start-distribution-first`: Windows-side code using a `\\wsl$` path with no step that starts the distribution first
- `must-use-one-line-ending-convention`: files whose line endings differ between Windows, WSL and containers
- `must-set-in-gitattributes`: `.gitattributes` fixes line endings per file type.
- `shell-scripts-must-stay-lf`: Shell scripts are LF.
- `install-git-per-file-system`: a workflow running Windows Git on WSL files, or WSL Git on Windows files
- `must-configure-git-same-convention`: Git installations in Windows and WSL configured with different line-ending settings
- `set-automount-options`: Code does not depend on Linux permissions of files on a Windows drive without the `metadata` option.
- `should-not-differ-only-by-case`: No two paths differ only by case. Per-directory case-sensitivity changes are intentional and documented.
- `must-call-with-exe`: Windows programs are called with their `.exe` suffix and only after a check that interop is available.
- `must-check-program-exists`: a script that calls a Windows program without checking that it exists
- `must-detect-wsl`: WSL detection guards every Windows-only command.
- `must-not-assume-networking-mode`: code that assumes the host and distribution do, or do not, share `localhost`
- `must-make-address-configurable`: Network addresses are configurable.
- `must-restart-after-config-change`: `wsl.conf` and `.wslconfig` changes say which scope they target and require a restart of the distribution.
