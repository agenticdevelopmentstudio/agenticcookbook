
- **audit-inventory-all-rules**: The pipeline MUST inventory every `.md` file in `.claude/rules/` (and `rules/` if present), recording the file path, line count, and byte size of each.
- **audit-measure-per-turn-cost**: The pipeline MUST calculate the aggregate per-turn cost: the sum of lines and bytes across all rule files that load without `globs` restrictions. Rules with `globs` frontmatter that would not match a generic file context MUST be excluded from the per-turn total.
- **audit-detect-duplication**: The pipeline MUST compare all rule files pairwise and identify paragraphs, list items, or sections that express the same constraint. A finding MUST include the overlapping text and both file locations.
- **audit-detect-ungated-rules**: The pipeline MUST flag any rule file that applies only to a specific file pattern (identifiable by content referencing specific directories or file types) but lacks `globs` frontmatter.
- **audit-detect-mandatory-reads**: The pipeline MUST identify every instruction in rule files that mandates reading external files (patterns: "read", "load", "review", "check" followed by a file path or glob). Each finding MUST record the rule file, the instruction, and the referenced file paths.

