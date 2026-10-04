
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

