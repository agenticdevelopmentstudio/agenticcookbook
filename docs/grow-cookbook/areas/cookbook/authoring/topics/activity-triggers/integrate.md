# Integrate: activity-triggers

## For the owner

Rules standing as they were until you decide each (`cookr validate` owner-decides):

- rule 'load-by-activity-not-all' cites 'load-by-activity-not-all-prior', which the research rules unsupported
- rule 'guideline-declares-activities' cites 'guideline-declares-activities-prior', which the research rules unsupported
- rule 'principles-always-loaded' cites 'principles-always-loaded-prior', which the research rules unsupported
- rule 'trigger-filtered-on-demand' cites 'trigger-filtered-on-demand-prior', which the research rules unsupported
- rule 'escalating-checkpoint-pattern' cites 'escalating-checkpoint-pattern-prior', which the research rules unsupported
- rule 'pre-commit-checklist' cites 'pre-commit-checklist-prior', which the research rules unsupported
- rule 'check-cost-proportional-to-stakes' cites 'check-cost-proportional-to-stakes-prior', which the research rules unsupported
- rule 'trigger-index-location' cites 'trigger-index-location-prior', which the research rules unsupported
- rule 'regenerate-index-after-change' cites 'regenerate-index-after-change-prior', which the research rules unsupported
- rule 'trigger-index-not-hand-edited' cites 'trigger-index-not-hand-edited-prior', which the research rules unsupported
- rule 'order-specific-to-general' cites 'order-specific-to-general-prior', which the research rules unsupported
- rule 'triggers-guideline-only' cites 'triggers-guideline-only-prior', which the research rules unsupported
- rule 'triggers-empty-until-classified' cites 'triggers-empty-until-classified-prior', which the research rules unsupported

Open questions from the owner list:

- Whether `refactor` (17 guidelines) and `research` (10 guidelines), in use at the base commit but absent from the canonical table, are nominated and added to the table or migrated to existing values; the governance verdicts give the procedure, not the outcome.
- Whether the guide keeps any counts (240 guidelines, 10-20 per query, ~12 for writing-tests, 27 principles, ~10 pre-commit rules): no source supports them and the cookbook's own state has outgrown them, so the owner decides between generated counts, ranges measured by an evaluation, or no numbers.
- Whether the pre-commit set stays 'mandatory' when git lets every pre-commit hook be bypassed with --no-verify, or whether the mandatory gate moves to a check the agent cannot skip (a required status check on the pull request).
- Whether trigger-filtered loading gets a fallback (a description- or keyword-based search over all guidelines, as Cursor's Apply Intelligently, Claude Code skill descriptions and the tool search tool do) for tasks whose tags miss a guideline, and how far the cookbook trades precision for recall there.
- What size of labelled task set the cookbook adopts to measure trigger selection: IIR's rule of thumb is 50 information needs, skill-creator uses 20 queries split 60/40; the owner sets the number and the recall target.
- Whether the 1-5 cap stays as is: Stack Overflow caps a question at 5 tags, while at the base commit no guideline carries more than 4 triggers; the owner decides whether the cap is 5, 4 or a soft warning.

## Lossless

New topic: its text was never in the cookbook at the base commit (it came from tbd/compliance/, which owner-list.md carries word for word), so `cookr roles lossless` has no base text to check.

## Validate

`cookr validate` passed; its owner-decides rows are listed under For the owner. Bumped to 1.0.1; /add-artifact approved it (lint 24 pass, 0 fail).

integrated: 2026-11-21
