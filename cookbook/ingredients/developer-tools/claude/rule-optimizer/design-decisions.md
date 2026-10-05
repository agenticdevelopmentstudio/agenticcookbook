
**Decision**: Guided pipeline with human gate, not fully autonomous.
**Rationale**: Rule files are behavioral guardrails — they control what Claude does and does not do. Autonomously modifying guardrails risks weakening safety constraints. The pr-review-pipeline is autonomous because it only reads and comments; this pipeline writes, so user confirmation is required before any modification.
**Approved**: pending

