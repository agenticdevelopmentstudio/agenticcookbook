
- **must-set-connection-and-read-timeouts**: Every request MUST set both connection and read timeouts.
- **must-not-use-infinite-timeouts**: Infinite timeouts MUST NOT be used.
- **should-use-the-default-timeouts**: Timeouts SHOULD use the defaults in the timeout table: connection (TCP + TLS handshake) 10 seconds, read / response (time to first byte) 30 seconds, total / request (entire lifecycle including retries) 60-120 seconds.
- **should-use-202-for-long-running-operations**: For long-running operations, services SHOULD use **202 Accepted** + polling pattern instead of extending timeouts.
