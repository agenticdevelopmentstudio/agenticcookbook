
- `must-key-every-restarting-value`, `must-key-or-wrap-every-read-variable`: **Too few keys** → the effect captures stale values and silently misbehaves.
- `must-wrap-fresh-non-restarting-values`, `must-key-or-wrap-every-read-variable`: **Too many keys** → the effect cancels and restarts needlessly (dropped coroutines, re-registered observers, flicker).
