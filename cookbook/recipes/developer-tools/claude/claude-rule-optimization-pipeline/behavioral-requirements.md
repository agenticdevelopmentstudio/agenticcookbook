
### Phase 1: Audit

- **audit-inventory-all-rules**: The pipeline MUST inventory every `.md` file in `.claude/rules/` (and `rules/` if present), recording the file path, line count, and byte size of each.
- **audit-measure-per-turn-cost**: The pipeline MUST calculate the aggregate per-turn cost: the sum of lines and bytes across all rule files that load without `globs` restrictions. Rules with `globs` frontmatter that would not match a generic file context MUST be excluded from the per-turn total.
- **audit-detect-duplication**: The pipeline MUST compare all rule files pairwise and identify paragraphs, list items, or sections that express the same constraint. A finding MUST include the overlapping text and both file locations.
- **audit-detect-ungated-rules**: The pipeline MUST flag any rule file that applies only to a specific file pattern (identifiable by content referencing specific directories or file types) but lacks `globs` frontmatter.
- **audit-detect-mandatory-reads**: The pipeline MUST identify every instruction in rule files that mandates reading external files (patterns: "read", "load", "review", "check" followed by a file path or glob). Each finding MUST record the rule file, the instruction, and the referenced file paths.

### Phase 2: Optimize

- **optimize-propose-before-apply**: The pipeline MUST present all proposed optimizations to the user and wait for explicit confirmation before modifying any files. Each proposal MUST state what will change, the expected per-turn cost reduction, and any behavioral impact.
- **optimize-consolidate-overlaps**: When audit-detect-duplication found overlapping content, the pipeline MUST propose consolidating into a single rule file or extracting shared content to a referenced file. The proposal MUST specify which file retains the content and which files get trimmed.
- **optimize-add-globs-scoping**: For each rule flagged by audit-detect-ungated-rules, the pipeline MUST propose adding `globs` frontmatter with the narrowest pattern that covers the rule's intended scope.
- **optimize-extract-to-skills**: When a rule file exceeds 200 lines or contains workflow content (multi-step procedures, checklists, evaluation criteria), the pipeline SHOULD propose extracting that content to an on-demand skill, replacing it with a one-line skill pointer in the rule.
- **optimize-deduplicate-must-nots**: The pipeline MUST scan each rule's MUST NOT section and flag items that restate constraints already expressed imperatively in the rule body. The proposal MUST list each redundant item with the body line it duplicates.
- **optimize-inline-summaries**: When audit-detect-mandatory-reads found external files with a frontmatter-to-content ratio exceeding 50%, the pipeline SHOULD propose replacing the mandatory read with an inline summary and an optional file path for reference.

### Phase 3: Validate

- **validate-behavioral-preservation**: After optimizations are applied, the pipeline MUST verify that every behavioral constraint from the original rules is present in the optimized output. The pipeline MUST enumerate each original MUST, MUST NOT, and SHOULD constraint and confirm its presence (exact or equivalent) in the optimized files.
- **validate-lint-each-rule**: The pipeline MUST run the lint-rule checklist (all C-series, B-series, R-series, and O-series checks) against each optimized rule file. Any FAIL result MUST block the pipeline from proceeding to Phase 4 until resolved.
- **validate-measure-reduction**: The pipeline MUST re-measure per-turn cost using the same method as audit-measure-per-turn-cost and calculate the percentage reduction from the audit baseline.

### Phase 4: Report

- **report-produce-artifact**: The pipeline MUST produce a report file at `.claude/rule-optimization-report.md` containing: timestamp, before metrics (from Phase 1), after metrics (from Phase 3), percentage reduction, list of changes applied, lint results per file, and any constraints that could not be optimized further.
- **report-idempotent**: Running the pipeline again on already-optimized rules MUST produce a report showing no changes needed rather than making unnecessary modifications.

### Cross-Phase

- **sequential-gating**: Phases MUST execute in order: 1 → 2 → 3 → 4. A phase MUST NOT start until the previous phase completes successfully.
- **human-gate-before-writes**: The pipeline MUST NOT modify any rule file without explicit user confirmation. Phases 1 and 4 are read-only. Phase 2 requires confirmation. Phase 3 re-validates after writes.

