---
id: 26092dc2-6338-4ab5-9bc4-2e22b8f31a00
title: Web Frontend Frameworks & Linters
domain: agenticdevelopercookbook://appendix/research/developer-tools/web/frontend-frameworks-and-linters
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: Web Frontend Frameworks & Linters
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# Web Frontend Frameworks & Linters

**Date:** 2026-03-29
**Context:** Frontend development tools that integrate with Claude Code for the plan/implement/verify loop. Focused on tools that are actively maintained (2025-2026), work well in a CLI/headless context, and can be invoked from Claude Code via MCP servers, hooks, or direct shell-out.

---

## Frameworks & Scaffolding (plan/implement)

### Vite + React

- **Link:** https://vite.dev
- **What it does:** Framework-agnostic build tool and dev server. Scaffolds React/Vue/Svelte/Lit projects via `create-vite`. Supports React, React + SWC, and TypeScript variants out of the box.
- **Loop phase:** plan, implement
- **Install:** `npm create vite@latest my-app -- --template react-ts`
- **Claude Code integration:** CLI shell-out. The `--template` and project name flags work non-interactively, so Claude can scaffold without prompts. Dev server at `localhost:5173` with HMR.
- **Notes:** Vite 8 is the current stable release. Vite+ (public preview early 2026) adds `vite new` for monorepo scaffolding, `vite test` for Vitest integration, and unified linting/formatting commands. The `--no-interactive` flag enables fully headless scaffolding. Vite is the recommended default for new React projects that don't need SSR.

### Next.js (create-next-app)

- **Link:** https://nextjs.org
- **What it does:** Full-stack React framework with SSR, SSG, API routes, and App Router. `create-next-app` scaffolds projects with TypeScript, ESLint, and Tailwind options.
- **Loop phase:** plan, implement
- **Install:** `npx create-next-app@latest my-app --typescript --tailwind --eslint --app --src-dir --no-import-alias`
- **Claude Code integration:** CLI shell-out. All options can be passed as flags for non-interactive scaffolding. Recent versions include agent-ready scaffolding capabilities.
- **Notes:** Next.js 16 (October 2025) made Turbopack the default bundler. Caching defaults changed in v15 (fetch no longer cached by default). The `next` CLI provides `dev`, `build`, `start`, `lint`, and `info` subcommands, all headless-friendly.

### SvelteKit

- **Link:** https://svelte.dev
- **What it does:** Full-stack Svelte framework with SSR, file-based routing, and form actions. Ships 50-70% less JavaScript than React-based frameworks.
- **Loop phase:** plan, implement
- **Install:** `npx sv create my-app`
- **Claude Code integration:** CLI shell-out. The `sv` CLI supports non-interactive project creation. Svelte 5's runes system and compiled output produce minimal bundles.
- **Notes:** Younger ecosystem than React/Vue, fewer ready-made modules. Progressive enhancement works by default. Strong Lighthouse scores. Good choice when bundle size is a primary concern.

### Astro

- **Link:** https://astro.build
- **What it does:** Content-focused framework with zero-JS-by-default architecture. Supports React, Vue, Svelte, and Solid components via islands architecture.
- **Loop phase:** plan, implement
- **Install:** `npm create astro@latest`
- **Claude Code integration:** CLI shell-out. The `create astro` CLI supports `--template`, `--yes` (accept defaults), and `--no-install` flags for headless usage. Cloudflare acquired Astro in January 2026.
- **Notes:** Best for content-heavy sites, documentation, and marketing pages. Often 2x faster than SPA frameworks for static content. The island architecture means Claude only needs to reason about interactive components, not the full page.

### Nuxt (Vue)

- **Link:** https://nuxt.com
- **What it does:** Full-stack Vue framework with SSR, SSG, ISR, file-based routing, and the Nitro server engine. Rich module ecosystem.
- **Loop phase:** plan, implement
- **Install:** `npx nuxi init my-app`
- **Claude Code integration:** CLI shell-out. The `nuxi` CLI supports non-interactive initialization. Module system provides ready-made solutions for auth, CMS, analytics, etc.
- **Notes:** Most mature Vue meta-framework. The module ecosystem is significantly richer than SvelteKit's. Good for teams already invested in Vue.

### React Router v7 (formerly Remix)

- **Link:** https://reactrouter.com
- **What it does:** Full-stack React framework that merged Remix upstream into React Router. Provides SSR, code splitting, file-based routing, and form handling in "framework mode."
- **Loop phase:** plan, implement
- **Install:** `npx create-react-router@latest my-app`
- **Claude Code integration:** CLI shell-out. Templates available for various deployment targets (Docker, Cloudflare Workers). Non-breaking upgrade from both React Router v6 and Remix v2.
- **Notes:** Good for teams already using React Router. Framework mode adds Remix-style server rendering and data loading. Library mode available for client-only apps.

