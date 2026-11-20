# Devteam-text batch 2 report

Keywords for new rules follow the brief: "never"/"no" is MUST NOT, "every"/"all" is MUST, a plain check is SHOULD.
Placed counts are the `lacking` sentences in the batch input. Every topic's `roles gaps` reports 0 lacking, `roles check` exits 0,
`roles lossless` exits 0, `bump` and `approve.py` pass (RESULT: APPROVED).

Note: for `access-pattern-analysis`, `json-columns` and `sync-engine-design`, `roles lossless --base 0005775` exits 2 ("planning/data/<topic> is not in 0005775"; the copy folded into each survivor does not exist at that commit). I ran it with the base recorded in each topic's own `lossless.json` (`1a179b2`) instead, and it exits 0.

## cookbook/guidelines/cookbook/skills-and-agents/agent-checklist (a23bc327)
6 placed, 0 rules added. This topic has no `look-for.md`; its review-focus parts are the four table parts, so the review-focus sentences went into `structure-format.md` and `best-practices.md`.
- **reader-specific**: "Read a Claude Code agent against three lenses." (placed under `must-have-yaml-frontmatter`; a procedure line)
- **new rules / contradictions / not placed**: none.

## cookbook/guidelines/implementing/code-quality/dependency-injection (ad6816f9)
3 placed, 0 rules added.
- Note: "watch for the captive-dependency anti-pattern where a `Scoped` (or `Transient`) service is injected into a `Singleton`" sits under `must-not-inject-scoped-into-singleton`, whose rule names only scoped services; the `Transient` case is carried in the bullet only, not as a rule.
- **reader-specific / contradictions / not placed**: none.

## cookbook/guidelines/implementing/code-quality/shared-components-and-tiers (004c593c)
20 placed, 3 rules added.
- **new rules**:
  - `should-recommend-abstractr-init-when-no-tier-map` (SHOULD), from "raise exactly one low-severity finding recommending `abstractr init`, then review from principles alone." and "the `abstractr init` finding appears only for the `NO-TIER-MAP:` case ... and at most once;"
  - `must-not-recommend-abstractr-init-when-binary-unavailable` (MUST NOT), from "do NOT raise the `abstractr init` finding in this case." and "never for `ABSTRACTR-UNAVAILABLE:`"
  - `must-account-for-every-check-new-refusal` (MUST), from "every `check --new` refusal in the evidence is accounted for."
- **reader-specific**:
  - "Read the `__evidence__/abstractr` unit first; it tells you which case you are in." and "Read the `__evidence__/abstractr` unit first."
  - "If it begins `NO-TIER-MAP:` the repo has no `.abstractr.json`: raise exactly one ..." and "If it begins `ABSTRACTR-UNAVAILABLE:` ... the unit lists the declared tiers (name, paths, depends_on, shared, holds) so you can judge placement from them; do NOT raise the `abstractr init` finding in this case."
  - "Otherwise use the `map` and `check --new` output as the facts." (placed under `must-account-for-every-check-new-refusal`)
  - "... and leave the one `abstractr init` suggestion to the repo-organization lens." (names another speciality)
  - "With `ABSTRACTR-UNAVAILABLE:` judge from the tiers the unit pastes; there is no exports listing, so look for duplicates yourself by searching the shared tiers for the names and behavior the diff adds." ("the diff")
  - "Otherwise the `exports matching added names` section lists shared exports that share a name with something the diff adds."
  - "For each added function, class or component ask:" with its four questions, kept as one bullet with sub-bullets (under `should-reuse-before-building-new`)
  - "Report the added code, the existing export or the tier it belongs in, and the dependency edge if one points the wrong way." (under `should-place-in-lowest-tier`)
  - "Each finding names the file or directory and the tier or layout rule it breaks, taken from the map or from the repo's visible layout;" (under `should-keep-every-file-in-a-tier-directory`)
  - "findings cite the tier map when the evidence has one." (under `should-place-in-lowest-tier`)
- **contradictions / not placed**: none.

## cookbook/guidelines/implementing/data/access-pattern-analysis (bf15aeda)
1 placed, 0 rules added.
- **reader-specific**: "A review passes when it establishes every item above." (compiled-skill footer; placed under `must-base-schema-on-query-patterns`)

## cookbook/guidelines/implementing/data/json-columns (fc1ee814)
1 placed, 0 rules added.
- **reader-specific**: "A review passes when it establishes every item above." (placed under `should-index-json-via-generated-columns`)

## cookbook/guidelines/implementing/data/sync-engine-design (f88f3753)
1 placed, 0 rules added.
- **reader-specific**: "A review passes when it establishes every item above." (placed under `should-separate-four-layers`)

## cookbook/guidelines/implementing/internationalization/localization (3fe08fa9)
1 placed, 0 rules added. Nothing reader-specific, no contradictions, nothing unplaced.

