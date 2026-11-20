
- `should-not-group-call-sites`, `should-note-cross-cutting-concerns-not-isolate`: Logging calls scattered through every file are not a scope group; they are woven in.
- `should-treat-call-sites-as-dependencies`: The call sites in other groups are dependencies on this group, not members of it.
- `should-classify-logging-configuration-as-infrastructure`: The `OSLog` / `Logger` configuration file is infrastructure. The `os.log("did the thing")` call in a view controller is not.
- `should-inject-not-merge-shared-dependency`: Pervasive coupling is an architectural smell, not a decomposition strategy.
- `must-give-auth-infrastructure-own-scope-group`, `must-not-treat-auth-as-merely-cross-cutting`: The SessionManager and token lifecycle have real behavior and state and warrant their own scope group (separate from where auth checks are enforced).
- `must-catalog-di-container-separately`: A composition root is not itself a scope group in the functional sense, but it is a file (or files) that must be cataloged separately.