### Angular CLI

- **Link:** https://angular.dev
- **What it does:** Full-featured framework with CLI that handles scaffolding, code generation, building, testing, and deployment. Angular 21 is the current stable release.
- **Loop phase:** plan, implement
- **Install:** `npx @angular/cli new my-app --style=scss --routing --strict`
- **Claude Code integration:** CLI shell-out. `ng generate` commands are fully non-interactive and produce consistent boilerplate. `ng g component`, `ng g service`, etc. work well for iterative AI-driven development.
- **Notes:** The CLI now defaults to Vitest for unit testing (replacing Karma). GenAI Scaffolding utilities for AI-powered Angular apps introduced in v21. Most opinionated framework of the group, which can be an advantage for Claude since there's one right way to do things.

---

## Linters & Formatters (implement/verify)

### ESLint

- **Link:** https://eslint.org
- **What it does:** The standard JavaScript/TypeScript linter. Flat config is the default since v9. Now supports CSS and HTML linting natively (February 2025). Multithreaded linting in v10.
- **Loop phase:** implement, verify
- **Install:** `npm install -D eslint @eslint/js`
- **Claude Code integration:** CLI shell-out (`npx eslint . --fix`). Zero-config possible with flat config. Output is structured and parseable.
- **Notes:** The ecosystem is massive but fragmenting. Legacy configs (airbnb, standard) need `FlatCompat` wrapper for flat config migration. ESLint v10.0.0-rc.0 is in release candidate stage. For new projects, prefer `@eslint/js` recommended config as the starting point rather than third-party configs.

### Biome

- **Link:** https://biomejs.dev
- **What it does:** Rust-based all-in-one linter and formatter (97% Prettier-compatible). Single binary, zero dependencies. 423+ lint rules as of v2.3. Replaces ESLint + Prettier with one tool and one config file.
- **Loop phase:** implement, verify
- **Install:** `npm install -D @biomejs/biome && npx biome init`
- **Claude Code integration:** CLI shell-out (`npx biome check --write .`). Single command for lint + format. 10-25x faster than ESLint + Prettier. JSON config is straightforward for Claude to read and modify.
- **Notes:** Biome 2.0 (March 2025) introduced plugins and type-aware linting. Ecosystem is younger than ESLint (not all ESLint plugins have equivalents). Best for new projects or teams willing to consolidate tooling. The speed advantage makes it ideal for Claude Code hooks that run on every file save.

### Oxlint

- **Link:** https://oxc.rs
- **What it does:** Rust-based linter with 650+ rules, 50-100x faster than ESLint. Zero-config by default with sensible rule presets for React, Vue, Svelte, and Astro.
- **Loop phase:** implement, verify
- **Install:** `npm install -D oxlint`
- **Claude Code integration:** CLI shell-out (`npx oxlint .`). Runs without config files by default. JS plugin support reached alpha in March 2026, with 80% of ESLint users able to switch as a drop-in replacement.
- **Notes:** From the VoidZero team (same as Vite). Best positioned as a "companion linter" that runs alongside ESLint for speed, or as a full replacement once plugin support stabilizes. The zero-config default is excellent for Claude since it just works out of the box.

### Prettier

- **Link:** https://prettier.io
- **What it does:** Opinionated code formatter for JS/TS/CSS/HTML/JSON/YAML/Markdown. v3 is the current stable release.
- **Loop phase:** implement
- **Install:** `npm install -D prettier`
- **Claude Code integration:** CLI shell-out (`npx prettier --write .`). The `--check` flag for verification without writing. Intentionally has few options, reducing config complexity.
- **Notes:** Still the most widely used formatter. No global config by design (reproducible per-project). Works alongside ESLint via `eslint-config-prettier` (disables conflicting rules). If adopting Biome, Prettier becomes redundant.

---

## TypeScript Tooling (implement/verify)

### TypeScript Compiler (tsc)

- **Link:** https://www.typescriptlang.org
- **What it does:** Type checks TypeScript code. `tsc --noEmit` validates types without producing output, making it ideal as a verification step.
- **Loop phase:** implement, verify
- **Install:** `npm install -D typescript`
- **Claude Code integration:** CLI shell-out (`npx tsc --noEmit`). Exit code 0/1 is clean for hook-based verification. Pair with `--pretty` for readable error output.
- **Notes:** Enable `strict: true` in tsconfig.json for maximum type safety (enables noImplicitAny, strictNullChecks, strictFunctionTypes, etc.). Claude should always run `tsc --noEmit` after TypeScript changes as a verify step.

### typescript-eslint

