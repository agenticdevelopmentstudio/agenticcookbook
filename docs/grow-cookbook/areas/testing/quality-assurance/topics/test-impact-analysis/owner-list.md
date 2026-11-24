# Owner list: test-impact-analysis

For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **each-selection-justified-by-diff** — verdict `unsupported` (claims: each-selection-justified-by-diff-prior, develocity-records-selection-reason, nx-explain-why-affected, target-determinator-verbose-explains, azure-tia-includes-failing-and-new, develocity-pts-always-chooses). Prior text, kept word for word: "Every included site is justified in the prose by a named path or hunk from the commit range. A site in the list with no stated reason is a fail." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Each Develocity build scan records which tests were selected and which were not, with the reason for each.
  - against: Nx can show why each task was selected as affected.
  - against: Target Determinator can explain why each target it selects is being run.
  - against: Azure TIA's selection includes, besides impacted tests, the tests that failed previously and the tests newly added.
  - against: Develocity Predictive Test Selection always selects tests that are recently new, recently changed, recently failed or recently flaky, whatever the model predicts.
- **every-changed-path-accounted-for** — verdict `unsupported` (claims: every-changed-path-accounted-for-prior, bazel-diff-changed-list-is-correctness-contract, azure-tia-unknown-file-type-runs-all). Prior text, kept word for word: "Every residue path handed to the analysis is accounted for: either attributed to sites, or named as unattributable with its candidate sites included anyway. A residue path that goes unmentioned is a fail." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: The list of changed files fed to a selection must include every file that actually changed; a changed file left off it silently drops the targets it impacts.
  - against: When Azure TIA meets a changed file of a type it cannot map, it runs all tests, which Microsoft calls good from a safety perspective.
- **fail-closed-is-stated** — verdict `unsupported` (claims: fail-closed-is-stated-prior, bazel-diff-fallback-costs-speed, develocity-records-selection-reason). Prior text, kept word for word: "Fail-closed is visible in the output: where the analysis was unsure, the prose says so and the sites are included. An answer that narrows the list on a judgment call it does not state is a fail." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: When bazel-diff cannot derive an incremental result it falls back to a full computation, trading speed but never correctness, and logs which path each run took.
  - against: Each Develocity build scan records which tests were selected and which were not, with the reason for each.
- **reasoning-cites-diff-contents** — verdict `unsupported` (claims: reasoning-cites-diff-contents-prior, bazel-diff-content-hashes, nx-selects-by-task-inputs, android-test-mapping-directory-rules, gha-paths-filter-any-match-runs). Prior text, kept word for word: "The reasoning cites the diff. A judgment resting only on commit messages, branch names, or file names without their contents is a fail." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: bazel-diff decides a source file changed from a hash of its content, not from its name or the commit metadata.
  - against: Nx selects a task as affected when the change touches one of that task's declared inputs, not by its place in the task graph.
  - against: Android's TEST_MAPPING files map a directory (optionally narrowed by file patterns) to the tests that run in presubmit when files in it change, with separate postsubmit groups.
  - against: A GitHub Actions paths filter runs the workflow when at least one changed path matches; it selects whole workflows by path pattern, with no knowledge of dependencies.

## Open questions

- How often the periodic full run happens and where: Azure TIA leaves the periodicity configurable, Launchable names post-merge and nightly, Develocity names nightly and pre-release, and Google TAP runs all affected targets per milestone (about every 45 minutes); the owner decides whether the rule names one cadence or requires the team to set and record one.
- Whether predictive (machine-learned) selection may gate a merge on its own, or only run pre-merge with a deterministic or full run behind it: Meta and Develocity accept a bounded miss rate, while the safe-selection literature does not.
- Whether each-selection-justified-by-diff, every-changed-path-accounted-for, fail-closed-is-stated and reasoning-cites-diff-contents keep their fail (MUST) strength as team checks or are restated at the SHOULD strength the sources support.
- Whether a test selected for a reason outside the diff (previously failing, newly added, recently flaky, as Azure TIA and Develocity do) counts as justified under each-selection-justified-by-diff.
- Which file classes a team may declare as unable to affect tests (Azure TIA's TIA_IncludePathFilters exclusions, GitHub paths-ignore), and who approves that list, since every exclusion narrows a fail-safe fallback.
- Which shared inputs select everything in the cookbook's general rule (lockfiles, build and CI configuration, toolchains, shared test fixtures): the tools differ, with Nx defaulting a lockfile change to every task and Pants treating a lockfile change as changing all users of any dependency.
