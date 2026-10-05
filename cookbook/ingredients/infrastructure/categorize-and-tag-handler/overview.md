
The `categorize_and_tag` handler is the primary concrete job handler shipped with the AI processing node. Given a piece of content (title and body), it uses the configured LLM backend to choose the single best-fit category and a set of keyword tags, and returns them as a structured result the backend maps onto its categories and keywords stores. Use it as the reference handler when adding new job types: it shows the payload contract, the schema-constrained output rule, and the idempotency rule in one small unit.