- **Link:** https://typescript-eslint.io
- **What it does:** Enables ESLint to lint TypeScript with type information. Provides `strict-type-checked` and `stylistic-type-checked` shared configs.
- **Loop phase:** implement, verify
- **Install:** `npm install -D @typescript-eslint/parser @typescript-eslint/eslint-plugin`
- **Claude Code integration:** CLI shell-out (runs as part of standard ESLint invocation). The `parserOptions.projectService: true` setting automatically resolves type info per file.
- **Notes:** The `strict-type-checked` config catches bugs that plain ESLint or tsc alone miss (e.g., floating promises, unsafe member access). Adds ~2-5x overhead vs non-typed linting due to type resolution. Both ESLint and tsc should be used together for maximum coverage.

### Strict tsconfig Recommendations

- **What it does:** Configuration presets that maximize TypeScript strictness beyond the default `strict` flag.
- **Loop phase:** implement
- **Key settings beyond `strict: true`:**
  - `noUncheckedIndexedAccess: true` -- catches undefined array/object access
  - `exactOptionalPropertyTypes: true` -- distinguishes `undefined` from missing
  - `noPropertyAccessFromIndexSignature: true` -- forces bracket notation for dynamic keys
  - `verbatimModuleSyntax: true` -- enforces explicit type-only imports
- **Notes:** Claude should check tsconfig strictness during the plan phase and recommend these settings for new projects. For existing projects, enable incrementally to avoid overwhelming type errors.

---

## CSS & Styling Tools (implement/verify)

### Stylelint

- **Link:** https://stylelint.io
- **What it does:** CSS linter with 100+ rules. Supports CSS, SCSS, Less, and CSS-in-JS. The CSS equivalent of ESLint.
- **Loop phase:** implement, verify
- **Install:** `npm install -D stylelint stylelint-config-standard`
- **Claude Code integration:** CLI shell-out (`npx stylelint "**/*.css" --fix`). Structured output with file/line/rule information.
- **Notes:** Use `stylelint-config-standard` as baseline. For SCSS projects, add `stylelint-config-standard-scss`. For Tailwind projects, add `stylelint-config-tailwindcss` to properly handle Tailwind directives like `@tailwind`, `@apply`, and `theme()`.

### stylelint-declaration-strict-value

- **Link:** https://github.com/AndyOGo/stylelint-declaration-strict-value
- **What it does:** Stylelint plugin that enforces CSS custom properties (design tokens) instead of hardcoded values for specified properties. Catches literal hex colors, pixel values, etc. where tokens should be used.
- **Loop phase:** verify
- **Install:** `npm install -D stylelint-declaration-strict-value`
- **Claude Code integration:** CLI shell-out (runs as part of Stylelint). Configure with property patterns (e.g., `/color/`, `/background/`, `font-size`) to enforce token usage.
- **Notes:** Critical for design system enforcement. Can be configured to allow specific keywords (inherit, currentColor) while blocking hardcoded values. Supports regex property matching and shorthand expansion.

### Tailwind CSS IntelliSense / tailwind-lint

- **Link (IntelliSense):** https://github.com/tailwindlabs/tailwindcss-intellisense
- **Link (CLI linter):** https://github.com/ph1p/tailwind-lint
- **What it does:** Validates Tailwind class usage, detects conflicting utilities, and enforces correct directive usage. The IntelliSense extension is VS Code-only; `tailwind-lint` brings the same checks to the CLI.
- **Loop phase:** verify
- **Install:** `npm install -D tailwind-lint`
- **Claude Code integration:** CLI shell-out (`npx tailwind-lint`). Supports Tailwind CSS v4 (CSS-based config) and v3 (JS config). Runs headlessly for CI/hook usage.
- **Notes:** The official IntelliSense only works in VS Code, but `tailwind-lint` wraps the same engine for CLI use. Validates `@tailwind`, `@screen`, `@variants`, `@apply` directives and detects conflicting utility classes.

### eslint-plugin-tailwindcss

- **Link:** https://github.com/francoismassart/eslint-plugin-tailwindcss
- **What it does:** ESLint plugin with 5+ rules for Tailwind: class ordering, no contradicting classes, no custom classnames (enforce utility-first), and enforced shorthand.
- **Loop phase:** implement, verify
- **Install:** `npm install -D eslint-plugin-tailwindcss`
- **Claude Code integration:** CLI shell-out (runs as part of standard ESLint). Supports `--fix` for auto-ordering classes. Tailwind v4 support in beta channel.
- **Notes:** Complements `prettier-plugin-tailwindcss` (which handles class sorting). The `no-custom-classname` rule is particularly useful for enforcing utility-first patterns.

### Lightning CSS

- **Link:** https://lightningcss.dev
- **What it does:** Extremely fast Rust-based CSS parser, transformer, bundler, and minifier. Replaces PostCSS + autoprefixer + postcss-preset-env in one tool.
- **Loop phase:** implement
- **Install:** `npm install -D lightningcss-cli`
- **Claude Code integration:** CLI shell-out (`npx lightningcss --minify --bundle input.css -o output.css`). Used internally by Vite for CSS processing.
- **Notes:** Not a linter -- use Stylelint for rule enforcement. Lightning CSS handles transformation (vendor prefixes, nesting, custom media queries) and minification. Dramatically faster than PostCSS for these tasks.

