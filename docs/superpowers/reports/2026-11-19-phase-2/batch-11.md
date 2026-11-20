# Phase 2 batch 11 report

Twenty principles. Each was a single intro (an H1, a statement paragraph, then bullets) and is now in roled parts. In every topic the statement paragraph stays in `intro`. A requirement it states is also named as a rule, so the bars cover it. The bullets that state requirements become the `rules` part. The bullets that give evidence, techniques or examples moved word for word into `rationale`, `how-to` or `examples` parts, keeping their original line breaks. No base text had an upper-case RFC 2119 keyword, so **every rule is promoted**. Each one is listed below, quoted before and after. No topic had text written for a reviewer, so all three bar parts are **authored** in every topic. No topic has an `obsolete` entry.

Where the base intro's lead sentence ended in ":" (dependency-injection, design-for-deletion, explicit-over-implicit, fail-fast), it now ends in a period in `intro`. Each such sentence holds a negation or more than eight content words, so `cookr roles lossless` does not read it as a bare lead-in, and its colon form maps to `intro` (plus its rule) as an ordinary moved entry.

## cookbook/principles/break-fixation-deliberately

**promoted** (2 rules):
- "Worst Possible Idea: generate deliberately terrible solutions, then invert — the inversion step / is mandatory; it is what converts the exercise from humor to insight" → `must-invert-worst-possible-ideas`: "When using Worst Possible Idea — generate deliberately terrible solutions, then invert — the inversion step is mandatory and MUST be done; it is what converts the exercise from humor to insight."
- "Signal to invoke: when the same category of idea recurs three or more times, or the user says / "I'm stuck," introduce a disruption before offering any more suggestions" → `should-disrupt-when-ideas-recur-or-user-is-stuck`: "Signal to invoke: when the same category of idea recurs three or more times, or the user says "I'm stuck," SHOULD introduce a disruption before offering any more suggestions."

**moved entries**: 4 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- The de Bono, reverse brainstorming and SCAMPER bullets moved word for word into a `how-to` part, *Disruption Techniques*.
- `must-invert-worst-possible-ideas` is MUST because the source calls the inversion step "mandatory". That word is not an RFC keyword, so the level is a reading for a judge to check.

**contradictions**: none

**unfinished**: none.

## cookbook/principles/bridge-distant-domains

**promoted** (2 rules):
- "LLMs default toward statistically-common (near-domain) associations; a brainstorming facilitator must deliberately reach for distant and unusual structural matches." (still word for word in `intro`) → `must-reach-for-distant-structural-matches`: "Because LLMs default toward statistically-common (near-domain) associations, a brainstorming facilitator MUST deliberately reach for distant and unusual structural matches."
- "The AI's unique contribution: ask "What problem in nature, history, or an unrelated industry is / structurally similar to this one?" before offering domain-native solutions" → `should-ask-for-structural-analogue-first`: "The AI's unique contribution: SHOULD ask "What problem in nature, history, or an unrelated industry is structurally similar to this one?" before offering domain-native solutions."

**moved entries**: 2 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- The Synectics bullet became a `how-to` part, the Velcro/sonar/Shinkansen bullet an `examples` part, and the Mednick and Fauconnier & Turner bullets a `rationale` part. All moved word for word.
- The statement paragraph stays in `intro` as written. Its lower-case "must" also becomes `must-reach-for-distant-structural-matches`, so the bars cover it.

**contradictions**: none

**unfinished**: none.

## cookbook/principles/cite-the-claim-not-the-document

**promoted** (3 rules):
- "Attach sources at the sentence or claim level, not as a document-wide reference list." → `should-attach-sources-at-claim-level`: "SHOULD attach sources at the sentence or claim level, not as a document-wide reference list."
- "Include the verbatim quote that supports the specific claim; never paraphrase the key evidence." → `should-include-verbatim-supporting-quote`: "SHOULD include the verbatim quote that supports the specific claim."
- "Include the verbatim quote that supports the specific claim; never paraphrase the key evidence." → `must-not-paraphrase-key-evidence`: "MUST NOT paraphrase the key evidence."

**moved entries**: 2 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- The three bullets that give reasons (claim-level citations let a reader verify each statement independently, and the two after it) moved word for word into a `rationale` part.
- "Include the verbatim quote ...; never paraphrase the key evidence" is split into a SHOULD (`should-include-verbatim-supporting-quote`) and a MUST NOT (`must-not-paraphrase-key-evidence`). The split follows the brief: "never" gives MUST NOT, and a plain imperative gives SHOULD.

