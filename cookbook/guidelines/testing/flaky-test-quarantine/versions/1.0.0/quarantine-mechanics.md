
- A quarantined test MUST be marked explicitly (e.g., a `@quarantined` tag, category, or skip-from-gate annotation) — never commented out or deleted.
- The gating suite MUST exclude quarantined tests; a separate non-gating job MUST continue running them on every build.
- Each quarantined test MUST carry: an owner, a fix deadline, and a link to the tracking issue, recorded in the annotation or a tracked registry.
- The quarantine bucket MUST be visible (a dashboard, report, or PR check summary). A quarantine no one looks at is a graveyard.

