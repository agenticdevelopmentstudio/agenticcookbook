# Devteam text batch 7 report

Every topic lists what was added. "Not placed" is empty for every topic: `cookr roles gaps` reported 0 lacking for every file of every topic.

Note on `roles lossless`: for `data/query-optimization` and `feature-management/ab-testing` (each has a folded copy that is not in `0005775`), `--base 0005775` is refused ("... is not in 0005775"). Both were checked against the base recorded in their own `lossless.json` instead (`1a179b2`, `2071c94e`). For `query-optimization` the added line made the one obsolete entry's pinned verdict stale (the pin covers the whole topic text), so an independent judge re-judged that entry and wrote the new pin.

## accessibility
- new rules: none.
- reader-specific: none.
- contradictions: none.
- not placed: none.

## dynamic-type
- new rules: none. reader-specific: none. contradictions: none. not placed: none.

## shell-scripts
- new rules: none. reader-specific: none. contradictions: none. not placed: none.

## data-types
- new rules: none.
- reader-specific (process): "A review passes when it establishes every item above." placed under `must-validate-json-on-both-sides` (the last rule); it belongs to no rule.
- contradictions: none. not placed: none.

## query-optimization
- new rules: none.
- reader-specific (process): "A review passes when it establishes every item above." placed under `should-index-both-sides-of-or`.
- contradictions: none. not placed: none.
- lossless: see the note above (stale obsolete pin re-judged).

## ab-testing
- new rules: none.
- reader-specific (process): "A review passes when it establishes every item above." placed under `store-page-tests-use-store-tools`.
- contradictions: none. not placed: none.

## swift
- new rules: none. reader-specific: none. contradictions: none. not placed: none.
- "structs, enums and protocols are preferred;" placed under `should-start-with-value-types`; "concurrency, UI-framework, lint and test guidelines are satisfied." under `should-pass-repository-lint-and-tests`.

## shortcuts-and-automation
- new rules (all SHOULD, none had a keyword in devteam's text):
  - `windows-expose-flows-via-protocol-activation`: "On Windows, key flows SHOULD be exposed via protocol activation URIs." from "expose key flows via protocol activation URIs".
  - `windows-handle-command-line-activation`: "On Windows, command-line activation SHOULD be handled if the app supports it." from "command-line activation handled if supported;".
  - `windows-document-winui-scripting-limits`: "The limitations of WinUI 3 scripting SHOULD be acknowledged in the docs." from "limitations of WinUI 3 scripting acknowledged in docs".
  - `swift-expose-key-actions-as-intents`: "In Swift, key app actions SHOULD be exposed as intents, with an `AppIntent` conformance for each." from "expose key app actions as intents;" and "`AppIntent` conformances present for key actions;".
  - `swift-provide-parameter-summaries-and-suggested-phrases`: "In Swift, intents SHOULD provide parameter summaries and suggested phrases." from "provide parameter summaries and suggested phrases".
  - `swift-use-standard-parameter-types`: "In Swift, intent parameter types SHOULD use standard types where possible." from "parameter types use standard types where possible".
  Each got one line in `a-build-must-establish.md` and a short line in the review part that lacked devteam's sentence.
- reader-specific: none. contradictions: none. not placed: none.

## dependency-security
- new rules: none. reader-specific: none (the focus sentence "Treat dependencies as attack surface and manage them actively." is placed under `should-manage-dependencies-actively`). contradictions: none. not placed: none.

## transport-security
- new rules: `must-not-expose-plain-http-endpoints` ("Production domains MUST NOT expose plain-HTTP endpoints.", MUST NOT from devteam's "(no plain-HTTP endpoints)"), with a build line and a short review-focus line.
- placed verbatim: "preload` and the domain is submitted to the preload list (no plain-HTTP endpoints);" (a mid-code-span fragment, kept as devteam wrote it) under `should-submit-to-hsts-preload-list`.
- reader-specific: none. contradictions: none. not placed: none.

## animation-motion
- new rules: none. reader-specific: none. contradictions: none. not placed: none.

## previews
- new rules: none. reader-specific: none. contradictions: none. not placed: none.

## runtime-conditions
- new rules:
  - `must-identify-new-runtime-conditions-with-gated-code`: "Every NEW permission or entitlement requirement, environment prerequisite, or feature-flag dependency introduced by the change MUST be identified with the code it gates." (MUST from "Every").
  - `must-scope-to-the-change-not-the-codebase`: "Scope MUST be the change under review, and MUST NOT be a whole-codebase inventory." (from "NOT a whole-codebase inventory").
- reader-specific: "Every NEW permission/entitlement requirement, environment prerequisite, or feature-flag dependency introduced in this diff is identified with the code it gates;" and "a diff that introduces none is explicitly cleared." (the second is process, placed under the first rule). "this diff" names devteam's input.
- contradictions: none. not placed: none.

## test-pyramid
- new rules: none. reader-specific: none. contradictions: none. not placed: none.

## idempotency
- new rules: none. reader-specific: none. contradictions: none. not placed: none.

## simplicity
- new rules (SHOULD, plain checks):
  - `should-justify-each-new-layer-singly`: "Each new layer SHOULD have a clear, single justification." from "each new layer has a clear, single justification;".
  - `should-give-each-unit-a-single-describable-concern`: "Each module or function SHOULD have a single describable concern." from "Each module or function has a single describable concern;".
- reader-specific: "complexity in instructions compounds — resist at introduction time"; "Skill/rule complexity reviewed before adding new abstraction;"; "skills do not mix orchestration and domain logic;" (the last two placed under `should-ask-whether-concerns-are-braided`).
- contradictions: none. not placed: none.

## support-automation
- new rules (SHOULD, plain checks):
  - `should-wrap-deterministic-operations-in-scripts` from "shell scripts wrap deterministic operations for direct invocation;".
  - `should-allow-chaining-without-confirmation` from "skills can be chained without requiring human confirmation at each step;".
  - `should-emit-machine-parseable-output` from "outputs are machine-parseable (not just human-readable)".
- reader-specific: "Skills and agents should expose capabilities through scriptable interfaces — not just interactive use;", "skills can be chained without requiring human confirmation at each step;" and the "shell scripts" / "workflows can drive the extension" wording.
- contradictions: none. not placed: none.

## yagni
- new rules:
  - `should-build-for-todays-known-requirements` (SHOULD): "Code SHOULD be built for today's known requirements, addressing actual current workflows and not hypothetical future ones." from "Build skills and agents for today's known requirements;" and "skills address actual current workflows, not hypothetical future ones".
  - `must-not-build-speculative-generality` (MUST NOT, "no" wording): "Code MUST NOT contain speculative abstractions, hooks for future features, unused abstraction layers, extension points or generalization beyond what current requirements demand." from "no speculative abstractions, hooks for future features, or generalization beyond current need;" and "No unused abstraction layers, extension points, or generalization not required by current features;"; "no speculative multi-platform handling not required by current targets;" is placed under it.
- reader-specific: "Build skills and agents for today's known requirements;", "speculative generality in prompts (adding \"in case we need it\" context, future-proofing flags, unused parameters) adds maintenance cost with no current value;", "No unused parameters or frontmatter fields;", "no \"in case we need it\" context blocks in skill bodies;", "skills address actual current workflows, not hypothetical future ones".
- contradictions: none. not placed: none.
