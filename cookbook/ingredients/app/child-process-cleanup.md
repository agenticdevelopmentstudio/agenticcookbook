---
id: 5546B9AD-B8B4-4973-817E-B3BC4F090618
title: "Child Process Cleanup"
domain: agenticdevelopercookbook://ingredients/app/child-process-cleanup
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Tracks child process handles and terminates them on quit with SIGHUP to the process group and a SIGKILL timeout fallback"
platforms:
  - ios
  - kotlin
  - macos
  - swift
  - web
  - windows
tags:
  - app
  - lifecycle
  - processes
depends-on: []
related:
  - agenticdevelopercookbook://ingredients/app/startup-behavior
  - agenticdevelopercookbook://recipes/app/lifecycle
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Child Process Cleanup

## Overview

Terminates every child process the app spawned (terminal sessions, background tasks, language servers, build processes) when the app quits, so no orphaned process survives it. Child process handles are tracked for the life of the app; on termination the app signals its process group, waits up to a timeout, and escalates to a forced kill for survivors.

### Terminology

| Term | Definition |
|------|-----------|
| Child process | Any process spawned by the app (terminal sessions, background tasks, language servers) that must be cleaned up on quit |
| Orphaned process | A child process that continues running after the parent app has terminated |
| Process group | A set of processes sharing a PGID, allowing bulk signal delivery |

## Behavioral Requirements

### Process cleanup

- **terminate-child-processes**: On app termination, the app MUST terminate all child processes (terminal sessions, background tasks, language servers, build processes).
- **sighup-process-group** (macOS): The app SHOULD send `SIGHUP` to its process group on `applicationWillTerminate` to ensure child processes receive a termination signal.
- **track-child-handles**: The app MUST NOT leave orphaned processes after quitting. All child process handles MUST be tracked and cleaned up.
- **cleanup-timeout-sigkill**: Child process cleanup MUST complete within a reasonable timeout (5 seconds). After the timeout, remaining processes SHOULD be sent `SIGKILL`.

## Appearance

Not applicable — process cleanup has no visual appearance.

## States

| State | Behavior |
|-------|----------|
| Quit requested, children running | Cleanup starts: SIGHUP to the process group (macOS), then each tracked handle is terminated (terminate-child-processes, sighup-process-group) |
| Children exited within timeout | Cleanup completes; the app continues terminating (track-child-handles) |
| Timeout elapsed, children remain | Remaining processes receive SIGKILL (cleanup-timeout-sigkill) |

## Accessibility

N/A — Process cleanup has no user-facing UI elements.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| lifecycle-010 | terminate-child-processes, track-child-handles | Launch app, start 3 terminal sessions, quit | All 3 child processes terminated; no orphaned processes in `ps` output |
| lifecycle-011 | sighup-process-group | (macOS) Launch app, start a child process, quit | `SIGHUP` sent to process group; child process terminated |
| lifecycle-012 | cleanup-timeout-sigkill | Launch app, start a process that ignores SIGHUP, quit | After 5-second timeout, process receives `SIGKILL` |

## Edge Cases

- **Child process ignores SIGHUP**: The app MUST escalate to `SIGKILL` after the timeout (cleanup-timeout-sigkill).

## Configuration

| Option | Type | Default | Description |
|---|---|---|---|
| `cleanupTimeoutSeconds` | integer | `5` | Time allowed for children to exit before SIGKILL |
| `signalProcessGroup` | Bool | `true` on macOS | Send SIGHUP to the whole process group on terminate |

## Logging

Subsystem: `{{bundle_id}}` | Category: `AppLifecycle`

| Event | Level | Message |
|-------|-------|---------|
| Child process cleanup started | info | `AppLifecycle: terminating {{count}} child process(es)` |
| SIGHUP sent | debug | `AppLifecycle: sent SIGHUP to process group {{pgid}}` |
| Child process terminated | debug | `AppLifecycle: child process {{pid}} ("{{name}}") terminated` |
| Child process cleanup timeout | warning | `AppLifecycle: child process {{pid}} ("{{name}}") did not terminate within {{timeout}}s, sending SIGKILL` |
| All child processes cleaned up | info | `AppLifecycle: all child processes terminated` |
| App terminating | info | `AppLifecycle: applicationWillTerminate` |

## Platform Notes

- **SwiftUI (macOS) with AppDelegate**: Implement `applicationWillTerminate(_:)` for process cleanup. For `SIGHUP` delivery, call `kill(0, SIGHUP)` to signal the entire process group, then iterate tracked child PIDs for any survivors.
- **UIKit (iOS/visionOS) with SceneDelegate**: In `applicationWillTerminate(_:)` on the `UIApplicationDelegate`, perform final cleanup. On iOS, background tasks should be cancelled via their task handles rather than POSIX signals. On visionOS, scene management follows the same pattern as iOS.
- **Android (Activity lifecycle, Compose)**: Child processes (if any) should be terminated in `onDestroy`.
- **Web (SPA with beforeunload)**: Web Workers or child processes (via `Worker` API) should be terminated with `worker.terminate()` in the `beforeunload` handler.

## Design Decisions

**Decision**: Escalate to SIGKILL after a fixed timeout rather than waiting indefinitely.
**Rationale**: A hung child must never keep the app from quitting; five seconds balances graceful exit against responsiveness.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [lifecycle-patterns](agenticdevelopercookbook://guidelines/planning/code-quality/lifecycle-patterns) | partial | Best Practices |
| [structured-logging](agenticdevelopercookbook://guidelines/implementing/observability/logging) | partial | Observability |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the App Lifecycle recipe |
