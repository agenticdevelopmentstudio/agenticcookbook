<!-- leaf: recipes-developer-tools/claude-claude-rule-optimization-pipeline--edge-cases · source: recipes/developer-tools/claude/claude-rule-optimization-pipeline.md -->

# Claude Rule Optimization Pipeline

**Rules** (cite as `recipes-developer-tools/claude-claude-rule-optimization-pipeline--edge-cases#<slug>`):

- `empty-rules-directory` MUST — .claude/rules/ exists but contains no .md files. The pipeline MUST complete Phase 1 with zero metrics and skip Phases …
- `single-rule-already-optimal` MUST — One rule file under 50 lines, no duplication, has globs, clean MUST NOTs. The pipeline MUST complete all 4 phases, with …
- `non-markdown-files` MUST — .claude/rules/ may contain .json, .yaml, .sh, or other files. The pipeline MUST ignore non-.md files during inventory.
- `broken-file-references` MUST — A rule mandates reading a file that no longer exists. The audit MUST flag this as a separate finding (broken reference) …
- `overly-broad-globs` MUST — A rule has globs: (matches everything, effectively ungated). The pipeline MUST treat this the same as no globs and …
- `circular-references` MUST — Rule A says "see rule B" and rule B says "see rule A." The deduplication check MUST handle this without infinite loops.
- `custom-rule-paths` SHOULD — Some projects put rules in non-standard paths referenced from CLAUDE.md. The pipeline SHOULD accept an optional path …
- `very-large-single-rule` MUST — The pipeline MUST still complete successfully and SHOULD propose splitting into a minimal always-on section plus one or …
- `user-declines-all-optimizations` MUST — Phase 2 proposes changes, user declines everything. Pipeline MUST proceed to Phase 4 with a report documenting the …
- `sensitive-content-in-rules` MUST — The report MUST NOT include literal file content that might expose credentials or internal paths beyond what is …

## Edge Cases

- **Empty rules directory**: `.claude/rules/` exists but contains no `.md` files. The pipeline MUST complete Phase 1 with zero metrics and skip Phases 2–3, producing a Phase 4 report that says "No rules found."
- **Single rule, already optimal**: One rule file under 50 lines, no duplication, has globs, clean MUST NOTs. The pipeline MUST complete all 4 phases, with Phase 2 reporting "No optimizations proposed."
- **Non-markdown files**: `.claude/rules/` may contain `.json`, `.yaml`, `.sh`, or other files. The pipeline MUST ignore non-`.md` files during inventory.
- **Broken file references**: A rule mandates reading a file that no longer exists. The audit MUST flag this as a separate finding (broken reference) distinct from optimization concerns.
- **Overly broad globs**: A rule has `globs: **` (matches everything, effectively ungated). The pipeline MUST treat this the same as no globs and suggest narrowing.
- **Circular references**: Rule A says "see rule B" and rule B says "see rule A." The deduplication check MUST handle this without infinite loops.
- **Custom rule paths**: Some projects put rules in non-standard paths referenced from `CLAUDE.md`. The pipeline SHOULD accept an optional path argument to scan additional directories.
- **Very large single rule (500+ lines)**: The pipeline MUST still complete successfully and SHOULD propose splitting into a minimal always-on section plus one or more skills, identifying natural section boundaries.
- **User declines all optimizations**: Phase 2 proposes changes, user declines everything. Pipeline MUST proceed to Phase 4 with a report documenting the proposals and the decision to decline.
- **Sensitive content in rules**: The report MUST NOT include literal file content that might expose credentials or internal paths beyond what is necessary to describe the optimization.
