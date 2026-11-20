
- Run external programs with `subprocess.run`, passing the command as a list: `subprocess.run(["git", "status"], check=True)`.
- Never use `shell=True` with a string that contains any value you did not write yourself. A list of arguments never reaches a shell, so there is nothing to escape. If a shell is truly required, quote each interpolated value with `shlex.quote`.
- Pass `check=True` so a non-zero exit raises `CalledProcessError`, or inspect `returncode` on purpose.
- Pass `timeout=` for any command that could hang. On expiry the child is killed and `TimeoutExpired` is raised.
- Use `capture_output=True` with `text=True` to read output. Do not combine `capture_output` with explicit `stdout` or `stderr` arguments.
- The `env` argument replaces the inherited environment. Build it from `os.environ` plus your changes unless you want a clean one.

