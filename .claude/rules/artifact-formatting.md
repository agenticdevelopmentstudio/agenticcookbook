# Artifact Formatting

This rule applies when creating or modifying any cookbook artifact (principle, guideline, ingredient, or recipe). Every artifact MUST conform to the structural formatting checks defined for its type.

---

## Formatting Specs

Each artifact type has a compliance file that defines its required structure:

| Type | Compliance File | Checks |
|------|----------------|--------|
| Principle | `tbd/compliance/artifact-formatting/principle-formatting.md` | 7 |
| Guideline | `tbd/compliance/artifact-formatting/guideline-formatting.md` | 13 |
| Ingredient | `tbd/compliance/artifact-formatting/ingredient-formatting.md` | 17 |
| Recipe | `tbd/compliance/artifact-formatting/recipe-formatting.md` | 15 |
| Cookbook | `tbd/compliance/artifact-formatting/cookbook-formatting.md` | 13 |

Before writing or modifying an artifact, read the compliance file for that artifact's type. Follow every MUST check. Address every SHOULD check unless there is a documented reason to skip it.

---

## Applying the Rule

1. **Identify the artifact type** from the `type` field in the frontmatter.
2. **Read the corresponding compliance file** listed above.
3. **Follow the required section order** — ingredients and recipes have strict section orders defined in their formatting files. Principles and guidelines have fewer constraints but MUST include all MUST-level sections.
4. **Use RFC 2119 keywords** for requirements — MUST, MUST NOT, SHOULD, SHOULD NOT, MAY.
5. **Name requirements in kebab-case** — `**must-do-something**: Component MUST ...`, not REQ-001.
6. **Edit the source folder** — the folder (`<name>/artifact.json` plus one `.md` per section) is
   the only committed form. Edit its section files directly, or compile a doc with `cookr compile`,
   edit it, fold it back with `cookr convert --update <doc>`, and delete the doc. A new artifact gets
   its folder from `cookr convert <path>` (then delete `<path>`), and `cookr update` adds it to
   `cookbook/index.json`. Record a version change with `cookr bump <folder> --summary "..."`.
7. **Link by UUID** — `depends-on`, `related` and `ingredients` hold UUIDs (`<cookbook-uuid>/<uuid>`
   for another cookbook's artifact); in body text write `[<rdid>](cookbook:<uuid>)`. There is no
   `domain` field.
8. **Write to the standard** (`guide/introduction/conventions.md`, *The Standard*) — a guideline or
   principle gives every part a role (`cookr roles set`), each rule is a named bullet of a `rules`
   part, each named rule cites the claims of the topic's `research/` it stands on, and the topic has
   one folder. A topic that already exists elsewhere is extended there, never written again; an
   existing copy is folded into its survivor with `cookr fold <copy> --into <topic>`. Write
   researched topics with `/grow-cookbook`.

---

## MUST NOT

- Do not create an artifact without reading its type's compliance file first.
- Do not omit MUST-level sections. If a section does not apply (e.g., `## Appearance` for an infrastructure recipe), include it with a brief explanation of why it is omitted.
- Do not invent new section names for recipes. Use the section order defined in `recipe-formatting.md`.
- Do not use numbered requirement IDs (REQ-001). Use descriptive kebab-case names.
- Do not write a second folder for a topic the cookbook already has, under any use case.
- Do not add a topic to `cookbook/research-exempt.json`. It lists only topics written before
  research-first; a topic leaves it in the commit that adds its research.
