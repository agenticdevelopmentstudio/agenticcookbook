# Agentic Developer Cookbook

A structured cookbook of principles, guidelines, ingredients, recipes, and workflows for AI-assisted multi-platform development. All content is markdown consumed directly by AI agents (Claude Code).

## Quick Start

### 1. Clone the cookbook

```bash
cd ~/projects
git clone git@github.com:agenticdevelopercookbook/cookbook.git
```

### 2. Install in your project

From your project directory, run the onboarding wizard (requires the [dev-team plugin](https://github.com/agenticdevelopercookbook/dev-team)):

```
/install-cookbook
```

This installs `cookbook.md` into your project's `.claude/rules/`, updates your CLAUDE.md, and offers recommended plugins. Everyone gets the full cookbook — no tiers, no partial installs.

## What "Trusted" Means

Code built with the Agentic Developer Cookbook is **trusted**. That means:

- **Complete** — every state handled, every edge case addressed, every platform considered. Not just the happy path.
- **Precise** — exactly what you asked for. No scope creep, no unrequested refactoring. Design decisions surfaced and approved, not made silently.
- **Consistent** — same patterns, conventions, and style across every file, every session, every platform. Your codebase looks like one person wrote it.
- **Verified** — built, tested, linted, accessibility-audited, logging-checked. Evidence, not hope.
- **Secure by default** — input validation, secure storage, no PII in logs, TLS, consent-first. Not bolted on after a security review.
- **Accessible from day one** — screen readers, keyboard navigation, Dynamic Type, high contrast. Not a follow-up ticket that never gets done.
- **Tested alongside** — tests written with the code, not after. Every function, every edge case, every error path.
- **Predictable** — the LLM follows a known process. You can walk away and come back to work that matches what was planned. No surprises, no tangents.
- **Maintainable** — dependency injection, immutability, separation of concerns, design for deletion. Code that's easy to change and easy to remove.
- **Native** — platform controls and conventions. SwiftUI on Apple, Compose on Android, native APIs everywhere. Not cross-platform lowest-common-denominator.
- **Incremental** — small commits, each tested, each meaningful. Reviewable, revertible, bisectable.
- **Documented** — design decisions recorded, not just in someone's head.
- **Observable** — structured logging so you can see what's happening at runtime.
- **Performant** — not prematurely optimized, but not accidentally O(n²). Work → Right → Fast, with evidence.

## What's in the Cookbook

The cookbook contains four types of **cookbook artifacts** — standalone markdown files with YAML frontmatter, named requirements, and change history. Each is stored as a source folder (`<name>/artifact.json` plus one file per section), and the `<name>.md` beside it is compiled from that folder by `cookr compile`:

### Principles (33 files)

*How to think about engineering.* Foundational ideas that guide all technical decisions.

Simplicity, YAGNI, Fail Fast, Dependency Injection, Immutability, Composition over Inheritance, Separation of Concerns, SRP, Connascence, Conway's Law, Design for Deletion, DRY, Explicit over Implicit, Make Illegal States Unrepresentable, Errors as Values, Small Reversible Decisions, Tight Feedback Loops, Manage Complexity Through Boundaries, Least Astonishment, Idempotency, Native Controls, Open Source Preference, Make It Work/Right/Fast, Steel Thread First, Deliberate Prudent Technical Debt, Optimize for Change, Type Precedes Method, Domain-Stratified Trust, Independence Before Corroboration, Provenance at Generation Time, Cite the Claim Not the Document, Suppress Unsupported Confidence.

### Guidelines (258 unique, 341 with use-case duplicates)

*What rules apply when building.* Organized by **use case** — the phase of work where they apply, with [trigger-based filtering](cookbook/introduction/trigger-guide.md) for AI agents:

| Use Case | Guidelines | When to use |
|----------|-----------|-------------|
| Planning | 63 | Architecture, data modeling, choosing patterns |
| Implementing | 166 | Writing new code |
| Testing | 24 | Writing and structuring tests |
| Reviewing | 50 | Checking code quality, security, accessibility |
| Shipping | 17 | Pre-commit, pre-PR, packaging |
| Cookbook | 16 | Writing cookbook content (recipes, skills, agents) |
| Researching | 5 | Gathering, verifying, and recording trustworthy research |

Guidelines that apply to multiple use cases are duplicated so each use-case directory is self-contained.

### Ingredients (19 files)

*The building blocks.* Atomic component specs defining individual UI components, panels, or infrastructure patterns with full detail: behavioral requirements, appearance, states, accessibility, configuration options, test vectors, and platform notes. Located in `cookbook/ingredients/`.

### Recipes (12 files)

*How things combine.* Compositions of configured ingredients into coherent features. Define how ingredients wire together: integration requirements, layout, shared state, and integration test vectors. Located in `cookbook/recipes/`.

### Compliance (10 categories, 81 checks)

*What to verify.* Curated indexes of guideline-derived checks grouped by concern: Security, User Safety, Performance, Best Practices, Access Patterns, Accessibility, Privacy & Data, Platform Compliance, Reliability, Internationalization.

### Workflows (6 files)

*How to work.* Branching, planning, implementation, verification, review.

## Cookbooks

A **cookbook** (`cookbook.json`) is a self-contained, platform-agnostic project definition. It defines *what* an app is — its structure, resources, and context — as a hierarchical manifest. Generation tools produce native, best-of-class code for any target platform (Swift/SwiftUI, Kotlin, C#/WinUI, etc.).

The manifest is the **single source of truth**. Ingredients and recipes are forked from this repo (the top-level cookbook), customized for the cookbook, and can be contributed back upstream. Resources (localization, icons, app config) are defined in platform-neutral JSON that generates to native formats per platform.

```
my-app-cookbook/
├── cookbook.json                # the manifest — defines everything
├── app/
│   ├── app.md                  # spec: app entry point
│   └── document-window/
│       ├── document-window.md  # spec: main window
│       ├── toolbar/
│       │   └── toolbar.md      # spec: formatting toolbar
│       └── editor/
│           └── editor.md       # spec: rich text editor
├── resources/
│   └── app-config.json         # generates to Info.plist, AndroidManifest, etc.
└── context/
    ├── decisions/              # architectural decisions
    └── research/               # design research and evaluations
```

See `cookbook/reference/cookbook.schema.json` for the JSON Schema. A complete example lives at `cookbook/reference/examples/my-document-editor-cookbook/`.

## Sibling Projects

### dev-team

Multi-agent development system, distributed as a Claude Code plugin. Orchestrates teams of specialist agents (13 domain experts + 6 platform experts) for product discovery, code generation, and linting.

All user-facing cookbook skills are provided by dev-team:

| Skill | Purpose |
|-------|---------|
| `/install-cookbook` | Onboarding — set up CLAUDE.md and install rules |
| `/configure-cookbook` | Manage preferences (recipe prompts, contribution prompts, optional rules) |
| `/plan-cookbook-recipe` | Interactive recipe design |
| `/contribute-to-cookbook` | Create a PR to the cookbook |
| `/validate-cookbook` | Validate cookbook integrity — frontmatter, references, indexes, placement |
| `/cookbook-help` | Interactive guide — setup status, content overview, troubleshooting |
| `/dev-team lint` | Lint artifacts against cookbook standards |

Repo: [agenticdevelopercookbook/dev-team](https://github.com/agenticdevelopercookbook/dev-team)

### agenticcookbookweb (moved to the adh monorepo)

The cookbook's public-facing website (React 19, TypeScript, Tailwind CSS 4) and the `update-website` sync skill have **moved into the `adh` monorepo** at `adh/websites/cookbook/`. The standalone `agenticcookbookweb` repo is deprecated, and this repo no longer ships an `update-website` skill or an automatic website-sync step.

## Repository Structure

```
cookbook/                # cookbook content root
  introduction/          # getting started, conventions, glossary
  principles/            # 33 engineering principles
  guidelines/            # 258 use-case-organized guidelines
  ingredients/           # atomic component specs (building blocks)
  recipes/               # compositions of ingredients into features
  compliance/            # 10 compliance categories (81 checks)
  workflows/             # 6 workflow specs (plan, implement, verify, review)
  reference/             # external best-practices links, schemas, examples
  appendix/              # research materials
  index.md               # table of contents
README.md                # this file
```

## Contributing

To contribute recipes, use `/contribute-to-cookbook` (via the [dev-team plugin](https://github.com/agenticdevelopercookbook/dev-team)) — it handles both admin (push access) and external (fork-based) workflows automatically.

## License

MIT
