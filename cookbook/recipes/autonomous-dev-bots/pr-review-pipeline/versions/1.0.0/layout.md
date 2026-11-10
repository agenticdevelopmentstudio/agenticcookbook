
This is a non-UI recipe: the layout is the pipeline arrangement and the identity each stage posts under.

```
 GitHub PR event ──▶ OpenClaw webhook (or cron poll fallback)
                          │ isolated session per run
                          ▼
   ┌────────────────┐  approve   ┌────────────────┐  approve   ┌────────────────┐
   │ Phase 1 Review │ ─────────▶ │ Phase 2 Scope  │ ─────────▶ │ Phase 3 Eval   │
   │ review-bot     │            │ scope-bot      │            │ eval-bot       │
   └───────┬────────┘            └───────┬────────┘            └───────┬────────┘
           │ Request Changes             │ Request Changes             │ recommendation
           ▼ (later phases skipped)      ▼                             ▼
   ┌─────────────────────────────────────────────────┐        human reviewer decides
   │ PR fix agent (fix-bot): commit or suggest        │ ── pushes → pipeline reruns from Phase 1
   └─────────────────────────────────────────────────┘
```

