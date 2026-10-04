
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

