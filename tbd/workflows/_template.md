---
id: 25a31b86-8a76-4fac-b510-bacdedd4b885
title: "Workflow Name"
domain: agenticdevelopercookbook://workflow/_template
type: workflow
version: 1.0.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-03-27
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "version: 1.0.0"
platforms: []
tags: []
depends-on: []
related: []
references: []
---

# Workflow Name

---
version: 1.0.0
status: draft
created: YYYY-MM-DD
last-updated: YYYY-MM-DD
author: claude-code
copyright: YYYY Mike Fullerton / Temporal
audience: claude-code
scope: []
tags: []
dependencies: []
---

## Overview

Brief description of what this workflow is, when to use it, and what it produces.

## Terminology

| Term | Definition |
|------|-----------|
| | |

## Inputs

What the developer/AI needs before starting this workflow.

- **Input 1**: Description of required input
- **Input 2**: Description of required input

## Phases

### Phase 1: Name

**Entry criteria**: What must be true before starting this phase.

- **REQ-001**: Workflow MUST ...
- **REQ-002**: Workflow SHOULD ...

**Exit criteria**: What must be true before moving to the next phase.

### Phase 2: Name

**Entry criteria**: ...

- **REQ-003**: Workflow MUST ...

**Exit criteria**: ...

## Behavioral Requirements

Requirements that apply across all phases (if any). Phase-specific requirements belong in the Phases section above.

## Guideline Cross-Reference

This workflow references the shared [guideline-checklist.md](guideline-checklist.md). Phase-specific notes:

| Phase | Checklist Items | Notes |
|-------|----------------|-------|
| Phase 1 | guide.*, guide.* | Phase-specific guidance |

## Conformance Test Vectors

| ID | Requirements | Scenario | Expected |
|----|-------------|----------|----------|
| workflow-001 | REQ-001 | Scenario description | Expected outcome |

## Edge Cases

- Describe boundary conditions, error states, unexpected situations

## Tool Notes

- **git**: Guidance for git usage in this workflow
- **gh**: Guidance for GitHub CLI usage
- **Claude Code**: Guidance for Claude Code-specific behavior

## Design Decisions

Record any decisions made during authoring that affect the workflow. Each decision should be approved by the repo owner.

**Decision**: Description of choice made.
**Rationale**: Why this choice was made.
**Approved**: pending

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | YYYY-MM-DD | Initial spec |

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
