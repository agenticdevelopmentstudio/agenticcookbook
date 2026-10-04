
- Kubernetes adds substantial operational surface (control plane, networking, RBAC, upgrades). You **SHOULD NOT** default to it. Prefer a managed PaaS, container service, or single VM until you have a measured need — multi-service orchestration, autoscaling, or multi-team self-service (per YAGNI).
- When the need justifies it, **SHOULD** use a managed control plane (e.g., EKS, GKE, AKS) rather than self-hosting, to shift undifferentiated operational load.

