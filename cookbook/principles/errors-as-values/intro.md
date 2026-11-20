
# Errors as values

Represent expected, recoverable failures as values in the type system — `Result`/`Either`, sealed error types — so that failure paths appear in function signatures and the compiler forces every caller to handle them. Reserve exceptions and panics for truly unrecoverable conditions. This makes the failure surface visible and exhaustiveness-checkable instead of hidden in control flow.
