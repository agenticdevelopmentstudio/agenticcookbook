
This is the primary concrete handler shipped with the node. It categorizes and tags a piece of content using the configured LLM backend.

### Input (job payload)

```json
{
  "title": "string",
  "body":  "string"
}
```

### Output (job result)

```json
{
  "category":   "string",
  "tags":       ["string"],
  "confidence": 0.0
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `category` | Yes | The single best-fit category string. The backend maps this to its categories store. |
| `tags` | Yes | Zero or more keyword strings. The backend maps these to its keywords store. |
| `confidence` | No | Advisory float in [0,1] expressing the LLM's self-reported confidence. The backend treats this as informational only. |

**Schema-constrained output rule** (`structured-output`): the handler MUST pass a JSON Schema (or equivalent structured-output constraint) for the result object when invoking the LLM. It MUST NOT parse category or tags from free-form text.

**Idempotency rule** (`idempotency`): categorizing the same `(title, body)` pair a second time MUST produce no additional writes if the backend already holds a result for this job ID.

