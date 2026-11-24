# Research brief: test-failure-triage

- **Area:** `testing/quality-assurance`
- **Topic:** `test-failure-triage` (new: no rules of its own yet; its folder holds only `research/` until stage 3)
- **Artifact:** `cookbook/guidelines/testing/quality-assurance/test-failure-triage`
- **Base commit:** `77a898dbc718928bbd96ef617723c83ec69cd549` (`base.txt`)
- **Research type:** Technology / software (intent Evaluate; domain test failure classification; method tool documentation, published industry studies and practitioner sources).
- **Research bar:** Technology / software with intent *Evaluate*, no escalation (owner approval 2026-11-24, Owner question 1). Any figure on failure-cause frequency (the share of failures that are flakes, environment faults or product bugs) takes the *Statistical* bar of `cookbook/guidelines/researching/process/research-methodology-and-sources`: name the study, its sample, its measure and its result, and score it on that bar.

## The topic

How a failed automated test is triaged before anyone fixes it: who triages it, what evidence is gathered first (trace, screenshot, log, rerun history, recent changes), which disposition the failure is classified into (a product bug, a flake, an environment fault, a test made stale by a legitimate product change, or uncertain), what separates each disposition from the others, and how the verdict states its evidence and its confidence.

The cookbook states general practice for any team that tests a product, not myagenticteams-qa-team's: the adh `e2e/` and `e2e/live/` layout, the `@smoke` tag, the LoginCard selectors and the `page.route` mocks of adh sites, the hub path for exploratory reports and charters, the JSON output contracts (fenced blocks, fingerprints, field names the team's runner parses), the team's step budgets and the site registry stay in the team and are not researched (owner ruling, 2026-11-21). No finding, claim or rule names any of them.

**Not this topic's:**

- What happens to a test once it is known to be flaky (quarantine, the retry rule, the fix-or-delete lifecycle) is `cookbook/guidelines/testing/flaky-test-quarantine`'s (`must-treat-retry-pass-as-flaky` and its lifecycle) and `cookbook/guidelines/testing/flaky-test-prevention`'s (`should-quarantine-flaky-tests-immediately`). A flake disposition hands the test to that lifecycle (owner ruling 2026-11-24, Owner question 3); this topic cites them and does not restate them.
- Production incidents and their severity tiers are `cookbook/guidelines/shipping/incident-response`'s; project issue tracking is `cookbook/guidelines/planning/project-management/issue-tracking`'s. Cited where a triaged bug becomes an issue.

## The four questions (verbatim)

1. **Best practices:** what is current best practice for this topic?
2. **Known solutions:** what solutions, patterns, libraries and tools already exist, and how do they compare?
3. **Platform guidelines:** what do the platform owners' own guidelines say, for each platform the topic touches (Apple, Android, Windows, web, the databases and runtimes concerned)?
4. **The expert's view:** if we hired an expert consultant in this topic, what would they tell us: what to do, what to avoid, and what people usually get wrong?

For this topic the platforms are the test runners and CI systems whose owners document diagnosing a failed test: Playwright (trace viewer, retries, flaky status), pytest (rerun plugins, `xfail`), JUnit/Gradle and Maven Surefire (rerun of failing tests), XCTest/Xcode test repetition (Apple), Android's test orchestration and Firebase Test Lab flaky detection, and the CI vendors' failure reports (GitHub Actions, GitLab, Azure DevOps, Buildkite, CircleCI). Name each platform the sources cover; Windows has no bearing beyond Azure DevOps unless a source says otherwise, so say so in one line.

## Research questions (from the area plan, verbatim)

