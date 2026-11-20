
An SLO is the target value for an SLI over a rolling window (commonly 28 or 30 days).

- **SLOs-are-targets-not-100**: SLOs MUST be below 100%. 100% is the wrong target — it forbids all change and is unobservable. Choose the lowest reliability users won't notice.
- **user-facing-needs-an-SLO**: Every user-facing service SHOULD have at least one SLO with an owner.
- **start-from-data**: Set the initial SLO from observed performance, then tighten deliberately. Do not promise a number you have never measured.

