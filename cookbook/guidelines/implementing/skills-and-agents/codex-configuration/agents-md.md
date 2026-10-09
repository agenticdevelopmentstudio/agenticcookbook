
- Global instructions come from the Codex home: Codex reads `AGENTS.override.md` if it exists, otherwise `AGENTS.md`, and uses the first non-empty file only.
- Project instructions are collected by walking from the project root down to the working directory. In each directory Codex checks `AGENTS.override.md`, then `AGENTS.md`, then any names listed in `project_doc_fallback_filenames`, and takes at most one file per directory. The files are concatenated from the root down, so a file closer to the working directory overrides a farther one.
- The combined size is limited by `project_doc_max_bytes`, which defaults to 32 KiB. Keep each file short and move reference material into skills, which load on demand.
- Write `AGENTS.md` as instructions for any agent, not for one tool, so other tools can read the same file.

