
```
RUNTIME CONDITIONS FINDINGS
============================

Permission Requirements:
  - <Permission> (<platform>) — requested in: <file list>
    Denial behavior: <what happens if denied — e.g., "feature disabled gracefully" | "hard crash" | "unclear">

Entitlements (iOS/macOS):
  - <entitlement key> — required by: <file list>

Minimum OS/Platform Version Gates:
  - <Version check> — files: <list>, guarded code: <brief description>

Environment/Configuration Prerequisites:
  - <Key or config file> — read in: <file list>, required vs optional: <required|optional>

Feature Flags:
  - <Flag name> (<system>) — guards: <file list or feature description>

Configuration Infrastructure Files:
  - <file> — purpose: <description>

Runtime Condition Anomalies:
  - <description — e.g., "Camera permission requested in 4 separate files with no centralized request handler">

Recommended Scope Group Candidates:
  - <Name> — <primary runtime condition>, <one-line rationale>
```

