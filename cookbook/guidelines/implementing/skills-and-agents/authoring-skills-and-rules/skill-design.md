
1. **Check the inventory first** -- Read the skills table in CLAUDE.md before creating a new skill. Do not duplicate an existing skill's purpose. If the skill is not already listed, confirm the name and purpose with the user before proceeding.

2. **Version from day one** -- Every skill MUST have a `version` field in its frontmatter, support a `--version` parameter, and print its version on every invocation. Increment the version on every change following semver: patch for fixes, minor for new behavior, major for breaking changes.

3. **Session version check** -- The skill MUST read its on-disk version during startup and compare it to the version loaded into the current session. If the versions differ, warn the user that the loaded skill may be stale. Continue running -- do not block execution.

4. **Use `$ARGUMENTS`** -- Do not describe argument handling in prose. Use `$ARGUMENTS`, `$0`, `$1` for input. If the `argument-hint` frontmatter field is declared, the skill body MUST reference these variables.

5. **Use `${CLAUDE_SKILL_DIR}`** -- Reference the skill's own supporting files with `${CLAUDE_SKILL_DIR}`. Use repo-relative paths or `../agenticdevelopercookbook/` paths for cookbook content.

6. **Description under 200 characters** -- The skill description is loaded into every session's context window. Keep it short and include natural trigger keywords so the model invokes the skill when appropriate.

7. **Atomic permission prompt** -- Before any file modifications, present a single yes/no prompt listing every file to be written and every command to be run, with reasons. See `rules/permissions.md` for the full protocol.

8. **Error handling** -- Check prerequisites before starting work. If required files are missing or the environment is misconfigured, stop immediately with a useful error message. Handle invalid arguments explicitly rather than failing silently.

9. **Include a Usage section** -- Every skill MUST include at least one example invocation showing the command and what to expect from the output.

10. **`disable-model-invocation` carefully** -- Use this frontmatter flag for skills that SHOULD only be invoked explicitly by the user. Do NOT set it on skills that other skills need to call via the Skill tool.

11. **No `context: fork` on chainable skills** -- Forked skills cannot invoke other skills or write files visible to the caller. Only use `context: fork` for isolated, read-heavy tasks that return a report.

12. **Don't duplicate between body and references** -- Maintain one authoritative source. Either the skill's markdown body is authoritative and references are supporting material, or vice versa. Never have both with overlapping content that can drift out of sync.

13. **Always lint after creating or modifying** -- Run `/lint-skill <path>` after every change. Fix all FAILs before considering the skill complete. Present WARNs to the user for review.

14. **Update CLAUDE.md and README.md** -- After creating a skill, add it to the skills table in both files. A skill that is not in the inventory is invisible to other sessions.

