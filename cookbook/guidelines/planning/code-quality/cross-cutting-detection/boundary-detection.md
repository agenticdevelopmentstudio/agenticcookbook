
1. **Cross-cutting concerns are noted, not isolated.** When a concern appears across all scope groups, note it in findings as cross-cutting and move on. Do not create a scope group whose members are "all the places that call log()".
2. **Shared infrastructure gets exactly one scope group.** If a concern has its own files (a Logger class, a SessionManager), those files form one scope group. The call sites in other groups are dependencies on this group, not members of it.
3. **Logging infrastructure vs logging call sites.** The `OSLog` / `Logger` configuration file is infrastructure. The `os.log("did the thing")` call in a view controller is not.
4. **Pervasive coupling is an architectural smell, not a decomposition strategy.** If every scope group directly calls a `GlobalSingleton`, note the anti-pattern — the solution is to inject the dependency, not to merge all groups into one because they share the dependency.
5. **Security/auth infrastructure is always its own scope group.** Never treat auth enforcement as merely cross-cutting — the SessionManager and token lifecycle have real behavior and state and warrant their own scope group (separate from where auth checks are enforced).

