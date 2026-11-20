
# Be strict and maintain: Postel reconsidered (RFC 9413)

The naive robustness principle — "be conservative in what you send, be liberal in what you accept" — is still widely taught but is **incomplete**. IETF/IAB RFC 9413 *Maintaining Robust Protocols* (Informational, June 2023) reframes it: unconstrained tolerance without active maintenance is harmful, because tolerated deviations harden into de-facto standards that later implementations must be "bug-for-bug compatible" with. Prefer strict parsing, loud rejection, and ongoing spec-and-implementation co-evolution.

