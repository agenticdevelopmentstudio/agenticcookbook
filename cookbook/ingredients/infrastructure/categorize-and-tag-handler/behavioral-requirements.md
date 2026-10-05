
- **handler-job-type**: The handler MUST register under the job type `categorize_and_tag`.
- **input-payload**: The handler MUST accept a job payload of the shape `{ "title": string, "body": string }`.
- **output-result**: The handler MUST return a result of the shape `{ "category": string, "tags": string[], "confidence": number }`, where `category` and `tags` are required and `confidence` is optional.
- **category-single-best-fit**: `category` MUST be the single best-fit category string; the backend maps it to its categories store.
- **tags-keywords**: `tags` MUST contain zero or more keyword strings; the backend maps them to its keywords store.
- **confidence-advisory**: `confidence`, when present, MUST be a float in [0,1] expressing the LLM's self-reported confidence. The backend treats it as informational only.
- **schema-constrained-output**: The handler MUST pass a JSON Schema (or equivalent structured-output constraint) for the result object when invoking the LLM, and MUST NOT parse category or tags from free-form text.
- **idempotent-categorization**: Categorizing the same `(title, body)` pair a second time MUST produce no additional writes if the backend already holds a result for this job ID.

