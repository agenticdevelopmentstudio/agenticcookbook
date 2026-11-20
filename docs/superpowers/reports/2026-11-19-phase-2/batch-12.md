# Phase 2 batch 12 report

Twenty principles, each converted from a single intro (a statement, then bullets) to roled parts. In every topic the
statement paragraph stays in `intro` (a trailing colon became a period), the bullets become the `rules` part, and
the three bar parts are new. No topic had a reviewer checklist, so `look-for`, `a-complete-review-must-establish`
and `a-build-must-establish` are **authored** in every topic. Evidence, citations and reasons were moved out of the
rule bullets into `rationale`, and named sources into `references`, where a topic had them.

Only one rule in the batch already carried an upper-case RFC 2119 keyword (`should-test-design-by-cognitive-load`, in
meta-principle-optimize-for-change). Every other rule is promoted. Lower-case "should"/"must" in the source is
counted as promoted, at the level the word names.

## How the tool read these principles

- **`cookr roles lossless` splits hard-wrapped text by line.** Three topics (frame-before-you-generate,
  human-first-ideation, keep-the-human-at-the-wheel) wrap their bullets across lines. Each wrapped line is its
  own "sentence" to the tool, so each is mapped on its own in `lossless.json`. That gives those topics more `moved`
  entries than rules.
- **A rewording must keep the source's verbs and 80% of its content words.** "Value types SHOULD be preferred" was
  refused for dropping "prefer", and "Phase 2 MUST NOT be skipped" for holding 71% of the words. Both were reworded
  closer to the source.
- **A `moved` entry names at most three targets.** The idempotency lead-in maps to the rule that restates it.

Every topic: `roles lossless --draft` exits 0, `roles check` exits 0, and `approve.py` printed `RESULT: APPROVED`. No
`obsolete` entries were needed.

## cookbook/principles/frame-before-you-generate

Commit `d4f491fd`. 4 rules; lossless.json: 10 moved, 0 obsolete. Extra parts: `rationale`, `references`.

**promoted** (4 rules):
- "Spend real time on problem definition: the Double Diamond (Design Council, 2005) devotes its entire first diamond to finding the right problem before the second diamond seeks solutions" → `should-spend-real-time-on-problem-definition`: "SHOULD spend real time on problem definition, finding the right problem before seeking solutions."
- "Use "How Might We" framing (IDEO; Min Basadur, 1990s) to convert closed problem statements into generative invitations: "How *Might* We [verb] [goal]?" assumes solvability, invites speculation without commitment, and creates shared ownership" → `should-use-how-might-we-framing`: "SHOULD use "How Might We" framing to convert closed problem statements into generative invitations: "How *Might* We [verb] [goal]?""
- "Apply Five Whys (Toyoda/Ohno, Toyota Production System, 1930s) to drill past stated symptoms to root causes; a stated goal is often a symptom, not the underlying need" → `should-apply-five-whys`: "SHOULD apply Five Whys to drill past stated symptoms to root causes; a stated goal is often a symptom, not the underlying need."
- "Use first-principles thinking to strip inherited assumptions and rebuild the problem from fundamental truths (Stanford d.school Empathize→Define, 2010; Aristotle; Musk/SpaceX)" → `should-use-first-principles-thinking`: "SHOULD use first-principles thinking to strip inherited assumptions and rebuild the problem from fundamental truths."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: Each bullet's citation and evidence moved to `rationale` and its source to `references`; the closing observation ("A good reframe often reveals…") is rationale, not a rule.

**contradictions**: none.

**unfinished**: none.

## cookbook/principles/human-first-ideation

Commit `647bbb21`. 4 rules; lossless.json: 11 moved, 0 obsolete. Extra parts: `rationale`, `references`.

**promoted** (4 rules):
- "Always invite the human to voice their own ideas before introducing any AI-generated alternatives." → `must-invite-human-ideas-first`: "The human MUST be invited to voice their own ideas before any AI-generated alternatives are introduced."
- "Ask "What have you been thinking?" before "Here's an idea" — always" → `must-ask-before-offering-ideas`: "The AI MUST ask "What have you been thinking?" before "Here's an idea"."
- "After the human has contributed, the AI may add — using "yes-and" (Sawyer, 2007) to build rather than replace, never to anchor or supplant" → `may-add-after-human-contributes`: "After the human has contributed, the AI MAY add, using "yes-and" to build rather than replace."
- "After the human has contributed, the AI may add — using "yes-and" (Sawyer, 2007) to build rather than replace, never to anchor or supplant" → `must-not-anchor-or-supplant`: "The AI's additions MUST NOT anchor or supplant the human's contributions."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: The two study bullets and the Vygotsky bullet are evidence, moved to `rationale`; their sources are listed in `references`. The intro statement is kept verbatim and is also rule `must-invite-human-ideas-first`.

