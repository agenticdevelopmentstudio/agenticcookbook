
- `/etc/wsl.conf` configures one distribution. `%UserProfile%\.wslconfig` configures all WSL 2 distributions.
- A change takes effect only after the distribution has stopped. Run `wsl --terminate <distro>` or `wsl --shutdown` and wait for the distribution to exit before restarting it.

