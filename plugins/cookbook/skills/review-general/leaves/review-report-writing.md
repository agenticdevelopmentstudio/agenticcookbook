<!-- leaf: review-general/review-report-writing · source: guidelines/reviewing/review-report-writing.md -->

**Rules** (cite as `review-general/review-report-writing#<slug>`):

- `report-executive-summary` MUST
- `report-issue-entry` MUST
- `report-precision-over-volume` MUST

# Writing the Review Report

A review is only as useful as its report. The enemy is noise: a report padded with trivial or low-confidence findings buries the defects that matter.

## Executive Summary
- **report-executive-summary**: The report MUST open with a 2-4 sentence executive summary stating the overall verdict and the most important findings.

## Per-Issue Entries
- **report-issue-entry**: Each issue entry MUST name the `file:line`, the concrete failure scenario (inputs/state to wrong output), and a one-line fix.

## Precision Over Volume
- **report-precision-over-volume**: The report MUST prefer precision over volume — roughly 80% noise is the enemy; a missed real defect is worse than a dropped trivial one, so low-confidence findings are summarized, not belabored.
