# Principles

Core engineering principles that guide all cookbook decisions and implementations.

| File | Description |
|------|-------------|
| [meta-principle-optimize-for-change/](meta-principle-optimize-for-change/) | Every principle is a strategy for making future change cheaper and safer |
| [simplicity/](simplicity/) | Simple means no interleaving of concerns; optimize for simplicity over ease |
| [separation-of-concerns/](separation-of-concerns/) | A module should have one reason to change |
| [srp/](srp/) | A module should be answerable to one and only one actor |
| [connascence/](connascence/) | Coupling has a rankable strength; weaken strong forms, especially as distance grows |
| [conways-law/](conways-law/) | A system's architecture mirrors the communication structure (or agent topology) that builds it |
| [composition-over-inheritance/](composition-over-inheritance/) | Default to composing behaviors from small, focused pieces |
| [dependency-injection/](dependency-injection/) | A component should receive its dependencies from the outside |
| [explicit-over-implicit/](explicit-over-implicit/) | Hidden behavior, magic, and implicit coupling create bugs that take days to find |
| [fail-fast/](fail-fast/) | Invalid state should be detected and surfaced immediately at the point of origin |
| [parse-dont-validate/](parse-dont-validate/) | Encode invariants in types; parse untrusted input once into a value that proves its validity |
| [errors-as-values/](errors-as-values/) | Represent expected failures as values so failure paths appear in signatures and must be handled |
| [idempotency/](idempotency/) | User actions and system operations should be safe to repeat without duplicate side effects |
| [immutability-by-default/](immutability-by-default/) | Default to immutable values; introduce mutability only when profiling demands it |
| [manage-complexity-through-boundaries/](manage-complexity-through-boundaries/) | Well-defined boundaries between subsystems let each side evolve independently |
| [design-for-deletion/](design-for-deletion/) | Every line of code is a maintenance liability; build disposable software |
| [dry/](dry/) | Every piece of knowledge should have a single, authoritative representation |
| [native-controls/](native-controls/) | Always use the platform's built-in frameworks before custom implementations |
| [open-source-preference/](open-source-preference/) | When no native solution exists, research battle-tested open-source libraries first |
| [principle-of-least-astonishment/](principle-of-least-astonishment/) | APIs, UI, and system behavior should match what users and callers expect |
| [small-reversible-decisions/](small-reversible-decisions/) | If a decision is cheap to reverse, make it fast |
| [tight-feedback-loops/](tight-feedback-loops/) | The speed of your feedback loop is the speed of your learning |
| [make-it-work-make-it-right-make-it-fast/](make-it-work-make-it-right-make-it-fast/) | Separate correctness, design quality, and performance into sequential phases |
| [support-automation/](support-automation/) | Applications should expose their capabilities through automation interfaces |
| [yagni/](yagni/) | Build for today's known requirements, not speculative generality |
| [steel-thread-first/](steel-thread-first/) | Build the thinnest end-to-end slice through every boundary before breadth |
| [deliberate-prudent-debt/](deliberate-prudent-debt/) | Trade rigor for speed only as a deliberate, recorded choice with a payback trigger |
| [type-precedes-method/](type-precedes-method/) | The research type sets the sources, the method, and the bar — classify before you research |
| [domain-stratified-trust/](domain-stratified-trust/) | A claim's bar is set by its domain (the cost of being wrong), not by how it was asked |
| [independence-before-corroboration/](independence-before-corroboration/) | Count sources by independence, not number — pages tracing to one origin are one source |
| [provenance-at-generation-time/](provenance-at-generation-time/) | Capture source, quote, and access date as you gather — never reconstruct citations after |
| [cite-the-claim-not-the-document/](cite-the-claim-not-the-document/) | Every claim carries its own citation and exact supporting quote; a bibliography is not auditable |
| [suppress-unsupported-confidence/](suppress-unsupported-confidence/) | Confident language over thin evidence is itself a red flag |
