
# No external dependencies in core libraries

`roadmap_lib` uses the standard library only. Third-party packages (PyYAML, requests, etc.) MUST NOT be added to core library code. This keeps the library portable and installable without dependency management.

