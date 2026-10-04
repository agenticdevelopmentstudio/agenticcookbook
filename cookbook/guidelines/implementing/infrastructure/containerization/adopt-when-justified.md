
- Orchestration platforms (Kubernetes, ECS, Nomad) and per-image vulnerability scanners add real operational weight. Adopt them when a measured need justifies the cost (scale, multi-service coordination, compliance) — not by default (per YAGNI). A single image deployed to a managed container host is often sufficient early on.

