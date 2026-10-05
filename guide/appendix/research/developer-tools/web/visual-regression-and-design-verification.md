---
id: 6445e312-9a50-44ef-809f-51e7aceb95aa
title: Visual Regression & Design Verification Research
domain: agenticdevelopercookbook://appendix/research/developer-tools/web/visual-regression-and-design-verification
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: Visual Regression & Design Verification Research
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# Visual Regression & Design Verification Research

**Date:** 2026-03-29
**Context:** The agenticdevelopercookbook documentation site needs a design-change-verification workflow loop and regression prevention. This research catalogs available plugins, tools, npm packages, and custom solutions.

---

## Already Installed — Underutilized Features

### Playwright Plugin (`playwright@claude-plugins-official`)
- **`--caps vision` flag** — enables multimodal screenshot capture where Claude can SEE the screenshots it takes. Currently not enabled — Claude captures screenshots blind.
- **`--save-trace`** — saves full Playwright traces for debugging.
- **`--save-video <size>`** — records video of browser sessions.
- **`--device "iPhone 15"`** — device emulation (143 devices available).
- **`--viewport-size "1280x720"`** — consistent screenshot dimensions.
- **`--codegen typescript`** — generates reusable Playwright test scripts from interactions.
- The MCP does NOT have built-in visual diff — it captures screenshots but comparison needs pixelmatch or external tooling.

### Figma Plugin (`figma@claude-plugins-official`, v2.0.2)
- **`figma-create-design-system-rules` skill** — analyzes codebase and generates project-specific design rules that Claude follows automatically. Covers component organization, styling, design tokens, and asset handling. Saves to CLAUDE.md. Never been run on this project.
- **`figma-implement-design` skill** — has a built-in validation checklist (Step 7) that verifies layout, typography, colors, interactive states, responsive behavior, and accessibility against Figma source.
- **`figma-code-connect-components`** — maps Figma components to code components for consistent reuse.

### Hookify Plugin (`hookify@claude-plugins-official`)
- Creates hooks from conversation patterns.
- Could create PostToolUse hooks that trigger visual checks whenever CSS/HTML/JSX files are edited.
- Includes rule engine and example hooks (e.g., `require-tests-stop` blocks stop if tests are missing).

### Semgrep Plugin (`semgrep@claude-plugins-official`)
- Can write custom rules for CSS/HTML patterns.
- Could enforce design system token usage (flag hardcoded hex colors, non-design-system class names).

### webapp-testing Skill (anthropic-agent-skills marketplace)
- Dedicated Playwright-based testing skill.
- Includes `scripts/with_server.py` for managing server lifecycle.
- Reconnaissance-then-action pattern for DOM inspection.
- Currently installed but not enabled.

---

## Plugins Available to Install

### Visual Regression

