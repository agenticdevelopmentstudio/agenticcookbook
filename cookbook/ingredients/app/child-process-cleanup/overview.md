
Terminates every child process the app spawned (terminal sessions, background tasks, language servers, build processes) when the app quits, so no orphaned process survives it. Child process handles are tracked for the life of the app; on termination the app signals its process group, waits up to a timeout, and escalates to a forced kill for survivors.

### Terminology

| Term | Definition |
|------|-----------|
| Child process | Any process spawned by the app (terminal sessions, background tasks, language servers) that must be cleaned up on quit |
| Orphaned process | A child process that continues running after the parent app has terminated |
| Process group | A set of processes sharing a PGID, allowing bulk signal delivery |

