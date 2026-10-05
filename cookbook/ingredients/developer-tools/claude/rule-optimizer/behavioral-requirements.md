
- **optimize-propose-before-apply**: The pipeline MUST present all proposed optimizations to the user and wait for explicit confirmation before modifying any files. Each proposal MUST state what will change, the expected per-turn cost reduction, and any behavioral impact.
- **optimize-consolidate-overlaps**: When audit-detect-duplication found overlapping content, the pipeline MUST propose consolidating into a single rule file or extracting shared content to a referenced file. The proposal MUST specify which file retains the content and which files get trimmed.
- **optimize-add-globs-scoping**: For each rule flagged by audit-detect-ungated-rules, the pipeline MUST propose adding `globs` frontmatter with the narrowest pattern that covers the rule's intended scope.
- **optimize-extract-to-skills**: When a rule file exceeds 200 lines or contains workflow content (multi-step procedures, checklists, evaluation criteria), the pipeline SHOULD propose extracting that content to an on-demand skill, replacing it with a one-line skill pointer in the rule.
- **optimize-deduplicate-must-nots**: The pipeline MUST scan each rule's MUST NOT section and flag items that restate constraints already expressed imperatively in the rule body. The proposal MUST list each redundant item with the body line it duplicates.
- **optimize-inline-summaries**: When audit-detect-mandatory-reads found external files with a frontmatter-to-content ratio exceeding 50%, the pipeline SHOULD propose replacing the mandatory read with an inline summary and an optional file path for reference.

