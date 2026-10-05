
An LLM backend is the inference provider a handler uses for its model step: a local model server, a hosted API, or a CLI tool run as a subprocess. This ingredient makes the provider a configured dependency rather than a code decision, so the same handler runs unmodified against a local model on a development machine and a hosted API in production, and can be tested against a stub. It also fixes how handlers obtain results: as schema-constrained structured output validated before the handler returns, never as free-form text parsed after the fact.

Use it in any worker or service where handlers call a language model and the deployment environment decides which model that is.

