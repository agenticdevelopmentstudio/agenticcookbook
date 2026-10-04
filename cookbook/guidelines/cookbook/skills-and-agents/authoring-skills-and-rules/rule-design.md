
1. **Imperative tone throughout** -- Use MUST, MUST NOT, SHOULD, MAY (RFC 2119) consistently. Rules are not advisory or suggestive -- they are directives.

2. **Explicit file paths** -- If the rule instructs the LLM to "read the principles" or "check the guidelines," list every file path it needs to read. An LLM following the rule MUST NOT have to search for referenced content.

3. **Single concern per rule** -- Each rule addresses one topic: planning, implementing, permissions, versioning, committing, etc. Do not combine unrelated concerns into a single rule file.

4. **MUST NOT section required** -- Every rule MUST include a dedicated section listing what the LLM must not do. This section captures anti-patterns, common mistakes, and behaviors that have caused problems in practice.

5. **Enforcement mechanism** -- Do not just state "do X." Include verification steps that confirm X was actually done. For example: "Before proceeding to the next step, confirm that the file was created and contains the expected content."

6. **Deterministic instructions** -- Avoid subjective language like "appropriate," "as needed," or "if it makes sense." Be specific enough that two independent sessions following the rule produce consistent, comparable results.

7. **Same-selection = repair** -- When a user re-selects the current configuration (e.g., re-runs a setup skill with the same parameters), re-apply everything from scratch. Do not skip steps with "already done" -- treat it as a repair operation.

8. **Named requirements, not numbered** -- Use descriptive kebab-case names for requirements, not sequential identifiers like REQ-001. Named requirements make cross-referencing meaningful and survive reordering.

9. **Always lint after creating or modifying** -- Run `/lint-rule <path>` after every change. Fix all FAILs before considering the rule complete. Present WARNs to the user for review.

