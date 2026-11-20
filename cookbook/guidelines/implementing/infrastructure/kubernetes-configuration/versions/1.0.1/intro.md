
# Kubernetes configuration and secrets

Externalize all configuration from container images: use ConfigMaps for non-sensitive settings and Secrets for credentials. Treat a Kubernetes Secret as **base64-encoded, not encrypted** — protect it at the cluster level or source it from a dedicated secret manager.

> Adopt Kubernetes only when a measured operational need justifies it (per YAGNI). A single container, a serverless platform, or a managed PaaS is often the simpler default; the guidance below applies once you have committed to Kubernetes.