**contradictions**: none

**unfinished**: none.

## cookbook/principles/composition-over-inheritance

**promoted** (4 rules):
- "Default to composing behaviors from small, focused pieces." (still word for word in `intro`) → `should-compose-from-small-focused-pieces`: "SHOULD default to composing behaviors from small, focused pieces."
- "When tempted to subclass, ask: "Is this truly an 'is-a' relationship, or am I just reusing code?"" → `should-use-inheritance-only-for-genuine-is-a`: "SHOULD use inheritance only for genuine "is-a" relationships, and even then sparingly; when tempted to subclass, SHOULD ask: "Is this truly an 'is-a' relationship, or am I just reusing code?""
- "Extract shared behavior into protocols or standalone functions instead of a base class" → `should-prefer-protocols-over-base-classes`: "SHOULD prefer protocols/interfaces over base classes, extracting shared behavior into protocols or standalone functions instead of a base class."
- "Wrap an existing type with a new type to add behavior rather than extending the inheritance chain" → `should-wrap-rather-than-subclass`: "When extending behavior, SHOULD wrap rather than subclass: wrap an existing type with a new type to add behavior rather than extending the inheritance chain."

**moved entries**: 3 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- The four statement sentences stay in `intro` as written, and each also becomes a rule. Each bullet is merged into the statement rule it elaborates: the is-a question into `should-use-inheritance-only-for-genuine-is-a`, extracting shared behavior into `should-prefer-protocols-over-base-classes`, and wrapping an existing type into `should-wrap-rather-than-subclass`.

**contradictions**: none

**unfinished**: none.

## cookbook/principles/connascence

**promoted** (6 rules):
- "Two rules govern it: **minimize** overall connascence by keeping coupled things close, and **weaken** strong forms into weaker ones as the distance between them grows." (still word for word in `intro`) → `should-minimize-overall-connascence`: "SHOULD **minimize** overall connascence by keeping coupled things close."
- "Rank, don't just detect: judge each coupling on three axes — strength (how hard it is to change in concert), degree (how many elements share it), and locality (how far apart they live)." → `should-rank-coupling-on-three-axes`: "SHOULD rank, not just detect: judge each coupling on three axes — strength (how hard it is to change in concert), degree (how many elements share it), and locality (how far apart they live)."
- "The farther apart two coupled elements live, the weaker the form between them must be — e.g. positional args → named parameters → a typed message across a boundary." → `must-weaken-coupling-with-distance`: "MUST **weaken** strong forms into weaker ones as the distance between them grows: the farther apart two coupled elements live, the weaker the form between them must be — e.g. positional args → named parameters → a typed message across a boundary."
- "Prefer the weakest form that does the job: replace positional arguments with named ones, magic numbers with named constants, duck-typed shapes with explicit types." → `should-prefer-weakest-form`: "SHOULD prefer the weakest form that does the job: replace positional arguments with named ones, magic numbers with named constants, duck-typed shapes with explicit types."
- "Use it as the vocabulary for coupling reviews: "connascence of position across a module boundary — convert to connascence of name" is a decision, not a matter of taste." → `should-use-connascence-as-review-vocabulary`: "SHOULD use connascence as the vocabulary for coupling reviews: "connascence of position across a module boundary — convert to connascence of name" is a decision, not a matter of taste."
- "Reach for the full lattice only when the three axes above don't settle the call." → `should-use-full-lattice-only-when-axes-do-not-settle`: "SHOULD reach for the full lattice only when the three axes above don't settle the call."

**moved entries**: 5 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- The statement paragraph stays in `intro` as written. Its "two rules", minimize and weaken, become `should-minimize-overall-connascence` and part of `must-weaken-coupling-with-distance`.
- `must-weaken-coupling-with-distance` is MUST because the source says the form "must be" weaker with distance (lower case). The intro's "weaken" clause has no level of its own and was merged into it.
- The reference-lattice sentence moved word for word into a `how-to` part. "A positional dependency is stronger ..." and "Weaken with distance: ... two services" moved word for word into `rationale`.

**contradictions**: none

**unfinished**: none.

## cookbook/principles/constraints-as-creative-fuel

