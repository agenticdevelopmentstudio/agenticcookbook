
- Code MUST convert paths with `wslpath` and MUST NOT use string replacement. `wslpath "C:\Users\me"` returns the Linux path, `wslpath -w` returns the Windows path (a `\\wsl.localhost\<distro>\...` path for files inside the distribution), and `wslpath -m` returns a `C:/...` form with forward slashes.
- The `\\wsl$` share resolves only while the distribution is running. The distribution MUST be started before code relies on the path.

