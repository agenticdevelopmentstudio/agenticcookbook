
- `must-set-connection-and-read-timeouts`: a request or client built without a connection timeout or without a read timeout, relying on library defaults.
- `must-not-use-infinite-timeouts`: a timeout of `None`, `0` or infinity, or a client whose default is no timeout.
- `should-use-the-default-timeouts`: a connection timeout other than 10 seconds, a read timeout other than 30 seconds, or a total timeout outside 60-120 seconds, with no stated reason.
- `should-use-202-for-long-running-operations`: a long-running operation served by raising timeouts instead of 202 Accepted and polling.
- `should-use-202-for-long-running-operations`: for long-running operations, do not extend timeouts to accommodate them — use the 202 Accepted plus polling pattern instead.
- `must-not-use-infinite-timeouts`: infinite timeouts must never be used, so flag any request configured with no timeout or with a 0/null/disabled timeout that lets it block forever.
- `should-use-202-for-long-running-operations`: For long-running operations, the answer is not to stretch these timeouts — use the 202 Accepted plus polling pattern instead of extending or removing timeouts to accommodate slow work.
