
| State | Behavior |
|-------|----------|
| Received | Payload validated against the input shape |
| Inferring | LLM request in flight with the result schema |
| Validated | LLM output conforms to the result schema |
| Rejected | Output failed validation; the handler reports a retryable failure |

