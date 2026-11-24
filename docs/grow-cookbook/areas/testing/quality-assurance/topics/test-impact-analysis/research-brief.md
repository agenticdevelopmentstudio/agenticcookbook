# Research brief: test-impact-analysis

- **Area:** `testing/quality-assurance`
- **Topic:** `test-impact-analysis` (new: no rules of its own yet; its folder holds only `research/` until stage 3)
- **Artifact:** `cookbook/guidelines/testing/quality-assurance/test-impact-analysis`
- **Base commit:** `77a898dbc718928bbd96ef617723c83ec69cd549` (`base.txt`)
- **Research type:** Technology / software (intent Decide; domain change-based test selection; method tool documentation, published industry studies and practitioner sources).
- **Research bar:** Technology / software, no escalation (owner approval 2026-11-24, Owner question 1). Any figure on selection recall, missed failures or time saved takes the *Statistical* bar of `cookbook/guidelines/researching/process/research-methodology-and-sources`: name the study, its sample, its measure and its result, and score it on that bar.

## The topic

How a team chooses which tests (or test targets) to run for a change so the run stays fast without missing a test the change breaks: the selection methods (build-graph affected-target queries, coverage-based mapping, path filters, predictive selection), how selection fails safe when a change cannot be mapped (a change of unknown reach selects everything), which changes always select everything (build config, dependencies, shared code), the periodic full run, and what evidence a selection decision records so it can be checked.

The cookbook states general practice for any team that tests a product, not myagenticteams-qa-team's: the adh `e2e/` and `e2e/live/` layout, the `@smoke` tag, the LoginCard selectors and the `page.route` mocks of adh sites, the hub path for exploratory reports and charters, the JSON output contracts (fenced blocks, fingerprints, field names the team's runner parses), the team's step budgets and the site registry stay in the team and are not researched (owner ruling, 2026-11-21). No finding, claim or rule names any of them.

**Not this topic's:**

- Excluding quarantined tests from the gating job is `cookbook/guidelines/testing/flaky-test-quarantine`'s (`must-exclude-quarantined-tests-from-gate`): selection by tag, not by change. Cited, not restated.
- How many tests a suite holds at each level is `cookbook/guidelines/planning/testing/test-pyramid`'s; how a failed selected test is classified is the sibling topic `test-failure-triage`'s.

## The four questions (verbatim)

1. **Best practices:** what is current best practice for this topic?
2. **Known solutions:** what solutions, patterns, libraries and tools already exist, and how do they compare?
3. **Platform guidelines:** what do the platform owners' own guidelines say, for each platform the topic touches (Apple, Android, Windows, web, the databases and runtimes concerned)?
4. **The expert's view:** if we hired an expert consultant in this topic, what would they tell us: what to do, what to avoid, and what people usually get wrong?

For this topic the platforms are the build systems and CI owners that document change-based selection: Bazel (`bazel query rdeps`, target determinators), Nx and Turborepo (`affected`), Gradle (build cache, test selection plugins), Pants and Buck2, GitHub Actions path filters, GitLab `rules:changes`, Azure DevOps Test Impact Analysis (Microsoft), and the published selection systems (Meta's predictive test selection, Google's TAP, Launchable). Apple and Android have no bearing beyond what Xcode test plans and Gradle say on running a subset; say so in one line if nothing bears.

## Research questions (from the area plan, verbatim)

1. Best practice: how should a team choose which tests to run for a change so the run stays fast without missing a test the change breaks?
2. Known solutions: how do Bazel's and Nx's affected-target queries, Microsoft's Test Impact Analysis, Launchable, Meta's and Google's published predictive test selection, and coverage-based selection compare, and what does each miss?
3. Platform guidelines: what do the build and CI owners' guides (Bazel, Nx, Gradle, GitHub Actions path filters, Azure DevOps Test Impact Analysis) say about selecting tests by change and when to run everything?
4. The expert's view: what do build and test engineers say teams get wrong with test selection (trusting path filters alone, skipping tests on config or dependency changes, no periodic full run), and what to do instead?
5. **Fail-closed impact analysis**: find how selection tools behave when a change cannot be mapped to tests, and state the rule that a change of unknown reach selects every target; each figure on selection recall or saved time takes the *Statistical* bar.
6. **Impact analysis evidence**: find what selection tools record for each choice, and state what a test-selection decision cites (the changed files, the mapping that linked them to each target) so it can be checked.

