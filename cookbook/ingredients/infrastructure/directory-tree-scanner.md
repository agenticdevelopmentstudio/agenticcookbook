---
id: 13715EF0-3351-4477-8FA6-24541C65697A
title: "Directory Tree Scanner"
domain: agenticdevelopercookbook://ingredients/infrastructure/directory-tree-scanner
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Builds a file tree from the filesystem with parallel top-level scanning and reloads only the directories affected by a change"
platforms:
  - ios
  - macos
  - swift
  - typescript
tags:
  - directory-sync
  - infrastructure
  - scanner
depends-on: []
related:
  - agenticdevelopercookbook://recipes/infrastructure/directory-sync
  - agenticdevelopercookbook://ingredients/infrastructure/directory-watch-coordinator
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Directory Tree Scanner

## Overview

A directory tree scanner produces the in-memory file tree for a directory subtree in two modes: a full sync that rebuilds the whole tree from the filesystem, and a surgical update that reloads only the children of directories a change event touched. Full sync runs top-level directories in parallel with bounded concurrency; surgical update keeps change handling cheap by never rebuilding what did not change. Use it as the scanning engine of a directory sync coordinator.

### Terminology

| Term | Definition |
|------|-----------|
| File tree node | An in-memory representation of a single file or directory: path, name, metadata, and children |
| Full sync | A complete traversal of the directory subtree that rebuilds the in-memory tree from scratch |
| Surgical update | A targeted reload that only rescans the directories affected by a filesystem change event |
| Package | A directory that the OS treats as a single opaque file (e.g., `.app`, `.playground`, `.catnip-proj`) |

## Behavioral Requirements

### Full Sync

- **rebuild-from-filesystem**: The scanner MUST rebuild the entire file tree from the filesystem on a background queue.
- **parallel-top-level-scan**: Top-level directories MUST be scanned in parallel via an `OperationQueue`.
- **configurable-scan-workers**: Parallel scan concurrency MUST be controlled by a configurable `maxScanWorkers` property. The default value MUST be `3`. Valid range MUST be `1` to `8` inclusive. Values outside this range MUST be clamped.
- **file-tree-node-fields**: Each file tree node MUST contain the following fields:
  - `path` — absolute filesystem path (`String`)
  - `name` — display name (`String`)
  - `isDirectory` — whether the node is a directory (`Bool`)
  - `isPackage` — whether the node is a package directory (`Bool`)
  - `fileSize` — size in bytes (`Int?`, nil for directories)
  - `modificationDate` — last modification timestamp (`Date?`)
  - `children` — ordered child nodes (`[FileTreeNode]?`, nil for files)

### Surgical Update

- **surgical-reload-affected**: On receiving filesystem change events, the scanner MUST only reload the children of the affected directories — not rebuild the full tree.
- **build-path-index**: The scanner MUST build a path index from the changed file paths to identify the set of affected parent directories.
- **background-load-children**: New children for affected directories MUST be loaded on a background queue.

## Appearance

Not applicable — a scanner is infrastructure with no visual surface.

## States

| State | Behavior |
|-------|----------|
| Idle | No scan in progress |
| Full sync in progress | Top-level directories are being scanned in parallel on a background queue |
| Surgical update in progress | Children of affected directories are being reloaded on a background queue |
| Complete | A new tree or a set of replacement children has been produced for the caller to apply |

## Accessibility

Not applicable — a scanner has no user-facing surface. UI presentation of the tree is handled by the file-tree-browser ingredient.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| tree-scanner-001 | rebuild-from-filesystem, parallel-top-level-scan | Full sync on a directory with 5 top-level subdirectories | All 5 subdirectories are scanned and the tree matches the filesystem |
| tree-scanner-002 | configurable-scan-workers | Set `maxScanWorkers` to 0 | Value is clamped to 1; the scan proceeds with 1 worker |
| tree-scanner-003 | configurable-scan-workers | Set `maxScanWorkers` to 10 | Value is clamped to 8; the scan proceeds with 8 workers |
| tree-scanner-004 | file-tree-node-fields | Scan a directory containing a file (100 bytes, modified 2026-01-15) and a subdirectory | File node has correct `fileSize`, `modificationDate`, `isDirectory: false`; directory node has `isDirectory: true` and `children` populated |
| tree-scanner-005 | surgical-reload-affected, build-path-index | Create a new file in subdirectory `src/` | Only `src/` children are reloaded; sibling directories are untouched |
| tree-scanner-006 | background-load-children | Trigger a surgical update | Children are loaded on a background queue, not the main thread |

## Edge Cases

- **Large repository (100k+ files)**: Full sync SHOULD complete within a reasonable time. Parallel scanning (parallel-top-level-scan) and configurable concurrency (configurable-scan-workers) mitigate this. The UI MUST remain responsive during sync — all scanning is off the main thread.
- **Permission denied on subdirectory**: The scanner MUST skip inaccessible directories during scan and log a warning. It MUST NOT crash or abort the entire sync.
- **Symlink cycles**: The scanner MUST NOT follow symlinks recursively into cycles. It SHOULD detect symlinks and either skip or represent them as leaf nodes.
- **Package directories**: Directories identified as packages (file-tree-node-fields `isPackage`) SHOULD NOT have their children scanned by default. They are treated as opaque files.
- **Empty directory**: A directory with no children MUST be represented as a node with an empty `children` array, not `nil`.

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `maxScanWorkers` | integer | 3 | Parallel top-level scan concurrency; clamped to 1–8 |

## Logging

Subsystem: `{{bundle_id}}` | Category: `DirectorySync`

| Event | Level | Message |
|-------|-------|---------|
| Full sync started | info | `DirectorySync: full sync started for "{{rootPath}}"` |
| Full sync completed | info | `DirectorySync: full sync completed, {{nodeCount}} nodes in {{duration}}s` |
| Surgical update started | debug | `DirectorySync: surgical update for {{dirCount}} directories` |
| Surgical update completed | debug | `DirectorySync: surgical update completed in {{duration}}s` |
| Directory skipped (permission) | warning | `DirectorySync: skipped "{{path}}" — permission denied` |
| Scan worker count | debug | `DirectorySync: maxScanWorkers={{count}}` |

## Platform Notes

- **SwiftUI (macOS)**: Use `FileManager` for directory enumeration. Use `OperationQueue` with `maxConcurrentOperationCount` for parallel scanning.
- **SwiftUI (iOS / visionOS)**: Surgical updates may need to rescan entire directories because file-level change granularity is limited. Consider `NSFilePresenter` / `NSFileCoordinator` for coordinated file access.
- **Compose / React/Web**: Not applicable — this ingredient targets Apple platforms and TypeScript services using a local filesystem.

## Design Decisions

**Decision**: Parallelize only the top-level directories, with a small clamped worker count.
**Rationale**: Top-level parallelism captures most of the speedup on large trees while keeping disk contention and thread counts bounded; clamping stops a bad configuration from starving the machine.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [main-thread-freedom](agenticdevelopercookbook://compliance/performance#main-thread-freedom) | partial | Performance |
| [resource-efficiency](agenticdevelopercookbook://compliance/performance#resource-efficiency) | partial | Performance |
| [fault-tolerance](agenticdevelopercookbook://compliance/reliability#fault-tolerance) | partial | Reliability |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Directory Sync / Watch Lifecycle recipe |
