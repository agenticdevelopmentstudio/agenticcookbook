# Research brief: exploratory-testing-charters

- **Area:** `testing/quality-assurance`
- **Topic:** `exploratory-testing-charters` (new: no rules of its own yet; its folder holds only `research/` until stage 3)
- **Artifact:** `cookbook/guidelines/testing/quality-assurance/exploratory-testing-charters`
- **Base commit:** `77a898dbc718928bbd96ef617723c83ec69cd549` (`base.txt`)
- **Research type:** How-to / troubleshooting (intent Do; domain exploratory testing; method practitioner sources and published method guides).
- **Research bar:** How-to / troubleshooting, no escalation (owner approval 2026-11-24, Owner question 1). Any metric claim (a session length or a defect yield backed by a study) takes the *Statistical* bar of `cookbook/guidelines/researching/process/research-methodology-and-sources`.

## The topic

How exploratory testing is planned, run and reported so it finds what scripted tests miss and its results can be acted on: what a charter holds (mission, target areas, resources, the information sought, what to leave alone) and how one is written, how a session is bounded (time or step cap) and debriefed under session-based test management, and what each finding records (where it was seen, what was seen, what was expected, whether and how it repeats).

The cookbook states general practice for any team that tests a product, not myagenticteams-qa-team's: the adh `e2e/` and `e2e/live/` layout, the `@smoke` tag, the LoginCard selectors and the `page.route` mocks of adh sites, the hub path for exploratory reports and charters, the JSON output contracts (fenced blocks, fingerprints, field names the team's runner parses), the team's step budgets and the site registry stay in the team and are not researched (owner ruling, 2026-11-21). No finding, claim or rule names any of them.

**Not this topic's:**

- Scripted end-to-end specs are the sibling topic `e2e-test-authoring`'s; classifying a failed scripted test is `test-failure-triage`'s. This topic cites them where a finding becomes a spec or a triaged failure.
- Project issue tracking (what an issue records once a finding is filed) is `cookbook/guidelines/planning/project-management/issue-tracking`'s; cited, not restated.

## The four questions (verbatim)

1. **Best practices:** what is current best practice for this topic?
2. **Known solutions:** what solutions, patterns, libraries and tools already exist, and how do they compare?
3. **Platform guidelines:** what do the platform owners' own guidelines say, for each platform the topic touches (Apple, Android, Windows, web, the databases and runtimes concerned)?
4. **The expert's view:** if we hired an expert consultant in this topic, what would they tell us: what to do, what to avoid, and what people usually get wrong?

For this topic the "platforms" are the standards bodies and method owners: ISO/IEC/IEEE 29119 (its exploratory and experience-based testing parts), the ISTQB Foundation and Advanced syllabi, and the method's own authors and their sites (James Bach and Jonathan Bach on session-based test management, Michael Bolton, Elisabeth Hendrickson's *Explore It!*, Cem Kaner). Apple, Android and Windows have no bearing on this topic beyond any published guidance on exploratory testing of their apps; if none, say so in one line. Where a standard is paywalled, use its owner's own public summary or excerpt and say so in the claim's trust basis.

## Research questions (from the area plan, verbatim)

