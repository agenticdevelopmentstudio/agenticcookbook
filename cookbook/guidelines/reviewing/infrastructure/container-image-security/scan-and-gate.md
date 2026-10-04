
- Images **MUST** be scanned for vulnerabilities in CI before any push to a registry, using a maintained scanner (e.g. Trivy, Grype, or Snyk).
- Gate on exploitability, not raw severity. Cross-reference `agenticdevelopercookbook://guidelines/reviewing/security/vulnerability-prioritization`: builds **MUST** fail on findings in the CISA KEV catalog and **SHOULD** fail on high EPSS scores, rather than blocking on every high-CVSS CVE.
- Images **MUST NOT** ship with unaddressed known-exploited (KEV) vulnerabilities.
- Re-scan published images on a schedule (e.g. daily). New CVEs are disclosed against images that were clean at build time, so point-in-time scanning is insufficient.
- Suppressions (`.trivyignore` and equivalents) **MUST** carry a justification and an expiry/review date; permanent blanket ignores are forbidden.

