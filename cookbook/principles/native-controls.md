---
id: dec7cf4a-449b-47fa-9d6e-f7e9376383a7
title: "Prefer native controls and libraries"
domain: agenticdevelopercookbook://principles/native-controls
type: principle
version: 1.0.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Always use the platform's built-in frameworks and controls before custom implementations, note which native controls are used and why, and justify any third-party UI dependency."
platforms:
  - swift
tags:
  - native-controls
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
---

# Prefer native controls and libraries

Always use the platform's built-in frameworks before custom implementations. Swift Concurrency over raw threads. Room/SwiftData over raw SQLite. Fetch API over custom HTTP.

When generating a component, explicitly note which native controls are being used and why. If there is ambiguity about whether a native control fits, ask the user before proceeding.

- Search the platform SDK for an existing control before writing a custom one
- When a native control almost fits, customize it rather than replacing it with a from-scratch implementation
- Justify every third-party UI dependency with a concrete gap the platform SDK cannot fill

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
