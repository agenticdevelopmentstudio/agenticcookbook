
```
LIFECYCLE PATTERNS FINDINGS
============================

Object Creation Hierarchies:
  - <OwnerObject> creates: <list of owned objects>
    Created in: <init | factory | two-phase setup>
    Destroyed in: <deinit | explicit teardown | disposal>

Session/Connection Lifecycles:
  - <SessionType> — start: <trigger>, end: <trigger>, managed in: <file>
    Duration: <e.g., "per request" | "per user session" | "app lifetime">

State Machines:
  - <StateMachine> — states: <list>, file(s): <list>
    Transitions driven by: <e.g., "user action" | "network response" | "timer">

Subscription Ownership:
  - <File> owns subscriptions to: <list of publishers/observables>
    Storage mechanism: <e.g., "AnyCancellable Set", "DisposeBag">

Resource Management Patterns:
  - <Pattern> — used in: <file list>, resource managed: <description>

Lifecycle Anomalies:
  - <description — e.g., "Timer created in viewDidLoad never invalidated — potential leak">
  - <description — e.g., "Two-phase init with no clear invariants between phases">

Recommended Scope Group Candidates:
  - <Name> — <lifecycle anchor object>, <one-line rationale>
```

