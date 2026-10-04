
# Value objects over primitive obsession

Agents default to "stringly-typed" code — bare `string`, `int`, and `map` for things like `Email`, `Money`, `UserId`, and `Percentage`. Wrapping a domain primitive in a small immutable value object centralizes its validation and makes an invalid instance impossible to construct. The value object is the concrete form of *make illegal states unrepresentable*.