**promoted** (2 rules):
- "Self-imposed constraints outperform externally-imposed ones: always offer the constraint as a / provocation ("What if you could only use three materials?") and let the user choose whether to / accept, modify, or reject it" → `must-offer-constraints-as-provocations`: "Self-imposed constraints outperform externally-imposed ones: MUST always offer the constraint as a provocation ("What if you could only use three materials?") and let the user choose whether to accept, modify, or reject it."
- "Invoke when the user is stuck or generating redundantly; a targeted constraint redirects energy / more effectively than asking for "more ideas"" → `should-invoke-constraint-when-stuck-or-redundant`: "SHOULD invoke a constraint when the user is stuck or generating redundantly; a targeted constraint redirects energy more effectively than asking for "more ideas"."

**moved entries**: 5 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- The Acar and Moreau & Dahl bullets moved word for word into `rationale`. The time/resource/scope-constraints bullet moved word for word into a `how-to` part, *Constraint Types*.

**contradictions**: none

**unfinished**: none.

## cookbook/principles/conways-law

**promoted** (9 rules):
- "The actionable corollary (the "inverse Conway maneuver") is to deliberately shape team and agent boundaries to match the architecture you want, then let the system grow into them." (still word for word in `intro`) → `should-shape-boundaries-to-target-architecture`: "SHOULD deliberately shape team and agent boundaries to match the architecture you want, then let the system grow into them (the "inverse Conway maneuver")."
- "**Agent assignment is therefore an architectural decision, not just a scheduling one.**" (still word for word in `intro`) → `should-treat-agent-assignment-as-architecture`: "Agent assignment SHOULD be treated as an architectural decision, not just a scheduling one."
- "Optimize the real coordination paths." → `should-optimize-real-coordination-paths`: "SHOULD optimize the real coordination paths — who actually coordinates with whom (shared context, handoffs, review loops) — not nominal reporting lines or agent labels."
- "**Treat the inverse maneuver as a lens, not a deterministic law.** Aligning boundaries makes a target architecture *easier*; it does not guarantee it." → `should-treat-inverse-maneuver-as-lens`: "SHOULD treat the inverse maneuver as a lens, not a deterministic law: aligning boundaries makes a target architecture *easier*; it does not guarantee it."
- "Verify the emergent structure against the intended design rather than assuming alignment." → `should-verify-emergent-structure`: "SHOULD verify the emergent structure against the intended design rather than assuming alignment."
- "**Assign agents along the seams you want in the code.** Give each module or bounded context to one agent (or one tightly-coordinating cluster)." → `should-assign-agents-along-desired-seams`: "SHOULD assign agents along the seams you want in the code: give each module or bounded context to one agent (or one tightly-coordinating cluster)."
- "**Watch for high-bandwidth handoffs.** Where two agents must exchange large, frequently-changing context to make progress, expect a tight coupling to appear at that boundary in the output." → `should-watch-for-high-bandwidth-handoffs`: "SHOULD watch for high-bandwidth handoffs: where two agents must exchange large, frequently-changing context to make progress, expect a tight coupling to appear at that boundary in the output."
- "If that coupling is undesirable, restructure the assignment, not just the prompt." → `should-restructure-assignment-not-prompt`: "If that coupling is undesirable, SHOULD restructure the assignment, not just the prompt."
- "**Re-partition when the architecture should change.** Because boundaries are sticky, a desired architectural shift usually requires reshaping who builds what — see `[adc.principle.meta-principle-optimize-for-change](cookbook:aadd048b-da52-415d-949f-45160b970381)`." → `should-repartition-when-architecture-changes`: "SHOULD re-partition when the architecture should change: because boundaries are sticky, a desired architectural shift usually requires reshaping who builds what — see `[adc.principle.meta-principle-optimize-for-change](cookbook:aadd048b-da52-415d-949f-45160b970381)`."

**moved entries**: 7 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- Both statement paragraphs stay in `intro` as written. The inverse-maneuver sentence and the bold "Agent assignment is therefore an architectural decision" also become rules.
- From the bullets, "**Communication patterns drive the effect — not org charts.** What matters is ..." and "Splitting a single coherent module ... fuse them" moved word for word into `rationale`. Every other sentence of the bullets is a named rule.
- In `should-watch-for-high-bandwidth-handoffs` the source's lower-case "must exchange" is kept as written. It describes the agents, not a requirement, so the rule's own level is SHOULD.

