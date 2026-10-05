---
id: 03DF8FFB-476C-49F5-B104-33AD3C52BBE4
title: "SQLite Helpers"
domain: agenticdevelopercookbook://ingredients/infrastructure/sqlite-helpers
type: ingredient
version: 1.0.0
status: accepted
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Small SQLite utility layer with parameterized exec, row queries, last-insert id, temp database URLs, and a dedicated error type"
platforms:
  - ios
  - macos
  - swift
tags:
  - infrastructure
  - sqlite
  - helpers
depends-on: []
related:
  - agenticdevelopercookbook://recipes/infrastructure/package-document
  - agenticdevelopercookbook://ingredients/infrastructure/package-document-storage
references: []
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# SQLite Helpers

## Overview

The SQLite helpers are the minimal utility layer a document storage format needs to talk to SQLite safely: create a unique temporary database path, execute SQL with parameterized bindings, read single or multiple rows, retrieve the last inserted row ID, and report failures through a dedicated error type. They keep raw `sqlite3` calls out of document code and make SQL injection impossible by construction, because values only ever travel as bindings. Use them wherever code reads or writes SQLite files directly.

## Behavioral Requirements

- **temp-database-url-helper**: The codebase MUST provide a `tempDatabaseURL()` helper that returns a URL in the temporary directory with a UUID-based filename and `.db` extension.
- **exec-with-bindings**: The codebase MUST provide an `exec()` function that executes a SQL statement with parameterized bindings (supporting at minimum `.text(String)`, `.int(Int)`, and `.null` binding types).
- **query-functions**: The codebase MUST provide `queryRow()` and `queryAll()` functions for reading single and multiple rows from the database.
- **last-insert-row-id**: The codebase MUST provide a `lastInsertRowID()` function to retrieve the row ID of the last inserted row.
- **sqlite-error-type**: SQLite errors MUST be represented as a dedicated error type with cases for: `cannotOpen`, `execFailed`, `missingData`, and `invalidDate`.

## Appearance

Not applicable — SQLite helpers are infrastructure with no visual surface.

## States

| State | Behavior |
|-------|----------|
| Closed | No database handle is open |
| Open | A handle is open on a database file; `exec` and query functions may run |
| Failed | An operation threw a `SQLiteError`; the caller decides whether to surface or recover |

## Accessibility

Not applicable — SQLite helpers have no user-facing surface.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| sqlite-helpers-001 | temp-database-url-helper | Call `tempDatabaseURL()` twice | Both URLs are in the temp directory, have `.db` extension, and are unique (different UUIDs) |
| sqlite-helpers-002 | exec-with-bindings | Call `exec("INSERT INTO settings (key, value) VALUES (?, ?)", [.text("k"), .text("v")])` | Row is inserted; no SQL injection is possible with parameterized bindings |
| sqlite-helpers-003 | query-functions | Call `queryRow("SELECT value FROM settings WHERE key = ?", [.text("k")])` | Returns single row with value `"v"` |
| sqlite-helpers-004 | last-insert-row-id | Insert a row and call `lastInsertRowID()` | Returns the integer row ID of the just-inserted row |
| sqlite-helpers-005 | sqlite-error-type | Attempt to open a non-existent database path | Throws error of type `.cannotOpen` |
| sqlite-helpers-006 | sqlite-error-type | Execute invalid SQL | Throws error of type `.execFailed` |
| sqlite-helpers-007 | query-functions | Call `queryAll` on a table with three rows | Returns all three rows in order |

## Edge Cases

- **Missing data**: A query that is expected to return a row but returns none throws `.missingData` rather than a default value.
- **Invalid date string**: A date column that does not parse as ISO 8601 throws `.invalidDate` rather than substituting a fallback date.
- **Null binding**: A `.null` binding writes SQL NULL, not the string "null".
- **Handle not closed on error**: A thrown error MUST NOT leak an open database handle; the helper closes it on every exit path.

## Configuration

This ingredient has no configurable options.

## Logging

Subsystem: `{{bundle_id}}` | Category: `PackageDocument`

| Event | Level | Message |
|-------|-------|---------|
| SQLite open failed | error | `PackageDocument: cannot open database at "{{path}}": {{error}}` |
| SQL exec failed | error | `PackageDocument: exec failed: {{sql}} — {{error}}` |

## Platform Notes

- **Swift (macOS, iOS, visionOS)**: Wrap the system `sqlite3` C API; represent bindings as an enum (`.text`, `.int`, `.null`) and errors as a Swift `Error` enum.
- **SwiftUI / Compose / React/Web**: Not applicable — the helpers have no view layer. Other languages would expose the same five functions over their SQLite binding.

## Design Decisions

**Decision**: Expose only parameterized execution; no string-interpolated SQL.
**Rationale**: Making bindings the only way to pass values removes SQL injection as a class of bug and keeps call sites uniform.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [input-sanitization](agenticdevelopercookbook://compliance/security#input-sanitization) | partial | Security |
| [explicit-error-handling](agenticdevelopercookbook://compliance/best-practices#explicit-error-handling) | partial | Best Practices |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the Package Document recipe |
