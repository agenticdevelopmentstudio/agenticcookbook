
- `must-run-security-scans-in-post-generation-verification`: security scans ran as part of post-generation verification
- `should-cover-three-scan-layers-matched-to-the-stack`: whether scanning covers SAST, dependency scanning and, for a web-facing change, DAST
- `should-run-sast-for-the-changed-language`: SAST run for the changed code's language (`semgrep scan --config=auto .`, plus Bandit for Python / CodeQL for deep analysis) with no critical findings;
- `should-run-dast-for-web-facing-changes`: DAST (OWASP ZAP) run against the local service when the change is web-facing;
- `must-run-security-scans-in-post-generation-verification`: the security layers matching the diff's language and surface were actually executed (not skipped) and any high/critical finding is resolved before completion.
- `should-treat-high-and-critical-findings-as-blocking`: whether any high or critical finding is left unresolved at completion
