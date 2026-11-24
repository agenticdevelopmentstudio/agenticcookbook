# Write brief: test-failure-triage

Today is 2026-11-24.
Artifact: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/test-failure-triage (new topic)
Research: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/testing/quality-assurance/test-failure-triage/research/research.md and research.json. Write
from these alone: not from the current text, the devteam's text or memory.
Second check: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/test-failure-triage/second-check.md (its corrections are below).
Owner list: /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/docs/grow-cookbook/areas/testing/quality-assurance/topics/test-failure-triage/owner-list.md.
cookr, this checkout's own (never an installed one): PYTHONPATH=/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/skills/cookr/cli /Users/mfullerton/.cache/grow-cookbook/cookr-venv/bin/python -P -m cookr -p /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook <command>

Review criteria. Stage 4 reviews against exactly these, and the author writes to them:

1. Every guideline in /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/recipe-quality/:
   behavioral-requirements, completeness, cookbook-compliance,
   cross-recipe-consistency, source-fidelity and template-conformance.
2. Source fidelity means fidelity to the research:
   - every rule follows from the claims it cites, at the strength it states;
   - no claim with a `supported` or `new` verdict is left without a rule;
   - every rule ends with its citation, and every cited claim exists.
3. The strength rule: each rule is at the strength of the weakest claim it
   cites. A claim the second check refuted (listed under "Second-check
   corrections, refuted" in the write brief; its `trust.basis` says "Second
   check … refuted") cannot carry MUST. A claim that only lost a citation
   whose source lacked the quote (listed under "citation dropped") is still
   supported, and its strength is unchanged.
4. A rule's citations are authoritative. A verdict's `claims` list is stage
   2's record of the old rule: nobody compares it with the rule's citations,
   and research is not edited after stage 2. A rule may cite any claim of
   research.json that some verdict names. Prior rule names (the names the
   verdicts key on) are fixed; new rules may be named and renamed freely.
5. The owner list (owner-list.md): a prior rule listed there keeps its prior
   text word for word, citing `<rule>-prior`. Only its wording is exempt from
   review, nothing else. Where the prior text has no RFC keyword, one lead-in
   in front of it carries the keyword the old text implied ("In TypeScript,
   the panel MUST be reached this way:"); owner-list.md lists the lead-in, and
   it is the one change accepted. An open question listed there is the
   owner's: the text does not settle it, and it is never a finding.
6. Frontmatter: the author updates `summary` (160 characters or fewer,
   describing the new text), `tags`, `platforms` and `related` to match the
   new guideline. `version`, `modified` and Change History are left for stage
   5's `cookr bump`: a stale version, modified date or history is never a
   finding.
7. One topic at a time: a finding about a sibling topic's guideline names the
   sibling, and the orchestrator routes it there; it is not this topic's to
   fix.

Write one roled guideline, as a single markdown doc with frontmatter, that:
- keeps every rule whose verdict is `supported`, reworded only where the
  research says it is wrong or unclear, at the strength of its weakest cited
  claim;
- adds a named rule for every `new` verdict, at the strength of its weakest
  cited claim;
- leaves every rule on the owner list below worded exactly as its prior
  text, citing its `<rule-name>-prior` claim: `(claim: <rule-name>-prior)`.
  Where the prior text has no MUST, SHOULD or MAY, put one lead-in in front of
  it carrying the keyword the old text implied, and keep the text after it
  word for word;
- settles none of the open questions on the owner list;
- follows /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/guideline-formatting/rules.md,
  gf-roled-parts and gf-named-rules: an intro; a `## Rules` section of
  named rules `- **kebab-name**: … MUST|SHOULD|MAY …`; how-to and example
  sections; `## What a reviewer looks for`;
  `## A complete review must establish`; `## A build must establish`;
  `## Rationale`; `## References`; `## Change History`;
- gives `## A build must establish` exactly one line per named rule,
  `` - `rule-name`: … ``, and no line naming anything that is not a named
  rule of `## Rules` (`cookr roles check` refuses a rule with no line and a
  line naming no rule);
- cites research exactly as `cookr validate` enforces it: every named rule
  ends with one citation, `(claim: <id>)` or `(claims: <id>, <id>)`, with
  nothing after it, not even a full stop; only one citation per rule;
  every id is a claim `id` in research.json that some verdict names
  (gf-rule-cites-research);
- updates `summary` (160 characters or fewer), `tags`, `platforms` and `related` to match the new text, and leaves `version`, `modified` and Change History to stage 5's `cookr bump`.

Edit only the draft. Never edit research, the owner list or another topic.
A finding you think is wrong is disputed, not obeyed: see the round sections
below, when there are any.

Verdicts:
- every-failure-gets-one-disposition: supported (claims: bp-sheriffs-review-every-failure, ks-treeherder-classification-set, bp-failure-classes-flaky-bug-obsolete)
- disposition-from-fixed-set: supported (claims: ks-treeherder-classification-set, bp-failure-classes-flaky-bug-obsolete, pg-firebase-inconclusive-vs-failure, ks-trunk-broken-vs-flaky, ev-google-flaky-failure-share)
- never-force-a-verdict: supported (claims: bp-rerun-same-code-separates-flake, ks-treeherder-classification-set, ks-datadog-flaky-categories, ks-meta-pfs-posterior-uncertainty, bp-explain-uncertainty-and-gaps)
- evidence-states-what-was-observed: supported (claims: bp-bug-report-observed-vs-expected, bp-failure-record-copies-log, bp-separate-information-from-judgment, ev-get-data-first)
- bug-names-observed-misbehavior: supported (claims: bp-bug-report-observed-vs-expected, bp-failure-message-desired-actual)
- flake-cites-history-or-race: supported (claims: pg-ci-flaky-same-code-history, pg-playwright-flaky-status, pg-surefire-flaky-counted, bp-rerun-same-code-separates-flake, ks-luo-flaky-root-causes, ks-datadog-flaky-categories)
- environment-cites-cross-test-signal: unsupported (claims: environment-cites-cross-test-signal-prior, pg-gradle-maxfailures-stops-retry, ks-treeherder-infra-classify-many, pg-firebase-inconclusive-vs-failure, ev-infrastructure-flakiness-share)
- spec-rot-names-new-assertion: unsupported (claims: spec-rot-names-new-assertion-prior, pg-jest-snapshot-bug-or-update, bp-tests-change-only-on-behavior-change)
- uncertain-names-missing-evidence: unsupported (claims: uncertain-names-missing-evidence-prior, bp-explain-uncertainty-and-gaps)
- high-confidence-needs-reproduction-and-mechanism: unsupported (claims: high-confidence-needs-reproduction-and-mechanism-prior, bp-explain-uncertainty-and-gaps, ev-get-data-first)
- triage-changes-nothing: contradicted (claims: triage-changes-nothing-prior, bp-triage-acts-on-verdict, bp-gardener-owns-new-failures)
- gather-failure-artifacts-before-classifying: new (claims: pg-playwright-trace-on-first-retry, pg-firebase-artifacts, pg-gitlab-failure-history-and-screenshots, pg-xcode-test-report-insights, bp-failure-record-copies-log, ks-rootfinder-compares-pass-fail-logs, pg-android-orchestrator-isolates-crashes)
- rerun-on-same-revision-before-calling-flake: new (claims: bp-rerun-same-code-separates-flake, pg-github-rerun-same-sha-debug, pg-ci-flaky-same-code-history, pg-pytest-rerun-mitigates, pg-xcode-repeat-tests)
- pass-on-retry-does-not-clear-a-bug: new (claims: ev-ignoring-flaky-hides-bugs, ev-flaky-fixes-fix-cut-bugs, ev-rerun-delays-root-cause, ev-flaky-erodes-trust, ev-reruns-may-not-manifest)
- find-the-change-that-introduced-the-failure: new (claims: ks-git-bisect-finds-culprit, bp-gardener-owns-new-failures, pg-gitlab-failure-history-and-screenshots)
- named-triage-rotation-owns-failures: new (claims: bp-sheriffs-review-every-failure, bp-gardener-owns-new-failures, ks-buildkite-notify-responsible-team)
- separate-infrastructure-outcomes-from-test-failures: new (claims: pg-firebase-inconclusive-vs-failure, ks-treeherder-infra-classify-many, pg-gradle-maxfailures-stops-retry, ev-infrastructure-flakiness-share, ev-larger-tests-flakier)
- stale-test-distinguished-by-intended-behavior-change: new (claims: bp-failure-classes-flaky-bug-obsolete, bp-tests-change-only-on-behavior-change, pg-jest-snapshot-bug-or-update, ev-regenerating-instead-of-examining)
- distinguish-broken-from-flaky-by-failure-pattern: new (claims: ks-trunk-broken-vs-flaky, ks-meta-pfs-broken-vs-flaky, pg-playwright-flaky-status)
- reproduce-in-the-failing-environment: new (claims: ev-ci-only-flakiness, ev-reruns-may-not-manifest, pg-xcode-repeat-tests, ev-get-data-first)
- verdict-states-confidence-and-its-basis: new (claims: bp-explain-uncertainty-and-gaps, bp-separate-information-from-judgment, ks-meta-pfs-posterior-uncertainty, ev-every-test-flaky-to-some-degree)
- record-flake-cause-category: new (claims: ks-luo-flaky-root-causes, ks-datadog-flaky-categories)
- known-failure-marked-expected-with-reason: new (claims: pg-pytest-xfail-strict-reason, pg-playwright-test-fail-annotation, ks-treeherder-classification-set)

Second-check corrections, refuted (criteria 3 applies to these claims):
- bp-sheriffs-review-every-failure: refuted (quote-found no, supports-claim partly); trust 72 -> 32; a rule citing it cannot carry MUST

Second-check corrections, citation dropped (the claim stands; its strength is unchanged):
none

Owner list:
For each rule below, only the rule's wording is exempt from review; everything else about it is reviewed as usual.

## Prior rules the research could not support

- **environment-cites-cross-test-signal** — verdict `unsupported` (claims: environment-cites-cross-test-signal-prior, pg-gradle-maxfailures-stops-retry, ks-treeherder-infra-classify-many, pg-firebase-inconclusive-vs-failure, ev-infrastructure-flakiness-share). Prior text, kept word for word: "An **environment** verdict cites a signal spanning unrelated sites or tests, or a probe/status observation. A single failing test never establishes it." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Gradle's test-retry plugin has a maxFailures setting that stops retrying once too many tests fail, because when everything starts failing retrying is unlikely to help.
  - against: Mozilla's sheriffing guide treats broken build infrastructure as the case where many jobs fail at once, and has sheriffs pin those jobs together and apply one classification to all of them.
  - against: Firebase Test Lab reports an inconclusive outcome, distinct from failure, for something unexpected that is likely a transient problem such as a Test Lab error, and its infrastructure errors do not trigger its flaky-test reruns.
  - against: Parry et al. report that Gruber et al. ran 22,352 Python projects' suites 200 times in original and random order, called a test infrastructure-flaky when it was flaky between iterations but not within one, and of 7,571 flaky tests found 28% infrastructure flakiness, 59% test order dependency and 13% other causes.
- **spec-rot-names-new-assertion** — verdict `unsupported` (claims: spec-rot-names-new-assertion-prior, pg-jest-snapshot-bug-or-update, bp-tests-change-only-on-behavior-change). Prior text, kept word for word: "A **spec-rot** verdict carries a non-empty `suggested_fix` naming what the spec should assert now. A suggested_fix that restates the failure, or says the spec needs updating without saying to what, is a fail." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: Jest's documentation says a failing snapshot means either the runner found a bug that should be fixed or the implementation changed and the snapshot needs updating, and that a bug must be fixed before snapshots are regenerated so the buggy behavior is not recorded.
  - against: Software Engineering at Google holds that changing a system's existing behavior is the one case in which existing tests are expected to change, and calls a test brittle when it fails on an unrelated change that introduces no real bug.
- **uncertain-names-missing-evidence** — verdict `unsupported` (claims: uncertain-names-missing-evidence-prior, bp-explain-uncertainty-and-gaps). Prior text, kept word for word: "An **uncertain** verdict names what evidence is missing and what would settle it. Bare "insufficient evidence" is a fail." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: ICD 203 has an analytic judgment state its confidence and the basis for its uncertainty, name the causes of uncertainty including knowledge gaps, and identify the indicators that would change that uncertainty.
- **high-confidence-needs-reproduction-and-mechanism** — verdict `unsupported` (claims: high-confidence-needs-reproduction-and-mechanism-prior, bp-explain-uncertainty-and-gaps, ev-get-data-first). Prior text, kept word for word: "`confidence` is 1-10. A 9 or 10 appears only where the evidence describes an actual reproduction *and* states the mechanism." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: ICD 203 has an analytic judgment state its confidence and the basis for its uncertainty, name the causes of uncertainty including knowledge gaps, and identify the indicators that would change that uncertainty.
  - against: Agans's debugging rules, as reviewed by Wheeler, say to make the failure happen again and to look at data rather than repair on a guess, and that many people try to fix things on a guess instead of gathering data to test a hypothesis.
- **triage-changes-nothing** — verdict `contradicted` (claims: triage-changes-nothing-prior, bp-triage-acts-on-verdict, bp-gardener-owns-new-failures). Prior text, kept word for word: "No finding files, closes, or comments on an issue, edits a spec, or claims to have changed anything — the disposition is the whole output." It has no RFC keyword: stage 3 keeps it word for word and may put one lead-in in front of it carrying the keyword the old text implied.
  - against: In the published triage procedures the triager acts on the verdict: Chromium's sheriffs disable a failing test and file a bug, and Azure DevOps's flaky-test workflow includes creating a bug and marking or unmarking the test as flaky as part of resolution.
  - against: Chromium assigns a gardener whose duties, in priority order, include keeping new test failures out and repairing existing ones, identifying the culprit change and reverting it.

## Open questions

- Whether triage stays a disposition-only output that files, closes, edits and reverts nothing (the team's rule triage-changes-nothing), or follows the sheriff and gardener practice in which the triager files the tracking bug, reverts the culprit or disables the test; the owner decides whether the cookbook states a general rule or leaves this to each team.
- Whether a stale-test (spec-rot) verdict must carry the assertion the test should make now, or only identify the intended behavior change that made the test stale (the change and its intent), leaving the new assertion to whoever updates the test.
- Whether the 1-10 confidence scale with 9-10 reserved for an observed reproduction and a stated mechanism is kept as the cookbook's scale, or replaced by a stated likelihood term with its basis and the gaps that limit it, as ICD 203 has it.
- Whether an environment verdict may rest on one test's cross-run or cross-machine pattern (as Gruber et al.'s infrastructure flakiness does), or only on a signal spanning unrelated tests or an infrastructure status observation as the team's rule requires.
- Whether 'an uncertain verdict names what evidence is missing and what would settle it' is kept as a must-hold check or stated at SHOULD, the strength ICD 203's standard on uncertainty carries.
- What the stale-test disposition is called in the cookbook: the team's 'spec-rot', Labuschagne et al.'s 'broken or obsolete test', or another name.
- Whether a flake disposition must also open a bug investigation of the product code, given that 24% of flaky-test fixes in Luo et al.'s sample changed the code under test, or whether that question is left to the flaky-test-quarantine lifecycle the flake is handed to.
