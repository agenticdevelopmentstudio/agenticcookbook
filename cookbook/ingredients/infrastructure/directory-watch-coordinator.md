---
id: 01DC6100-4AA9-4B7B-9385-E056260B57B3
title: "Directory Watch Coordinator"
domain: agenticdevelopercookbook://ingredients/infrastructure/directory-watch-coordinator
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Orchestrator that owns one directory's sync lifecycle and publishes its tree and syncing state, plus the workspace manager that pools one coordinator per directory entry"
platforms:
  - ios
  - macos
  - swift
  - typescript
tags:
  - directory-sync
  - infrastructure
  - coordinator
  - workspace
depends-on:
  - agenticdevelopercookbook://ingredients/infrastructure/directory-tree-cache
  - agenticdevelopercookbook://ingredients/infrastructure/directory-tree-scanner
  - agenticdevelopercookbook://ingredients/infrastructure/filesystem-watcher
related:
  - agenticdevelopercookbook://recipes/infrastructure/directory-sync
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Directory Watch Coordinator

## Overview

The directory watch coordinator (`DirectoryWatchCoordinator`) owns the sync lifecycle for a single directory: it publishes the in-memory tree and an `isSyncing` state, saves the cache after every change to the tree, and applies updates to the tree on the main thread. The workspace manager (`WorkspaceDirectoryManager`) pools one coordinator per workspace directory entry and aggregates their syncing state. The coordinator does not scan, cache, or watch by itself — it drives the cache, scanner, and watcher ingredients (see the Directory Sync recipe for the phase wiring).

### Terminology

| Term | Definition |
|------|-----------|
| Coordinator | The orchestrator (`DirectoryWatchCoordinator`) that owns the lifecycle for one directory |
| Workspace | A collection of directory entries, each managed by its own coordinator via `WorkspaceDirectoryManager` |
| Package | A directory that the OS treats as a single opaque file (e.g., `.app`, `.playground`, `.catnip-proj`) |

## Behavioral Requirements

### Coordinator

- **publish-before-sync**: A loaded cache MUST be published to the UI before the full sync begins, so users see an instant tree.
- **publish-syncing-state**: The coordinator MUST publish an `isSyncing` boolean state that is `true` during the full sync and `false` after it completes. The UI SHOULD use this to display a status bar indicator.
- **save-cache-after-sync**: After the full sync completes, the coordinator MUST save the updated cache to disk as a fire-and-forget operation on a background queue. A save failure MUST NOT block or crash the coordinator.
- **save-cache-after-update**: After a surgical update, the coordinator MUST save the updated cache to disk (fire-and-forget on a background queue).
- **apply-on-main-thread**: The updated children MUST be applied to the in-memory tree on the main thread.

### Workspace Variant

- **coordinator-per-entry**: `WorkspaceDirectoryManager` MUST manage a pool of coordinators, one per workspace directory entry.
- **aggregate-syncing-state**: `WorkspaceDirectoryManager` MUST aggregate the `isSyncing` state across all coordinators. The workspace-level `isSyncing` MUST be `true` if any coordinator is syncing.
- **auto-discover-packages**: `WorkspaceDirectoryManager` MUST additionally scan for `.catnip-proj` packages for auto-discovery of projects.
- **dedicated-cache-directory**: Each coordinator in the workspace MUST use a dedicated cache directory named `cache-{entryID}`.

## Appearance

Not applicable — a coordinator is infrastructure with no visual surface. It publishes `isSyncing` so a status bar can render a sync indicator.

## States

| State | Behavior |
|-------|----------|
| No cache, first launch | Coordinator loads empty state, begins full sync immediately |
| Cache available | Coordinator displays cached tree instantly, then begins full sync in background |
| Full sync in progress | `isSyncing` is `true`, UI shows sync indicator |
| Full sync complete | `isSyncing` is `false`, watch phase starts, cache saved |
| Watch active, no changes | Coordinator idle, FSEvents stream listening |
| Filesystem change detected | Surgical update runs on affected directories only |
| Surgical update in progress | Affected directory children reloaded, tree patched, cache saved |
| Watch stopped (e.g., directory deleted) | Coordinator publishes empty tree, stops FSEvents stream |

