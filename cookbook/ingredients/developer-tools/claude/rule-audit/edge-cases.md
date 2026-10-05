
- **Empty rules directory**: `.claude/rules/` exists but contains no `.md` files. The audit MUST complete with zero metrics so the pipeline can report "No rules found."
- **Non-markdown files**: `.claude/rules/` may contain `.json`, `.yaml`, `.sh`, or other files. The audit MUST ignore non-`.md` files during inventory.
- **Broken file references**: A rule mandates reading a file that no longer exists. The audit MUST flag this as a separate finding (broken reference) distinct from optimization concerns.
- **Overly broad globs**: A rule has `globs: **` (matches everything, effectively ungated). The audit MUST treat this the same as no globs.
- **Circular references**: Rule A says "see rule B" and rule B says "see rule A." Duplication detection MUST handle this without infinite loops.
- **Custom rule paths**: Some projects put rules in non-standard paths referenced from `CLAUDE.md`. The audit SHOULD accept an optional path argument to scan additional directories.
- **Very large single rule (500+ lines)**: The audit MUST still complete successfully.

