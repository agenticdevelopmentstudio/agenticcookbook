---
id: 3182E2CF-BBFC-4933-93EC-6ACE057E0B43
title: "Reliability"
type: compliance
version: 1.0.1
status: draft
language: en
created: 2026-03-28
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Compliance checks for error recovery, graceful degradation, fault tolerance, state management, and operational reliability."
platforms: []
tags: [compliance, reliability]
depends-on: []
related:
  - tbd/compliance/access-patterns.md
  - tbd/compliance/performance.md
  - tbd/compliance/security.md
references: []
---

# Reliability

Reliability checks ensure that components recover from failures, degrade gracefully under adverse conditions, and maintain data integrity throughout their lifecycle. These checks are derived from networking, testing, and core engineering principles and apply to any recipe or guideline that handles errors, manages state, communicates over networks, or runs as a long-lived process.

## Applicability

All recipes that handle errors, manage state, communicate over networks, or run as long-lived processes. Guidelines covering error handling, state management, or resilience patterns.

## Checks

### error-recovery

Components MUST recover gracefully from transient errors without user intervention.

**Applies when:** recipe performs network calls, file I/O, or other operations subject to transient failure.

**Guidelines:**
- [adc.guideline.implementing.networking.retry-and-resilience](cookbook:cef41f52-bfc6-4ff0-bb67-eb52521c7391)

---

### graceful-degradation

Components MUST degrade gracefully when dependencies are unavailable rather than crashing.

**Applies when:** recipe depends on external services, APIs, or optional subsystems.

**Guidelines:**
- [adc.guideline.implementing.networking.offline-and-connectivity](cookbook:67c59594-a5dc-46f2-aa61-3436921294c7)

---

### fault-tolerance

Components MUST handle unexpected input and states without crashing.

**Applies when:** recipe accepts external input or operates in environments with unpredictable state.

**Guidelines:**
- [adc.principle.fail-fast](cookbook:425271ea-92b6-4df6-9a83-94795f1be377)

---

### state-recovery

Components MUST restore state correctly after process interruption or restart.

**Applies when:** recipe maintains persistent state.

**Guidelines:**
- None (derived from core engineering principles)

---

### idempotent-operations

Retried operations MUST produce the same result regardless of repetition count.

**Applies when:** recipe performs write operations that may be retried due to failure or timeout.

**Guidelines:**
- [adc.principle.idempotency](cookbook:39c2d053-006f-42c9-9db4-d991c1688024)

---

### timeout-handling

Operations that time out MUST leave the system in a consistent state.

**Applies when:** recipe performs operations with configured or implicit timeouts.

**Guidelines:**
- [adc.guideline.implementing.networking.timeouts](cookbook:c3883e6e-3bce-4bb9-a3be-61509a139288)

---

### data-integrity

Read and write operations MUST validate data integrity; corrupt data MUST be detected and reported.

**Applies when:** recipe reads or writes persistent data.

**Guidelines:**
- None (derived from core engineering principles)

---

### health-observability

Long-running components SHOULD emit health metrics suitable for monitoring.

**Applies when:** recipe runs as a long-lived process or background service.

**Guidelines:**
- [adc.guideline.implementing.observability.logging](cookbook:0f0c1da3-1c53-417b-890d-0259d7513c65)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-03-28 | Mike Fullerton | Initial creation |
