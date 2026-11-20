
`wslpath "C:\Users\me"` returns the Linux path, `wslpath -w` returns the Windows path (a `\\wsl.localhost\<distro>\...` path for files inside the distribution), and `wslpath -m` returns a `C:/...` form with forward slashes.
