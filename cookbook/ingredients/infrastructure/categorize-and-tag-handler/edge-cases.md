
- **Empty body**: A payload with a title and an empty body is still valid; the handler categorizes from the title.
- **Missing payload field**: A payload missing `title` or `body` MUST be reported as a failure rather than sent to the LLM.
- **Result already held by the backend**: The handler returns the held result without re-applying it (idempotent-categorization).

