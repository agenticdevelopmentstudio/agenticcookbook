
The node is a linear pipeline arranged around one control loop: the job worker, the handler for the claimed job's type, and the LLM backend:

```
 adh backend ──claim (types, batch)──▶ ┌─────────────────────────────┐
     ▲                                  │ Job worker                   │
     │  heartbeat / complete / fail     │  poll-claim loop             │
     └───────────────────────────────── │  lease heartbeat per job     │
                                        │  dispatch table (type → fn)  │
                                        └──────────────┬──────────────┘
                                                       │ payload
                                        ┌──────────────▼──────────────┐
                                        │ Handler for the job's type   │
                                        │  categorize_and_tag          │
                                        │  jobs.step.ai ──tools──▶ /mcp│
                                        │  jobs.step.script (machine)  │
                                        └──────────────┬──────────────┘
                                                       │ schema + prompt
                                        ┌──────────────▼──────────────┐
                                        │ LLM backend (configured)     │
                                        │  HTTP API, or the claude-code│
                                        │  CLI process                 │
                                        └─────────────────────────────┘
```

`categorize_and_tag` and `jobs.step.ai` ask the LLM backend; `jobs.step.script` runs its script as a subprocess and asks no model. A `jobs.step.ai` step whose claim carries an acting token may call the hub's `/mcp` tools under that token between model turns.

This is a non-UI recipe: the arrangement is the logical dataflow above, not a visual layout.

