<!-- leaf: implement-networking/robust-protocol-maintenance · source: guidelines/implementing/networking/robust-protocol-maintenance.md -->

**Rules** (cite as `implement-networking/robust-protocol-maintenance#<slug>`):

- `inputs-parsed-strictly-against-dated` SHOULD — Inputs SHOULD be parsed strictly against a dated, pinned version of the spec or schema, and violations SHOULD be …
- `implementations-not-silently-fix-up-guess` MUST — Implementations MUST NOT silently "fix up" or guess intent for malformed protocol or API messages on machine-to-machine …
- `rejections-emit-explicit-actionable-error` SHOULD — Rejections SHOULD emit an explicit, actionable error (what failed, which rule, expected shape) so the sending party …
- `protocols-apis-carry-explicit-version-so` SHOULD — Protocols and APIs SHOULD carry an explicit version so strictness can evolve without breaking peers; pin the revision …
- `stateless-unauthenticated-endpoints-soften-loud-rejection-where` MAY — Stateless or unauthenticated endpoints MAY soften loud rejection where verbose errors enable amplification or DoS (RFC …
- `you-treat-tolerated-deviation-tracked` SHOULD — You SHOULD treat each tolerated deviation as a tracked maintenance item: file it, decide whether the spec or the sender …

# Be strict and maintain: Postel reconsidered (RFC 9413)

The naive robustness principle — "be conservative in what you send, be liberal in what you accept" — is still widely taught but is **incomplete**. IETF/IAB RFC 9413 *Maintaining Robust Protocols* (Informational, June 2023) reframes it: unconstrained tolerance without active maintenance is harmful, because tolerated deviations harden into de-facto standards that later implementations must be "bug-for-bug compatible" with. Prefer strict parsing, loud rejection, and ongoing spec-and-implementation co-evolution.

## Why naive tolerance fails (RFC 9413, 2023)

- Silently accepting malformed input creates a **pathological feedback cycle**: the deviation goes unreported, spreads, and becomes load-bearing.
- The cure is **active maintenance** — designers, implementers, and deployers evolve the spec and deployments together — not permanent tolerance.
- This is a deliberate, cited correction of a contested heuristic, **not** a claim that Postel was wrong in all contexts. Tolerance still has a place at the human-facing edge (see below).

## Rules

- Inputs **SHOULD** be parsed strictly against a dated, pinned version of the spec or schema, and violations **SHOULD** be rejected clearly rather than silently coerced (ties to `parse-dont-validate` and `fail-fast`).
- Implementations **MUST NOT** silently "fix up" or guess intent for malformed protocol or API messages on machine-to-machine paths.
- Rejections **SHOULD** emit an explicit, actionable error (what failed, which rule, expected shape) so the sending party gets visible feedback — RFC 9413 calls this "virtuous intolerance".
- Protocols and APIs **SHOULD** carry an explicit **version** so strictness can evolve without breaking peers; pin the revision you validate against.
- Stateless or unauthenticated endpoints **MAY** soften loud rejection where verbose errors enable amplification or DoS (RFC 9413 notes this exception) — log internally instead.
- You **SHOULD** treat each tolerated deviation as a tracked maintenance item: file it, decide whether the spec or the sender is wrong, and close the gap — do not let it become permanent behavior.

## Strict core, forgiving edge — do not over-rotate

| Boundary | Posture | Rationale |
|----------|---------|-----------|
| Machine-to-machine (wire, internal API) | **Strict** parse, reject + report | Tolerance here breeds undocumented coupling |
| External/3rd-party input you don't control | **Strict** parse, but graceful degradation | You cannot fix their sender; fail safe, log, alert |
| Human/UX edge (forms, CLI args, NL) | **Forgiving** — normalize then validate | Usability; humans are not protocols |

Do **NOT** read this guideline as "be hostile and strict everywhere." Hostile strictness at the human edge harms usability; the synthesis is: **strict internally, forgiving at the human edge, with active maintenance closing the loop**.
