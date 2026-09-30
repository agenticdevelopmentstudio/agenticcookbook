<!-- leaf: compliance/reliability · source: compliance/reliability.md -->

**Rules** (cite as `compliance/reliability#<slug>`):

- `components-recover-gracefully-from-transient` MUST — Components MUST recover gracefully from transient errors without user intervention.
- `components-degrade-gracefully-dependencies-unavailable` MUST — Components MUST degrade gracefully when dependencies are unavailable rather than crashing.
- `components-handle-unexpected-input-states` MUST — Components MUST handle unexpected input and states without crashing.
- `components-restore-state-correctly-after` MUST — Components MUST restore state correctly after process interruption or restart.
- `retried-operations-produce-same-result-regardless` MUST — Retried operations MUST produce the same result regardless of repetition count.
- `operations-time-out-leave-system-consistent-state` MUST — Operations that time out MUST leave the system in a consistent state.
- `read-write-operations-validate-data-integrity-corrupt` MUST — Read and write operations MUST validate data integrity; corrupt data MUST be detected and reported.
- `long-running-components-emit-health-metrics-suitable` SHOULD — Long-running components SHOULD emit health metrics suitable for monitoring.

# Reliability

Reliability checks ensure that components recover from failures, degrade gracefully under adverse conditions, and maintain data integrity throughout their lifecycle. These checks are derived from networking, testing, and core engineering principles and apply to any recipe or guideline that handles errors, manages state, communicates over networks, or runs as a long-lived process.

## Applicability

All recipes that handle errors, manage state, communicate over networks, or run as long-lived processes. Guidelines covering error handling, state management, or resilience patterns.

## Checks

### error-recovery

Components MUST recover gracefully from transient errors without user intervention.

**Applies when:** recipe performs network calls, file I/O, or other operations subject to transient failure.

**Guidelines:**
- Retry and Resilience

---

### graceful-degradation

Components MUST degrade gracefully when dependencies are unavailable rather than crashing.

**Applies when:** recipe depends on external services, APIs, or optional subsystems.

**Guidelines:**
- Offline and Connectivity

---

### fault-tolerance

Components MUST handle unexpected input and states without crashing.

**Applies when:** recipe accepts external input or operates in environments with unpredictable state.

**Guidelines:**
- Fail Fast

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
- Idempotency

---

### timeout-handling

Operations that time out MUST leave the system in a consistent state.

**Applies when:** recipe performs operations with configured or implicit timeouts.

**Guidelines:**
- Timeouts

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
- Logging
