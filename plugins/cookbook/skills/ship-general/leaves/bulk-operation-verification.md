<!-- leaf: ship-general/bulk-operation-verification · source: guidelines/shipping/bulk-operation-verification.md -->

**Rules** (cite as `ship-general/bulk-operation-verification#<slug>`):

- `restructurings-bulk-updates-have-verification-pass-before` MUST — Any operation that touches more than 5 files — renames, migrations, restructurings, bulk updates — MUST have a …
- `stale-references` MUST — The entire repo MUST be grepped for old names, paths, or identifiers that should have been updated. Check source code, …
- `bulk-operation-not-marked-complete-until-verification` MUST — A bulk operation MUST NOT be marked complete until the verification pass returns zero stale references.

# Bulk operation verification

Any operation that touches more than 5 files — renames, migrations, restructurings, bulk updates — MUST have a verification pass before the task is considered complete.

## What to verify

After the bulk operation finishes:

1. **Stale references**: The entire repo MUST be grepped for old names, paths, or identifiers that should have been updated. Check source code, documentation, configuration files, indexes, skills, rules, and test fixtures.

2. **Cross-reference integrity**: Verify that every file that references a renamed/moved entity has been updated. Common miss points:
   - README and CLAUDE.md
   - Index files and tables of contents
   - Import statements and require paths
   - Skill files that reference other skills by name
   - Rule files that reference skills or other rules
   - CI/CD configuration
   - Symlinks

3. **Completeness**: Confirm the operation covered all intended files. List what was changed and compare against what should have been changed.

## When to run

- After any rename (files, directories, functions, variables across files)
- After migrating content between directories or repos
- After restructuring a directory layout
- After updating a convention across multiple files (e.g., frontmatter format)

## For cross-repo operations

Verify each repo independently. Then run a cross-repo check to confirm consistency — the same identifier should resolve correctly in every repo that references it.

## The rule

A bulk operation MUST NOT be marked complete until the verification pass returns zero stale references.
