
- **macOS/Linux**: Hook script uses `#!/bin/bash` shebang and `chmod +x`. Works on any POSIX system with bash.
- **Windows**: Hook script requires Git Bash, WSL, or another bash-compatible shell. The `$HOME` variable in the settings command path resolves correctly in these environments. Native PowerShell is not supported.