**contradictions**: none. `may-add-after-human-contributes` keeps the source's "may" as MAY; a judge should confirm MAY is the intended level.

**unfinished**: none.

## cookbook/principles/idempotency

Commit `e8177115`. 5 rules; lossless.json: 5 moved, 0 obsolete. Extra parts: none.

**promoted** (5 rules):
- "User actions and system operations should be safe to repeat without duplicate side effects:" → `should-make-operations-safe-to-repeat`: "User actions and system operations SHOULD be safe to repeat without duplicate side effects."
- "Debounce or disable buttons during async operations" → `should-debounce-buttons-during-async`: "Buttons SHOULD be debounced or disabled during async operations."
- "Use idempotency keys for API calls with side effects" → `should-use-idempotency-keys`: "API calls with side effects SHOULD use idempotency keys."
- "Database migrations must be safe to run multiple times" → `must-make-migrations-rerunnable`: "Database migrations MUST be safe to run multiple times."
- "Check current state before applying state transitions" → `should-check-state-before-transitions`: "Current state SHOULD be checked before applying state transitions."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: The statement used a lower-case "should" and the migrations bullet a lower-case "must"; neither was an RFC keyword, so both rules are counted as promoted, at SHOULD and MUST. The statement's colon became a period in `intro`.

**contradictions**: none.

**unfinished**: none.

## cookbook/principles/immutability-by-default

Commit `81274b39`. 4 rules; lossless.json: 4 moved, 0 obsolete. Extra parts: `rationale`.

**promoted** (4 rules):
- "Default to immutable values; introduce mutability only where necessary:" → `should-default-to-immutable-values`: "Values SHOULD be immutable by default; mutability SHOULD be introduced only where necessary."
- "Use `let` (Swift), `val` (Kotlin), `const` (JS/TS) by default" → `should-use-immutable-bindings-by-default`: "`let` (Swift), `val` (Kotlin), `const` (JS/TS) SHOULD be used by default."
- "Prefer value types (structs, data classes) over reference types" → `should-prefer-value-types`: "SHOULD prefer value types (structs, data classes) over reference types."
- "Contain mutation behind clear boundaries (actors, StateFlow, useState)" → `should-contain-mutation-behind-boundaries`: "Mutation SHOULD be contained behind clear boundaries (actors, StateFlow, useState)."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: The statement's colon became a period in `intro`; its first sentence (the reason) is also the rationale for all four rules.

**contradictions**: none.

**unfinished**: none.

## cookbook/principles/independence-before-corroboration

Commit `da8f3e81`. 3 rules; lossless.json: 2 moved, 0 obsolete. Extra parts: `rationale`.

**promoted** (3 rules):
- "Count sources by their independence, not their number — many pages tracing back to one origin are still one source." → `should-count-sources-by-independence`: "Sources SHOULD be counted by their independence, not their number — many pages tracing back to one origin are still one source."
- "Before treating a claim as corroborated, check that its sources do not share an origin." → `should-check-sources-share-no-origin`: "Before a claim is treated as corroborated, its sources SHOULD be checked to confirm they do not share an origin."
- "Record each claim's corroboration as independent, single, or uncorroborated." → `should-record-corroboration-level`: "Each claim's corroboration SHOULD be recorded as independent, single, or uncorroborated."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: Three bullets are reasons, not requirements (citation loops inflate support; two independent sources beat ten; independence is the primary defense); they are `rationale`, verbatim.

**contradictions**: none.

**unfinished**: none.

## cookbook/principles/keep-the-human-at-the-wheel

Commit `a62d7a0d`. 5 rules; lossless.json: 11 moved, 0 obsolete. Extra parts: `rationale`, `references`.

