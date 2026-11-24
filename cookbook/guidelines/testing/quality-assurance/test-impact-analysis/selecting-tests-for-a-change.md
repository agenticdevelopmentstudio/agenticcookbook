
This section is informative: it shows one way to keep the rules, not a required method.

1. Fix the two revisions. Diff the head against a known-good base. Nx recommends the latest commit on `main` whose CI run succeeded; GitLab's `rules:changes:compare_to` names the branch to compare against where a pipeline has no natural base; Target Determinator computes the Bazel targets changed between two Git commits.
2. Fetch enough history. Turborepo needs the whole history between base and head, and treats every package as changed when the checkout is too shallow.
3. Take every changed file. bazel-diff treats its list of modified paths as a correctness contract: a truly changed file left off it has its impacted targets missed. bazel-diff hashes source files by content, and hashes every attribute and input of a target, so any change to a target's inputs marks it impacted.
4. Walk the graph from the changed set to the tests:
   - Bazel: `rdeps(universe, changed)` gives the reverse dependencies, and `tests(...)` narrows them to test rules.
   - Nx: a task is affected when the change touches one of its declared inputs; a `dependsOn` edge alone does not make a task affected, so declare inputs accurately.
   - Pants: `--changed-since` runs only the directly changed files unless `--changed-dependents` adds the targets that depend on them.
   - Turborepo: `--affected` runs only the packages affected by changes on the current branch.
   - Gradle: in a well-defined build the test task reruns only when the tests or the production code change.
   - Coverage-based tools build the map from tests to production code by recording coverage or instrumentation while each test runs. A tracer inside one language runtime misses dependencies that cross languages or processes.
5. Fall back to everything when the map runs out. Azure DevOps Test Impact Analysis runs all tests for any commit it cannot understand and for any unknown file type, such as HTML or CSS. GitHub Actions runs a path-filtered workflow whenever generating the diff times out. GitLab's `rules:changes` is true for new-branch pipelines and pipelines with no push event unless `compare_to` names a base.
6. Treat shared inputs as reaching everything that uses them. By default Nx treats a lockfile change as affecting every task, and Pants treats a change to any dependency in a lockfile as changing all users of any dependency. This guideline does not yet settle which shared inputs select everything (lockfiles, build and CI configuration, toolchains, shared fixtures); the tools differ.
7. Add the tests history marks. Azure TIA adds previously failing and newly added tests; Develocity Predictive Test Selection always chooses recently new, changed, failed or flaky tests. Neither says how far back "previously" or "recently" reaches, so the team states the window, for example the last ten runs, and records it beside the selection.
8. Record the selection. Develocity build scans list which tests were selected and which were not, with the reason; Nx's `--explain` shows why tasks are affected; Target Determinator's `-verbose` explains why each target runs; bazel-diff's log says whether each run was incremental or a fallback.
9. Keep a full run behind the subset, later in the pipeline or on a schedule: Azure TIA's configured periodic full run, Launchable's later and nightly full runs, Develocity's remaining-tests mode in nightly and pre-release stages, Mill's heuristic-free run after merge, Xcode's umbrella scheme before integrating. Two later runs are wider selections, not full runs: Google TAP batches consecutive commits into a milestone and runs every target affected since the previous milestone, and Android's TEST_MAPPING maps a separate postsubmit group of tests beside the presubmit one.
10. Check the selection before trusting it. Run the selected tests and then all tests and confirm the same failures (Azure TIA), or use Launchable's observation mode, which runs the full suite and records what the subset would have run.

A GitHub Actions workflow skipped by a `paths` filter does not report its checks, so a pull request that requires them stays blocked; a path filter also selects whole workflows by pattern with no knowledge of dependencies.

