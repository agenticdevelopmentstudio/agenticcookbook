
- `must-use-roadmap-frontmatter-uuid`: a roadmap ID taken from anywhere but the `id`/UUID in the roadmap file's own YAML frontmatter
- `must-not-generate-random-uuids`: a call such as `uuid4()` / `UUID.randomUUID()` / `crypto.randomUUID()` minting an ID
- `must-be-deterministic-and-reproducible`: an ID that depends on time, randomness or run order, so a rerun yields a different value
