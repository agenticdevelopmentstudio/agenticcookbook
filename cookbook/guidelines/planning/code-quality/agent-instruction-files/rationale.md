
- `should-symlink-one-canonical-file`: two maintained copies drift; a symlink keeps one source.
- `should-nest-per-package-files`: Agents read the **nearest** file up the directory tree, so the closest one takes precedence over the root file.
- `must-stay-concise`: A widely-reported failure mode is that bloated, stale instruction files get partially ignored and can degrade task success.
- `should-delete-obsolete-instructions`: Note this is a practitioner heuristic, not a settled empirical result; the durable principle is signal-to-noise.
