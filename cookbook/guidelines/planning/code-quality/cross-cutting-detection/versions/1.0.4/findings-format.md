
```
CROSS-CUTTING DETECTION FINDINGS
==================================

Cross-Cutting Concerns (not scope groups — call sites are woven in):
  - <Concern> — call sites in <n> files across <m> candidate groups
    Infrastructure file(s): <list> — these ARE shared infrastructure (see below)

Shared Infrastructure Scope Groups (distinct from call sites):
  - <Name> — files: <list>
    Reason it is infrastructure, not cross-cutting: <one sentence>
    Consumed by: <n> other scope groups

Coupling Anomalies (pervasive anti-patterns):
  - <description — e.g., "Analytics.shared accessed in 23 files with no abstraction layer — recommend wrapping in an injected AnalyticsService">

DI / Composition Root:
  - <file(s)> — wires together: <list of scope groups>

Recommended Scope Group Candidates (infrastructure only):
  - <Name> — <one-line rationale>

Concerns to Exclude from Scope Group Map (truly cross-cutting):
  - <list of concerns that are only call sites and should not form scope groups>
```

