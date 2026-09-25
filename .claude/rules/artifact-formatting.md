# Artifact Formatting

This rule applies when creating or modifying any cookbook artifact (principle, guideline, ingredient, or recipe). Every artifact MUST conform to the structural formatting checks defined for its type.

---

## Formatting Specs

Each artifact type has a compliance file that defines its required structure:

| Type | Compliance File | Checks |
|------|----------------|--------|
| Principle | `cookbook/compliance/artifact-formatting/principle-formatting.md` | 7 |
| Guideline | `cookbook/compliance/artifact-formatting/guideline-formatting.md` | 8 |
| Ingredient | `cookbook/compliance/artifact-formatting/ingredient-formatting.md` | 17 |
| Recipe | `cookbook/compliance/artifact-formatting/recipe-formatting.md` | 15 |
| Cookbook | `cookbook/compliance/artifact-formatting/cookbook-formatting.md` | 13 |

Before writing or modifying an artifact, read the compliance file for that artifact's type. Follow every MUST check. Address every SHOULD check unless there is a documented reason to skip it.

---

## Applying the Rule

1. **Identify the artifact type** from the `type` field in the frontmatter.
2. **Read the corresponding compliance file** listed above.
3. **Follow the required section order** — ingredients and recipes have strict section orders defined in their formatting files. Principles and guidelines have fewer constraints but MUST include all MUST-level sections.
4. **Use RFC 2119 keywords** for requirements — MUST, MUST NOT, SHOULD, SHOULD NOT, MAY.
5. **Name requirements in kebab-case** — `**must-do-something**: Component MUST ...`, not REQ-001.

---

## MUST NOT

- Do not create an artifact without reading its type's compliance file first.
- Do not omit MUST-level sections. If a section does not apply (e.g., `## Appearance` for an infrastructure recipe), include it with a brief explanation of why it is omitted.
- Do not invent new section names for recipes. Use the section order defined in `recipe-formatting.md`.
- Do not use numbered requirement IDs (REQ-001). Use descriptive kebab-case names.
