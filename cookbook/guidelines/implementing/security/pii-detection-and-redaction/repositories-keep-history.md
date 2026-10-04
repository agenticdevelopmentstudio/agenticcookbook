
- **scan-history-not-just-the-tip** — redacting the working tree does NOT purge PII or secrets
  already committed; git retains them in prior commits even after the file changes. Treat a
  public repo's history as part of the exposed surface.
- **remediate-then-rotate** — purge with `git filter-repo` (or BFG Repo-Cleaner), force-update
  the remote, and **rotate** any exposed secret — a purged credential that was public must be
  assumed compromised. `gitleaks` (fast regex/entropy, good in a pre-commit hook) and
  `trufflehog` (verifies whether a found credential is still live, good for full-history scans)
  are the standard scanners.

