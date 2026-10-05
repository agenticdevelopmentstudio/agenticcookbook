---
id: 00000000-0000-0000-0000-000000000001
title: "Agentic Developer Cookbook"
domain: agenticdevelopercookbook://index
type: reference
version: 4.3.0
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "A library of principles, guidelines, ingredients, recipes, and workflows for building software with AI-assisted development."
platforms: []
tags: []
depends-on: []
related: []
references:
  - https://github.com/agenticdevelopercookbook/cookbook
---

# Agentic Developer Cookbook

A library of principles, guidelines, ingredients, recipes, and workflows for building software with AI-assisted development.

## Introduction

*Start here.* How to use this book — conventions, terminology, and getting started.

| Topic | Description |
|-------|-------------|
| [Getting Started](introduction/getting-started.md) | Setup and first steps |
| [Conventions](introduction/conventions.md) | File format, naming, cross-referencing |
| [Glossary](introduction/glossary.md) | Term definitions |
| [Trigger Guide](introduction/trigger-guide.md) | Activity-based trigger system for AI agents |
| [Top 10 Guidelines](introduction/top-10-guidelines.md) | Highest-signal guidelines shortlist |

## Principles

*How to think about engineering.* Foundational ideas that guide all technical decisions.

| Principle | Summary |
|-----------|---------|
| [Simplicity](principles/simplicity.md) | No interleaving of concerns. Simple beats easy. |
| [Make It Work, Make It Right, Make It Fast](principles/make-it-work-make-it-right-make-it-fast.md) | Three sequential phases — never skip phase 2. |
| [YAGNI](principles/yagni.md) | Build for today's known requirements. |
| [Steel Thread First](principles/steel-thread-first.md) | Build the thinnest end-to-end slice through every boundary before breadth. |
| [Deliberate, Prudent Technical Debt](principles/deliberate-prudent-debt.md) | Trade rigor for speed only as a deliberate, recorded choice with a payback trigger. |
| [Fail Fast](principles/fail-fast.md) | Detect invalid state at the point of origin. |
| [Make Illegal States Unrepresentable](principles/parse-dont-validate.md) | Parse untrusted input once into a type that proves its validity. |
| [Errors as Values](principles/errors-as-values.md) | Recoverable failures are values in signatures, not hidden throws. |
| [Dependency Injection](principles/dependency-injection.md) | Receive dependencies from outside. |
| [Immutability by Default](principles/immutability-by-default.md) | Default to immutable values; mutate only when necessary. |
| [Composition over Inheritance](principles/composition-over-inheritance.md) | Compose small pieces over deep hierarchies. |
| [Separation of Concerns](principles/separation-of-concerns.md) | One reason to change per module. |
| [SRP](principles/srp.md) | A module should be answerable to one and only one actor. |
| [Connascence](principles/connascence.md) | Coupling has a rankable strength; weaken strong forms, especially as distance grows. |
| [Conway's Law](principles/conways-law.md) | Architecture mirrors the communication structure — or agent topology — that builds it. |
| [Design for Deletion](principles/design-for-deletion.md) | Build disposable software, not reusable software. |
| [DRY](principles/dry.md) | Every piece of knowledge has a single, authoritative representation. |
| [Explicit over Implicit](principles/explicit-over-implicit.md) | Visible dependencies, clear intent. |
| [Small, Reversible Decisions](principles/small-reversible-decisions.md) | Cheap to reverse? Decide fast. Expensive? Invest in understanding. |
| [Tight Feedback Loops](principles/tight-feedback-loops.md) | The speed of your feedback loop is the speed of your learning. |
| [Manage Complexity Through Boundaries](principles/manage-complexity-through-boundaries.md) | Well-defined interfaces let each side evolve independently. |
| [Principle of Least Astonishment](principles/principle-of-least-astonishment.md) | Behavior matches what the name promises. |
| [Idempotency](principles/idempotency.md) | Safe to repeat without duplicate side effects. |
| [Native Controls](principles/native-controls.md) | Prefer platform built-in frameworks. |
| [Open Source Preference](principles/open-source-preference.md) | Prefer proven libraries over custom solutions. |
| [Support Automation](principles/support-automation.md) | Expose capabilities through automation interfaces, not just interactive UI. |
| [Optimize for Change](principles/meta-principle-optimize-for-change.md) | Every principle is a strategy for making future change cheaper. |
| [Type Precedes Method](principles/type-precedes-method.md) | Classify what you're researching before deciding how. |
| [Domain-Stratified Trust](principles/domain-stratified-trust.md) | The bar scales with the cost of being wrong, by domain. |
| [Independence Before Corroboration](principles/independence-before-corroboration.md) | Many sources tracing to one origin are still one source. |
| [Provenance at Generation Time](principles/provenance-at-generation-time.md) | Capture source, quote, and date as you gather — never after. |
| [Cite the Claim, Not the Document](principles/cite-the-claim-not-the-document.md) | Claim-level citations with the supporting quote; bibliographies aren't auditable. |
| [Suppress Unsupported Confidence](principles/suppress-unsupported-confidence.md) | Confident language over thin evidence is a red flag. |
| [Frame Before You Generate](principles/frame-before-you-generate.md) | Find the real problem before generating solutions. |
| [Diverge Before You Converge](principles/diverge-before-you-converge.md) | Open the solution space wide before narrowing it. |
| [Human-First Ideation](principles/human-first-ideation.md) | The human contributes before the AI injects ideas. |
| [Defer Judgment, Go for Quantity](principles/defer-judgment-go-for-quantity.md) | Suspend evaluation during generation; volume unlocks quality. |
| [Counteract Homogenization with Diversity](principles/counteract-homogenization-with-diversity.md) | Use structural diversity to escape the AI's mean. |
| [Bridge Distant Domains](principles/bridge-distant-domains.md) | Import solution patterns from structurally similar but distant fields. |
| [Constraints as Creative Fuel](principles/constraints-as-creative-fuel.md) | Deliberate constraints break fixation and spark novel directions. |
| [Break Fixation Deliberately](principles/break-fixation-deliberately.md) | Interrupt mental lock-in with a structured break before continuing. |
| [Critique Without Killing](principles/critique-without-killing.md) | Interrogate ideas productively without verdicts. |
| [Keep the Human at the Wheel](principles/keep-the-human-at-the-wheel.md) | Selection, judgment, and direction belong to the human. |
| [Document the Process, Not a Conclusion](principles/document-the-process-not-a-conclusion.md) | Record the journey, not just the destination. |

## Guidelines

*What rules apply when building.* Organized by **use case** — the phase of work where they apply. [Trigger-based filtering](introduction/trigger-guide.md) lets AI agents load only relevant guidelines. See the [full index](guidelines/INDEX.md) for every guideline.

| Use Case | Guidelines | When to use |
|----------|-----------|-------------|
| [Planning](guidelines/planning/) | 63 | Architecture, data modeling, choosing patterns |
| [Implementing](guidelines/implementing/) | 165 | Writing new code |
| [Testing](guidelines/testing/) | 24 | Writing and structuring tests |
| [Reviewing](guidelines/reviewing/) | 48 | Checking code quality, security, accessibility |
| [Shipping](guidelines/shipping/) | 17 | Pre-commit, pre-PR, packaging |
| [Cookbook](guidelines/cookbook/) | 16 | Writing cookbook content (recipes, skills, agents) |
| [Researching](guidelines/researching/) | 5 | Gathering, verifying, and recording trustworthy research |
| [Brainstorming](guidelines/brainstorming/) | 4 | Facilitating idea generation sessions with framing-techniques, divergent-techniques, convergent-techniques, and facilitation-without-anchoring |

## Ingredients

*The building blocks.* Atomic component specs for UI components, panels, and infrastructure patterns.

| Category | Description |
|----------|-------------|
| [UI Components](ingredients/ui/components/) | Leaf building blocks — ai-chat-control, collapsible-pane-header, color-profile, empty-state, git-status-indicator, metadata-line, status-bar |
| [Panels](ingredients/ui/panels/) | Content panes — ai-settings-panel, code-editor-pane, debug-panel, file-tree-browser, inspector-panel, terminal-pane |
| [Windows](ingredients/ui/windows/) | Window bodies — project-split-layout, settings-category-browser, terminal-window-shell, workspace-browser, workspace-document |
| [Apps](ingredients/ui/apps/) | App scaffolding — xcodegen-apple-project, component-catalog |
| [App-Level](ingredients/app/) | Lifecycle and menus — startup-behavior, session-restore, child-process-cleanup, creation-menu-commands, document-creation-flow |
| [Infrastructure](ingredients/infrastructure/) | Non-visual patterns — logging, settings-keys, window-frame-persistence; directory sync — directory-tree-cache, directory-tree-scanner, filesystem-watcher, directory-watch-coordinator; package documents — package-document-type, package-document-storage, sqlite-helpers; AI processing — job-worker, llm-backend, categorize-and-tag-handler |
| [Autonomous Dev Bots](ingredients/autonomous-dev-bots/) | PR review phases — pr-review-phase, pr-scope-phase, pr-evaluate-phase, pr-fix-agent |
| [Developer Tools](ingredients/developer-tools/) | Claude Code workarounds — yolo-mode; rule optimization — rule-audit, rule-optimizer, rule-validation-report; MCP building blocks — mcp-tool |
| [Web Controls](ingredients/web/) | Web UI controls — appearance-mode-toggle |

## Recipes

*How things combine.* Compositions of configured ingredients into coherent features.

| Category | Description |
|----------|-------------|
| [Windows](recipes/ui/windows/) | Top-level layouts — project-window, workspace-window, settings-window, standalone-terminal-window |
| [Apps](recipes/ui/apps/) | Application-level UI — apple test app suite |
| [App-Level](recipes/app/) | Lifecycle, menus, commands |
| [Autonomous Dev Bots](recipes/autonomous-dev-bots/) | Long-running agent processes — pr-review-pipeline |
| [Developer Tools](recipes/developer-tools/) | Claude Code pipelines — claude-rule-optimization-pipeline; MCP — mcp-server |
| [Infrastructure](recipes/infrastructure/) | Non-visual patterns — directory-sync, package-document |

## Workflows

*How to work.* Development process recipes for AI-assisted coding sessions.

| Workflow | Description |
|----------|-------------|
| [Branching Strategy](workflows/branching-strategy.md) | Worktree + draft PR lifecycle |
| [Code Planning](workflows/code-planning.md) | Pre-implementation decision-making |
| [Code Implementation](workflows/code-implementation.md) | Disciplined phased execution |
| [Code Verification](workflows/code-verification.md) | Post-implementation validation |
| [Code Review](workflows/code-review.md) | Structured review process |

## Compliance

*What to verify.* Curated indexes of guideline-derived checks, grouped by concern.

| Category | Checks | Scope |
|----------|--------|-------|
| [Security](compliance/security.md) | 12 | Auth, storage, input, transport, logging, dependencies |
| [User Safety](compliance/user-safety.md) | 6 | Content moderation, age-gating, abuse prevention |
| [Performance](compliance/performance.md) | 8 | Render time, animation, resources, caching |
| [Best Practices](compliance/best-practices.md) | 8 | Testing, linting, error handling, code quality |
| [Access Patterns](compliance/access-patterns.md) | 8 | Client-server, offline, retry, pagination |
| [Accessibility](compliance/accessibility.md) | 8 | Screen readers, keyboard, contrast, motion |
| [Privacy & Data](compliance/privacy-and-data.md) | 8 | Collection, storage, retention, consent |
| [Platform Compliance](compliance/platform-compliance.md) | 8 | App Store, Google Play, design language |
| [Reliability](compliance/reliability.md) | 8 | Error recovery, degradation, state, idempotency |
| [Internationalization](compliance/internationalization.md) | 7 | Strings, RTL, locale formatting, Unicode |

## Reference

*Where to find more.* External best-practices links organized by platform.

| Platform | Link |
|----------|------|
| [Apple](reference/best-practices/apple.md) | HIG, Swift API Guidelines, App Store Review |
| [Android](reference/best-practices/android.md) | Material Design, Kotlin style, Play policies |
| [Web](reference/best-practices/web.md) | MDN, WCAG, web.dev |
| [Windows](reference/best-practices/windows-net.md) | .NET guidelines, WinUI, Fluent |
| [UI Design](reference/best-practices/ui-design.md) | NNGroup, Apple HIG, Material Design |
| [Networking](reference/best-practices/networking.md) | REST guidelines, RFC references |
| [Security](reference/best-practices/security.md) | OWASP, CWE, Mozilla |
| [Testing](reference/best-practices/testing.md) | Google SWE Book, Fowler, Kent Beck |
| [Cross-Platform](reference/best-practices/cross-platform.md) | Nielsen Norman, MASVS, MASTG |
| [References](reference/references.md) | Additional reference materials |
| [Example Cookbook](reference/examples/) | My Document Editor — complete cookbook example |

## Appendix

*Supplementary materials.* Contribution guides, design decisions, and research notes.

| Section | Description |
|---------|-------------|
| [Contributing](appendix/contributing/) | How to author and contribute content |
| [Decisions](appendix/decisions/) | Architecture decision records |
| [Research](appendix/research/) | Platform and tooling research notes |

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 4.3.0 | 2026-10-04 | Mike Fullerton | List the 29 ingredients extracted when recipes became ingredient compositions |
| 4.2.0 | 2026-04-21 | Mike Fullerton | Add DRY and SRP principles |
| 4.1.0 | 2026-04-09 | Mike Fullerton | Add trigger system, top-10 shortlist, AI guidelines; recategorize 20→12 |
| 4.0.0 | 2026-04-09 | Mike Fullerton | Reorganize guidelines by use case (planning, implementing, testing, reviewing, shipping, cookbook) |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
| 3.1.0 | 2026-04-05 | Mike Fullerton | Populate ingredients and recipes sections after reclassification of 18 ingredients from legacy recipes |
| 3.2.0 | 2026-04-06 | Mike Fullerton | Rename concoction to cookbook |
| 3.0.0 | 2026-04-05 | Mike Fullerton | Add ingredient/recipe/concoction hierarchy; mark existing recipes as legacy pending reclassification |
| 2.0.0 | 2026-04-02 | Mike Fullerton | Reorganize as book structure — flatten cookbook/ to top level, add introduction/ and appendix/ |
