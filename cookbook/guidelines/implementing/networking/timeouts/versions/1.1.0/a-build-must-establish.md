
- `must-set-connection-and-read-timeouts`: every request path sets an explicit connection timeout and an explicit read timeout
- `must-not-use-infinite-timeouts`: no timeout anywhere is infinite
- `should-use-the-default-timeouts`: connection is 10 seconds, read 30 seconds and total (including retries) 60-120 seconds, or the code says why not
- `should-use-202-for-long-running-operations`: long-running operations return 202 Accepted and are polled, with no timeout extended to fit them, or the code says why not
