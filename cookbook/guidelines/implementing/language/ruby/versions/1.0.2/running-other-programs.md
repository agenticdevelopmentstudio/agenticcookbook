
- Code SHOULD use `Open3.capture2`, `capture2e` or `capture3` with separate arguments: `Open3.capture2e("git", "status")`. With an executable path plus arguments no shell is involved. A single command string is handed to the shell, so code MUST NOT build one from outside input.
- These calls return the output and a `Process::Status`; code MUST check `status.success?` rather than ignoring it. A missing executable raises `Errno::ENOENT`, so code SHOULD rescue that when absence is expected.
- Standard input SHOULD be fed through the `stdin_data:` option.
- `Process.spawn` and similar calls also route a single string that contains shell metacharacters through `/bin/sh`. Code MUST pass an argument list instead.

