
A tool-call eval **SHOULD** report each dimension separately so failures are diagnosable:

| Dimension | Question | Signal |
|-----------|----------|--------|
| Tool selection | Did it call the correct tool (and avoid wrong/no-op calls)? | accuracy, false-call rate |
| Argument correctness | Are argument names, types, and values right? | exact/semantic match |
| Ordering | Were dependent calls made in a valid sequence? | trajectory match |
| Stopping | Did it stop instead of looping or over-calling? | extra-call count |
| Task completion | Did the end-to-end task succeed? | pass/fail |

