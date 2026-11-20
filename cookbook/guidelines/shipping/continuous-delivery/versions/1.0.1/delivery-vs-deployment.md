
These are distinct practices; do not conflate them.

| Practice | What it means | Who decides to release |
|----------|---------------|------------------------|
| Continuous **delivery** | Every change that passes the pipeline is *deployable* to production at any time. | A human / business decision (a button press). |
| Continuous **deployment** | Every change that passes the pipeline is *automatically deployed* to production. | The pipeline, with no manual gate. |

- The pipeline MUST keep main releasable. Whether releases auto-ship is a separate choice.
- A change MUST NOT merge to main if it leaves main un-releasable.

