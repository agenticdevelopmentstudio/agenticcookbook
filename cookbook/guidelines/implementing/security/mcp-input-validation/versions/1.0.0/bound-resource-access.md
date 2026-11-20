
- **File paths**: canonicalize (resolve symlinks + `..`) and confine to an allowlisted root; reject paths that escape it. Treat path traversal as a primary attack on file tools.
- **URL arguments**: block SSRF — allowlist schemes/hosts, resolve and reject private, loopback, and link-local IP ranges, and disable redirects to disallowed targets.
- **Database**: use parameterized queries only; scope every query to the authorized tenant/row set — never interpolate an argument into SQL or a query path.
- **Shell/OS**: avoid shell invocation; if unavoidable, pass arguments as an argv array (never a concatenated string) and allowlist the executable.