## Method

- Research to `cookbook/guidelines/researching/process/research-methodology-and-sources`, using its source
  catalogue for the domain. Primary sources (specifications, standards, the tool and platform owners' own
  documentation, the published studies themselves) come before secondary ones (practitioner articles, books);
  use a secondary source only for what no primary source covers, and say so in the claim's trust basis.
- Score each claim 0–100 per `cookbook/guidelines/researching/evidence/verification-and-trust-scoring`,
  applying the principles `cite-the-claim-not-the-document`, `independence-before-corroboration`,
  `domain-stratified-trust`, `suppress-unsupported-confidence` and `provenance-at-generation-time`.
- Verify every rule listed below. Each is quoted **verbatim**, with the file it is in, as a claim to check,
  never as a source. Never restate or summarize a rule.
- `supported` means supported at the rule's stated strength. Every rule below is marked *no RFC keyword*: it
  states its obligation in plain words (a Verify clause reads as a check that must hold; a Worker Focus
  clause as what the worker attends to). Judge each at the strength its words carry, and say in research.md
  what strength (MUST, SHOULD or MAY) the sources support. Judge each as general practice: a word that
  names the team's own setting (a site, a cluster, a pass, a browser) stands for its general counterpart
  (the system under test, a group of failures, a session, the product's UI), and no claim, finding or new
  rule carries the team's word where the general one fits.
- A rule the research cannot support or finds against is recorded as its own `<rule-name>-prior` claim,
  `source_type` `prior cookbook text`, its one citation `title` `test-impact-analysis (teams/myagenticteams-qa-team/specialities/testing/commit-impact.md)`, `author`
  `Agentic Developer Cookbook`, `publisher` `agenticcookbook`, `date` `n.d.`, `url`
  `git:15f998560f57f3d0604c04af9acee6cc59d0d5a5:teams/myagenticteams-qa-team/specialities/testing/commit-impact.md` (the teams repo commit the rule is quoted at; the topic has no part files yet).
- Find what the topic is missing: practice the research finds that no rule covers. Give each a `new` verdict
  naming the kebab-case rule stage 3 will write and the strength its sources support. Each bold-named research
  question above (the plan's Missing subjects) owes at least one `new` verdict, unless a listed rule already
  covers it.
- What the research leaves to a policy choice goes in `open_questions`, one entry per question.

## The rules to verify

Each rule is quoted verbatim from `teams/myagenticteams-qa-team/specialities/testing/commit-impact.md` in the teams repo at commit `15f998560f57f3d0604c04af9acee6cc59d0d5a5` (myagenticteams-qa-team's
compiled speciality; the cookbook base commit is `77a898dbc718928bbd96ef617723c83ec69cd549`), as a claim to check, never as a source. Only the
file's general clauses are quoted; its team-specific clauses (named under *The topic*) are not this topic's
and are not quoted. The rules, one per clause, named here; the names are fixed from here on:

1. **fail-closed-when-unsure** (no RFC keyword; section *Worker Focus*): "Fail-closed: when unsure about a path, include the sites it might touch."
2. **each-selection-justified-by-diff** (no RFC keyword; section *Verify*): "Every included site is justified in the prose by a named path or hunk from the commit range. A site in the list with no stated reason is a fail."
3. **every-changed-path-accounted-for** (no RFC keyword; section *Verify*): "Every residue path handed to the analysis is accounted for: either attributed to sites, or named as unattributable with its candidate sites included anyway. A residue path that goes unmentioned is a fail."
4. **fail-closed-is-stated** (no RFC keyword; section *Verify*): "Fail-closed is visible in the output: where the analysis was unsure, the prose says so and the sites are included. An answer that narrows the list on a judgment call it does not state is a fail."
5. **reasoning-cites-diff-contents** (no RFC keyword; section *Verify*): "The reasoning cites the diff. A judgment resting only on commit messages, branch names, or file names without their contents is a fail."