### PostCSS

- **Link:** https://postcss.org
- **What it does:** CSS transformation framework with a plugin ecosystem. Handles autoprefixing, nesting, custom properties polyfills, and more.
- **Loop phase:** implement
- **Install:** `npm install -D postcss postcss-cli autoprefixer`
- **Claude Code integration:** CLI shell-out (`npx postcss src/styles.css -o dist/styles.css`). Config via `postcss.config.js`. Required by Tailwind CSS v3 (not v4).
- **Notes:** Still widely used but being displaced by Lightning CSS for performance-sensitive pipelines. The plugin ecosystem remains unmatched for niche transformations. If your project already uses PostCSS, keep it; for new projects, prefer Lightning CSS or Vite's built-in CSS handling.

---

## Build Tools (implement)

### Vite (as bundler)

- **Link:** https://vite.dev
- **What it does:** Dev server with native ES module serving and Rollup-based production bundling. HMR is near-instant regardless of app size.
- **Loop phase:** implement
- **Install:** Included when scaffolding with `create-vite`. Standalone: `npm install -D vite`
- **Claude Code integration:** CLI shell-out (`npx vite build` for production, `npx vite` for dev). Config in `vite.config.ts` is well-documented and Claude-friendly. Ecosystem of plugins via `vite-plugin-*`.
- **Notes:** The default recommendation for most new projects. Vite 8 is current stable. The environment API enables framework-specific optimizations. For SSR frameworks (Next.js, Nuxt, SvelteKit), Vite is already the underlying bundler.

### Turbopack

- **Link:** https://turbo.build/pack
- **What it does:** Rust-based bundler from Vercel, now the default in Next.js 16. Claims 700x faster updates than webpack and 10x faster than Vite for large apps. Cold starts under 1 second for 30,000+ module apps.
- **Loop phase:** implement
- **Install:** Built into Next.js 16+. No separate install needed.
- **Claude Code integration:** Automatic when using Next.js dev/build commands. No separate CLI invocation required.
- **Notes:** Not a standalone bundler -- currently only usable through Next.js. If you're on Next.js, you get Turbopack by default. If you're not on Next.js, use Vite or Rspack instead.

### Rspack

- **Link:** https://rspack.rs
- **What it does:** Drop-in webpack replacement written in Rust. 10-23x faster than webpack 5 with ~85% webpack ecosystem compatibility (loaders, plugins).
- **Loop phase:** implement
- **Install:** `npm install -D @rspack/cli @rspack/core`
- **Claude Code integration:** CLI shell-out (`npx rspack build`). Config format mirrors webpack, so Claude can read/modify `rspack.config.js` using existing webpack knowledge. Migration from webpack takes 1-2 days for most projects.
- **Notes:** Best choice for teams with heavy webpack configurations that can't migrate to Vite. Not competing with Turbopack (different use case). If you're starting fresh, use Vite. If you're migrating a webpack monorepo, use Rspack.

### esbuild

- **Link:** https://esbuild.github.io
- **What it does:** Extremely fast Go-based bundler and minifier. Cold production builds in ~300ms for small libraries, ~700ms for larger ones. 10-100x faster than webpack.
- **Loop phase:** implement
- **Install:** `npm install -D esbuild`
- **Claude Code integration:** CLI shell-out (`npx esbuild src/index.ts --bundle --outfile=out.js --minify`). Both CLI and JS API available. Nearly zero config for simple use cases.
- **Notes:** Still in beta (v0.27.x) but widely used in production. No TypeScript type checking (use `tsc --noEmit` separately). Best for library bundling and simple apps. Used internally by Vite for dependency pre-bundling and by size-limit for fast bundle analysis.

### webpack

- **Link:** https://webpack.js.org
- **What it does:** The original JavaScript module bundler. Massive plugin ecosystem. Still powers many production applications.
- **Loop phase:** implement
- **Install:** `npm install -D webpack webpack-cli`
- **Claude Code integration:** CLI shell-out (`npx webpack --mode production`). Config in `webpack.config.js`. Claude understands webpack config well due to extensive training data.
- **Notes:** Not recommended for new projects -- use Vite, Rspack, or esbuild instead. For existing webpack projects, consider migrating to Rspack for a quick performance win with minimal config changes. webpack 5 is the current major version with no v6 announced.

---

## Component Libraries (implement)

### shadcn/ui

