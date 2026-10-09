
- Use `Open3.capture2`, `capture2e` or `capture3` with separate arguments: `Open3.capture2e("git", "status")`. With an executable path plus arguments no shell is involved. A single command string is handed to the shell, so never build one from outside input.
- These calls return the output and a `Process::Status`; check `status.success?` rather than ignoring it. A missing executable raises `Errno::ENOENT`, so rescue that when absence is expected.
- Feed standard input through the `stdin_data:` option.
- `Process.spawn` and similar calls also route a single string that contains shell metacharacters through `/bin/sh`. Pass an argument list instead.

