---
id: 9096c8f4-5f89-41cf-b06c-954861117d69
title: "SRP"
domain: agenticdevelopercookbook://principles/srp
type: principle
version: 1.0.0
status: accepted
language: en
created: 2026-04-21
modified: 2026-04-21
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "A module should be answerable to one and only one actor. Reason-to-change is a stakeholder, not a concern."
platforms: []
tags:
  - srp
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-21"
---

# SRP

A module should be answerable to one and only one actor — one stakeholder, one source of change requests. "Reason to change" is a person or role, not an abstract concern. When two actors can each independently demand a change to the same module, the module is serving two masters and its history will show conflicting edits that each broke the other actor's expectations. Where separation-of-concerns partitions by *kind of work* (UI, logic, data), SRP partitions by *who requests the change*.

- Trace each anticipated change request to a stakeholder — if two stakeholders can drive changes to the same module independently, the module carries two responsibilities and should split
- Keep code that changes together, together; separate code that changes for different reasons even if it looks similar today
- Treat unexpected merge conflicts between unrelated features as a signal that a module is absorbing responsibilities for more than one actor
- A long function or wide class is usually a sign that multiple actors share it — prefer narrow units each answerable to one actor

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-04-21 | Mike Fullerton | Initial creation |