- **Link:** https://ui.shadcn.com
- **What it does:** Copy-paste component collection built on Radix UI (or Base UI as of Feb 2026) and Tailwind CSS. Components live in your codebase, not node_modules. 75,000+ GitHub stars.
- **Loop phase:** implement
- **Install:** `npx shadcn@latest init` then `npx shadcn@latest add button dialog ...`
- **Claude Code integration:** CLI shell-out. The `npx shadcn add` command is non-interactive and installs components directly into your project. Claude can read and modify the source since it's plain files in your repo.
- **Notes:** The industry default for new React projects in 2026. Works exceptionally well with AI-assisted development because components are local files (not opaque node_modules), so Claude can read, understand, and modify them directly. The Feb 2026 Visual Builder further reduces friction. Supports both Radix UI and Base UI as the primitive layer.

### Radix UI Primitives

- **Link:** https://www.radix-ui.com
- **What it does:** Unstyled, accessible React component primitives. Handles ARIA, keyboard navigation, and focus management. The foundation under shadcn/ui.
- **Loop phase:** implement
- **Install:** `npm install @radix-ui/react-dialog @radix-ui/react-dropdown-menu ...` (per-component)
- **Claude Code integration:** CLI shell-out (install) + direct code usage. Components are composable and well-documented.
- **Notes:** Maintained by the WorkOS team. Development pace has slowed since WorkOS acquisition, but the primitives are stable and widely adopted. Use via shadcn/ui rather than directly unless you need custom styling from scratch. Unified package available as of Feb 2026.

### Headless UI

- **Link:** https://headlessui.com
- **What it does:** Unstyled, accessible UI components from the Tailwind CSS team. Covers common patterns: dialogs, menus, listboxes, comboboxes, tabs, transitions.
- **Loop phase:** implement
- **Install:** `npm install @headlessui/react`
- **Claude Code integration:** Direct code usage. Smaller API surface than Radix (fewer components), which makes it easier for Claude to work with.
- **Notes:** Fewer components than Radix but tighter Tailwind integration. Good for projects that want accessible primitives without the full shadcn/ui system. Supports React and Vue.

### Mantine

- **Link:** https://mantine.dev
- **What it does:** Batteries-included React component library with 120+ components and 100+ hooks. Covers rich text editors, date pickers, notifications, spotlight search, and drag-and-drop.
- **Loop phase:** implement
- **Install:** `npm install @mantine/core @mantine/hooks`
- **Claude Code integration:** Direct code usage. Extensive component API means Claude can accomplish most UI tasks without custom code.
- **Notes:** v7 dropped Emotion for CSS Modules, eliminating CSS-in-JS runtime overhead and improving SSR performance. Strongest all-around choice for projects that want comprehensive components out of the box rather than building from primitives.

### Material UI (MUI)

- **Link:** https://mui.com
- **What it does:** React implementation of Google's Material Design. 90+ components, extensive theming system, enterprise support.
- **Loop phase:** implement
- **Install:** `npm install @mui/material @emotion/react @emotion/styled`
- **Claude Code integration:** Direct code usage. The most-documented React component library, so Claude has extensive training data. Theme configuration is JSON-based and easy to modify.
- **Notes:** The Emotion dependency adds CSS-in-JS runtime overhead. Large bundle size compared to alternatives. Best for enterprise apps or teams already committed to Material Design. v6 is current.

### Chakra UI

- **Link:** https://chakra-ui.com
- **What it does:** Accessible React component library with style props API. Strong focus on accessibility (WCAG compliance).
- **Loop phase:** implement
- **Install:** `npm install @chakra-ui/react`
- **Claude Code integration:** Direct code usage. Style props API is intuitive for Claude to generate (`<Box p={4} bg="gray.100">`).
- **Notes:** Choose Chakra when accessibility is the top priority. The style props API is distinctive -- components are styled inline rather than via class names. 2025 update introduced Chakra Pro with motion library and AI-powered responsive design suggestions.

---

## Design System Enforcement (verify)

### Stylelint + stylelint-declaration-strict-value

- **Link:** https://github.com/AndyOGo/stylelint-declaration-strict-value
- **What it does:** Enforces that specified CSS properties use variables/tokens instead of hardcoded values. Catches literal hex colors, pixel values, and font names where design tokens should be used.
- **Loop phase:** verify
- **Install:** `npm install -D stylelint stylelint-declaration-strict-value`
- **Claude Code integration:** CLI shell-out (`npx stylelint "**/*.css"`). Configure with property patterns to flag violations. Works as a pre-commit hook or CI gate.
- **Notes:** The most direct tool for preventing hardcoded values in CSS. Configure for your token properties: `/color/`, `/background/`, `font-size`, `font-family`, `border-radius`, `box-shadow`, spacing properties.

### ESLint Custom Rules (for JSX/TSX token enforcement)

