# Devteam text, batch 6 report

Contradictions (R4): none found in any topic. Anything unfinished: nothing. Every `roles gaps` run ended at 0 lacking, so there is nothing under "not placed" in any topic.

Note for the orchestrator: `primary-keys`, `transactions-and-concurrency` and `constraints-and-validation` carried a `lossless.json` accounting for base `1a179b2`, not `0005775`. `roles lossless --base 0005775` refused them (for the first two: "planning/data/... is not in 0005775", the folded copy). I ran `roles lossless` against `1a179b2` for those three, where it passed; `bump` then re-based the file to `0005775`.

Process sentences below were placed verbatim under the nearest rule and are listed as reader-specific.

## recipe-quality/template-conformance
- new rules: none. Placed 1 sentence ("All frontmatter fields present and correctly typed;") under `must-include-required-frontmatter-fields`.
- reader-specific: none.

## skills-and-agents/rule-checklist
- new rules: none. Placed 2.
- reader-specific: "Read a Claude Code rule file across four lenses." (process, under `should-have-single-responsibility` in content-quality.md).

## skills-and-agents/skill-checklist
- new rules: none. Placed 4.
- reader-specific: "Read a Claude Code skill across three lenses." (process, under `must-have-yaml-frontmatter`).

## data/constraints-and-validation
- new rules: none. Placed 1.
- reader-specific: "A review passes when it establishes every item above." (under `should-use-table-level-checks-only-for-multi-column`).

## data/primary-keys
- new rules: none. Placed 1.
- reader-specific: "A review passes when it establishes every item above." (under `should-default-to-integer-primary-key`).

## data/transactions-and-concurrency
- new rules: none. Placed 1.
- reader-specific: "A review passes when it establishes every item above." (under `must-enable-wal-mode`).

## language/python
- new rules: none. Placed 2, each cited under the rules it concerns.
- reader-specific: none.

## observability/analytics
- new rules: `should-keep-abstraction-same-shape-across-platforms` ("The analytics abstraction SHOULD be the same shape across platforms: an interface/protocol plus a logging default."), from "the abstraction is the same shape across platforms (interface/protocol plus a logging default);". Keyword SHOULD (plain check). Given a build-bar line.
- Placed 7 (4 review-focus, 3 review-bar).
- reader-specific: "flag any direct coupling to an analytics backend (Mixpanel, Amplitude, PostHog and the like) in business or UI code;" (reviewer instruction).

## security/authentication
- new rules: `must-not-use-implicit-flow` ("The deprecated Implicit flow (removed in OAuth 2.1) MUST NOT appear anywhere."), from "the deprecated Implicit flow (removed in OAuth 2.1) must not appear anywhere." Keyword MUST NOT. Build-bar line and a short review-bar line ("whether any client uses the Implicit flow") added.
- Placed 2.
- reader-specific: none.

## security/sensitive-data
- new rules: none. Placed 1.
- reader-specific: none.

## testing/testing (test-adequacy and testing)
- new rules:
  - `should-test-new-risk-bearing-paths` ("A change SHOULD include a test, in the change or a named existing test, that exercises each new risk-bearing code path it introduces: retry/backoff loops, ... and boundary parsing of external input."), from "Flag NEW risk-bearing code paths this diff introduces that no test in the diff ... exercises: ...". SHOULD (a plain check).
  - `should-provoke-a-concrete-failure-mode` ("The test of a new risk-bearing path SHOULD provoke a specific failure mode that is concrete and that a test could actually assert."), from "Each finding names the specific untested path and the failure mode a test would have to provoke." and "the named failure mode is concrete and provocable (a test could actually assert it);". SHOULD.
  - Each has a build-bar line; the lead-in joined to its items as one bullet.
- Placed 10.
- reader-specific (all moved verbatim, mostly under `should-test-new-risk-bearing-paths`):
  - "Flag NEW risk-bearing code paths this diff introduces that no test in the diff (or named existing test) exercises: ..."
  - "Each finding names the specific untested path and the failure mode a test would have to provoke."
  - "if the diff adds no such path — or every risky path it adds is exercised — report zero findings;"
  - "never file blanket \"add more tests\" advice, never flag pre-existing untested code the diff merely touches, and never re-argue the design of the path itself (that belongs to the owning lane — cross-reference it instead)."
  - "The flagged path is genuinely new in this diff (not pre-existing code);"
  - "no test added or changed in the diff exercises it and the finding does not misname an existing test that does;"
  - "the finding is not disguised design criticism or generic coverage advice"
- Possible contradiction to note, not an R4 conflict: the topic's `must-test-every-change` versus "never flag pre-existing untested code the diff merely touches". Left as is.

## ui/always-show-progress
- new rules: `should-update-progress-bar-as-work-completes` ("A progress bar SHOULD update as work completes."), from "progress bar updates as work completes". SHOULD. Build-bar and look-for lines added.
- Placed 4.
- reader-specific: none.

## ui/data-display
- new rules: none. Placed 1 (cited under both `should-sort-or-filter-ten-plus-items` and `must-search-fifty-plus-items`).
- reader-specific: none.

## ui/platform-design-languages
- new rules:
  - `should-follow-wcag-and-conventions-on-web` ("A web target SHOULD follow WCAG 2.1 (AA minimum) and browser/OS design conventions."), from "Web target follows WCAG 2.1 and browser/OS design conventions;" and "WCAG 2.1 AA minimum followed;". SHOULD.
  - `should-use-system-font-stack-on-web` ("A web target SHOULD use the platform-appropriate system font stack (`system-ui, -apple-system, sans-serif`)."), from "use platform-appropriate system font stack;" and "System font stack used (...);". SHOULD.
  - `must-document-rationale-for-design-deviations` ("A custom design deviation MUST NOT be made without a documented rationale."), from "no custom design deviations without documented rationale". MUST NOT.
  - Each has a build-bar line; the deviations rule has a short look-for line.
- Placed 6.
- reader-specific: none.

## code-quality/interface-cohesion
- new rules: none. Placed 2 (under `should-place-shared-types-with-primary-consumer`).
- reader-specific: none.

## code-quality/module-boundaries
- new rules: none. Placed 3 (under `should-treat-each-declared-target-as-candidate`).
- reader-specific: none.

## code-quality/system-interactions
- new rules: none. Placed 4, all under `should-treat-each-os-integration-point-as-distinct`.
- reader-specific:
  - "In the code **this diff adds or changes**, identify OS lifecycle callbacks (...)..."
  - "Every OS lifecycle hook, IPC mechanism, background-execution path, or notification/deep-link handler the diff introduces or changes is identified and traced;"
  - "a diff that introduces none is explicitly cleared."
  - "Scope is the change under review — NOT a whole-codebase inventory."

## principles/separation-of-concerns (architecture and claude-code)
- new rules: `should-separate-workflow-steps-into-distinct-agents` ("Workflow steps SHOULD be separated into distinct agents rather than one agent doing everything."), from "workflow steps are separated into distinct agents rather than one agent doing everything". SHOULD. Build-bar and look-for lines added.
- Placed 9.
- reader-specific: none.
