
- Match on field presence and type, and on matcher-based values (e.g. "an ISO-8601 string", "a positive integer"), not on exact literals that change per request.
- Assert the error/status codes the consumer branches on; ignore codes it never inspects.
- A contract that breaks on a *backward-compatible* provider change (a new optional field, a reordered list) is too strict — loosen it.