| Plugin | Source | Description |
|---|---|---|
| **visual-regression-tester** | `jeremylongshore/claude-code-plugins-plus-skills` marketplace | Wraps Percy, Chromatic, and BackstopJS workflows. MIT licensed, free. |
| **claude-code-frontend-dev** | [GitHub](https://github.com/hemangjoshi37a/claude-code-frontend-dev) | First multimodal visual testing plugin for Claude Code. Uses Claude 4.5 Sonnet vision to SEE the UI. Closed-loop: write code → test visually → AI sees results → auto-fix → repeat. Stores screenshots between runs for regression detection. |

### Accessibility

| Plugin | Source | Description |
|---|---|---|
| **AccessLint** | `accesslint/claude-marketplace` | WCAG 2.1 Level A/AA conformance checking, reviewer agent, color contrast MCP server, structured audit reports. |
| **accessibility-agents** | [GitHub](https://github.com/Community-Access/accessibility-agents) | Eleven specialist agents enforcing WCAG 2.2 AA compliance. Integrates @axe-core/cli and pa11y. |
| **claude-a11y-skill** | [GitHub](https://github.com/airowe/claude-a11y-skill) | Runs comprehensive accessibility audits using axe-core + jsx-a11y. |

### Other

| Plugin | Source | Description |
|---|---|---|
| **skill-creator** | Official marketplace | Create, test, and benchmark custom skills. Useful for building visual testing skills. |
| **commit-commands** | Official marketplace | Streamlined git workflow that could integrate pre-commit visual checks. |

---

## NPM Packages for Visual Regression

### Image Comparison Libraries

| Package | Type | Key Feature | Install |
|---|---|---|---|
| **pixelmatch** | Library | Fast pixel-level image comparison, used internally by Playwright | `npm i pixelmatch` |
| **looks-same** | Library | Perceptual comparison with anti-aliasing detection | `npm i looks-same` |
| **resemble.js** | Library | Image analysis and comparison with tolerance settings | `npm i resemblejs` |

### Frameworks

| Package | Type | Key Feature | Install |
|---|---|---|---|
| **Playwright built-in** | Framework | `toHaveScreenshot()` and `toMatchSnapshot()` assertions | Already available via `@playwright/test` |
| **BackstopJS** | Framework | Best HTML reporting, before/after scrubber, multi-viewport | `npm i backstopjs` |
| **reg-suit** | Framework | GitHub PR integration, S3 storage for baselines | `npm i reg-suit` |
| **reg-cli** | CLI | Standalone visual diff CLI, generates reports | `npm i reg-cli` |
| **jest-image-snapshot** | Jest plugin | Integrates visual snapshots into Jest test suites | `npm i jest-image-snapshot` |

### SaaS (Cloud-Based)

| Package | Type | Key Feature | Install |
|---|---|---|---|
| **Percy** | SaaS | 5,000 free screenshots/month, cross-browser, CI integration | `npm i @percy/cli` |
| **Chromatic** | SaaS | Best for Storybook, component-level testing | `npm i chromatic` |
| **Applitools Eyes** | SaaS | AI-powered visual comparison (ignores anti-aliasing, dynamic content) | `npm i @applitools/eyes-playwright` |

### Accessibility Testing

| Package | Purpose | Install |
|---|---|---|
| **@axe-core/playwright** | Accessibility testing integrated with Playwright | `npm i @axe-core/playwright` |
| **pa11y** | Automated accessibility testing | `npm i pa11y` |
| **pa11y-ci** | CI-friendly accessibility testing | `npm i pa11y-ci` |

### CSS/HTML Linting

| Package | Purpose | Install |
|---|---|---|
| **Stylelint** | CSS linting and design system enforcement | `npm i stylelint` |
| **htmlhint** | HTML linting | `npm i htmlhint` |

---

## Playwright Visual Regression Approaches

### Approach A: Built-in Visual Comparisons (Recommended Starting Point)

```typescript
// test/visual.spec.ts
import { test, expect } from '@playwright/test';

test('homepage visual regression', async ({ page }) => {
  await page.goto('http://localhost:5173');
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixelRatio: 0.01,
    threshold: 0.2,
  });
});
```

- Baselines stored in `test/visual.spec.ts-snapshots/`
- Update baselines: `npx playwright test --update-snapshots`
- Use `--shard` for parallel CI execution

### Approach B: Playwright MCP + pixelmatch (Claude-Driven Workflow)

1. Claude captures screenshot via `browser_take_screenshot` (Playwright MCP tool)
2. Custom Node.js script runs pixelmatch against stored baseline
3. Claude reads the diff image and analyzes changes using vision

### Approach C: Multi-Viewport Capture with Device Emulation

- Configure Playwright MCP with `--device "iPhone 15"` or `--viewport-size "1280x720"`
- Capture the same page at multiple breakpoints
- Compare all viewports against baselines

### Approach D: Component-Level Snapshots

- Screenshot individual components rather than full pages
- Smaller images = faster comparison, fewer false positives
- Use `page.locator('.component').screenshot()` for component isolation

---

## Custom Solutions That Could Be Built

### Hooks (via hookify or settings.json)

1. **PostToolUse CSS/HTML guard** — matches `Edit` or `Write` on `*.css`, `*.tsx`, `*.jsx`. Auto-runs Stylelint + HTMLHint after every edit.
2. **PostToolUse screenshot capture** — after any edit to a UI file, auto-captures a Playwright screenshot and presents it to Claude for visual review.
3. **PreToolUse design-token enforcer** — before allowing a CSS/style edit, checks that the proposed change uses design system tokens.
4. **Stop verification hook** — before Claude finishes a task, runs visual regression tests and accessibility checks. Blocks completion if regressions are found.

### Skills

5. **`/visual-diff`** — takes before/after screenshots, runs pixelmatch, generates diff image, Claude analyzes the result.
6. **`/screenshot-test`** — captures all key pages at desktop/tablet/mobile, compares against stored baselines.
7. **`/design-system-audit`** — scans codebase for violations: hardcoded colors, non-standard fonts, missing tokens. Combines Stylelint + semgrep + Claude analysis.
8. **`/a11y-check`** — runs axe-core against running pages via Playwright, reports WCAG violations.
9. **`/visual-qa`** — full workflow: start dev server, capture key pages, compare against Figma designs, generate pass/fail report.

### Agents

10. **Visual Regression Agent** — sub-agent for PR review pipeline. Captures screenshots of changed pages, compares against main branch baselines, posts diff report as PR comment.
11. **Design Compliance Agent** — reads design system rules, scans changed files, verifies token usage, component reuse, naming conventions.

---

## Recommended Priority Order

1. **Enable `--caps vision` on Playwright MCP** — one config change, immediate payoff. Claude can see what it's building.
2. **Add Playwright visual regression tests** — `toHaveScreenshot()` for homepage, each section index, a doc page, dark + light mode. This is the core regression prevention.
3. **Run Figma's `create-design-system-rules`** — auto-generates enforcement rules.
4. **Install AccessLint** — free, zero config, catches accessibility issues.
5. **Build PostToolUse hook** via hookify — auto-screenshot on file edit.
6. **Evaluate claude-code-frontend-dev** — multimodal closed-loop testing is exactly the design-change-verification workflow.
7. **Add Stylelint with custom rules** — enforces design token usage at CSS level.

---

## Sources

- [Playwright MCP GitHub](https://github.com/microsoft/playwright-mcp)
- [Playwright Visual Comparisons Docs](https://playwright.dev/docs/test-snapshots)
- [claude-code-frontend-dev Plugin](https://github.com/hemangjoshi37a/claude-code-frontend-dev)
- [visual-regression-tester Plugin](https://claudecodeplugins.io/plugins/visual-regression-tester/)
- [AccessLint Claude Marketplace](https://github.com/accesslint/claude-marketplace)
- [accessibility-agents](https://github.com/Community-Access/accessibility-agents)
- [claude-a11y-skill](https://github.com/airowe/claude-a11y-skill)
- [claude-code-plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills)
- [Giving Claude Code Eyes: Round-Trip Screenshot Testing](https://medium.com/@rotbart/giving-claude-code-eyes-round-trip-screenshot-testing-ce52f7dcc563)
- [Figma MCP Server Docs](https://developers.figma.com/docs/figma-mcp-server/)
- [Percy](https://percy.io/)
- [Chromatic](https://www.chromatic.com/)
- [BackstopJS](https://github.com/garris/BackstopJS)
- [Stylelint](https://stylelint.io/)
- [Pixelmatch](https://github.com/mapbox/pixelmatch)
