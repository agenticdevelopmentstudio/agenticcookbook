---
id: 22640534-3a5b-4f8a-9f22-500a2dabc7ca
title: "Writing the Review Report"
domain: agenticdevelopercookbook://guidelines/reviewing/review-report-writing
type: guideline
version: 1.0.1
status: draft
language: en
created: 2026-06-29
modified: 2026-10-03
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Write a review report that leads with a short executive summary, gives each issue a file:line + failure + one-line fix, and prizes precision over volume."
platforms: []
tags:
  - reviewing
  - code-review
  - reporting
related:
  - agenticdevelopercookbook://guidelines/reviewing/conformance-criterion-walk
triggers: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-03"
depends-on: []
references: []
---

# Writing the Review Report

A review is only as useful as its report. The enemy is noise: a report padded with trivial or low-confidence findings buries the defects that matter.

## Executive Summary
- **report-executive-summary**: The report MUST open with a 2-4 sentence executive summary stating the overall verdict and the most important findings.

## Per-Issue Entries
- **report-issue-entry**: Each issue entry MUST name the `file:line`, the concrete failure scenario (inputs/state to wrong output), and a one-line fix.

## Precision Over Volume
- **report-precision-over-volume**: The report MUST prefer precision over volume — roughly 80% noise is the enemy; a missed real defect is worse than a dropped trivial one, so low-confidence findings are summarized, not belabored.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-29 | Mike Fullerton | Initial creation |
| 1.0.1 | 2026-10-03 | Mike Fullerton | Add the missing Change History section |
