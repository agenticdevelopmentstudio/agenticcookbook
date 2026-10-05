
This is a CLI pipeline with no visual UI, so the layout is the order of the phases and which of them may write.

```
 ┌───────────────┐   findings   ┌────────────────┐  confirmed edits  ┌───────────────────────────┐
 │ 1 Rule audit  │ ───────────▶ │ 2 Rule         │ ────────────────▶ │ 3 Validate (rule          │
 │ read-only     │              │ optimizer      │   (human gate)    │   validation and report)  │
 └───────────────┘              │ proposes, then │                   │ re-measure + lint         │
                                │ writes if OK'd │                   └─────────────┬─────────────┘
                                └────────────────┘                                 │ pass
                                                                      ┌────────────▼────────────┐
                                                                      │ 4 Report (read-only)    │
                                                                      │ .claude/rule-           │
                                                                      │   optimization-report.md│
                                                                      └─────────────────────────┘
```

