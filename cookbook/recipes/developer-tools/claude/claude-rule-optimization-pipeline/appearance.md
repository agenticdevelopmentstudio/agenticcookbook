
The pipeline's visible output is the report file at `.claude/rule-optimization-report.md`:

- **Heading structure**: H1 title, H2 per section (Timestamp, Before Metrics, After Metrics, Reduction, Changes Applied, Lint Results, Notes)
- **Metrics tables**: Markdown tables with columns: Metric | Before | After | Change
- **Changes list**: Bulleted list, one item per optimization applied, with file path and description
- **Lint results**: One H3 per rule file, followed by the lint-rule checklist results (PASS/WARN/FAIL per check)

