---
id: eeddf232-7bc1-4aa4-ab34-dbcbaebc102d
title: "Dashboard service is display-only"
domain: agenticdevelopercookbook://guidelines/planning/ui/dashboard-service-is-display-only
type: guideline
version: 1.0.3
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "The dashboard service is a generic API and UI layer with no knowledge of git, files, or roadmap structure. Agents sync data to it, and it only displays what it receives."
platforms: []
languages:
  - python
tags:
  - dashboard-service-is-display-only
  - language
  - python
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
triggers:
  - ui-implementation
  - new-module
---

# Dashboard service is display-only

The dashboard service is a generic API and UI layer. It MUST NOT have knowledge of git, files, or roadmap structure. Agents sync data to it; it MUST only display what it receives.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.3 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