- **What it does:** Custom ESLint rules that catch hardcoded color values, spacing, and non-token style usage in JSX/TSX files.
- **Loop phase:** verify
- **Install:** Write custom rules or use `eslint-plugin-no-hardcoded-colors` (community)
- **Claude Code integration:** CLI shell-out (standard ESLint). Claude can write custom ESLint rules during the plan phase that enforce project-specific token constraints.
- **Notes:** Complements Stylelint for projects using CSS-in-JS, style props, or inline styles. Claude can generate project-specific rules that validate against your actual token set.

### Semgrep (Custom CSS/HTML Rules)

- **Link:** https://semgrep.dev
- **What it does:** Static analysis tool that can write pattern-based rules for any language, including CSS and HTML. Can enforce design system token usage and catch non-compliant patterns.
- **Loop phase:** verify
- **Install:** `pip install semgrep` or via Claude Code's Semgrep plugin
- **Claude Code integration:** MCP server (Semgrep plugin for Claude Code). The `semgrep_scan_with_custom_rule` tool lets Claude write and run ad-hoc rules for design system validation.
- **Notes:** More powerful than Stylelint for complex pattern matching. Can validate that Tailwind classes match an allowed set, that CSS custom properties follow naming conventions, or that components use the correct design tokens. The MCP integration means Claude can write, run, and iterate on rules in a single conversation.

### Tokens Studio (Figma sync)

- **Link:** https://tokens.studio
- **What it does:** Syncs design tokens from Figma to code via GitHub/GitLab. Supports color, typography, spacing, border-radius, and shadow tokens. 264,000+ active users.
- **Loop phase:** plan, verify
- **Install:** Figma plugin + `npm install -D @tokens-studio/sd-transforms`
- **Claude Code integration:** Indirect -- tokens are synced to JSON/CSS files that Claude can read and reference. The Figma MCP plugin can read token definitions from Figma.
- **Notes:** The W3C Design Tokens specification reached its first stable version (2025.10) in October 2025. Tokens Studio aligns with this standard, enabling cross-tool portability.

---

## Performance & Bundle Analysis (verify)

### Lighthouse CI

- **Link:** https://github.com/GoogleChrome/lighthouse-ci
- **What it does:** Runs Lighthouse audits (performance, accessibility, best practices, SEO) in CI or locally. Sets performance budgets and fails builds when Core Web Vitals (LCP, CLS, TBT) regress.
- **Loop phase:** verify
- **Install:** `npm install -g @lhci/cli`
- **Claude Code integration:** CLI shell-out (`lhci autorun`). Configure via `lighthouserc.json` with score thresholds and performance budgets. JSON output is parseable.
- **Notes:** Essential for verify-phase performance gates. Configure assertion budgets: `"performance": 0.9, "accessibility": 0.95`. Runs headless Chrome internally. Use after significant UI changes or dependency updates.

### web-vitals

- **Link:** https://github.com/GoogleChrome/web-vitals
- **What it does:** Tiny library (1.5KB) for measuring Core Web Vitals (LCP, CLS, INP, FCP, TTFB) in the browser. Reports real user metrics.
- **Loop phase:** verify (runtime)
- **Install:** `npm install web-vitals`
- **Claude Code integration:** Direct code usage (import and call in app entry point). Claude can add measurement code and analyze results. Not a CLI tool -- requires a running browser.
- **Notes:** For real-user monitoring (RUM), not synthetic testing. Pair with Lighthouse CI for synthetic and web-vitals for production monitoring. Claude can add the instrumentation code but can't directly observe the metrics without Playwright.

### size-limit

- **Link:** https://github.com/ai/size-limit
- **What it does:** Calculates the real cost (size + load time) of your JS. Modular architecture with plugins for webpack, esbuild, and time estimation. Shows pull request size impact via GitHub Action.
- **Loop phase:** verify
- **Install:** `npm install -D size-limit @size-limit/preset-app` (or `preset-small-lib`, `preset-big-lib`)
- **Claude Code integration:** CLI shell-out (`npx size-limit`). Configure budgets in `package.json`. The `--why` flag shows a treemap of what's contributing to size. Exit code 1 on budget violation.
- **Notes:** Better than raw bundle size checks because it estimates actual load time, not just byte count. The `@size-limit/esbuild` plugin is faster than the webpack plugin for analysis. The GitHub Action posts size changes as PR comments. Use as a pre-commit hook or CI gate.

### webpack-bundle-analyzer

- **Link:** https://github.com/webpack-contrib/webpack-bundle-analyzer
- **What it does:** Generates interactive treemap visualizations of webpack bundle contents. Shows parsed, gzipped, and Brotli sizes of every module.
- **Loop phase:** verify
- **Install:** `npm install -D webpack-bundle-analyzer`
- **Claude Code integration:** CLI shell-out (`npx webpack-bundle-analyzer stats.json --mode static --report report.html --no-open`). The `--mode static` flag generates an HTML file without launching a browser. The `--mode json` flag outputs machine-readable data.
- **Notes:** v5.3.0 is current (2.5M+ weekly npm downloads). The `--no-open` flag is essential for headless/Claude Code usage. For Vite projects, use `rollup-plugin-visualizer` instead. For Rspack, use `@rspack/plugin-bundle-analyzer`.

