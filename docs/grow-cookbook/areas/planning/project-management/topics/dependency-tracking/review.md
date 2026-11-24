# Review: dependency-tracking

## Findings

none

## Checked

- `rationale.md`, first paragraph (the only text diff-3 changes): each blocker strength now has its own reason. The day count is an option "so that it matches task breakdown's `blocker-records-dates`", and keeping resolved blockers is a recommendation because Leopold and Magennis say it emphatically. Neither reason is used for the other strength any more.
- The quote "DON'T THROW THE BLOCKER POST-ITS AWAY!" is in the quote of `leopold-red-blocker-sticker-days-blocked` in research.json. That is the claim `keep-resolved-dependency-blockers` cites.
- `task-breakdown` has `blocker-records-dates` at MAY and `keep-resolved-blockers` at SHOULD in its `rules.md`. These match the rationale's description and the strengths of `count-days-dependency-blocked` (MAY) and `keep-resolved-dependency-blockers` (SHOULD).
- The rest of the changed sentence ("A blocked dependency's reason rests on the practitioners and on Jira's flag comment, so it is a recommendation") was left unchanged.
- `cookr roles check` on the folder: ok, 25 rules, no findings.

## Rulings

- R2.1: fixed — the rationale gives each strength its own reason: the MAY day count matches `task-breakdown`'s `blocker-records-dates`, and the SHOULD on keeping resolved blockers rests on Leopold and Magennis's emphatic quote and matches `keep-resolved-blockers`. "rests on the practitioners alone, so" is gone.

## Lint

lint-artifact on `cookbook/guidelines/planning/project-management/dependency-tracking`, type guideline: FM-01 to FM-13 (including FM-11a, `cookr validate` passed), gf-type-field, gf-title-heading, GF-01 to GF-03, gf-roled-parts, gf-named-rules, gf-rule-cites-research, build-bar, gf-research-folder and gf-triggers-field all PASS. There are two WARNs: the `owner-decides` notes for unsupported rules, and GF-04 (no optional `## Compliance` section). Pass 29, Warn 2, Fail 0. RESULT: CLEAN.

lint: clean

verdict: pass