**contradictions**: none

**unfinished**: none.

## cookbook/principles/counteract-homogenization-with-diversity

**promoted** (3 rules):
- "Resist statistically-common ideas; deploy diverse specialist personas and, where feasible, multiple models with different training data." (still word for word in `intro`) → `should-deploy-diverse-personas-and-models`: "SHOULD resist statistically-common ideas and deploy diverse specialist personas and, where feasible, multiple models with different training data."
- "Always ask "what would be the most *surprising* version of this?" to reach the low-probability / tail of the idea distribution rather than the statistical center" → `must-ask-for-most-surprising-version`: "MUST always ask "what would be the most *surprising* version of this?" to reach the low-probability tail of the idea distribution rather than the statistical center."
- "Prefer genuine multi-model diversity (different providers, different training data) over / multi-prompt diversity within one model where feasible" → `should-prefer-multi-model-diversity`: "SHOULD prefer genuine multi-model diversity (different providers, different training data) over multi-prompt diversity within one model where feasible."

**moved entries**: 4 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- The Anderson, Meincke/Nave/Terwiesch and MultiAgent Research Ideator bullets moved word for word into `rationale`. The statement stays in `intro`, and its directive also becomes `should-deploy-diverse-personas-and-models`.

**contradictions**: none

**unfinished**: none.

## cookbook/principles/critique-without-killing

**promoted** (4 rules):
- "Productive critique, applied after divergence is complete, strengthens the idea pool rather than shrinking it." (still word for word in `intro`) → `should-critique-after-divergence-is-complete`: "Critique SHOULD be applied after divergence is complete, so it strengthens the idea pool rather than shrinking it."
- "The form matters: questions ("What would have to be true for this to succeed?") preserve the idea for refinement; verdicts ("This won't work") end it." (still word for word in `intro`) → `should-critique-with-questions-not-verdicts`: "Critique SHOULD take the form of questions ("What would have to be true for this to succeed?"), which preserve the idea for refinement, not verdicts ("This won't work"), which end it."
- "Nemeth & Rogers (1996): devil's advocate groups generated more alternatives and made better decisions than groups without — but ONLY when the challenge targeted the idea, not the person" (still word for word in `rationale`) → `should-target-the-idea-not-the-person`: "A challenge SHOULD target the idea, not the person."
- "Tom Kelley (IDEO, 2005): ... the constructive version requires proposing an alternative direction after every objection" (still word for word in `rationale`) → `must-propose-alternative-after-every-objection`: "Constructive devil's advocacy MUST propose an alternative direction after every objection."

**moved entries**: 0 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- Every base sentence is kept word for word, so `lossless.json` has no entries. The statement stays in `intro`. The Klein premortem and Disney Method bullets moved into a `how-to` part, *Critique Techniques*. The Nemeth & Rogers, Kelley and Schulze-Bentrop bullets moved into `rationale`.
- Its rules are named from requirements that the statement and two evidence bullets state as findings. A judge should check that each one is a requirement the topic makes, not one added to it. `must-propose-alternative-after-every-objection` is MUST because Kelley's bullet says the constructive version "requires" it.

**contradictions**: none

**unfinished**: none.

## cookbook/principles/defer-judgment-go-for-quantity

**promoted** (3 rules):
- "During divergent phases, withhold all evaluation — no scoring, no ranking, no "yes, but."" (still word for word in `intro`) → `should-withhold-evaluation-during-divergence`: "During divergent phases, SHOULD withhold all evaluation — no scoring, no ranking, no "yes, but.""
- "Volume precedes quality; the pool must be large before selection is meaningful." (still word for word in `intro`) → `must-grow-pool-before-selection`: "Volume precedes quality; the pool must be large before selection is meaningful, so selection MUST wait for a large pool."
- "Concretely: set a count target before evaluating ("let's get to 15 ideas before we talk about / which ones are best")" → `should-set-count-target-before-evaluating`: "Concretely: SHOULD set a count target before evaluating ("let's get to 15 ideas before we talk about which ones are best")."

**moved entries**: 2 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- All four evidence bullets moved word for word into `rationale`. The statement stays in `intro`, and its two requirements also become rules.
- `should-withhold-evaluation-during-divergence` is SHOULD, because "withhold all evaluation" is a plain imperative. `must-grow-pool-before-selection` is MUST, from the source's lower-case "the pool must be large". See the contradictions section for how this sits beside diverge-before-you-converge.