**promoted** (5 rules):
- "Shneiderman (2020, *Human-Centered AI*): AI tools should support human autonomy, competence, and oversight — not absorb or replace the creative function; the human remains the author" → `should-support-human-autonomy`: "AI tools SHOULD support human autonomy, competence, and oversight — not absorb or replace the creative function; the human remains the author."
- "Rezwana & Maher (2024, arXiv 2411.12527): the target state is Level 4 co-creativity where both parties contribute meaningfully and the human maintains creative direction" → `should-target-level-4-co-creativity`: "Collaboration SHOULD target Level 4 co-creativity, where both parties contribute meaningfully and the human maintains creative direction."
- ""Yes-and" as default conversational stance (Sawyer, 2007; Hatcher, 2018): accept the human's contribution and build on it; never replace the human's framing with the AI's own" → `should-use-yes-and-stance`: ""Yes-and" SHOULD be the default conversational stance: accept the human's contribution and build on it."
- ""Yes-and" as default conversational stance (Sawyer, 2007; Hatcher, 2018): accept the human's contribution and build on it; never replace the human's framing with the AI's own" → `must-not-replace-human-framing`: "The AI MUST NOT replace the human's framing with its own."
- "Vygotsky (1978): scaffold at the Zone of Proximal Development — challenge enough to push into unexplored territory, support enough not to be overwhelming; taking the first move pulls the human below the creative work" → `should-scaffold-at-zpd`: "The AI SHOULD scaffold at the Zone of Proximal Development — challenge enough to push into unexplored territory, support enough not to be overwhelming."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: The HAICo bullet is evidence only and became `rationale`; every bullet's citation is in `references`.

**contradictions**: none.

**unfinished**: none.

## cookbook/principles/make-it-work-make-it-right-make-it-fast

Commit `f8554872`. 5 rules; lossless.json: 5 moved, 0 obsolete. Extra parts: none.

**promoted** (5 rules):
- "Separate correctness, design quality, and performance into sequential phases:" → `should-separate-into-sequential-phases`: "Correctness, design quality, and performance SHOULD be separated into sequential phases."
- "Get a working solution for the common case" → `should-first-make-it-work`: "Phase 1 SHOULD get a working solution for the common case."
- "Refactor for clarity, handle edge cases, clean up design" → `should-then-make-it-right`: "Phase 2 SHOULD refactor for clarity, handle edge cases, and clean up design."
- "Optimize only what measurement proves is slow" → `should-optimize-only-measured-slowness`: "Phase 3 SHOULD optimize only what measurement proves is slow."
- "Never skip phase 2 to jump to phase 3." → `must-not-skip-make-it-right`: "MUST NOT skip phase 2 to jump to phase 3."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: The numbered phases became one rule each; "Never skip phase 2 to jump to phase 3." became MUST NOT.

**contradictions**: none. `should-optimize-only-measured-slowness` reads "Optimize only what measurement proves is slow" at SHOULD (plain imperative); "only" could be read as MUST, so a judge should check it.

**unfinished**: none.

## cookbook/principles/manage-complexity-through-boundaries

Commit `a42e158b`. 10 rules; lossless.json: 6 moved, 0 obsolete. Extra parts: `rationale`.

**promoted** (10 rules):
- "Define ports (interfaces) that describe what the application needs." → `should-define-ports`: "SHOULD define ports (interfaces) that describe what the application needs."
- "Use adapters to translate between external technologies and your ports." → `should-use-adapters`: "SHOULD use adapters to translate between external technologies and your ports."
- "Test the core application without databases, UIs, or networks." → `should-test-core-without-infrastructure`: "SHOULD test the core application without databases, UIs, or networks."
- "Define each external dependency as a protocol the app owns, not a concrete type the vendor owns" → `should-define-dependencies-as-owned-protocols`: "SHOULD define each external dependency as a protocol the app owns, not a concrete type the vendor owns."
- "Keep adapter implementations thin — translate and delegate, never add business logic" → `should-keep-adapters-thin`: "SHOULD keep adapter implementations thin — translate and delegate."
- "Keep adapter implementations thin — translate and delegate, never add business logic" → `must-not-add-business-logic-to-adapters`: "Adapter implementations MUST NOT add business logic."
- "If two modules need to share a type, extract it into a shared contract rather than coupling the modules directly" → `should-extract-shared-contracts`: "If two modules need to share a type, SHOULD extract it into a shared contract rather than coupling the modules directly."
- "Verify boundaries by confirming core logic compiles and tests pass with no framework imports" → `should-verify-boundaries-without-framework-imports`: "SHOULD verify boundaries by confirming core logic compiles and tests pass with no framework imports."
- "Extend at the boundary, don't break the contract: once a boundary is stable and widely depended on, add capability through new implementations behind the port rather than changing the port's existing shape — the durable kernel of the open/closed principle." → `should-extend-at-the-boundary`: "Extend at the boundary, don't break the contract: once a boundary is stable and widely depended on, SHOULD add capability through new implementations behind the port rather than changing the port's existing shape."
- "Apply it only to boundaries that have actually stabilized; do not pre-generalize one you are still discovering (see yagni, steel-thread-first)." → `should-not-pre-generalize-unstable-boundaries`: "SHOULD apply extend-at-the-boundary only to boundaries that have actually stabilized, and SHOULD NOT pre-generalize one you are still discovering (see yagni, steel-thread-first)."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: The three imperatives in the statement paragraph stay in `intro` verbatim and are also rules. "Keep adapter implementations thin — translate and delegate, never add business logic" split into a SHOULD (thin) and a MUST NOT (no business logic). The open/closed remark is `rationale`.

