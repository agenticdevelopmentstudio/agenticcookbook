# Devteam's review text moved into its topics (ruling R7)

Ruling R7 of teamtesting's `docs/superpowers/plans/2026-11-16-finish-the-cookbook-roles.md`: "A speciality's text
that the topic lacks moves into the topic, losslessly, before the speciality is regenerated from it."

`cookr roles gaps` was run on each devteam speciality's own `Review focus` and `A complete review must establish`
text (agenticdevteam 7e3b0a2) against the roled topic it stands on. It found 498 lacking sentences in 142 topics. The
nine batch reports here (`batch-0.md` … `batch-8.md`) record the work one topic at a time. Every topic:
- took each lacking sentence verbatim, as a bullet in its `review-focus` or `review-bar` part, naming the rule it
  concerns;
- gained a named rule for each requirement it lacked, with that rule's line in the build bar and in whichever
  review part did not already carry devteam's sentence;
- passed `roles check`, `roles lossless` (against the base its own `lossless.json` records), `bump` and the scripted
  `/approve-artifact`, and was committed on its own.

After the batches, `gaps` re-run across every speciality reads 0 lacking for every roled topic. The only topics still
listed are the 10 under `guidelines/reviewing/`. They stay unroled by rule, and `cookbook_skills.py` keeps devteam's
own text for them.

Two follow-up fixes, after the batches:
- `principles/native-controls`: "No custom reimplementations of standard WinUI 3 controls" had been held under the
  SHOULD rule `should-prefer-winui3-controls-over-custom-drawn`. R7's mapping makes "no" wording MUST NOT, so it is now
  its own rule, `must-not-reimplement-standard-winui3-controls`. Review finding f5 then dropped the SHOULD rule, since
  it stated the same requirement at a second strength; devteam's "WinUI 3 controls over custom-drawn equivalents"
  now sits under the MUST NOT rule.
- `guidelines/implementing/code-quality/dependency-injection`: the Transient-into-Singleton capture sat only as
  bullet text under `must-not-inject-scoped-into-singleton`. It is now the named rule
  `should-not-inject-transient-into-singleton`.

## For the owner: contradictions (R4), moved and left unfixed

After review finding f6, a devteam sentence that contradicts a rule no longer sits under that rule, or under any
rule: it is an untagged closing paragraph of the topic's review bar, so it still reaches the review verifier but tags
no rule it would cancel. That holds for atomic-commits and for the four planning topics' scope sentence.

- `guidelines/implementing/code-quality/atomic-commits`: devteam's "Judge from the diff and messages only — never
  demand evidence that a build or test run happened before the commit." against the topic's
  `must-pass-build-and-tests-before-commit`: "The build MUST pass and existing tests MUST still pass before
  committing."
- `guidelines/planning/code-quality/framework-conventions`: "Scope is the change under review — NOT a whole-codebase inventory." against
  `should-default-to-conventional-units`, which works over the whole codebase.
- `guidelines/planning/code-quality/algorithmic-complexity`, `runtime-conditions` and `system-dependencies`: the same
  sentence, "Scope is the change under review — NOT a whole-codebase inventory.", against topics whose rules group the
  whole codebase into scope groups. The batches had made it a MUST rule in each; review finding f2 showed that rule
  contradicts the topic, so it is no rule now. Devteam's sentence stays in each review bar, for the owner to rule on.
- `principles/yagni`: devteam's "No unused abstraction layers, extension points, or generalization not required by
  current features" against `principles/meta-principle-optimize-for-change`'s
  `should-provide-extension-points-where-change-is-anticipated`: "Key extension points (swappable backends, injectable
  services) SHOULD be present where change is anticipated." The batches had made devteam's sentence a MUST NOT rule;
  review finding f3 showed it contradicts optimize-for-change and restates yagni's own SHOULD rule
  `should-confirm-requirement-before-adding-extension-points` at a stronger strength, so it is no rule now. Devteam's
  sentences stay in yagni's review parts.
- `principles/immutability-by-default`: devteam's "no shared mutable state across concurrent contexts" against the
  topic's own `should-contain-mutation-behind-boundaries` (actors, StateFlow) and the concurrency topics, which allow
  shared mutable state behind a lock or an actor. The batches had made it the rule "There MUST be no shared mutable
  state…"; review finding f4 showed the contradiction, so the rule now reads "Mutable state shared across concurrent
  contexts MUST NOT be accessed without synchronization or an owning actor." Devteam's sentence stays in the review
  bar, for the owner to rule on.

Duplicate strengths removed after review finding f5, each requirement now at one strength:
- `guidelines/testing/the-testing-workflow`: "All 7 workflow steps MUST be executed in order" made the SHOULD steps
  (mutation testing, E2E) mandatory. The rule is now `must-execute-workflow-steps-in-order`: the steps that run go in
  order, and a skipped SHOULD step is stated with its reason. Devteam's "All 7 workflow steps executed in order;"
  stays in the review bar.
- `guidelines/testing/security-testing`: the SHOULD rule `should-run-the-scan-layers-that-match-language-and-surface`
  restated the existing MUST rule `must-run-security-scans-in-post-generation-verification`. It is gone, and devteam's
  sentences sit under the MUST rule.

Tensions the batches noted (no rule directly contradicted):
- `guidelines/implementing/ui/layout`: devteam's "breakpoints use `em`/`rem` or device-class media queries;"
  against the topic's `should-design-for-content-not-screen-size`. After review finding f8 the rule is
  `should-use-relative-unit-breakpoints-on-the-web` (`em`/`rem`, set where the content needs them), and its two
  web-only neighbours say "On the web". Devteam's sentence stays in the review bar.
- `guidelines/implementing/ui/typography`: devteam allows a custom font with justification; the topic says "The platform's system font MUST
  be used".
- `guidelines/implementing/networking/offline-and-connectivity`: devteam's "circuit breaker present or explicitly scoped out" against the
  SHOULD rule `should-use-a-circuit-breaker`.
- `guidelines/cookbook/recipe-quality/template-conformance`: "never flag pre-existing untested code the diff merely touches" against
  `must-test-every-change`.

## For the owner: reader-specific text

Text that names devteam's own machinery (the diff, a lane, `read_base_file`, "your summary", another speciality)
moved verbatim like everything else. Each batch report lists it, quoted, under **reader-specific**. One process
sentence recurs: "A review passes when it establishes every item above." It sits under the last rule of each topic
that had it.
