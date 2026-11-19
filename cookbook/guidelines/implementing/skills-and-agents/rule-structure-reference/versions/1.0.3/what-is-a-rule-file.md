
Rules are standalone markdown files containing imperative instructions for an LLM. Unlike skills (which have `SKILL.md` + directory structure) or agents (which have specialized frontmatter), rules are plain `.md` files that get loaded into context — either via CLAUDE.md references, `.claude/` drop-in, or direct inclusion.

Rules enforce behavior: "You MUST do X", "Do not skip Y", "Read Z before proceeding."