1. Best practice: how should exploratory testing be planned, run and reported so it finds what scripted tests miss and its results can be acted on?
2. Known solutions: how do session-based test management, charter templates (Elisabeth Hendrickson's "Explore ... with ... to discover ..."), test tours and heuristics such as SFDIPOT compare?
3. Platform guidelines: what do ISO/IEC/IEEE 29119 and the ISTQB syllabus say about exploratory and experience-based testing, and what do the method owners (James Bach, Jonathan Bach, Michael Bolton, Elisabeth Hendrickson) publish on charters and sessions?
4. The expert's view: what do exploratory testers say teams get wrong (exploring with no charter, no notes, reports that cannot be reproduced, treating it as ad hoc clicking), and what to do instead?
5. **Charter structure**: find the fields the method owners give a charter, and state what a charter holds and how one is written.
6. **Exploratory session time-boxing**: find how session-based test management bounds and debriefs a session, and state how a session is bounded (time or step cap) and what its debrief records.
7. **Exploratory anomaly reports**: find what the method owners and bug-report guidance require of a finding, and state the fields an exploratory finding records (where, what was seen, what was expected, whether it repeats).

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
  `source_type` `prior cookbook text`, its one citation `title` `exploratory-testing-charters (teams/myagenticteams-qa-team/specialities/testing/exploratory-charter.md)`, `author`
  `Agentic Developer Cookbook`, `publisher` `agenticcookbook`, `date` `n.d.`, `url`
  `git:15f998560f57f3d0604c04af9acee6cc59d0d5a5:teams/myagenticteams-qa-team/specialities/testing/exploratory-charter.md` (the teams repo commit the rule is quoted at; the topic has no part files yet).
- Find what the topic is missing: practice the research finds that no rule covers. Give each a `new` verdict
  naming the kebab-case rule stage 3 will write and the strength its sources support. Each bold-named research
  question above (the plan's Missing subjects) owes at least one `new` verdict, unless a listed rule already
  covers it.
- What the research leaves to a policy choice goes in `open_questions`, one entry per question.

## The rules to verify

Each rule is quoted verbatim from `teams/myagenticteams-qa-team/specialities/testing/exploratory-charter.md` in the teams repo at commit `15f998560f57f3d0604c04af9acee6cc59d0d5a5` (myagenticteams-qa-team's
compiled speciality; the cookbook base commit is `77a898dbc718928bbd96ef617723c83ec69cd549`), as a claim to check, never as a source. Only the
file's general clauses are quoted; its team-specific clauses (named under *The topic*) are not this topic's
and are not quoted. The rules, one per clause, named here; the names are fixed from here on:

1. **charter-names-scope-cap-focus-and-exclusions** (no RFC keyword; section *Worker Focus*): "it names the base URL, step cap, ranked focus areas, and "leave alone" rules for this pass"
2. **look-for-what-specs-cannot-anticipate** (no RFC keyword; section *Worker Focus*): "You are looking for anomalies specs can't anticipate: broken layouts, console errors, dead links, wrong data, jarring UX."
3. **session-has-hard-step-cap** (no RFC keyword; section *Worker Focus*): "Hard cap: 25 browser steps per pass."
4. **stay-on-charter-origin** (no RFC keyword; section *Worker Focus*): "Stay on the site's own origin."
5. **report-anomaly-where-what-expected-repeatable** (no RFC keyword; section *Worker Focus*): "Report each anomaly with: where (URL/path), what you saw, what you expected, and how repeatable it seems."
6. **no-anomalies-said-plainly** (no RFC keyword; section *Worker Focus*): "No anomalies is a fine result — say so plainly."
7. **anomaly-carries-all-four-parts** (no RFC keyword; section *Verify*): "Every reported anomaly carries all four parts: where (URL or path), what was seen, what was expected instead, and how repeatable it appeared. An anomaly missing the expectation is a fail — without it there is no claim of wrongness."
8. **finding-is-observed-not-inferred** (no RFC keyword; section *Verify*): "Each anomaly describes something observed in the browser. A finding inferred from source, from the charter's own wording, or from what a site of this kind usually does is a fail."
9. **findings-stay-inside-charter** (no RFC keyword; section *Verify*): "Findings stay inside the charter's ranked focus areas and respect its "leave alone" rules; an anomaly in an excluded area is reported as out-of-charter rather than raised as a finding."
10. **clean-pass-reports-coverage** (no RFC keyword; section *Verify*): "A pass that found nothing says so plainly and reports the areas actually covered. Padding a clean pass with severity-free observations is a fail, and so is a silent empty result."
11. **repeatability-states-retry** (no RFC keyword; section *Verify*): "Repeatability claims say what was retried. "Intermittent" without a stated second attempt is a fail."
