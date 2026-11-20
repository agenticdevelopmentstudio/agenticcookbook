
Introduce a value object when a primitive meets any of these (and not before — see yagni):

- It carries **invariants** (an email must be well-formed; a percentage is 0–100; money has a currency).
- It is **validated in more than one place** — the value object lets you validate once, at construction.
- It is **easily confused with another same-shaped primitive** (a `UserId` and an `OrderId` are both strings; the type stops you passing one where the other is meant).

A primitive with none of these does not need wrapping — over-wrapping every field fights simplicity.

