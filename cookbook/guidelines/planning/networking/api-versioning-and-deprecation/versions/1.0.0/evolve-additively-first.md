
- You **MUST** treat additive changes (new optional fields, new endpoints, new optional query params, new enum values consumers can ignore) as non-breaking and ship them without a version bump.
- You **MUST** treat these as breaking and requiring a version: removing or renaming a field, changing a type or units, tightening validation, changing defaults, altering status codes, or changing pagination/auth semantics.
- Clients **MUST** tolerate unknown fields (ignore, don't reject) so the server can add fields freely. Per the observable-behavior-contract guideline (Hyrum's Law), assume consumers depend on *every* observable detail — undocumented field order, error text, timing — so changing those can break someone even when the spec did not.

