
### Validate

- **validate-behavioral-preservation**: After optimizations are applied, the pipeline MUST verify that every behavioral constraint from the original rules is present in the optimized output. The pipeline MUST enumerate each original MUST, MUST NOT, and SHOULD constraint and confirm its presence (exact or equivalent) in the optimized files.
- **validate-lint-each-rule**: The pipeline MUST run the lint-rule checklist (all C-series, B-series, R-series, and O-series checks) against each optimized rule file. Any FAIL result MUST block the pipeline from proceeding to Phase 4 until resolved.
- **validate-measure-reduction**: The pipeline MUST re-measure per-turn cost using the same method as audit-measure-per-turn-cost and calculate the percentage reduction from the audit baseline.

### Report

- **report-produce-artifact**: The pipeline MUST produce a report file at `.claude/rule-optimization-report.md` containing: timestamp, before metrics (from Phase 1), after metrics (from Phase 3), percentage reduction, list of changes applied, lint results per file, and any constraints that could not be optimized further.
- **report-idempotent**: Running the pipeline again on already-optimized rules MUST produce a report showing no changes needed rather than making unnecessary modifications.

