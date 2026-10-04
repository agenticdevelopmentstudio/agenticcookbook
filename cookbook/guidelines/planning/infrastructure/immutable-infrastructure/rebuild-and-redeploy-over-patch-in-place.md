
- To change configuration, dependencies, or code, you **MUST** rebuild the image and roll out new instances — not SSH in to mutate the live one.
- Running instances **SHOULD** be treated as read-only; no manual `apt install`, no live config edits, no hotfix scripts that survive a restart.
- This eliminates **configuration drift**: every instance of version `vN` is byte-identical, so "works on that box but not this one" cannot happen.