### bundlesize

- **Link:** https://github.com/siddharthkp/bundlesize
- **What it does:** Tests asset sizes against thresholds. Integrates with GitHub to post pass/fail status on PRs. Supports gzip and Brotli compression.
- **Loop phase:** verify
- **Install:** `npm install -D bundlesize`
- **Claude Code integration:** CLI shell-out (`npx bundlesize`). Configure in `package.json` with path patterns and max sizes.
- **Notes:** Simpler than size-limit (just size checks, no load time estimation). Good for quick CI gates. For more sophisticated analysis, prefer size-limit.

### Vitest (bonus: testing framework)

- **Link:** https://vitest.dev
- **What it does:** Vite-native testing framework with Jest-compatible API. Smart watch mode, native v8/istanbul coverage, browser mode for component testing. Supports Vue, React, Svelte, Lit, and Marko.
- **Loop phase:** verify
- **Install:** `npm install -D vitest`
- **Claude Code integration:** CLI shell-out (`npx vitest run` for CI, `npx vitest --reporter=json` for parseable output). Since Vitest 3, tests can be specified by filename and line number. Shell autocompletions available.
- **Notes:** The default testing framework for modern JS/TS projects in 2026. Shares Vite config, so no separate bundler setup needed. The `vitest list` command prints matching tests without running them (useful for Claude to understand test structure). Angular 21 CLI now defaults to Vitest over Karma.

---

## Browser Integration (verify)

### Playwright MCP Server (Microsoft)

- **Link:** https://github.com/microsoft/playwright-mcp
- **What it does:** Official MCP server that gives Claude Code direct browser control. 34 tools across core automation, tab management, vision-based interactions, and test assertions. Uses accessibility snapshots by default (no screenshots needed for structure).
- **Loop phase:** verify
- **Install:** `claude mcp add playwright -- npx @playwright/mcp@latest`
- **Claude Code integration:** MCP server (first-class). Claude can navigate pages, fill forms, click elements, read DOM structure, take screenshots, and run assertions -- all via natural language.
- **Notes:** Capabilities can be extended with `--caps vision` (multimodal screenshots), `--caps pdf`, and `--caps devtools`. The `--device` flag supports 143+ device emulation profiles. The `--viewport-size` flag ensures consistent screenshot dimensions. Essential for verify-phase UI testing.

### Playwright DevTools MCP

- **Link:** https://github.com/ariangibson/playwright-devtools-mcp
- **What it does:** Specialized MCP server providing Chrome DevTools Protocol access through Playwright. Enables autonomous debugging, performance analysis, and security inspection via DevTools.
- **Loop phase:** verify
- **Install:** See repo for setup instructions
- **Claude Code integration:** MCP server. Provides access to Chrome DevTools panels (Network, Performance, Console, Security) programmatically.
- **Notes:** More specialized than the standard Playwright MCP. Use for deep performance debugging, network waterfall analysis, and security header inspection. Still in active development.

### Playwright Test Runner (CLI)

- **Link:** https://playwright.dev
- **What it does:** End-to-end testing framework with cross-browser support (Chromium, Firefox, WebKit). Auto-waiting, trace recording, and parallel test execution.
- **Loop phase:** verify
- **Install:** `npm install -D @playwright/test && npx playwright install`
- **Claude Code integration:** CLI shell-out (`npx playwright test`). JSON reporter for parseable results. The `--ui` flag launches an interactive test viewer (not useful for Claude), but `--reporter=json` gives structured output.
- **Notes:** Claude can both write and run Playwright tests. The `codegen` feature generates test scripts from browser interactions. Trace files (`.zip`) can be saved with `--trace on` for debugging test failures. For visual regression, pair with `pixelmatch` or a service like Percy/Chromatic.

### Figma Dev Mode MCP

- **Link:** Installed via `figma@claude-plugins-official`
- **What it does:** Exposes Figma design structure (hierarchy, auto-layout, variants, text styles, spacing tokens, component references) directly to Claude Code.
- **Loop phase:** plan, verify
- **Install:** Claude Code plugin marketplace
- **Claude Code integration:** MCP server. Skills: `figma-implement-design` (with built-in validation checklist), `figma-create-design-system-rules` (generates project-specific rules), `figma-code-connect-components` (maps Figma components to code).
- **Notes:** Enables Claude to generate code against real design data rather than guessing from screenshots. The `figma-create-design-system-rules` skill is particularly valuable for establishing design system enforcement rules that persist across sessions.

