# Integrate: principle-formatting

## For the owner

Rules standing as they were until you decide each (`cookr validate` owner-decides):

- rule 'pf-title-heading' cites 'pf-title-heading-prior', which the research rules unsupported
- rule 'pf-statement' cites 'pf-statement-prior', which the research rules unsupported
- rule 'pf-brevity' cites 'pf-brevity-prior', which the research rules unsupported
- rule 'pf-change-history' cites 'pf-change-history-prior', which the research rules unsupported
- rule 'roles-vocabulary' cites 'roles-vocabulary-prior', which the research rules unsupported
- rule 'roles-every-part-roled' cites 'roles-every-part-roled-prior', which the research rules unsupported
- rule 'roles-principle-skill-names' cites 'roles-principle-skill-names-prior', which the research rules unsupported
- rule 'roles-principle-routing' cites 'roles-principle-routing-prior', which the research rules unsupported

Open questions from the owner list:

- Which length figure the principle rule should name: the research supports no ~50-line per-principle cap; it supports a budget for everything always loaded (Claude Code's under-200-lines-per-file target) and an on-demand body bound (SKILL.md under 500 lines / under 5000 tokens). Whether principles are always loaded together (then the cap is the shared budget divided across the cookbook's principles, about 45 today) or load on demand as compiled skills (then the skill bound applies) is the owner's to decide.
- Whether pf-frontmatter-complete's field list should match conventions.md's Field Definitions table, which marks approved-by and approved-date as required (written by /approve-artifact, not linted) while the draft list omits them.
- Whether pf-title-heading keeps its exact-match MUST as an internal consistency check (tool-decidable) although no outside source requires it, or is restated as the single-title practice the sources support.
- Whether pf-statement and pf-change-history stay MUST as definitions of the artifact type (internal design) or drop to the SHOULD their outside sources support.
- How a principle's actionable bullets relate to Diataxis, which keeps instruction out of explanation: whether a principle is an explanation page with a short action list, or a separate artifact kind for which Diataxis is not the model.

Disputed findings the author left for you:

- R1.1: The fix is right but not one the draft can make. `names_hosts` is a key of `artifact.json` only, never of the doc: `read_document` sets no `names_hosts`, and `save_document`/`convert --update` copy it from the folder's current manifest (`skills/cookr/cli/cookr/core/artifact.py`, `artifact.names_hosts = current.names_hosts`), so no text in draft.md can set it, and the author may edit draft.md alone. The wording stays, as the finding says (the host figures are the evidence for `pf-always-loaded-budget` and the rules citing `claude-md-*`/`codex-*` claims, and `roles-every-part-roled` forbids `hosts/`). Route it to integration: set `"names_hosts": "Cites agent hosts' published instruction budgets and guidance as the evidence for its rules."` in the folder's `artifact.json`. With the round-2 draft folded in, `cookr validate` reports nothing else for this folder except the expected `owner-decides` rows.

Notes:

- The names_hosts dispute above is settled: integration set names_hosts in artifact.json with the reason the author proposed.

## Lossless

New topic: its text was never in the cookbook at the base commit (it came from tbd/compliance/, which owner-list.md carries word for word), so `cookr roles lossless` has no base text to check.

## Validate

`cookr validate` passed; its owner-decides rows are listed under For the owner. Bumped to 1.0.1; /add-artifact approved it (lint 24 pass, 0 fail).

integrated: 2026-11-21