**contradictions**: Level mismatch with `diverge-before-you-converge` (same batch), left as found. defer-judgment `should-withhold-evaluation-during-divergence`: "During divergent phases, SHOULD withhold all evaluation — no scoring, no ranking, no "yes, but."" diverge-before-you-converge `must-not-let-convergent-thinking-into-divergence`: "MUST NOT allow convergent thinking to enter a divergent phase." Both say the same thing at different levels. The sources gave a plain imperative ("withhold") in one and "never" in the other, and the brief maps those to SHOULD and MUST NOT.

**unfinished**: none.

## cookbook/principles/deliberate-prudent-debt

**promoted** (5 rules):
- "Deliberate and prudent only: "ship the simple version now, revisit when X happens" is fine when it's written down; an undocumented shortcut nobody chose is reckless debt." → `must-take-debt-only-deliberately-and-prudently`: "Technical debt MUST be taken only deliberately and prudently — a conscious, recorded choice with a payback trigger, never reckless or silent: "ship the simple version now, revisit when X happens" is fine when it's written down; an undocumented shortcut nobody chose is reckless debt."
- "Record it at the point of compromise: leave a tracked marker (debt register, issue, or a TODO that states the condition) naming the trigger that should prompt repayment." → `should-record-debt-at-point-of-compromise`: "SHOULD record it at the point of compromise: leave a tracked marker (debt register, issue, or a to-do comment that states the condition) naming the trigger that should prompt repayment."
- "Budget repayment: allocate capacity each iteration to pay debt down; debt with no payback plan compounds into decay." → `should-budget-repayment-each-iteration`: "SHOULD budget repayment: allocate capacity each iteration to pay debt down; debt with no payback plan compounds into decay."
- "Account for AI volume: agent-generated code can inflate duplication and churn faster than debt is repaid — size debt budgets against the volume produced, and prefer paying down before adding more." → `should-size-debt-budgets-against-ai-volume`: "SHOULD account for AI volume: agent-generated code can inflate duplication and churn faster than debt is repaid — size debt budgets against the volume produced, and prefer paying down before adding more."
- "Take the shortcut on purpose, write down what you deferred and why, budget time to repay it, and keep the debt visible rather than letting quality decay unnoticed." (still word for word in `intro`) → `should-keep-debt-visible`: "SHOULD keep the debt visible rather than letting quality decay unnoticed."

**moved entries**: 4 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- **Wording change forced by approve.py:** "or a TODO that states the condition" is now "or a to-do comment that states the condition" in `should-record-debt-at-point-of-compromise`. approve.py's FM-13 fails on the literal token `TODO` as placeholder text, and the source used it as a real marker kind. The meaning is unchanged, and the `lossless.json` moved entry records the rewording for the judge.
- `must-take-debt-only-deliberately-and-prudently` is MUST because the intro says the trade is legitimate "only when" deliberate and prudent, and "never reckless or silent".

**contradictions**: none

**unfinished**: none.

## cookbook/principles/dependency-injection

**promoted** (5 rules):
- "A component should receive its dependencies from the outside, not construct them internally:" → `should-receive-dependencies-from-outside`: "A component SHOULD receive its dependencies from the outside, not construct them internally."
- "Pass services via constructor/initializer parameters or protocol properties" → `should-pass-services-via-initializer-or-protocol-properties`: "SHOULD pass services via constructor/initializer parameters or protocol properties."
- "Never instantiate a concrete service inside the component that uses it" → `must-not-instantiate-concrete-service-in-its-user`: "MUST NOT instantiate a concrete service inside the component that uses it."
- "Use protocol/interface types for dependencies, not concrete types" → `should-depend-on-protocol-types`: "SHOULD use protocol/interface types for dependencies, not concrete types."
- "Avoid service locator pattern (hidden global lookup)" → `should-avoid-service-locator`: "SHOULD avoid the service locator pattern (hidden global lookup)."

**moved entries**: 5 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- The intro's lead sentence ended in ":", which leads into the bullets. In `intro` it now ends in a period. The base sentence with the colon maps to `intro` and `should-receive-dependencies-from-outside`. It has a negation, so `lossless` does not read it as a bare lead-in.

