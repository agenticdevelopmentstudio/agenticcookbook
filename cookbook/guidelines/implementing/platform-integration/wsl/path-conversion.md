
- Convert paths with `wslpath`, never by string replacement. `wslpath "C:\Users\me"` returns the Linux path, `wslpath -w` returns the Windows path (a `\\wsl.localhost\<distro>\...` path for files inside the distribution), and `wslpath -m` returns a `C:/...` form with forward slashes.
- The `\\wsl$` share resolves only while the distribution is running. Start it before relying on the path.