**contradictions**: none.

**unfinished**: none.

## cookbook/principles/meta-principle-optimize-for-change

Commit `3024d3f8`. 6 rules; lossless.json: 5 moved, 0 obsolete. Extra parts: `rationale`.

**promoted** (5 rules):
- "When evaluating any technical decision, the primary question is: "Does this make future change easier or harder?"" → `should-ask-whether-future-change-gets-easier`: "When evaluating any technical decision, the primary question SHOULD be: "Does this make future change easier or harder?""
- "Before committing to an architecture, ask: "What would it cost to reverse this in six months?"" → `should-ask-reversal-cost`: "Before committing to an architecture, SHOULD ask: "What would it cost to reverse this in six months?""
- "Prefer decisions that keep options open over decisions that lock in a technology or pattern" → `should-prefer-decisions-that-keep-options-open`: "SHOULD prefer decisions that keep options open over decisions that lock in a technology or pattern."
- "When two approaches are otherwise equal, choose the one that is easier to change later" → `should-choose-easier-to-change-when-equal`: "When two approaches are otherwise equal, SHOULD choose the one that is easier to change later."
- "so use cognitive load as a lens (proxies: fan-out, file count, time-to-onboard), not a thresholded metric." → `should-use-cognitive-load-as-a-lens`: "SHOULD use cognitive load as a lens (proxies: fan-out, file count, time-to-onboard), not a thresholded metric."
- not promoted (already RFC): `should-test-design-by-cognitive-load`

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: `should-test-design-by-cognitive-load` already carried **SHOULD** and is not promoted. The cognitive-load caveat split into a rule (`should-use-cognitive-load-as-a-lens`) and its reason (`rationale`).

**contradictions**: none between rules. The statement opens "Every principle above…", which in a one-topic folder refers to nothing above it; left unchanged.

**unfinished**: none.

## cookbook/principles/native-controls

Commit `ecef282a`. 6 rules; lossless.json: 5 moved, 0 obsolete. Extra parts: none.

**promoted** (6 rules):
- "Always use the platform's built-in frameworks before custom implementations." → `must-use-built-in-frameworks-first`: "MUST use the platform's built-in frameworks before custom implementations: Swift Concurrency over raw threads, Room/SwiftData over raw SQLite, Fetch API over custom HTTP."
- "When generating a component, explicitly note which native controls are being used and why." → `should-note-native-controls-used`: "When generating a component, SHOULD explicitly note which native controls are being used and why."
- "If there is ambiguity about whether a native control fits, ask the user before proceeding." → `should-ask-when-native-fit-is-ambiguous`: "If there is ambiguity about whether a native control fits, SHOULD ask the user before proceeding."
- "Search the platform SDK for an existing control before writing a custom one" → `should-search-sdk-before-custom-control`: "SHOULD search the platform SDK for an existing control before writing a custom one."
- "When a native control almost fits, customize it rather than replacing it with a from-scratch implementation" → `should-customize-near-fit-native-controls`: "When a native control almost fits, SHOULD customize it rather than replacing it with a from-scratch implementation."
- "Justify every third-party UI dependency with a concrete gap the platform SDK cannot fill" → `should-justify-third-party-ui-dependencies`: "SHOULD justify every third-party UI dependency with a concrete gap the platform SDK cannot fill."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: The statement's "Always use…" stays in `intro` verbatim and is also rule `must-use-built-in-frameworks-first` at MUST; the second intro paragraph became two rules.