**contradictions**: none

**unfinished**: none.

## cookbook/principles/design-for-deletion

**promoted** (5 rules):
- "Build disposable software, not reusable software:" → `should-build-disposable-software`: "SHOULD build disposable software, not reusable software."
- "Write code that is easy to throw away without affecting the rest of the system" → `should-write-code-easy-to-throw-away`: "SHOULD write code that is easy to throw away without affecting the rest of the system."
- "Treat lines of code as lines spent — deleting code reduces maintenance cost" → `should-treat-lines-as-spent`: "SHOULD treat lines of code as lines spent — deleting code reduces maintenance cost."
- "Do not abstract prematurely in pursuit of reuse" → `should-not-abstract-prematurely-for-reuse`: "SHOULD NOT abstract prematurely in pursuit of reuse."
- "When in doubt, duplicate rather than couple" → `should-duplicate-rather-than-couple-when-in-doubt`: "When in doubt, SHOULD duplicate rather than couple."

**moved entries**: 5 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- "Build disposable software, not reusable software:" now ends in a period in `intro`. Its colon form maps to `intro` and `should-build-disposable-software`.
- "Do not abstract prematurely" became SHOULD NOT. It is a plain negative imperative, not "never".

**contradictions**: Not a contradiction, noted for the judge: `should-duplicate-rather-than-couple-when-in-doubt` ("When in doubt, SHOULD duplicate rather than couple.") sits beside DRY's `should-consolidate-facts-across-layers`. DRY's own `should-duplicate-when-unsure` carries the same exception, so the two agree.

**unfinished**: none.

## cookbook/principles/diverge-before-you-converge

**promoted** (5 rules):
- "Hold generation and evaluation in strictly separated phases; never allow convergent thinking to enter a divergent phase." (still word for word in `intro`) → `should-separate-generation-and-evaluation-phases`: "SHOULD hold generation and evaluation in strictly separated phases."
- "Hold generation and evaluation in strictly separated phases; never allow convergent thinking to enter a divergent phase." (still word for word in `intro`) → `must-not-let-convergent-thinking-into-divergence`: "MUST NOT allow convergent thinking to enter a divergent phase."
- "Phase transitions must be named, explicit, and mutually agreed — never a silent drift." (still word for word in `intro`) → `must-name-and-agree-phase-transitions`: "Phase transitions MUST be named, explicit, and mutually agreed — never a silent drift."
- "Announce phases explicitly ("We're diverging now — no evaluation yet") and treat a phase shift" → `should-announce-phases-explicitly`: "SHOULD announce phases explicitly ("We're diverging now — no evaluation yet")."
- "Announce phases explicitly ("We're diverging now — no evaluation yet") and treat a phase shift / as a joint decision: never shift unilaterally" → `must-not-shift-phase-unilaterally`: "SHOULD treat a phase shift as a joint decision: MUST NOT shift unilaterally."

**moved entries**: 2 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- All four evidence bullets moved word for word into `rationale`. The statement stays in `intro` and is also split into three rules: hold the phases apart (SHOULD, a plain imperative), never let convergent thinking in (MUST NOT), and transitions "must be" named and agreed (MUST).

**contradictions**: See defer-judgment-go-for-quantity: the same requirement appears there at SHOULD and here at MUST NOT.

**unfinished**: none.

## cookbook/principles/document-the-process-not-a-conclusion

**promoted** (5 rules):
- "Document the journey (thought graph, timeline, sources) so it can be resumed, revisited, and mined — and respect incubation by making pauses a first-class feature." (still word for word in `intro`) → `should-document-the-journey`: "SHOULD document the journey (thought graph, timeline, sources) so it can be resumed, revisited, and mined."
- "Document the journey (thought graph, timeline, sources) so it can be resumed, revisited, and mined — and respect incubation by making pauses a first-class feature." (still word for word in `intro`) → `should-make-pauses-first-class`: "SHOULD respect incubation by making pauses a first-class feature."
- "A "parked" branch is not a failed idea — it is a resumable thread; the thought graph preserves / what was *not* chosen as richly as what was, enabling later mining" → `should-preserve-unchosen-branches`: "A "parked" branch is not a failed idea — it is a resumable thread; the thought graph SHOULD preserve what was *not* chosen as richly as what was, enabling later mining."
- "Shneiderman's CST principle "Leverage rich history" (2002, 2007, CACM): tools should preserve all past work so users can return; showing only current state destroys the journey's accumulated value" (still word for word in `rationale`) → `should-preserve-all-past-work`: "Tools SHOULD preserve all past work so users can return; showing only current state destroys the journey's accumulated value."
- "The facilitator's closing move is always to document where the session was heading, so the next / session can pick up from the right place without losing orientation" → `must-document-where-session-was-heading`: "The facilitator's closing move MUST always be to document where the session was heading, so the next session can pick up from the right place without losing orientation."

