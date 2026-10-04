
- **MUST** use ordinary deterministic tests for parsers, schema validation, tool-call argument construction, retries, and any logic with a fixed correct output. Do not wrap deterministic code in an LLM judge.
- **MUST** use an eval harness when the artifact under test is an agent's decisions, an LLM's generated text, multi-step tool use, or RAG answer quality — outputs that vary run to run.
- **SHOULD** isolate the deterministic and probabilistic layers so each is tested with the cheaper appropriate method.