**contradictions**: none.

**unfinished**: none.

## cookbook/principles/open-source-preference

Commit `7b27f2d9`. 8 rules; lossless.json: 6 moved, 0 obsolete. Extra parts: none.

**promoted** (8 rules):
- "When no native solution exists, research battle-tested open-source libraries and present options to the user before building a custom solution." → `should-research-open-source-before-building`: "When no native solution exists, SHOULD research battle-tested open-source libraries and present options to the user before building a custom solution."
- "A custom implementation can always be chosen instead, but it should be a deliberate decision, not a default." → `should-make-custom-a-deliberate-decision`: "A custom implementation MAY always be chosen instead, but it SHOULD be a deliberate decision, not a default."
- "Before reaching outward, check what you already have: the platform's standard library and the dependencies already in the project often solve the problem — prefer those before adding anything new" → `should-check-what-you-already-have`: "Before reaching outward, SHOULD check what you already have: the platform's standard library and the dependencies already in the project often solve the problem — SHOULD prefer those before adding anything new."
- "Evaluate candidates by maintenance activity, license compatibility, and community adoption before recommending" → `should-evaluate-candidates-before-recommending`: "SHOULD evaluate candidates by maintenance activity, license compatibility, and community adoption before recommending."
- "Verify a candidate is real before adopting it: confirm the package actually exists, is actively maintained, and is widely used." → `should-verify-candidate-is-real`: "SHOULD verify a candidate is real before adopting it: confirm the package actually exists, is actively maintained, and is widely used."
- "Never install a package name an AI suggested without verifying it — hallucinated and typosquatted names are a live supply-chain risk" → `must-not-install-unverified-ai-suggested-packages`: "MUST NOT install a package name an AI suggested without verifying it — hallucinated and typosquatted names are a live supply-chain risk."
- "Present at least two options with trade-offs rather than silently picking one" → `should-present-at-least-two-options`: "SHOULD present at least two options with trade-offs rather than silently picking one."
- "If building custom, document why the available open-source options were rejected" → `should-document-why-open-source-was-rejected`: "If building custom, SHOULD document why the available open-source options were rejected."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: The statement's lower-case "should" was not an RFC keyword (promoted). "can always be chosen" was read as MAY, inside `should-make-custom-a-deliberate-decision`. "Never install…" became its own MUST NOT rule.

**contradictions**: none.

**unfinished**: none.

## cookbook/principles/parse-dont-validate

Commit `312ec25c`. 5 rules; lossless.json: 4 moved, 0 obsolete. Extra parts: `examples`, `rationale`.

**promoted** (5 rules):
- "Encode invariants in the type system so invalid values cannot be constructed, and *parse* untrusted input once at the boundary into a type that carries proof of its own validity — rather than passing raw primitives inward and re-validating them at every use. A value that type-checks should already be known-good." → `should-encode-invariants-in-types`: "SHOULD encode invariants in the type system so invalid values cannot be constructed; a value that type-checks SHOULD already be known-good."
- "Parse at the boundary: convert untrusted input into a domain type exactly once; the parsed value *is* the proof." → `should-parse-at-the-boundary`: "Parse at the boundary: SHOULD convert untrusted input into a domain type exactly once; the parsed value *is* the proof."
- "Don't thread raw strings and maps through the system and re-check them downstream." → `should-not-revalidate-downstream`: "SHOULD NOT thread raw strings and maps through the system and re-check them downstream."
- "Make illegal states unconstructable: model with the narrowest type that fits — sum types/enums for "one of", non-empty collections, bounded ranges, opaque/branded types — so a whole class of "this should never happen" branches disappears." → `should-make-illegal-states-unconstructable`: "Make illegal states unconstructable: SHOULD model with the narrowest type that fits — sum types/enums for "one of", non-empty collections, bounded ranges, opaque/branded types — so a whole class of "this should never happen" branches disappears."
- "Push the burden of proof upward, but no further: validate as early as the information is available, without forcing callers to prove things they cannot yet know." → `should-push-proof-upward-but-no-further`: "Push the burden of proof upward, but no further: SHOULD validate as early as the information is available, without forcing callers to prove things they cannot yet know."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: The per-language bullet became an `examples` part, and the "Complements input-validation" bullet a `rationale` part, both verbatim. The intro statement stays verbatim; its requirement is also rule `should-encode-invariants-in-types`.