---

## Sources

### Frameworks
- [Vite - Getting Started](https://vite.dev/guide/)
- [Vite+ Unveiled with Unified Toolchain](https://www.infoq.com/news/2025/10/vite-plus-unveiled/)
- [Next.js - create-next-app](https://nextjs.org/docs/app/api-reference/cli/create-next-app)
- [Nuxt vs Next.js vs Astro vs SvelteKit: 2026 Frontend Framework Showdown](https://www.nunuqs.com/blog/nuxt-vs-next-js-vs-astro-vs-sveltekit-2026-frontend-framework-showdown)
- [Angular Version History](https://www.grapestechsolutions.com/blog/angular-version-history/)
- [React Router v7 | Remix](https://remix.run/blog/react-router-v7)

### Linters & Formatters
- [Biome: The ESLint and Prettier Killer? Migration Guide for 2026](https://dev.to/pockit_tools/biome-the-eslint-and-prettier-killer-complete-migration-guide-for-2026-27m)
- [ESLint vs Biome 2026](https://www.pkgpulse.com/blog/eslint-vs-biome-2026)
- [Oxlint v1.0 Stable Released](https://www.infoq.com/news/2025/08/oxlint-v1-released/)
- [Oxlint JS Plugins Alpha](https://oxc.rs/blog/2026-03-11-oxlint-js-plugins-alpha)
- [ESLint Configuration Migration Guide](https://eslint.org/docs/latest/use/configure/migration-guide)
- [ESLint Now Officially Supports CSS](https://eslint.org/blog/2025/02/eslint-css-support/)

### TypeScript
- [typescript-eslint Shared Configs](https://typescript-eslint.io/users/configs/)
- [Typed Linting](https://typescript-eslint.io/getting-started/typed-linting/)
- [TypeScript TSConfig Reference](https://www.typescriptlang.org/tsconfig/)

### CSS & Styling
- [Stylelint](https://stylelint.io/)
- [stylelint-declaration-strict-value](https://github.com/AndyOGo/stylelint-declaration-strict-value)
- [Lightning CSS](https://lightningcss.dev)
- [tailwind-lint CLI](https://github.com/ph1p/tailwind-lint)
- [eslint-plugin-tailwindcss](https://github.com/francoismassart/eslint-plugin-tailwindcss)
- [Tailwind CSS IntelliSense Linting](https://tailwindcss.com/blog/introducing-linting-for-tailwindcss-intellisense)

### Build Tools
- [Turbopack in 2026: Complete Guide](https://pockit.tools/blog/turbopack-nextjs-bundler-complete-guide/)
- [Rspack vs Webpack: Drop-In Replacement Performance Deep Dive 2026](https://www.pkgpulse.com/blog/rspack-vs-webpack-deep-2026)
- [esbuild](https://esbuild.github.io/)
- [Vite vs Turbopack vs Rspack: 2025 JavaScript Bundler Guide](https://drcodes.com/posts/vite-vs-turbopack-vs-rspack-2025-javascript-bundler-guide)

### Component Libraries
- [shadcn/ui](https://ui.shadcn.com/)
- [shadcn/ui vs Base UI vs Radix: Components in 2026](https://www.pkgpulse.com/blog/shadcn-ui-vs-base-ui-vs-radix-components-2026)
- [React UI Libraries in 2025](https://makersden.io/blog/react-ui-libs-2025-comparing-shadcn-radix-mantine-mui-chakra)
- [Mantine vs Chakra UI vs MUI 2026](https://adminlte.io/blog/mantine-vs-chakra-ui-vs-mui/)
- [15 Best React UI Libraries for 2026](https://www.builder.io/blog/react-component-libraries-2026)

### Design System Enforcement
- [Enforcing Design Tokens: A Practical Guide](https://medium.com/@barshaya97_76274/design-tokens-enforcement-977310b2788e)
- [W3C Design Tokens Specification Stable](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/)
- [Design Token Management Tools 2025](https://cssauthor.com/design-token-management-tools/)

### Performance
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- [size-limit](https://github.com/ai/size-limit)
- [webpack-bundle-analyzer](https://github.com/webpack-contrib/webpack-bundle-analyzer)

### Browser Integration
- [Playwright MCP Server](https://github.com/microsoft/playwright-mcp)
- [Playwright MCP with Claude Code](https://til.simonwillison.net/claude-code/playwright-mcp-claude-code)
- [Best MCP Servers for Claude Code 2026](https://www.builder.io/blog/best-mcp-servers-2026)
- [Claude Code MCP Documentation](https://code.claude.com/docs/en/mcp)

### Testing
- [Vitest](https://vitest.dev/)
- [Vitest in 2026](https://dev.to/ottoaria/vitest-in-2026-the-testing-framework-that-makes-you-actually-want-to-write-tests-kap)
