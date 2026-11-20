
A verifier MUST check each of the following items. The recipe PASSES cookbook compliance only if every item is satisfied.

- [ ] No behavioral requirement in the recipe contradicts a MUST in any applicable cookbook guideline.
- [ ] Where cookbook guidelines apply to this recipe's domain, they are cited in `depends-on` or `references`.
- [ ] If the recipe involves authentication, authorization, or sensitive data: a security section is present covering storage, transmission, and violation handling.
- [ ] If the recipe involves authentication, authorization, or sensitive data: token lifetimes, storage mechanisms, and revocation are specified.
- [ ] If the recipe involves a UI element or interaction: an accessibility section is present.
- [ ] If the recipe involves a UI element: requirements cover contrast, touch target size, keyboard navigation, and control labels.
- [ ] If the recipe involves network requests: failure modes, retry behavior, and user-facing error communication are all addressed.
- [ ] If the recipe involves data persistence: durability guarantees and backup/conflict behavior are specified.
- [ ] No requirement defers entirely to "best practices" without citing specific, verifiable practices.
- [ ] No guideline content is reproduced verbatim without a reference back to the source guideline.
- [ ] `must-be-at-least-as-strict-as-guideline-musts`: No requirement relaxes a guideline's MUST to a SHOULD or MAY without an explicit documented exception approved by the cookbook maintainers.
- [ ] `must-satisfy-all-applicable-guidelines-together`: Every applicable guideline is satisfied at once; compliance with one is not used to justify non-compliance with another.
- [ ] `should-reference-guideline-inline`: Each requirement derived from or constrained by a guideline carries an inline reference to it.
- [ ] `must-not-make-required-accessibility-optional`: Accessibility is not marked MAY where law or platform policy requires it (e.g., WCAG 2.1 AA, Apple Human Interface Guidelines).
- [ ] `should-reference-accessibility-guideline`: A UI recipe names the applicable accessibility guideline in `depends-on`.
- [ ] `must-not-make-routine-error-handling-should`: A networking recipe does not make error handling a SHOULD where failure is a routine operating condition.
