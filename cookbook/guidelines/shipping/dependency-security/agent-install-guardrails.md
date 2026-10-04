
An AI agent MUST NOT freely install packages. Constrain what it can pull:

- **Allowlist, enforced deterministically** — scope an explicit package/registry allowlist to the
  task or session and enforce it through DETERMINISTIC gates (pre-install hooks, CI checks, sandbox
  policy), NOT prompt text. Agents can ignore prompt instructions, so prose alone MUST NOT be the
  only control.
- **Registry cooldown** — apply a cooldown window (e.g. pip's dependency cooldown) so brand-new
  releases are not auto-pulled, reducing exposure to freshly compromised versions.
- **Human-in-the-loop approval** — any NEW dependency MUST require explicit human approval before it
  is added or merged.
- **Verify existence and maintenance (anti-slopsquatting)** — before adding a candidate package,
  confirm it actually exists and is actively maintained; an agent MUST NOT install a hallucinated or
  abandoned name. Cross-reference [reuse-before-build](agenticdevelopercookbook://guidelines/planning/code-quality/reuse-before-build).

References:
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)
- [SLSA Framework](https://slsa.dev/)
- [Sigstore](https://www.sigstore.dev/)

