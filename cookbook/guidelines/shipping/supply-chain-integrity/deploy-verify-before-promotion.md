
Detection alone is insufficient — the gate is verification.

- The deploy step **MUST** verify the artifact signature against the expected signer identity (CI workload, repo, ref).
- The deploy step **SHOULD** verify provenance: the artifact was built from the expected source repo and commit, on the expected builder, with expected parameters. A signature without provenance only proves *who signed*, not *how it was built*.
- A failed signature or provenance check **MUST** block promotion (fail-fast) — never warn-and-continue.
- Store SBOMs and attestations as immutable release evidence for incident response and audits.

