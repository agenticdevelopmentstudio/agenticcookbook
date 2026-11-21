# Review: activity-triggers

## Findings

- `rules.md`, **measure-trigger-selection-with-labelled-tasks** (source-fidelity: no `supported` or `new` claim is left without a rule): this round's split dropped `ev-fifty-information-needs` from the rule's citation. No rule cites it now. The claim belongs to the `new` verdict for measure-trigger-selection-with-labelled-tasks ("As a rule of thumb, 50 information needs has usually been found to be a sufficient minimum."). Only the how-to `measuring-selection.md` step 1 still uses it ("IIR's rule of thumb is a minimum of 50 information needs"), with no rule behind it. My script found no other claim of a `supported` or `new` verdict that has lost its citation. Fix: cite `ev-fifty-information-needs` again on measure-trigger-selection-with-labelled-tasks, or on a rule of its own at SHOULD at most. Give the rule of thumb as the research's reference point and leave the adopted count to the owner, as the owner list's open question on the set's size and `measuring-selection.md` both do.

## Checked

- `cookr roles check` reports ok with 58 rules and no findings, and the four skills compile.
- `cookr validate` passes with no entry for this folder. `names_hosts` is set, so the neutrality census no longer lists it as unlisted.
- Every rule ends with a citation. Every cited id is a claim of research.json and is named by some verdict. All 35 verdict rule names are still present.
- Every rule has exactly one `## A build must establish` line, and every line has a rule.
- The owner-list rules keep their prior text word for word, each with only its listed lead-in, and they cite `<rule>-prior`.
- Strength of the new and split rules against their quotes:
  - At MUST: retire-assesses-impact-and-migrates and retired-value-marked-retrieval-only rest on bp-retire-consider-impact and bp-retained-term-marked, both "must". trigger-one-meaning-one-label, trigger-single-canonical-label and trigger-values-not-redundant rest on bp-one-meaning-per-term ("must"), pg-skos-one-preflabel (normative S14) and bp-controlled-vocabulary-defined ("must have an unambiguous, non-redundant definition").
  - At SHOULD: retired-value-points-to-successor ("should be provided"); review-flags-overused-and-rare-values; review-tests-the-vocabulary.
  - At MAY: one-for-one-retag-automatically ("may be implemented"); old-value-matched-not-shown, at MAY on the refuted pg-skos-hidden-label.
- No refuted claim carries a MUST. The rules on refuted claims are all SHOULD or MAY: reject-unparseable-frontmatter, tune-recall-first, hold-out-part-of-task-set, repeat-runs-for-a-rate, old-value-matched-not-shown, rename-keeps-old-value-as-alias and trigger-scope-note-per-value.
- reject-unparseable-frontmatter states only what pg-bad-frontmatter-loads-always's quote supports ("loads the rule as if it had no `paths`"). It drops the refuted "silently".
- The rationale's sentence on unknown fields now matches pg-unknown-fields-ignored-silently and the wording of validate-trigger-values-mechanically.
- The canonical table's location, `guide/introduction/trigger-guide.md`, is named in canonical-values-only, in how-to step 1 and in both bars. The trigger-guide.md table exists, and lint's gf-triggers-field check reads it.
- The first example's order is specific to general: `schema-design`, then `database-operations`, then `performance-optimization`.
- `related` holds both UUIDs, both resolve in `cookbook/index.json`, and the rationale links both as `[<rdid>](cookbook:<uuid>)`.
- The bars and the how-to state nothing that no rule states. Each line on deletion, parse failure, the editor's review, thresholds and measurement now has a rule behind it.
- Every relative term that round 1 named is gone or anchored, either to "what every task needs" or to the review policy's recorded thresholds.
- `summary`, `tags` and `related` describe the new text, and the summary is under 160 characters.

## Rulings

- R1.1: fixed — The rule is split. retire-assesses-impact-and-migrates is a MUST for considering impact. retired-value-marked-retrieval-only is a MUST for marking a kept value and recording the dated status change. retired-value-points-to-successor is a SHOULD. trigger-change-history no longer holds a MAY on the discontinuation date, so nothing weakens that MUST.
- R1.2: fixed — add-trigger-to-guide-first now covers only nominating a candidate, at SHOULD. Being "in the table before use" is stated as a consequence inside canonical-values-only's MUST, and both bars follow.
- R1.3: fixed — Every listed compound is split into one rule per keyword-bearing behaviour. Each keeps the verdict's name on its main behaviour, and each new rule has its own citation and build-bar line. one-to-five-triggers' review clause is dropped.
- R1.4: fixed — "Small and focused", "stayed small" and "keeps growing" now read "holds only what every task needs". The outlier wording is anchored to the review policy's recorded thresholds in the rules and the how-to. "Strong case", "realistic tasks" and "extensive guideline text" are gone.
- R1.5: fixed — `guide/introduction/trigger-guide.md` is named in canonical-values-only, in how-to step 1 and in both bars, with no new citation.
- R1.6: fixed — The order is now `schema-design`, `database-operations`, `performance-optimization`, with a note explaining the order.
- R1.7: fixed — (a) reject-unparseable-frontmatter is a SHOULD with its own bar line. (b) no-delete-without-replacement is a SHOULD NOT citing bp-delete-without-replacement-loses-access and bp-retire-consider-impact. (c) The review bar's and reviewer's per-change measurement lines are cut back to what measure-trigger-selection-with-labelled-tasks, hold-out-part-of-task-set and report-recall-and-precision say.
- R1.8: fixed — The rationale now reads "an agent host ignores a frontmatter field it does not know without an error".
- R1.9: fixed — Both siblings are linked by UUID in the rationale, and 456f23bd-4523-47e8-9541-073ac046f2ad is added to `related`.
- R1.10: fixed — `names_hosts` is set, and `cookr validate` passes with no neutrality entry for this folder.

## Lint

lint-artifact v2.0.1: guideline, compliance `tbd/compliance/artifact-formatting/guideline-formatting.md`. Pass: 24, Warn: 1, Fail: 0.

- FM-01 through FM-13 pass.
- GF-01, GF-02 and GF-03 pass.
- [WARN] GF-04 / gf-compliance-section: there is no `## Compliance` section. It is optional, and recommended only when other compliance checks reference this guideline.
- gf-triggers-field, gf-roled-parts, gf-named-rules, gf-build-bar parity (58 lines for 58 rules), gf-research-folder and gf-rule-cites-research pass.

RESULT: CLEAN. The artifact passes all checks.

lint: clean

verdict: fail