**moved entries**: 4 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- The Wallas, provenance and Shneiderman bullets moved word for word into `rationale`. The statement stays in `intro`, and its two directives also become rules. Shneiderman's "tools should preserve all past work" also becomes `should-preserve-all-past-work`.

**contradictions**: none

**unfinished**: none.

## cookbook/principles/domain-stratified-trust

**promoted** (5 rules):
- "The bar a claim must clear is set by its domain — the cost of being wrong — not by how casually or urgently it was asked." (still word for word in `intro`) → `should-set-the-bar-by-domain`: "The bar a claim must clear SHOULD be set by its domain — the cost of being wrong — not by how casually or urgently it was asked."
- "High-consequence domains (medical, legal, financial, scientific) demand independent primary or credentialed sources." → `must-demand-primary-sources-in-high-consequence-domains`: "High-consequence domains (medical, legal, financial, scientific) MUST demand independent primary or credentialed sources."
- "Low-consequence, subjective domains (recipes, product picks, opinion) may validate by broad independent consensus." → `may-validate-low-consequence-by-consensus`: "Low-consequence, subjective domains (recipes, product picks, opinion) MAY validate by broad independent consensus."
- "A confident tone or expert phrasing never lowers the bar; the domain does." → `must-not-lower-the-bar-for-confident-tone`: "A confident tone or expert phrasing MUST NOT lower the bar; the domain does."
- "Cap a claim's trust score when it fails its domain's minimum source, however plausible it sounds." → `should-cap-trust-below-domain-minimum`: "SHOULD cap a claim's trust score when it fails its domain's minimum source, however plausible it sounds."

**moved entries**: 4 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- The "Candy bars cure colds" bullet moved word for word into an `examples` part.
- `must-demand-primary-sources-in-high-consequence-domains` is MUST, read from "demand". `may-validate-low-consequence-by-consensus` is MAY, read from the source's lower-case "may". `must-not-lower-the-bar-for-confident-tone` is MUST NOT, read from "never lowers".

**contradictions**: none

**unfinished**: none.

## cookbook/principles/dry

**promoted** (5 rules):
- "Every piece of knowledge — a business rule, a constant, a data schema, a validation — should have a single, unambiguous, authoritative representation in the system." (still word for word in `intro`) → `should-give-each-piece-of-knowledge-one-representation`: "Every piece of knowledge — a business rule, a constant, a data schema, a validation — SHOULD have a single, unambiguous, authoritative representation in the system."
- "Ask "does this code encode the same knowledge?" before deduplicating — if two fragments will evolve for different reasons, leave them alone" → `should-ask-whether-same-knowledge-before-deduplicating`: "SHOULD ask "does this code encode the same knowledge?" before deduplicating — if two fragments will evolve for different reasons, leave them alone."
- "When the same fact appears across layers (model, validation, UI copy, tests), consolidate to one source and derive the rest" → `should-consolidate-facts-across-layers`: "When the same fact appears across layers (model, validation, UI copy, tests), SHOULD consolidate to one source and derive the rest."
- "Prefer code generation, configuration, or derivation over hand-synchronized copies of the same fact" → `should-prefer-derivation-over-synchronized-copies`: "SHOULD prefer code generation, configuration, or derivation over hand-synchronized copies of the same fact."
- "If you are unsure whether two fragments represent the same knowledge, duplicate — a coincidental twin is cheaper to split later than a wrong abstraction is to unwind" → `should-duplicate-when-unsure`: "If you are unsure whether two fragments represent the same knowledge, SHOULD duplicate — a coincidental twin is cheaper to split later than a wrong abstraction is to unwind."

**moved entries**: 4 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- The statement stays in `intro` as written, including the paragraph's note that DRY is about knowledge, not code shape. Its "should have a single ... representation" also becomes a rule.

**contradictions**: none

