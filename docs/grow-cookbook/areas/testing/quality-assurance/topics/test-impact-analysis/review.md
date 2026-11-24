# Review: test-impact-analysis

## Findings

none

## Checked

- `run-the-full-suite-periodically` now cites only claims that describe a full run (Azure TIA, Launchable, Develocity, Mill, Hammant, Apple). "Before integrating" follows from `apple-test-plans-umbrella-full-run`.
- `batch-affected-runs` (MAY) cites `tap-milestones-batch-commits` and `tap-all-affected-infeasible-per-change`. The second claim was refuted by the second check and is not carried at MUST. "Cut as often as compute allows" in the rationale matches the TAP quote.
- `map-a-separate-postsubmit-group` (MAY) follows from `android-test-mapping-directory-rules`. Both `new`-verdict claims are still cited.
- Step 9 lists only full runs. It calls TAP milestones and Android postsubmit groups wider selections, not full runs, and the reviewer focus says that neither counts as the full run.
- Rationale paragraph 4 names the four sources that keep a full run and names the selecting tools that say nothing of one. "In every source that selects" is gone.
- The rationale now gives reasons for `diff-against-a-known-good-base` (Nx, Target Determinator, Turborepo, with GitLab `compare_to` as the accepted departure) and `log-each-fallback` (`bazel-diff-fallback-costs-speed`). It gives the condition for `decide-change-by-content` (`bazel-diff-content-hashes`) and the conditions for the two new MAY rules.
- `always-select-new-changed-and-failing-tests` and `retrain-a-learned-selector` are tied to a window and a cadence that the team states and records. Step 7, the intro, the build lines and the rationale say that no source gives a number. Retraining "on changes submitted since it was last trained" is a fair reading of `meta-retrain-model` ("recently submitted code changes").
- The intro defines site, residue path, the prose, the output, an answer and the commit range. The rationale says "the four rules kept as the owner's text", not "Verify checks". The four owner rules keep their wording and the lead-in "This MUST hold:" as listed in owner-list.md.
- The example ties each changed path to named tests. The lockfile fallback names pricing:test, checkout:test, cart:test and search:test. The history window is stated, and the unselected docs:test gives a reason that matches the window.
- The new rules appear in the review-bar and build-bar parts, one build line each. The summary is still under 160 characters and still accurate.

## Rulings

- R1.1: fixed — step 9 and rationale paragraph 4 no longer call TAP milestones or Android postsubmit groups full runs, and they name the sources that keep a full run. Both claims are cited by the new MAY rules `batch-affected-runs` and `map-a-separate-postsubmit-group`.
- R1.2: fixed — the rationale gives the reason for `diff-against-a-known-good-base`, including when another base is acceptable, and for `log-each-fallback`. It also gives the condition for using `decide-change-by-content`, drawn from claims already cited.
- R1.3: fixed — "recently" and "regularly" are replaced in the rules and build lines with a window and a cadence the team states and records. The rationale and step 7 say the sources give no threshold.
- R1.4: fixed — "Verify checks" is replaced. The intro defines site, residue path and the other owner-rule terms, and the build lines gloss them, while the owner rules keep their wording.
- R1.5: fixed — the record lists the tests that the package-lock.json fallback selected, and it ties every changed path to named tests.

## Lint

lint-artifact v2.0.1: Pass 22 | Warn 1 | Fail 0. The warning is GF-04: there is no ## Compliance section, which is optional and wanted only when another check references this guideline. `cookr validate` passed. It reported four owner-decides warnings for the four owner-text MUST rules, and those warnings are not errors. RESULT: CLEAN.
lint: clean

verdict: pass
