---
id: da56ab62-98ad-4f52-b972-3ebfda5b1718
title: "Principle of least astonishment"
domain: agenticdevelopercookbook://principles/principle-of-least-astonishment
type: principle
version: 1.0.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "APIs, UI, and system behavior should match what users and callers expect. A name must deliver the behavior it suggests, and side effects should be obvious from the signature."
platforms: []
tags:
  - principle-of-least-astonishment
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
---

# Principle of least astonishment

APIs, UI, and system behavior should match what users and callers expect. If a name suggests one behavior, it must deliver that behavior. Side effects should be obvious from the API signature.

- Name functions and types so a reader can predict what they do without reading the implementation
- If a method mutates state, make that visible in the name or signature — never hide side effects
- Follow platform naming conventions even when you prefer a different style
- When reviewing code, ask: "Would a new team member be surprised by this behavior?"

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
