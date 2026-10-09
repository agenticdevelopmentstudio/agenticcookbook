
- Linux-tool project files are not placed under `/mnt/c`, and no path hardcodes the automount root.
- Paths cross the boundary through `wslpath`, not string substitution.