1. Best practice: how should a failed automated test be triaged: who triages it, what is gathered first, and how the cause is classified before anyone fixes it?
2. Known solutions: how do the flake-detection and failure-classification systems published by Google, Meta, Microsoft and others, and the reporting features of Playwright, BuildPulse, Datadog CI Visibility and Trunk, classify a failure, and how do they compare?
3. Platform guidelines: what do the test-runner owners' guides (Playwright's trace viewer and retries, pytest's rerun and xfail markers, GitHub Actions' and other CI vendors' failure reports) say about diagnosing a failed test?
4. The expert's view: what do test engineers say teams get wrong when triaging failures (calling every failure a flake, rerunning until green, fixing the test when the product is broken), and what to do instead?
5. **Failure disposition taxonomy**: find the classes published studies and tools sort test failures into, and state the dispositions a failure is triaged into and what separates each from the others; each figure on failure-cause frequency takes the *Statistical* bar.
6. **Failure triage evidence and confidence**: find what evidence practitioners and tools gather for a verdict and how they express uncertainty, and state what a triage verdict cites and how its confidence is stated, including when the verdict is "uncertain".

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
  `source_type` `prior cookbook text`, its one citation `title` `test-failure-triage (teams/myagenticteams-qa-team/specialities/testing/failure-triage.md)`, `author`
  `Agentic Developer Cookbook`, `publisher` `agenticcookbook`, `date` `n.d.`, `url`
  `git:15f998560f57f3d0604c04af9acee6cc59d0d5a5:teams/myagenticteams-qa-team/specialities/testing/failure-triage.md` (the teams repo commit the rule is quoted at; the topic has no part files yet).
- Find what the topic is missing: practice the research finds that no rule covers. Give each a `new` verdict
  naming the kebab-case rule stage 3 will write and the strength its sources support. Each bold-named research
  question above (the plan's Missing subjects) owes at least one `new` verdict, unless a listed rule already
  covers it.
- What the research leaves to a policy choice goes in `open_questions`, one entry per question.

## The rules to verify

Each rule is quoted verbatim from `teams/myagenticteams-qa-team/specialities/testing/failure-triage.md` in the teams repo at commit `15f998560f57f3d0604c04af9acee6cc59d0d5a5` (myagenticteams-qa-team's
compiled speciality; the cookbook base commit is `77a898dbc718928bbd96ef617723c83ec69cd549`), as a claim to check, never as a source. Only the
file's general clauses are quoted; its team-specific clauses (named under *The topic*) are not this topic's
and are not quoted. The rules, one per clause, named here; the names are fixed from here on:

1. **every-failure-gets-one-disposition** (no RFC keyword; section *Verify*): "Every input cluster has exactly one disposition finding — none invented, none silently dropped."
2. **disposition-from-fixed-set** (no RFC keyword; section *Verify*): "Each `disposition` is exactly one of bug, flake, environment, spec-rot, uncertain."
3. **never-force-a-verdict** (no RFC keyword; section *Worker Focus*): "Never force a verdict."
4. **evidence-states-what-was-observed** (no RFC keyword; section *Verify*): "`evidence` states what was observed, and where. A finding that only restates the cluster's error text, or argues from what is likely, has no evidence — regardless of how plausible the verdict reads."
5. **bug-names-observed-misbehavior** (no RFC keyword; section *Verify*): "A **bug** names the observed misbehavior (status, error, wrong content) at a named URL, or states why the error cannot be a spec or environment artifact."
6. **flake-cites-history-or-race** (no RFC keyword; section *Verify*): "A **flake** cites the occurrence history (flake_count, pass-on-retry) or a race visible in the error. "Seems intermittent" is not a flake finding."
7. **environment-cites-cross-test-signal** (no RFC keyword; section *Verify*): "An **environment** verdict cites a signal spanning unrelated sites or tests, or a probe/status observation. A single failing test never establishes it."
8. **spec-rot-names-new-assertion** (no RFC keyword; section *Verify*): "A **spec-rot** verdict carries a non-empty `suggested_fix` naming what the spec should assert now. A suggested_fix that restates the failure, or says the spec needs updating without saying to what, is a fail."
9. **uncertain-names-missing-evidence** (no RFC keyword; section *Verify*): "An **uncertain** verdict names what evidence is missing and what would settle it. Bare "insufficient evidence" is a fail."
10. **high-confidence-needs-reproduction-and-mechanism** (no RFC keyword; section *Verify*): "`confidence` is 1-10. A 9 or 10 appears only where the evidence describes an actual reproduction *and* states the mechanism."
11. **triage-changes-nothing** (no RFC keyword; section *Verify*): "No finding files, closes, or comments on an issue, edits a spec, or claims to have changed anything — the disposition is the whole output."
