
| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `supportedJobTypes` | string[] | (required) | Job types the node claims; fixed for the life of the process |
| `batchSize` | integer | 1 | Maximum jobs requested per claim |
| `pollIntervalSeconds` | number | 5 | Wait between claims that return zero jobs |
| `handlerTimeoutSeconds` | number | (none) | Per-handler timeout; unset means no timeout |
| `concurrency` | integer | 1 | Maximum jobs processed at once from a batch |

