
- `must-run-security-scans-in-post-generation-verification`: the post-generation verification output includes the security scans' results
- `should-cover-three-scan-layers-matched-to-the-stack`: scanning covers SAST, dependency scanning and, for a web-facing change, DAST, each matched to the changed code's stack, or the code says why not
- `should-run-sast-for-the-changed-language`: SAST ran for the changed code's language with no critical findings
- `should-run-dast-for-web-facing-changes`: a web-facing change was scanned with OWASP ZAP against the local running service
- `should-run-the-scan-layers-that-match-language-and-surface`: every scan layer matching the change's language and surface was executed, not skipped, and came back clean
- `should-treat-high-and-critical-findings-as-blocking`: no high or critical SAST finding or vulnerable dependency is left open at completion
