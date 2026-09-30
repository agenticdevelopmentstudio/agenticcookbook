<!-- leaf: plan-code-quality/essential-vs-accidental-complexity · source: guidelines/planning/code-quality/essential-vs-accidental-complexity.md -->

**Rules** (cite as `plan-code-quality/essential-vs-accidental-complexity#<slug>`):

- `tooling-ceremony-you-use-split-thinking-tool` SHOULD — Fred Brooks's *No Silver Bullet* (1986; reprinted in *The Mythical Man-Month*, 1995) splits software difficulty into …
- `you-name-essential-complexity-module` SHOULD — You SHOULD name the essential complexity of a module *before* writing code: what are the irreducible rules, states, and …
- `you-not-treat-boundary-precise-classifier` MUST — You MUST NOT treat the boundary as a precise classifier. It is fuzzy and observer-dependent — what is accidental at one …
- `you-delete-generate-away-accidental` MUST — You SHOULD delete or generate-away accidental complexity aggressively (better abstractions, code generation, fewer …
- `two-entangled-you-refactor-isolate-essential-core` SHOULD — When the two are entangled, you SHOULD refactor to isolate the essential core behind a thin layer so the accidental …
- `fast-cheaply-you-route-work-agents-review` SHOULD — LLM coding agents are the strongest tool yet against accidental complexity: they emit boilerplate, glue, scaffolding, …
- `human-judgment-you-keep-design-review-requirement` MUST — Agents cannot reduce essential complexity — they can restate it, but the irreducible domain decisions still require …

# Essential vs accidental complexity

Fred Brooks's *No Silver Bullet* (1986; reprinted in *The Mythical Man-Month*, 1995) splits software difficulty into **essential** complexity — the irreducible interlocking of the problem domain itself — and **accidental** (incidental) complexity — everything else: boilerplate, scaffolding, syntax, glue code, build tooling, and ceremony. You **SHOULD** use this split as a thinking tool when scoping a new module: it tells you where an agent can help and where human design judgment must stay in the loop.

## What goes in each bucket

| Essential (irreducible) | Accidental (incidental) |
|---|---|
| The domain rules, invariants, and edge cases the problem actually requires | Framework boilerplate, config, project setup |
| The interactions and dependencies between parts of the problem | Translating a design into a specific language's syntax |
| Concurrency/consistency demands inherent to the requirements | Wiring, adapters, serialization, glue between libraries |
| Genuinely ambiguous requirements that must be resolved | Repetitive test fixtures, mocks, and CRUD scaffolding |

## How to apply it

- You **SHOULD** name the essential complexity of a module *before* writing code: what are the irreducible rules, states, and interactions? That set is the real work; everything else is overhead to minimize.
- You **MUST NOT** treat the boundary as a precise classifier. It is fuzzy and observer-dependent — what is accidental at one altitude (a language's verbosity) can feel essential at another (a hard latency budget). Use it to guide attention, not to mechanically sort lines of code.
- You **SHOULD** delete or generate-away accidental complexity aggressively (better abstractions, code generation, fewer moving parts) but **MUST NOT** "simplify" by dropping essential cases — that is hiding complexity, not removing it, and it resurfaces as bugs.
- When the two are entangled, you **SHOULD** refactor to isolate the essential core behind a thin layer so the accidental parts can change or be regenerated independently. This advances `simplicity` and `design-for-deletion`.

## In the AI era

- LLM coding agents are the strongest tool yet against **accidental** complexity: they emit boilerplate, glue, scaffolding, and syntax fast and cheaply. You **SHOULD** route that work to agents and review it for correctness, not for novelty.
- Agents **cannot** reduce **essential** complexity — they can restate it, but the irreducible domain decisions still require human judgment. You **MUST** keep design review, requirement disambiguation, and invariant definition under human ownership even when an agent writes the code.
- Treat "AI eliminates complexity" as a **forecast/marketing claim, not an established result**. Brooks's argument that no single tool yields an order-of-magnitude gain against the essential part remains the durable, contested-by-some baseline; cheaper accidental-complexity reduction does not refute it.
- Practical consequence: as accidental cost falls, the **design bottleneck shifts toward managing essential complexity**. Spend the time saved on agents harvesting the incidental on sharper problem decomposition, not on shipping more under-specified features (see `yagni`).
