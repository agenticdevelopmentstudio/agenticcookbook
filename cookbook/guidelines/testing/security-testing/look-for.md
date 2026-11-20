
- `must-run-security-scans-in-post-generation-verification`: a post-generation verification with no security scan (SAST, dependency or DAST) in it
- `must-run-security-scans-in-post-generation-verification`: Security scans MUST be run as part of post-generation verification — they are CLI tools the agent can invoke directly, so "not run" is a failure, not an acceptable default.
- `should-cover-three-scan-layers-matched-to-the-stack`: Three layers, matched to the changed code's stack: (1) SAST — Semgrep for all languages (`semgrep scan --config=auto .`), Bandit for Python (`bandit -r src/`), CodeQL for deep analysis (Swift, Kotlin, C#, Python, TS, Go); (2) Dependency scanning — `pip-audit` (Python), `npm audit` (Node.js), `dotnet list package --vulnerable` (.NET), or Snyk (`snyk test`) for any stack; (3) DAST — OWASP ZAP against running web services (`zap-cli quick-scan http://localhost:...`) when the change is web-facing.
- `should-run-sast-for-the-changed-language`: a change with no SAST run for its language, or a SAST run that left critical findings
- `should-run-dast-for-web-facing-changes`: a web-facing change with no DAST (OWASP ZAP) run against the local service
- `must-run-security-scans-in-post-generation-verification`: confirm the layers appropriate to the diff's language and surface were actually run and came back clean;
- `should-treat-high-and-critical-findings-as-blocking`: treat high/critical SAST findings and vulnerable dependencies as blocking, and pair scanning with the implementing/security guidelines for the full reference.
