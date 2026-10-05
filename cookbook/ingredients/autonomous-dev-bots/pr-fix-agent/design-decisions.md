
**Decision**: Fix preference asked before PR submission, default auto-fix.
**Rationale**: Most contributors want hands-off after submission. Power users who want control can opt into review-each. The choice is per-PR, stored as PR metadata.
**Approved**: yes

**Decision**: The fix bot is a separate GitHub App from the phase bots.
**Rationale**: The fix bot writes code while the phase bots are read-only reviewers, so separating identities keeps write permission (`contents:write`) off the reviewers.
**Approved**: yes

