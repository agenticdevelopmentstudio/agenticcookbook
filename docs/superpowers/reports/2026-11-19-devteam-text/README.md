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
  its own rule, `must-not-reimplement-standard-winui3-controls`.
- `guidelines/implementing/code-quality/dependency-injection`: the Transient-into-Singleton capture sat only as
  bullet text under `must-not-inject-scoped-into-singleton`. It is now the named rule
  `should-not-inject-transient-into-singleton`.

## For the owner: contradictions (R4), moved and left unfixed

- `guidelines/implementing/code-quality/atomic-commits`: devteam's "Judge from the diff and messages only — never
  demand evidence that a build or test run happened before the commit." against the topic's
  `must-pass-build-and-tests-before-commit`: "The build MUST pass and existing tests MUST still pass before
  committing."
- `guidelines/planning/code-quality/framework-conventions`: "Scope is the change under review — NOT a whole-codebase inventory." against
  `should-default-to-conventional-units`, which works over the whole codebase.

Tensions the batches noted (no rule directly contradicted):
- `guidelines/planning/code-quality/system-dependencies`: the same diff-only scope against a topic that groups the whole
  codebase.
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
