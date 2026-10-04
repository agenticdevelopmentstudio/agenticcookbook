
- **healthcheck**: The image SHOULD declare a `HEALTHCHECK` (or the orchestrator's liveness/readiness probe SHOULD cover it) so the runtime can detect an unhealthy container. Keep the check cheap and specific to the app's actual readiness.

