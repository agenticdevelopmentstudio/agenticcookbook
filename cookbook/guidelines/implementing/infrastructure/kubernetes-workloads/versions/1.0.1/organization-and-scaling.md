
- **SHOULD** isolate workloads with namespaces and apply the recommended `app.kubernetes.io/*` labels for selection and tooling.
- **SHOULD** scale stateless workloads with a `HorizontalPodAutoscaler` driven by CPU, memory, or custom metrics; pair it with cluster autoscaling so capacity follows demand.

> Security and isolation guidance here is engineering practice, not a compliance certification; validate against your own regulatory and threat-model requirements.

