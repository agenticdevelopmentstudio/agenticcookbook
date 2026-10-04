
```
DEPENDENCY CLUSTERS FINDINGS
=============================

Import Graph Summary:
  Total files analyzed: <n>
  Total import relationships: <n>
  Internal import relationships: <n> (<pct>%)
  External import relationships: <n> (<pct>%)

Identified Clusters:
  - Cluster: <name or directory path>
      Files: <count>
      Internal coupling ratio: <0.0–1.0>
      External dependencies: <list of external targets>
      Verdict: <"cohesive" | "loosely coupled" | "mixed">

High Fan-In Files (shared infrastructure candidates):
  - <file> — imported by <n> files across <m> directories

Circular Dependencies:
  - <file A> ↔ <file B> [↔ <file C>] — forces co-location

Coupling Anomalies:
  - <description — e.g., "AuthManager imports 8 files from PaymentModule, suggesting misplaced responsibility">

Recommended Scope Group Candidates:
  - <ClusterName> — internal coupling ratio <x>, <one-line rationale>
```