## cookbook/guidelines/implementing/networking/caching (db8d23dc)
2 placed, 0 rules added. The review-bar fragment "Immutable assets have long-lived `Cache-Control:" was placed as the whole clause "Immutable assets have long-lived `Cache-Control: immutable`;".
- **reader-specific / contradictions / not placed**: none.

## cookbook/guidelines/implementing/security/content-security-policy (a6ef8f33)
3 placed, 0 rules added. The Trusted Types lead-in is joined to its "emit `require-trusted-types-for 'script'` and declare a named policy via `trusted-types <policy-name>`;" item.
- **reader-specific / contradictions / not placed**: none.

## cookbook/guidelines/implementing/skills-and-agents/never-clobber-user-files (a246a43c)
1 placed, 0 rules added. Nothing reader-specific, no contradictions, nothing unplaced.

## cookbook/guidelines/implementing/skills-and-agents/skill-structure-reference (fb885651)
2 placed, 2 rules added.
- **new rules**:
  - `should-follow-skills-directory-layout` (SHOULD), from "Skill directory follows `.claude/skills/<name>/SKILL.md` layout;"
  - `should-set-argument-hint-when-using-arguments` (SHOULD), from "`argument-hint` present when `$ARGUMENTS` used"
- **reader-specific / contradictions / not placed**: none.

## cookbook/guidelines/implementing/ui/spacing (c66ce722)
4 placed, 1 rule added.
- **new rules**: `should-use-spacing-tokens` (SHOULD), from "CSS custom properties or design tokens for spacing on 4px scale (4/8/12/16/24/32/48/64);" and "CSS variables used for spacing tokens;"
- **reader-specific / contradictions / not placed**: none.

## cookbook/guidelines/implementing/ui/visual-hierarchy (37755a0b)
5 placed, 0 rules added. The bar fragment "`<span>` used correctly for interactive vs." was placed as the whole clause "`<button>` vs. `<span>` used correctly for interactive vs. static;".
- **reader-specific / contradictions / not placed**: none.

## cookbook/guidelines/planning/code-quality/lifecycle-patterns (a51d3b13)
1 placed, 0 rules added. Nothing reader-specific, no contradictions, nothing unplaced.

## cookbook/guidelines/testing/security-testing (49a2a284)
8 placed, 5 rules added.
- **new rules** (all SHOULD, plain checks):
  - `should-cover-three-scan-layers-matched-to-the-stack`, from "Three layers, matched to the changed code's stack: (1) SAST ... (3) DAST ..."
  - `should-run-sast-for-the-changed-language`, from "SAST run for the changed code's language (`semgrep scan --config=auto .`, plus Bandit for Python / CodeQL for deep analysis) with no critical findings;"
  - `should-run-dast-for-web-facing-changes`, from "(3) DAST — OWASP ZAP against running web services ... when the change is web-facing." and "DAST (OWASP ZAP) run against the local service when the change is web-facing;"
  - `should-run-the-scan-layers-that-match-language-and-surface`, from "confirm the layers appropriate to the diff's language and surface were actually run and came back clean;" and "the security layers matching the diff's language and surface were actually executed (not skipped) ..."
  - `should-treat-high-and-critical-findings-as-blocking`, from "treat high/critical SAST findings and vulnerable dependencies as blocking, ..." and "any high/critical finding is resolved before completion."
- **reader-specific**:
  - "confirm the layers appropriate to the diff's language and surface were actually run and came back clean;" ("the diff")
  - "treat high/critical SAST findings and vulnerable dependencies as blocking, and pair scanning with the implementing/security guidelines for the full reference."
  - "Security scans MUST be run as part of post-generation verification — they are CLI tools the agent can invoke directly, so "not run" is a failure, not an acceptable default." (placed under the existing `must-run-security-scans-in-post-generation-verification`; no new rule)
  - "the security layers matching the diff's language and surface were actually executed (not skipped) ..." ("the diff")
- **contradictions / not placed**: none.

## cookbook/guidelines/testing/the-testing-workflow (28d89a40)
3 placed, 3 rules added.
- **new rules**:
  - `must-execute-all-workflow-steps-in-order` (MUST), from "All 7 workflow steps executed in order;"
  - `should-review-mutation-results-before-declaring-tests-complete` (SHOULD), from "mutation testing results reviewed before declaring tests complete;"
  - `should-cover-critical-user-journeys-in-e2e` (SHOULD), from "E2E verification covers critical user journeys"
- **reader-specific / contradictions / not placed**: none.

## cookbook/principles/composition-over-inheritance (9c26a7af)
2 placed, 1 rule added.
- **new rules**: `must-not-nest-inheritance-more-than-one-level` (MUST NOT), from "No inheritance hierarchies more than 1 level deep except for genuine is-a relationships;"
- "no subclassing to extend behavior where wrapping is possible" is placed under the existing `should-wrap-rather-than-subclass`.
- **reader-specific / contradictions / not placed**: none.

## Unfinished
Nothing.