**contradictions**: none.

**unfinished**: none.

## cookbook/principles/principle-of-least-astonishment

Commit `f1da38b3`. 7 rules; lossless.json: 4 moved, 0 obsolete. Extra parts: none.

**promoted** (7 rules):
- "APIs, UI, and system behavior should match what users and callers expect." → `should-match-caller-expectations`: "APIs, UI, and system behavior SHOULD match what users and callers expect."
- "If a name suggests one behavior, it must deliver that behavior." → `must-deliver-the-behavior-a-name-suggests`: "If a name suggests one behavior, it MUST deliver that behavior."
- "Side effects should be obvious from the API signature." → `should-make-side-effects-obvious-from-signature`: "Side effects SHOULD be obvious from the API signature."
- "Name functions and types so a reader can predict what they do without reading the implementation" → `should-name-for-predictability`: "SHOULD name functions and types so a reader can predict what they do without reading the implementation."
- "If a method mutates state, make that visible in the name or signature — never hide side effects" → `must-make-mutation-visible`: "If a method mutates state, MUST make that visible in the name or signature — never hide side effects."
- "Follow platform naming conventions even when you prefer a different style" → `should-follow-platform-naming-conventions`: "SHOULD follow platform naming conventions even when you prefer a different style."
- "When reviewing code, ask: "Would a new team member be surprised by this behavior?"" → `should-ask-would-a-new-team-member-be-surprised`: "When reviewing code, SHOULD ask: "Would a new team member be surprised by this behavior?""

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: The three statement sentences used lower-case "should"/"must" and became rules at SHOULD/MUST (promoted), with the statement kept in `intro`. The bullet "When reviewing code, ask…" is reviewer text; it is kept as a rule, and its line in `look-for` is authored from it.

**contradictions**: none.

**unfinished**: none.

## cookbook/principles/provenance-at-generation-time

Commit `320a033e`. 4 rules; lossless.json: 3 moved, 0 obsolete. Extra parts: `rationale`.

**promoted** (4 rules):
- "Capture a claim's provenance as you gather it — the source, the exact supporting quote, and the access date — never reconstruct it afterward." → `must-capture-provenance-while-gathering`: "MUST capture a claim's provenance as you gather it — the source, the exact supporting quote, and the access date — and MUST NOT reconstruct it afterward."
- "Attach the citation and the verbatim supporting quote at the moment the claim is made." → `should-attach-citation-when-claim-is-made`: "SHOULD attach the citation and the verbatim supporting quote at the moment the claim is made."
- "Record what was searched and where the claim came from, not just the conclusion." → `should-record-search-and-origin`: "SHOULD record what was searched and where the claim came from, not just the conclusion."
- "A claim whose provenance cannot be captured does not belong in the output." → `should-not-output-claims-without-provenance`: "A claim whose provenance cannot be captured SHOULD NOT be in the output; it does not belong there."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: Two bullets are reasons (reconstructed citations invite fabrication; late provenance is guessed) and became `rationale`, verbatim.

**contradictions**: none. `should-not-output-claims-without-provenance` reads "does not belong in the output" (no keyword, no never/always) at SHOULD NOT; it could be meant as MUST NOT, so a judge should check it.

**unfinished**: none.

## cookbook/principles/separation-of-concerns

Commit `ff2ab8d8`. 5 rules; lossless.json: 5 moved, 0 obsolete. Extra parts: `rationale`.

**promoted** (5 rules):
- "A module should have one reason to change." → `should-have-one-reason-to-change`: "A module SHOULD have one reason to change. This applies at every scale: functions, modules, services, teams."
- "Describe each module's responsibility in one sentence without using "and" — if you cannot, split it" → `should-split-when-description-needs-and`: "SHOULD describe each module's responsibility in one sentence without using "and" — if you cannot, split it."
- "Keep UI rendering, business logic, and data access in separate layers that can change independently" → `should-separate-ui-logic-and-data`: "SHOULD keep UI rendering, business logic, and data access in separate layers that can change independently."
- "When a change to one feature forces edits in an unrelated feature, treat it as a coupling defect" → `should-treat-cross-feature-edits-as-coupling`: "When a change to one feature forces edits in an unrelated feature, SHOULD treat it as a coupling defect."
- "Counterweight — locality of behavior: separate by *reason to change*, but co-locate by *reason to read*." → `should-co-locate-by-reason-to-read`: "Counterweight — locality of behavior: SHOULD separate by *reason to change*, but co-locate by *reason to read*; choose per case rather than maximizing either."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: The locality counterweight split into a rule (`should-co-locate-by-reason-to-read`) and its reasoning (`rationale`).

