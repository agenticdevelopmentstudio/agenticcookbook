
- **must-run-security-scans-in-post-generation-verification**: Security scans MUST be run as part of post-generation verification ([adc.guideline.testing.post-generation-verification](cookbook:563aebde-52bf-4011-8907-ecc473fd942c)).
- **should-cover-three-scan-layers-matched-to-the-stack**: Security scanning SHOULD cover three layers matched to the changed code's stack: SAST, dependency scanning, and DAST when the change is web-facing.
- **should-run-sast-for-the-changed-language**: SAST SHOULD be run for the changed code's language (Semgrep `semgrep scan --config=auto .`, plus Bandit for Python and CodeQL for deep analysis), with no critical findings.
- **should-run-dast-for-web-facing-changes**: When the change is web-facing, DAST SHOULD be run with OWASP ZAP against the local running service.
- **should-run-the-scan-layers-that-match-language-and-surface**: The scan layers that match the change's language and surface SHOULD actually be run, not skipped, and come back clean.
- **should-treat-high-and-critical-findings-as-blocking**: High and critical SAST findings and vulnerable dependencies SHOULD be treated as blocking: any high or critical finding is resolved before completion.
