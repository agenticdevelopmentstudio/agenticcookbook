---
id: 7E284016-0CEB-4C5E-B3D2-52D9366685CB
title: "Filesystem Watcher"
domain: agenticdevelopercookbook://ingredients/infrastructure/filesystem-watcher
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "FSEvents-based file-level change monitor with debounce and configurable path exclusions"
platforms:
  - ios
  - macos
  - swift
tags:
  - directory-sync
  - infrastructure
  - fsevents
  - watch
depends-on: []
related:
  - agenticdevelopercookbook://recipes/infrastructure/directory-sync
  - agenticdevelopercookbook://ingredients/infrastructure/directory-watch-coordinator
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Filesystem Watcher

## Overview

A filesystem watcher delivers coalesced, file-level change notifications for a directory subtree. On macOS it wraps an FSEvents stream created with file-level granularity, debounces rapid changes into a single batch, filters out paths under excluded prefixes (such as `.git` and package directories), and hands the surviving paths to the main thread. Use it to drive live updates of an in-memory tree after the initial scan has finished.

### Terminology

| Term | Definition |
|------|-----------|
| FSEvents | The macOS kernel subsystem that delivers file-level change notifications |
| Debounce latency | The coalescing window during which rapid changes are batched into one event |
| Excluded prefix | A path prefix whose changes are ignored |

## Behavioral Requirements

- **start-fsevents-watch**: After full sync completes, the watcher MUST start filesystem monitoring using FSEvents (macOS) with file-level granularity.
- **file-level-granularity**: The FSEvents stream MUST be created with `kFSEventStreamCreateFlagFileEvents` for file-level granularity.
- **debounce-latency**: The FSEvents stream MUST use a debounce latency of `0.5` seconds to coalesce rapid changes.
- **utility-qos-queue**: The FSEvents dispatch queue MUST use utility QoS.
- **exclude-path-prefixes**: The watcher MUST exclude paths matching configurable prefixes from change processing. The default excluded prefixes MUST include `.git` and package directories.
- **configurable-exclusions**: Excluded path prefixes MUST be configurable.
- **filter-excluded-paths**: The FSEvents callback MUST filter changed paths against the excluded prefixes before dispatching.
- **dispatch-to-main-thread**: Change events from the FSEvents callback MUST be dispatched to the main thread for UI updates.

## Appearance

Not applicable — a watcher is infrastructure with no visual surface.

## States

| State | Behavior |
|-------|----------|
| Stopped | No stream exists |
| Watching, no changes | Stream is active and idle |
| Debouncing | Changes were received; the watcher waits out the debounce window |
| Delivering | A coalesced, filtered batch is dispatched to the main thread |
| Stopped (root removed) | The watched directory was deleted or unmounted; the stream is stopped |

## Accessibility

Not applicable — a watcher has no user-facing surface.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| fs-watcher-001 | debounce-latency | Create 10 files within 0.3 seconds | A single coalesced change event is delivered after the 0.5s debounce |
| fs-watcher-002 | exclude-path-prefixes, filter-excluded-paths | Create a file inside `.git/` | No event is delivered for it; the batch is empty |
| fs-watcher-003 | file-level-granularity | Modify one file in a nested directory | The event names the file path, not only its parent directory |
| fs-watcher-004 | configurable-exclusions | Add a custom prefix to the exclusions and change a file under it | No event is delivered for that file |
| fs-watcher-005 | dispatch-to-main-thread | Change a watched file | The change callback runs on the main thread |
| fs-watcher-006 | start-fsevents-watch | Start the watcher after a full sync | Stream is active and subsequent changes produce events |

## Edge Cases

- **Rapid filesystem changes**: The 0.5s debounce (debounce-latency) coalesces rapid changes into a single event. If changes arrive faster than the consumer processes them, the consumer SHOULD batch them rather than queue unbounded updates.
- **Network/remote drives**: FSEvents may not work reliably on network-mounted volumes. The watcher SHOULD fall back to periodic polling or disable watch mode for non-local filesystems. Implementors SHOULD detect volume type and adapt.
- **Directory deleted while watching**: The watcher MUST handle the root directory being deleted or unmounted. It SHOULD stop the FSEvents stream and report the removal so the consumer can publish an empty tree.

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `debounceLatencySeconds` | number | 0.5 | FSEvents coalescing window |
| `excludedPathPrefixes` | string[] | `.git`, package directories | Prefixes whose changes are filtered out |

## Logging

Subsystem: `{{bundle_id}}` | Category: `DirectorySync`

| Event | Level | Message |
|-------|-------|---------|
| Watch started | info | `DirectorySync: FSEvents watch started for "{{rootPath}}"` |
| Watch stopped | info | `DirectorySync: FSEvents watch stopped` |
| Change event received | debug | `DirectorySync: {{changeCount}} changes received, {{affectedDirCount}} directories affected` |
| Excluded path filtered | debug | `DirectorySync: filtered {{count}} excluded paths` |

## Platform Notes

- **SwiftUI (macOS)**: Use `FSEventStreamCreate` with `kFSEventStreamCreateFlagFileEvents` and `kFSEventStreamCreateFlagUseCFTypes`. Schedule on a `DispatchQueue` with `.utility` QoS.
- **SwiftUI (iOS / visionOS)**: FSEvents is not available on iOS or visionOS. Use `DispatchSource.makeFileSystemObjectSource` for directory-level monitoring on individual directories, or poll on a timer. File-level granularity is limited. On visionOS, the same iOS limitations apply.
- **Compose / React/Web**: Not applicable — FSEvents is an Apple kernel facility; other platforms would substitute their native file-watching API (inotify, ReadDirectoryChangesW) behind the same requirements.

## Design Decisions

**Decision**: Debounce at 0.5 seconds.
**Rationale**: Half a second coalesces bursts such as a build writing many files, while keeping the tree responsive to single edits.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [resource-efficiency](agenticdevelopercookbook://compliance/performance#resource-efficiency) | partial | Performance |
| [graceful-degradation](agenticdevelopercookbook://compliance/reliability#graceful-degradation) | partial | Reliability |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Directory Sync / Watch Lifecycle recipe |
