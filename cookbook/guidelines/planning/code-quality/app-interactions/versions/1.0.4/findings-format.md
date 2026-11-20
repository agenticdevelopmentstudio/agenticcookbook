
```
APP INTERACTIONS FINDINGS
==========================

Delegation Patterns:
  - <ProtocolName> — defined in: <file>, implemented by: <file list>

Notification/Event Patterns:
  - <NotificationName> — posted in: <file list>, observed in: <file list>
    Coupling scope: <"within one directory" | "crosses multiple directories">

Shared State:
  - <StateDescription> (<mechanism>) — read by: <n> files, written by: <n> files
    Scope: <"local to one group" | "cross-group — flag as cross-cutting">

Dependency Injection:
  - DI mechanism: <e.g., "Swinject container in AppDelegate", "Hilt modules">
  - Registration sites: <file list>
  - Injection points: <count and description>

Navigation/Routing:
  - Pattern: <e.g., "Coordinator", "centralized Router", "direct push from view">
  - Coordinator/Router files: <list>
  - Deep link handler: <file>

Coupling Anomalies:
  - <description — e.g., "HomeViewController directly calls PaymentService.shared — bypasses dependency injection">

Recommended Scope Group Candidates:
  - <Name> — <primary interaction pattern>, <one-line rationale>
```

