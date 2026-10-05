
| State | Behavior |
|-------|----------|
| Idle | A claim returned zero jobs; the node waits the poll interval and polls again |
| Claiming | A batch claim request is in flight to the backend |
| Processing | A job is claimed, its handler is running, and its heartbeat is active |
| Reporting | The handler finished; the node is calling complete or fail and the heartbeat has stopped |
| Lease lost | A heartbeat indicated the lease is invalid; work on the job is cancelled and nothing is reported |