**contradictions**: Mild tension, left unfixed: the intro says "If describing what a module does requires 'and,' consider splitting." while the bullet says "Describe each module's responsibility in one sentence without using 'and' — if you cannot, split it". The rule keeps the bullet's firmer wording, and the intro keeps its own.

**unfinished**: none.

## cookbook/principles/simplicity

Commit `ed100e14`. 3 rules; lossless.json: 4 moved, 0 obsolete. Extra parts: none.

**promoted** (3 rules):
- "Before adding abstraction, ask: "Am I braiding two concerns together?"" → `should-ask-whether-concerns-are-braided`: "Before adding abstraction, SHOULD ask: "Am I braiding two concerns together?""
- "Favor constructs that do one thing over constructs that feel convenient" → `should-favor-single-purpose-constructs`: "SHOULD favor constructs that do one thing over constructs that feel convenient."
- "Complexity is never removed later — it compounds. Resist it at introduction time" → `should-resist-complexity-at-introduction`: "SHOULD resist complexity at introduction time — complexity is never removed later; it compounds."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: "Complexity is never removed later — it compounds" is a claim, not an instruction, so its "never" does not raise the rule to MUST; `should-resist-complexity-at-introduction` is SHOULD, from "Resist it".

**contradictions**: none.

**unfinished**: none.

## cookbook/principles/small-reversible-decisions

Commit `6a210781`. 5 rules; lossless.json: 4 moved, 0 obsolete. Extra parts: none.

**promoted** (5 rules):
- "If a decision is cheap to reverse, make it fast." → `should-make-cheap-to-reverse-decisions-fast`: "If a decision is cheap to reverse, SHOULD make it fast."
- "If it is expensive to reverse, invest in understanding first:" → `should-invest-in-understanding-expensive-decisions`: "If a decision is expensive to reverse, SHOULD invest in understanding first."
- "Prefer incremental delivery over phased releases" → `should-prefer-incremental-delivery`: "SHOULD prefer incremental delivery over phased releases."
- "Defer binding decisions until the last responsible moment" → `should-defer-binding-decisions`: "SHOULD defer binding decisions until the last responsible moment."
- "Treat architecture as a continuous activity, not an up-front phase" → `should-treat-architecture-as-continuous`: "SHOULD treat architecture as a continuous activity, not an up-front phase."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: The statement's two sentences became two rules; its colon became a period in `intro`.

**contradictions**: none.

**unfinished**: none.

## cookbook/principles/srp

Commit `9b563265`. 5 rules; lossless.json: 4 moved, 0 obsolete. Extra parts: none.

**promoted** (5 rules):
- "A module should be answerable to one and only one actor — one stakeholder, one source of change requests." → `should-answer-to-one-actor`: "A module SHOULD be answerable to one and only one actor — one stakeholder, one source of change requests."
- "Trace each anticipated change request to a stakeholder — if two stakeholders can drive changes to the same module independently, the module carries two responsibilities and should split" → `should-split-modules-two-stakeholders-drive`: "SHOULD trace each anticipated change request to a stakeholder — if two stakeholders can drive changes to the same module independently, the module carries two responsibilities and SHOULD split."
- "Keep code that changes together, together; separate code that changes for different reasons even if it looks similar today" → `should-keep-code-that-changes-together-together`: "SHOULD keep code that changes together, together; SHOULD separate code that changes for different reasons even if it looks similar today."
- "Treat unexpected merge conflicts between unrelated features as a signal that a module is absorbing responsibilities for more than one actor" → `should-treat-unexpected-merge-conflicts-as-a-signal`: "SHOULD treat unexpected merge conflicts between unrelated features as a signal that a module is absorbing responsibilities for more than one actor."
- "A long function or wide class is usually a sign that multiple actors share it — prefer narrow units each answerable to one actor" → `should-prefer-narrow-units`: "A long function or wide class is usually a sign that multiple actors share it — SHOULD prefer narrow units each answerable to one actor."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: The statement's and first bullet's lower-case "should" were not RFC keywords (promoted at SHOULD).

