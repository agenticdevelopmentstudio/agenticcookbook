
- `Open3` and `Process` calls pass separate arguments. No interpolated command string.
- The `Process::Status` is checked. `Errno::ENOENT` is rescued where a missing tool is expected.

