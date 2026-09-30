<!-- leaf: implement-networking/timeouts · source: guidelines/implementing/networking/timeouts.md -->

**Rules** (cite as `implement-networking/timeouts#<slug>`):

- `request-set-both-connection-read` MUST — Every request MUST set both connection and read timeouts. Infinite timeouts MUST NOT be used.

# Timeouts

Every request MUST set both connection and read timeouts. Infinite timeouts MUST NOT be used.

| Timeout | Purpose | Default |
|---------|---------|---------|
| Connection | TCP + TLS handshake | 10 seconds |
| Read / Response | Time to first byte | 30 seconds |
| Total / Request | Entire lifecycle including retries | 60-120 seconds |

For long-running operations, use **202 Accepted** + polling pattern instead of extending
timeouts.
