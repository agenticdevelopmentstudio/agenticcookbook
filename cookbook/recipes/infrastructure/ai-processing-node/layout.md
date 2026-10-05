
The node is a linear pipeline of three components arranged around one control loop:

```
 adh backend ──claim (types, batch)──▶ ┌─────────────────────────────┐
     ▲                                  │ Job worker                   │
     │  heartbeat / complete / fail     │  poll-claim loop             │
     └───────────────────────────────── │  lease heartbeat per job     │
                                        │  dispatch table (type → fn)  │
                                        └──────────────┬──────────────┘
                                                       │ payload
                                        ┌──────────────▼──────────────┐
                                        │ categorize_and_tag handler   │
                                        └──────────────┬──────────────┘
                                                       │ schema + prompt
                                        ┌──────────────▼──────────────┐
                                        │ LLM backend (configured)     │
                                        │  HTTP API  or  CLI process   │
                                        └─────────────────────────────┘
```

This is a non-UI recipe: the arrangement is the logical dataflow above, not a visual layout.

