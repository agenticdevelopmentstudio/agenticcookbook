<!-- leaf: implement-code-quality/code-for-the-ai-reader · source: guidelines/implementing/code-quality/code-for-the-ai-reader.md -->

**Rules** (cite as `implement-code-quality/code-for-the-ai-reader#<slug>`):

- `names-searchable-literal-strings-prefer` MUST — Names MUST be searchable as literal strings. Prefer one canonical spelling of a concept over synonyms scattered across …
- `grepping-handle-payment-find-definition-fragment-assembled` SHOULD — Avoid constructing identifiers at runtime (string-concatenated method names, dynamically generated attributes). An …
- `sites-discoverable-function-reachable-searching-name-only` SHOULD — Keep call sites discoverable: a function SHOULD be reachable by searching for its name, not only through a registry, …
- `tests-live-close-code-they` SHOULD — Tests SHOULD live close to the code they exercise so an agent loading a module also loads its executable specification.
- `readability-norms-you-not-maximize-machine-legibility-costs` MUST — This guidance is in genuine tension with some human-readability norms, and you MUST NOT maximize machine-legibility at …

# Writing code for the AI reader

A large and growing share of code is read, navigated, and edited by AI agents, not just by onboarding humans. Agents work from a finite context window and locate behavior by searching text, so explicitness, greppability, and locality directly affect whether an agent finds the right code and changes it correctly on the first try. Treat machine-legibility as one reader audience to serve — not a license to abandon human readability.

## Write for grep, not for cleverness

- Names **MUST** be searchable as literal strings. Prefer one canonical spelling of a concept over synonyms scattered across the codebase.
- Avoid constructing identifiers at runtime (string-concatenated method names, dynamically generated attributes). An agent grepping for `handle_payment` **SHOULD** find the definition, not a fragment assembled from `"handle_" + verb`.
- Keep call sites discoverable: a function **SHOULD** be reachable by searching for its name, not only through a registry, decorator, or dependency-injection wiring that hides the connection.

## Make behavior visible, not inferred

- Minimize reflection, dynamic dispatch, and runtime metaprogramming that hides what code actually does. These force an agent (and a human) to simulate the runtime to predict behavior.
- Function signatures act as design documents the agent reads first — keep parameter names and return types explicit and accurate. (See the reference.)
- Explicit types and verbose, intention-revealing names are a deliberate **semantic investment**: they encode meaning the agent would otherwise have to reconstruct from context it may not have loaded. Prefer them where a language makes them optional.
- Prefer explicit control flow over implicit magic (auto-registration, monkey-patching, import-time side effects). Surprising behavior costs both audiences — see `principle-of-least-astonishment`.

## Colocate behavior with its tests

- Tests **SHOULD** live close to the code they exercise so an agent loading a module also loads its executable specification.
- A test named for the behavior it verifies doubles as greppable documentation of intent.

## Balance, not dogma (IMPORTANT)

This guidance is in genuine tension with some human-readability norms, and you **MUST NOT** maximize machine-legibility at all costs:

- Very short files and aggressive file-splitting can aid humans but scatter related behavior an agent must assemble from many sources. Favor **locality of related behavior**.
- Heavy DRY and deep indirection trade duplication for hidden coupling. A small, explicit repetition is often easier for both readers than a clever abstraction three layers deep. Apply judgment per case.
- The claim "agents now read code more than humans do" is a **plausible direction of travel, not a measured fact** — do not cite it as an established statistic. Justify each choice by concrete readability for the next reader, human or agent, not by appeal to that trend.
- When a human-readability convention and an AI-readability heuristic conflict and the cost is low, prefer the option that keeps behavior explicit and local. When the human cost is high, weigh both and document the trade-off.