**contradictions**: none.

**unfinished**: none.

## cookbook/principles/steel-thread-first

Commit `9a20ede7`. 6 rules; lossless.json: 5 moved, 0 obsolete. Extra parts: none.

**promoted** (6 rules):
- "Before building breadth, build the thinnest end-to-end slice that exercises every integration boundary and the deployment path — a "steel thread" or walking skeleton. ... prove the whole shape connects once, end to end, then fill it in." → `should-build-the-steel-thread-first`: "Before building breadth, SHOULD build the thinnest end-to-end slice that exercises every integration boundary and the deployment path — a "steel thread" or walking skeleton — and prove the whole shape connects once, end to end, then fill it in."
- "Thin but complete: one real path through every layer and boundary (UI → API → store → deploy), not a finished feature — connect the architecture before investing in any single part." → `should-keep-the-thread-thin-but-complete`: "Thin but complete: the thread SHOULD be one real path through every layer and boundary (UI → API → store → deploy), not a finished feature — connect the architecture before investing in any single part."
- "This is the balance with YAGNI: build the shell only for the path you are committed to and that is expensive to wire up later." → `should-build-the-shell-only-for-the-committed-path`: "This is the balance with YAGNI: SHOULD build the shell only for the path you are committed to and that is expensive to wire up later."
- "Do not pre-build features, options, or abstractions you don't yet need — that remains YAGNI." → `should-not-pre-build-unneeded-features`: "SHOULD NOT pre-build features, options, or abstractions you don't yet need — that remains YAGNI."
- "Front-load the risky integrations: the thread should pierce the boundaries most likely to surprise you (auth, third-party APIs, the deploy pipeline), so failures surface while they are cheap." → `should-front-load-risky-integrations`: "Front-load the risky integrations: the thread SHOULD pierce the boundaries most likely to surprise you (auth, third-party APIs, the deploy pipeline), so failures surface while they are cheap."
- "For agents: validate the end-to-end shape before spending effort on breadth, so a wrong architecture is caught early instead of after generating volume against it." → `should-validate-shape-before-breadth`: "For agents: SHOULD validate the end-to-end shape before spending effort on breadth, so a wrong architecture is caught early instead of after generating volume against it."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: The statement's first sentence stays in `intro` verbatim and is also rule `should-build-the-steel-thread-first`. "Do not pre-build…" was read at SHOULD NOT (no never/always).

**contradictions**: none.

**unfinished**: none.

## cookbook/principles/support-automation

Commit `c0867800`. 5 rules; lossless.json: 4 moved, 0 obsolete. Extra parts: `rationale`.

**promoted** (5 rules):
- "Applications should expose their capabilities through automation interfaces, not just interactive UI." → `should-expose-capabilities-through-automation`: "Applications SHOULD expose their capabilities through automation interfaces, not just interactive UI; automation support is a design constraint, not an afterthought."
- "Expose core actions through platform automation frameworks (AppIntents, AppActions, UI Automation, APIs) wherever the platform provides them" → `should-use-platform-automation-frameworks`: "SHOULD expose core actions through platform automation frameworks (AppIntents, AppActions, UI Automation, APIs) wherever the platform provides them."
- "Treat the accessibility tree as the automation backbone — scriptability and assistive technology share the same semantic foundation" → `should-treat-accessibility-tree-as-backbone`: "SHOULD treat the accessibility tree as the automation backbone — scriptability and assistive technology share the same semantic foundation."
- "Design operations as discrete, composable commands that can be invoked programmatically, not just through clicks and taps" → `should-design-composable-commands`: "SHOULD design operations as discrete, composable commands that can be invoked programmatically, not just through clicks and taps."
- "Provide non-interactive entry points (CLI, URL schemes, intent filters) so workflows and tools can drive the app without a human in the loop" → `should-provide-non-interactive-entry-points`: "SHOULD provide non-interactive entry points (CLI, URL schemes, intent filters) so workflows and tools can drive the app without a human in the loop."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**notes**: The statement's lower-case "should" was not an RFC keyword (promoted). Its second sentence stays in `intro` and is also the `rationale`.

**contradictions**: none.

**unfinished**: none.