**unfinished**: none.

## cookbook/principles/errors-as-values

**promoted** (5 rules):
- "Expected vs exceptional: model recoverable outcomes (not-found, validation-failed, conflict) as returned values; let exceptions signal bugs and unrecoverable states." → `should-model-recoverable-outcomes-as-values`: "Expected vs exceptional: SHOULD model recoverable outcomes (not-found, validation-failed, conflict) as returned values."
- "Expected vs exceptional: model recoverable outcomes (not-found, validation-failed, conflict) as returned values; let exceptions signal bugs and unrecoverable states." → `should-reserve-exceptions-for-unrecoverable`: "SHOULD reserve exceptions and panics for truly unrecoverable conditions: let exceptions signal bugs and unrecoverable states."
- "Put the failure in the signature: a function that can fail should say so in its return type, not through an undeclared throw a caller can't see." → `should-put-the-failure-in-the-signature`: "Put the failure in the signature: a function that can fail SHOULD say so in its return type, not through an undeclared throw a caller can't see."
- "Choose a boundary policy deliberately and keep it consistent per layer: Rust `Result`, Go explicit error returns, Kotlin sealed `Result`, Swift `Result`/`throws`, TypeScript Result-style libraries." → `should-keep-boundary-policy-consistent-per-layer`: "SHOULD choose a boundary policy deliberately and keep it consistent per layer: Rust `Result`, Go explicit error returns, Kotlin sealed `Result`, Swift `Result`/`throws`, TypeScript Result-style libraries."
- "Never swallow: log-and-continue, a silent `null`, or a default that masks failure is the documented failure mode — propagate or handle explicitly." → `must-not-swallow-failures`: "MUST NOT swallow: log-and-continue, a silent `null`, or a default that masks failure is the documented failure mode — MUST propagate or handle explicitly."

**moved entries**: 4 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- The bullet beginning "Complements the wire format ..." is a scope note, and it moved word for word into `rationale`. The statement stays in `intro`.
- The bullet "Expected vs exceptional" maps to two rules: `should-model-recoverable-outcomes-as-values`, and `should-reserve-exceptions-for-unrecoverable`, which also restates the intro's "Reserve exceptions and panics".

**contradictions**: none

**unfinished**: none.

## cookbook/principles/explicit-over-implicit

**promoted** (3 rules):
- "Make dependencies visible (injection over hidden globals)" → `should-make-dependencies-visible`: "SHOULD make dependencies visible (injection over hidden globals)."
- "Name things for what they do, not how they are implemented" → `should-name-for-what-things-do`: "SHOULD name things for what they do, not how they are implemented."
- "Prefer clear parameter passing over ambient state" → `should-prefer-parameters-over-ambient-state`: "SHOULD prefer clear parameter passing over ambient state."

**moved entries**: 4 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- The intro's lead sentence ("... take days to find:") now ends in a period. Its colon form maps to `intro`, which holds it whole. With 10 content words it is too long for `lossless` to read as a bare lead-in.

**contradictions**: none

**unfinished**: none.

## cookbook/principles/fail-fast

**promoted** (6 rules):
- "Invalid state should be detected and surfaced immediately at the point of origin, not propagated silently:" → `should-surface-invalid-state-at-origin`: "Invalid state SHOULD be detected and surfaced immediately at the point of origin, not propagated silently."
- "Use assertions and preconditions in debug builds" → `should-assert-preconditions-in-debug`: "SHOULD use assertions and preconditions in debug builds."
- "Validate inputs at system boundaries" → `should-validate-inputs-at-boundaries`: "SHOULD validate inputs at system boundaries."
- "Return typed errors rather than swallowing exceptions" → `should-return-typed-errors`: "SHOULD return typed errors rather than swallowing exceptions."
- "Never use empty catch blocks" → `must-not-use-empty-catch-blocks`: "MUST NOT use empty catch blocks."
- "In production, fail gracefully with clear messages; in debug, fail loudly" → `should-fail-gracefully-in-production-loudly-in-debug`: "In production, SHOULD fail gracefully with clear messages; in debug, SHOULD fail loudly."

**moved entries**: 6 reworded, 0 obsolete.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

- The intro's lead sentence now ends in a period. Its colon form maps to `intro` and `should-surface-invalid-state-at-origin`.

**contradictions**: none

**unfinished**: none.
