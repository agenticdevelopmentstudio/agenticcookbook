
- **should-introduce-value-object-when-criteria-met**: You SHOULD introduce a value object when a primitive meets any of these (and not before — see yagni):
  - It carries **invariants** (an email must be well-formed; a percentage is 0–100; money has a currency).
  - It is **validated in more than one place** — the value object lets you validate once, at construction.
  - It is **easily confused with another same-shaped primitive** (a `UserId` and an `OrderId` are both strings; the type stops you passing one where the other is meant).
  - A primitive with none of these does not need wrapping — over-wrapping every field fights simplicity.
- **must-validate-at-construction**: Validate at construction and reject invalid input there (parse, don't validate) — a constructed instance MUST be known-valid.
- **should-be-immutable-with-value-equality**: A value object SHOULD be immutable with value equality (two value objects with the same contents are equal).
- **should-keep-value-object-small-and-focused**: A value object SHOULD be kept small and focused on the single concept it represents.