## Accessibility

Not applicable — a coordinator has no direct user-facing UI. UI presentation of the synced directory tree is handled by the file-tree-browser ingredient.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| dir-coordinator-001 | publish-syncing-state | Observe `isSyncing` during full sync | Value is `true` during the scan, `false` after completion |
| dir-coordinator-002 | save-cache-after-sync | Full sync completes | `file-tree-cache.json` exists on disk with valid JSON content |
| dir-coordinator-003 | apply-on-main-thread | Surgical update completes | Updated nodes are applied to the tree on the main thread |
| dir-coordinator-004 | save-cache-after-update | Surgical update completes | Cache file on disk reflects the new file |
| dir-coordinator-005 | coordinator-per-entry | Workspace with 3 directory entries | 3 coordinators are created, one per entry |
| dir-coordinator-006 | aggregate-syncing-state | 1 of 3 workspace coordinators is syncing | Workspace-level `isSyncing` is `true` |
| dir-coordinator-007 | aggregate-syncing-state | All 3 workspace coordinators finish syncing | Workspace-level `isSyncing` is `false` |
| dir-coordinator-008 | auto-discover-packages | Workspace directory contains a `.catnip-proj` package | Package is auto-discovered and reported |
| dir-coordinator-009 | dedicated-cache-directory | Two workspace entries with IDs "abc" and "def" | Cache directories are `cache-abc` and `cache-def` respectively |
| dir-coordinator-010 | publish-before-sync | Launch with a valid cache on disk | The cached tree is published before the full sync starts |

## Edge Cases

- **Directory deleted while watching**: The coordinator MUST handle the root directory being deleted or unmounted. It SHOULD publish an empty tree and stop the FSEvents stream.
- **Rapid filesystem changes**: If changes arrive faster than the update cycle, the coordinator SHOULD batch them rather than queueing unbounded updates.
- **Cache save in flight during update**: A surgical update that completes while a previous save is still running SHOULD coalesce or serialize the saves.
- **Workspace with zero entries**: The workspace manager holds no coordinators and its aggregate `isSyncing` is `false`.

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `entryID` | string | (required for workspaces) | Identifier used to name the coordinator's cache directory `cache-{entryID}` |

## Logging

Subsystem: `{{bundle_id}}` | Category: `DirectorySync`

| Event | Level | Message |
|-------|-------|---------|
| Workspace coordinator created | debug | `DirectorySync: workspace coordinator created for entry "{{entryID}}"` |
| Workspace syncing state changed | debug | `DirectorySync: workspace isSyncing={{value}}` |
| Project auto-discovered | info | `DirectorySync: discovered .catnip-proj at "{{path}}"` |

## Platform Notes

- **SwiftUI (macOS)**: Publish `isSyncing` via `@Published` on an `@Observable` or `ObservableObject` coordinator. Apply tree updates on the main actor.
- **SwiftUI (iOS / visionOS)**: The same publication pattern applies; the watcher and scanner ingredients document the platform differences in change monitoring.
- **Compose / React/Web**: Not applicable — this ingredient targets Apple platforms; other UI frameworks would expose the same `isSyncing` and tree state through their own observable primitives.

## Design Decisions

**Decision**: The coordinator is a thin orchestrator over separate cache, scanner, and watcher ingredients.
**Rationale**: Each of those components has its own requirements and can be reused or replaced independently; the coordinator only owns ordering, published state, and main-thread application.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [main-thread-freedom](agenticdevelopercookbook://compliance/performance#main-thread-freedom) | partial | Performance |
| [separation-of-concerns](agenticdevelopercookbook://compliance/best-practices#separation-of-concerns) | partial | Best Practices |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Directory Sync / Watch Lifecycle recipe |
