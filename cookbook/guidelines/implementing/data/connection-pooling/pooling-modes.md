
| Mode | Connection held for | Use when | Cost |
|------|--------------------|----------|------|
| Session | Whole client session | Need full session features | Lowest multiplexing; one server conn per active client |
| Transaction | One transaction | High fan-out, short transactions | Best multiplexing; breaks session-scoped state |
| Statement | One statement (autocommit only) | Extreme fan-out, no multi-statement txns | Most aggressive; disallows multi-statement transactions |
