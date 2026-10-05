
| State | Behavior |
|-------|----------|
| Unconfigured | No backend kind is configured; startup reports a configuration error rather than defaulting silently |
| Ready | A backend kind and its endpoint or command are configured and selected |
| Inferring | A handler request is in flight to the backend |
| Output invalid | The backend responded but the output failed schema validation; the handler reports a retryable failure |

