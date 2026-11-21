# agent-run: principle-formatting research (fallback Opus agent)

The research team could not run (`team_probe.py researchteam`: "missing distributions: PyYAML, aiohttp, mcp, websockets"), so one fresh Opus Agent ran the `research` prompt as `write_brief.py prompt research` printed it. Its reply, verbatim:

---

I wrote both research files, but the validate line you gave never printed `Research passed.` It stops before reading the research, because the new topic folder has no `artifact.json`:

```
✗ .../cookbook/authoring/principle-formatting: not an artifact source folder (no artifact.json)
```

You told me to write exactly two files, so I did not create `artifact.json`. Instead I ran the same research checks from cookr (its `_findings` function) on the two files in memory, with an empty stand-in artifact. They returned no findings. The validate line should print `Research passed.` once the topic's folder has its `artifact.json`. I have not committed the files.

**Files**
- /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/principle-formatting/research/research.json
- /Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-2/external/teams/external/agenticcookbook/cookbook/guidelines/cookbook/authoring/principle-formatting/research/research.md

**Claims per question** (75 in total, 7 of them prior claims; every claim appears in research.md and in at least one verdict)
- best-practices: 12
- known-solutions: 19
- platform-guidelines: 29
- experts-view: 15

**Verdicts**

The 19 brief rules:
- pf-frontmatter-complete, supported: pep-preamble-required, skill-frontmatter-required, json-schema-required, astro-frontmatter-schema
- pf-type-field, supported: json-schema-const, pep-preamble-required, astro-frontmatter-schema
- pf-title-heading, unsupported: pf-title-heading-prior, md041-frontmatter-title-satisfies, md025-frontmatter-title-counts, markdownlint-custom-rules-frontmatter
- pf-statement, unsupported: pf-statement-prior, lead-with-main-point, ms-lead-with-most-important, google-opening-sentence, pep-abstract-short, google-paragraph-length, vale-metric-formulas
- pf-actionable-guidance, supported: right-altitude, claude-md-specific-concise, claude-md-headers-and-bullets, cursor-focused-actionable, ms-lists-short, nygard-bullets-not-fragments, diataxis-keep-bounded
- pf-change-history, unsupported: pf-change-history-prior, changelog-entry-per-version, changelog-dated, md043-required-headings
- pf-brevity, unsupported: pf-brevity-prior, claude-md-200-lines, skill-body-500-lines, agentskills-progressive-disclosure, cursor-rules-500-lines, codex-32kib-combined, copilot-two-pages, ifscale-density-degrades, chroma-context-rot, lost-in-the-middle, context-finite-resource, minimal-not-short, claude-md-line-gets-lost, ms-be-brief, adr-short-record, diataxis-keep-bounded, md013-measures-line-width
- standard-roled-parts, supported: evaluator-optimizer, skills-lighter-than-always-loaded, agentskills-progressive-disclosure
- standard-named-rules, supported: claude-md-headers-and-bullets, cursor-rules-500-lines, ms-lists-short
- standard-one-source-per-topic, supported: claude-md-conflicts, cursor-reference-not-copy, diataxis-keep-bounded
- standard-research-cited, supported: adr-motivation-lost, prompting-explain-why, diataxis-explain-why
- roles-vocabulary, unsupported: roles-vocabulary-prior
- roles-intro-history-unroled, supported: changelog-for-humans, claude-md-every-line-costs, claude-md-only-what-agent-lacks, lead-with-main-point
- roles-principle-may-be-roled, supported: evaluator-optimizer, skills-lighter-than-always-loaded, agentskills-progressive-disclosure
- roles-every-part-roled, unsupported: roles-every-part-roled-prior
- roles-four-skills, supported: evaluator-optimizer, skills-lighter-than-always-loaded
- roles-principle-skill-names, unsupported: roles-principle-skill-names-prior
- roles-rationale-references-linked, supported: agentskills-progressive-disclosure, skill-body-500-lines, skills-lighter-than-always-loaded
- roles-principle-routing, unsupported: roles-principle-routing-prior

New practices, each supported at SHOULD:
- pf-single-title, new: google-single-h1, md025-single-title, md041-title-heading
- pf-state-why, new: prompting-explain-why, diataxis-explain-why, adr-motivation-lost
- pf-only-what-the-agent-lacks, new: skill-only-new-context, claude-md-only-what-agent-lacks, cursor-use-a-linter, smallest-high-signal-set, cursor-start-simple
- pf-summary-what-and-when, new: skill-description-what-and-when, agentskills-metadata-always-loaded
- pf-history-newest-first, new: changelog-latest-first, changelog-entry-per-version, changelog-dated
- pf-format-checks-tool-enforced, new: docs-as-code, codex-lint-in-ci, cursor-use-a-linter, claude-md-hooks-for-absolutes, md043-required-headings, json-schema-required, markdownlint-custom-rules-frontmatter, vale-metric-formulas, vale-occurrence, vale-script, agentsmd-any-headings
- pf-always-loaded-budget, new: claude-md-200-lines, codex-32kib-combined, claude-md-every-line-costs, ifscale-density-degrades, agentskills-metadata-always-loaded
- pf-key-guidance-first, new: lost-in-the-middle, ifscale-earlier-instructions, ms-first-screen, google-opening-sentence

**Findings that shape the guideline**
- **Length:** no source supports the ~50-line cap. The evidence sets budgets instead: Claude Code targets under 200 lines for an always-loaded file, and a skill body should stay under 500 lines or 5000 tokens.
- **Title:** with default settings, markdownlint MD025 flags a document that has both a frontmatter title and a matching `# Title`.
- **Questions for the owner:** research.json lists five, under `open_questions`. They are which length figure to use, the approved-by and approved-date fields, keeping the exact title match, MUST or SHOULD for the statement and change-history rules, and how a principle relates to Diátaxis.

---

Orchestrator's note on steps 3–4: research.json holds 75 claims (8 of them `prior cookbook text`, not 7 as the reply says), 27 verdicts (11 supported, 8 unsupported, 8 new), no duplicate id, every claim named by a verdict and every verdict's claims defined; research.md has the four headings in order and repeats no trust score or independence value.
