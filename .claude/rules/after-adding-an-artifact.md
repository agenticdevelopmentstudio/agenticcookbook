# After Adding an Artifact

This rule applies after any cookbook artifact (principle, guideline, ingredient, or recipe) is added, modified, or removed. Every post-change step MUST be completed before the work is considered done.

---

## Step 1: Lint and Approve

Run `/approve-artifact` on the new or modified artifact. The artifact MUST pass approval before proceeding.

If the artifact fails approval:
1. Fix the reported issues.
2. Re-run `/approve-artifact`.
3. Do not proceed to Step 2 until approval passes.

If the artifact was removed, skip this step.

---

## Step 2: Referential Integrity

Check and update all files that reference or are referenced by the changed artifact.

### Index files

- `cookbook/index.md` MUST list every artifact. If an artifact was added, add its entry in the correct section. If removed, remove the entry.
- Section-level index files (e.g., `cookbook/guidelines/testing/INDEX.md`) MUST be updated if they exist.

### Cross-references in other artifacts

- Search all `.md` files for `agenticdevelopercookbook://` URIs that reference the changed artifact's domain.
- If the artifact was renamed or moved, update every reference to the new domain.
- If the artifact was removed, remove or replace every reference to it.
- Check `depends-on` and `related` fields in other artifacts' frontmatter for stale references.

### Documentation files

- `README.md` — update artifact counts if the total changed (e.g., "18 principles" becomes "19 principles"). Update category tables if a new category was added.
- `.claude/CLAUDE.md` — update the Cookbook Artifacts table counts if totals changed.
- `cookbook/introduction/glossary.md` — update if the artifact introduces or changes a defined term.

---

## Verification

Before marking the work complete, confirm:

- [ ] `/approve-artifact` passed on every new or modified artifact
- [ ] Every new or modified artifact has a source folder its `.md` matches (`cookr compile --check` passes)
- [ ] `cookbook/index.md` reflects the current set of artifacts — no missing entries, no dead links
- [ ] No broken `agenticdevelopercookbook://` cross-references exist in any `.md` file
- [ ] README.md and CLAUDE.md artifact counts are accurate

---

## MUST NOT

- Do not skip `/approve-artifact`. Every new or modified artifact MUST be approved.
- Do not leave `cookbook/index.md` out of sync. Every artifact addition or removal updates the index.
- Do not ignore cross-references. A renamed or removed artifact with dangling references is a broken cookbook.
- Do not update artifact counts in README.md or CLAUDE.md without verifying the actual count.
