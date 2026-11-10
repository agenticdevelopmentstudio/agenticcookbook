---
id: eb0764d5-aeac-40cc-9aa4-d84e4eaa652d
title: Guidelines Index
type: reference
version: 2.7.0
status: accepted
language: en
created: 2026-03-27
modified: '2026-11-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: Complete index of all guidelines, organized by use case.
platforms: []
tags: []
depends-on: []
related: []
references: []
approved-by: ''
approved-date: ''
---

# Guidelines Index

Guidelines are organized by **use case** — the phase of work where they apply. Guidelines that apply to multiple use cases are duplicated into each so the agent gets everything it needs by reading one directory.

| Use Case | Guidelines | When to use |
|----------|-----------|-------------|
| [Planning](#planning-63-guidelines) | 63 | Architecture, data modeling, choosing patterns |
| [Implementing](#implementing-182-guidelines) | 182 | Writing new code |
| [Testing](#testing-24-guidelines) | 24 | Writing and structuring tests |
| [Reviewing](#reviewing-64-guidelines) | 64 | Checking code quality, security, accessibility |
| [Shipping](#shipping-17-guidelines) | 17 | Pre-commit, pre-PR, packaging |
| [Cookbook](#cookbook-16-guidelines) | 16 | Writing cookbook content (recipes, skills, agents) |
| [Researching](#researching-5-guidelines) | 5 | Gathering, verifying, and recording trustworthy research |
| [Storytelling](#storytelling-6-guidelines) | 6 | Telling a project's story: positioning, explanation, narrative, grounded in the record |
| [Brainstorming](#brainstorming-4-guidelines) | 4 | Framing a problem, generating ideas and converging, without anchoring |

275 unique guidelines, 381 total (with duplicates across use cases).

---

### Planning (63 guidelines)


**code-quality**
- [Agent instruction files (AGENTS.md / CLAUDE.md)](planning/code-quality/agent-instruction-files/)
- [Algorithmic Complexity](planning/code-quality/algorithmic-complexity/)
- [App Interactions](planning/code-quality/app-interactions/)
- [Architecture](planning/code-quality/architecture/)
- [Cross-Cutting Detection](planning/code-quality/cross-cutting-detection/)
- [Dependency Clusters](planning/code-quality/dependency-clusters/)
- [Choosing a .NET target framework](planning/code-quality/dotnet-target-framework/)
- [Essential vs accidental complexity](planning/code-quality/essential-vs-accidental-complexity/)
- [Framework Conventions](planning/code-quality/framework-conventions/)
- [Interface Cohesion](planning/code-quality/interface-cohesion/)
- [Kotlin Multiplatform](planning/code-quality/kotlin-multiplatform/)
- [Lifecycle Patterns](planning/code-quality/lifecycle-patterns/)
- [Module Boundaries](planning/code-quality/module-boundaries/)
- [Purpose Classification](planning/code-quality/purpose-classification/)
- [Search for existing solutions before building](planning/code-quality/reuse-before-build/)
- [Runtime Conditions](planning/code-quality/runtime-conditions/)
- [Scope discipline](planning/code-quality/scope-discipline/)
- [Spec-driven development (plan before code)](planning/code-quality/spec-driven-development/)
- [System Dependencies](planning/code-quality/system-dependencies/)
- [System Interactions](planning/code-quality/system-interactions/)
- [Choosing a Windows UI framework and deployment model](planning/code-quality/windows-ui-framework-and-deployment/)

**data**
- [Access Pattern Analysis](planning/data/access-pattern-analysis/)
- [Clock Systems for Sync](planning/data/clock-systems/)
- [Conflict Resolution](planning/data/conflict-resolution/)
- [CQRS and event sourcing](planning/data/cqrs-and-event-sourcing/)
- [Database](planning/data/database/)
- [Choosing a primary datastore](planning/data/datastore-selection/)
- [Indexing](planning/data/indexing/)
- [JSON columns and generated columns](planning/data/json-columns/)
- [Normalization and denormalization](planning/data/normalization-and-denormalization/)
- [Offline-First Architecture](planning/data/offline-first-architecture/)
- [Primary key strategies](planning/data/primary-keys/)
- [Relationship patterns](planning/data/relationships/)
- [Choose SwiftData vs Core Data](planning/data/swiftdata-vs-core-data/)
- [Sync Engine Design](planning/data/sync-engine-design/)
- [Sync Protocol](planning/data/sync-protocol/)
- [Sync Schema Design](planning/data/sync-schema-design/)
- [SQLite Sync Tooling](planning/data/sync-tooling/)
- [Transactions and Concurrency](planning/data/transactions-and-concurrency/)
- [Vector search and retrieval](planning/data/vector-search-and-retrieval/)

**feature-management**
- [Feature flags](planning/feature-management/feature-flags/)

**infrastructure**
- [Immutable infrastructure](planning/infrastructure/immutable-infrastructure/)
- [Infrastructure as code](planning/infrastructure/infrastructure-as-code/)

**networking**
- [Design-first API development with OpenAPI](planning/networking/api-design-first/)
- [API Design](planning/networking/api-design/)
- [Choosing an API style (REST, gRPC, GraphQL)](planning/networking/api-style-selection/)
- [API versioning and deprecation](planning/networking/api-versioning-and-deprecation/)
- [Caching](planning/networking/caching/)
- [Offline and Connectivity](planning/networking/offline-and-connectivity/)
- [Pagination](planning/networking/pagination/)
- [Real-Time Communication](planning/networking/real-time-communication/)

**security**
- [Authentication](planning/security/authentication/)
- [Data privacy regulations](planning/security/data-privacy-regulations/)
- [Privacy by design](planning/security/privacy-by-design/)
- [Privacy and security by default](planning/security/privacy/)
- [Threat modeling](planning/security/threat-modeling/)

**testing**
- [Test Pyramid](planning/testing/test-pyramid/)

**ui**
- [Dashboard service is display-only](planning/ui/dashboard-service-is-display-only/)
- [Data Display](planning/ui/data-display/)
- [Design tokens](planning/ui/design-tokens/)
- [Platform Design Languages](planning/ui/platform-design-languages/)
- [Choose a rendering strategy per route, minimize client JS](planning/ui/rendering-strategy/)
- [Separate server state from client state](planning/ui/state-management/)

---

### Implementing (182 guidelines)


**accessibility**
- [Accessibility from day one](implementing/accessibility/accessibility/)
- [Dynamic Type](implementing/accessibility/dynamic-type/)
- [Font Scaling](implementing/accessibility/font-scaling/)

**code-quality**
- [Architecture](implementing/code-quality/architecture/)
- [Small, atomic commits](implementing/code-quality/atomic-commits/)
- [Writing code for the AI reader](implementing/code-quality/code-for-the-ai-reader/)
- [Completeness: finish the work, don't defer by default](implementing/code-quality/completeness/)
- [Delete what you supersede](implementing/code-quality/delete-what-you-supersede/)
- [Dependency Injection](implementing/code-quality/dependency-injection/)
- [File paths](implementing/code-quality/file-paths/)
- [Hilt dependency injection for Android](implementing/code-quality/hilt-dependency-injection/)
- [Linting before the first PR](implementing/code-quality/linting/)
- [Naming](implementing/code-quality/naming/)
- [No external dependencies in core libraries](implementing/code-quality/no-external-dependencies-in-core-librari/)
- [Nullable Reference Types](implementing/code-quality/nullable-reference-types/)
- [Scope discipline](implementing/code-quality/scope-discipline/)
- [Shared components and tiers](implementing/code-quality/shared-components-and-tiers/)
- [Shell scripts](implementing/code-quality/shell-scripts/)
- [Type hints](implementing/code-quality/type-hints/)
- [TypeScript strictness configuration](implementing/code-quality/typescript-strictness/)
- [Use roadmap_lib](implementing/code-quality/use-roadmaplib/)
- [Value objects over primitive obsession](implementing/code-quality/value-objects/)
- [Verification harnesses as agent guardrails](implementing/code-quality/verification-harness/)
- [Visual Studio project files](implementing/code-quality/visual-studio-project-files/)
- [Xcode project hygiene](implementing/code-quality/xcode-project-hygiene/)
- [YAML frontmatter](implementing/code-quality/yaml-frontmatter/)

**concurrency**
- [No blocking the main thread](implementing/concurrency/concurrency/)
- [Immutability](implementing/concurrency/immutability/)
- [Kotlin Flow and StateFlow: lifecycle-aware state exposure](implementing/concurrency/kotlin-flow-stateflow/)
- [Adopt Swift 6 strict concurrency incrementally](implementing/concurrency/swift6-strict-concurrency/)

**data**
- [Access Pattern Analysis](implementing/data/access-pattern-analysis/)
- [Advanced database indexing](implementing/data/advanced-indexing/)
- [Database backup and recovery](implementing/data/backup-and-recovery/)
- [Clock Systems for Sync](implementing/data/clock-systems/)
- [Conflict Resolution](implementing/data/conflict-resolution/)
- [Connection pooling for server and serverless backends](implementing/data/connection-pooling/)
- [Constraints and validation](implementing/data/constraints-and-validation/)
- [Data retention and deletion](implementing/data/data-retention-and-deletion/)
- [Data types and type affinity](implementing/data/data-types/)
- [Database](implementing/data/database/)
- [Deterministic IDs](implementing/data/deterministic-ids/)
- [Foreign keys and referential integrity](implementing/data/foreign-keys/)
- [Indexing](implementing/data/indexing/)
- [JSON columns and generated columns](implementing/data/json-columns/)
- [Database naming conventions](implementing/data/naming-conventions/)
- [Normalization and denormalization](implementing/data/normalization-and-denormalization/)
- [Offline-First Architecture](implementing/data/offline-first-architecture/)
- [Table partitioning and time-series data](implementing/data/partitioning-and-time-series/)
- [Primary key strategies](implementing/data/primary-keys/)
- [Query Optimization](implementing/data/query-optimization/)
- [Relationship patterns](implementing/data/relationships/)
- [Room persistence on Android](implementing/data/room-persistence/)
- [Schema evolution and migrations](implementing/data/schema-evolution/)
- [Sync Engine Design](implementing/data/sync-engine-design/)
- [Sync Protocol](implementing/data/sync-protocol/)
- [Sync Schema Design](implementing/data/sync-schema-design/)
- [SQLite Sync Tooling](implementing/data/sync-tooling/)
- [Transaction isolation and serialization-failure retry](implementing/data/transaction-isolation/)
- [Transactions and Concurrency](implementing/data/transactions-and-concurrency/)
- [Zero-downtime migrations: expand and contract](implementing/data/zero-downtime-migrations/)

**documentation**
- [Writing comments and docs](implementing/documentation/writing-comments-and-docs/)

**feature-management**
- [A/B testing](implementing/feature-management/ab-testing/)
- [Debug mode](implementing/feature-management/debug-mode/)
- [Feature flags](implementing/feature-management/feature-flags/)

**infrastructure**
- [Containerization](implementing/infrastructure/containerization/)
- [Kubernetes configuration and secrets](implementing/infrastructure/kubernetes-configuration/)
- [Kubernetes workloads](implementing/infrastructure/kubernetes-workloads/)
- [Twelve-factor configuration](implementing/infrastructure/twelve-factor-config/)

**internationalization**
- [Localizability](implementing/internationalization/localization/)
- [RTL layout support](implementing/internationalization/rtl-support/)

**language**
- [Objective-C](implementing/language/objective-c/)
- [PowerShell](implementing/language/powershell/)
- [Python](implementing/language/python/)
- [Ruby](implementing/language/ruby/)
- [Swift](implementing/language/swift/)

**networking**
- [AI Cost Management](implementing/networking/ai-cost-management/)
- [API Design](implementing/networking/api-design/)
- [Caching](implementing/networking/caching/)
- [Error Responses](implementing/networking/error-responses/)
- [HTTP conditional requests and optimistic concurrency](implementing/networking/http-conditional-requests/)
- [Idempotency keys for write APIs](implementing/networking/idempotency-keys/)
- [MCP server design](implementing/networking/mcp-server-design/)
- [Offline and Connectivity](implementing/networking/offline-and-connectivity/)
- [Pagination](implementing/networking/pagination/)
- [Rate Limiting](implementing/networking/rate-limiting/)
- [Real-Time Communication](implementing/networking/real-time-communication/)
- [Retry and Resilience](implementing/networking/retry-and-resilience/)
- [Be strict and maintain: Postel reconsidered (RFC 9413)](implementing/networking/robust-protocol-maintenance/)
- [Timeouts](implementing/networking/timeouts/)
- [Web services](implementing/networking/web-services/)

**observability**
- [AI Provider Observability](implementing/observability/ai-provider-observability/)
- [Analytics](implementing/observability/analytics/)
- [Continuous profiling](implementing/observability/continuous-profiling/)
- [Distributed tracing and context propagation](implementing/observability/distributed-tracing/)
- [Instrumented logging](implementing/observability/logging/)
- [Metrics instrumentation: RED and USE](implementing/observability/metrics-red-use/)
- [Service-level objectives and error budgets](implementing/observability/service-level-objectives/)

**platform-integration**
- [App Intents](implementing/platform-integration/app-intents/)
- [Background tasks](implementing/platform-integration/background-tasks/)
- [Deep linking](implementing/platform-integration/deep-linking/)
- [Handoff and continuity](implementing/platform-integration/handoff-and-continuity/)
- [Notifications](implementing/platform-integration/notifications/)
- [Use AppKit and UIKit, not SwiftUI](implementing/platform-integration/prefer-explicit-apple-apis/)
- [Search integration](implementing/platform-integration/search-integration/)
- [Share and inter-app data flow](implementing/platform-integration/share-and-inter-app-data/)
- [Scriptable and automatable](implementing/platform-integration/shortcuts-and-automation/)
- [Widgets and glanceable surfaces](implementing/platform-integration/widgets-and-glanceable-surfaces/)
- [Windows Subsystem for Linux](implementing/platform-integration/wsl/)

**security**
- [Agent guardrails](implementing/security/agent-guardrails/)
- [Authentication](implementing/security/authentication/)
- [Authorization](implementing/security/authorization/)
- [Consent management](implementing/security/consent-management/)
- [Content Security Policy](implementing/security/content-security-policy/)
- [CORS](implementing/security/cors/)
- [Data subject rights (DSAR)](implementing/security/data-subject-rights/)
- [Dependency Security](implementing/security/dependency-security/)
- [Input Validation](implementing/security/input-validation/)
- [LLM and agentic application security](implementing/security/llm-application-security/)
- [MCP tool input validation](implementing/security/mcp-input-validation/)
- [MCP server security](implementing/security/mcp-server-security/)
- [Passkeys and WebAuthn](implementing/security/passkeys-and-webauthn/)
- [PII detection and redaction](implementing/security/pii-detection-and-redaction/)
- [PII handling and classification](implementing/security/pii-handling/)
- [Privacy and security by default](implementing/security/privacy/)
- [Secure Storage](implementing/security/secure-storage/)
- [Security Headers Checklist](implementing/security/security-headers-checklist/)
- [Sender-constrained access tokens](implementing/security/sender-constrained-tokens/)
- [Sensitive Data](implementing/security/sensitive-data/)
- [Token Handling](implementing/security/token-handling/)
- [Transport Security](implementing/security/transport-security/)

**skills-and-agents**
- [Agent Structure Reference](implementing/skills-and-agents/agent-structure-reference/)
- [Authoring Skills and Rules](implementing/skills-and-agents/authoring-skills-and-rules/)
- [Codex configuration](implementing/skills-and-agents/codex-configuration/)
- [Context and memory management for agents](implementing/skills-and-agents/context-and-memory-management/)
- [GitHub Copilot configuration](implementing/skills-and-agents/copilot-configuration/)
- [Kimi configuration](implementing/skills-and-agents/kimi-configuration/)
- [Never overwrite a user's files](implementing/skills-and-agents/never-clobber-user-files/)
- [Performance: Speed and Token Efficiency](implementing/skills-and-agents/performance/)
- [Rule Structure Reference](implementing/skills-and-agents/rule-structure-reference/)
- [Skill Structure Reference](implementing/skills-and-agents/skill-structure-reference/)

**testing**
- [Property-Based Testing](implementing/testing/property-based-testing/)
- [Swift Testing](implementing/testing/swift-testing/)
- [Test Data](implementing/testing/test-data/)
- [Test Doubles](implementing/testing/test-doubles/)
- [Comprehensive unit testing](implementing/testing/testing/)
- [Unit Test Patterns](implementing/testing/unit-test-patterns/)

**ui**
- [Always show progress](implementing/ui/always-show-progress/)
- [Android edge-to-edge and window insets](implementing/ui/android-edge-to-edge/)
- [Android navigation in Compose](implementing/ui/android-navigation/)
- [Android predictive back](implementing/ui/android-predictive-back/)
- [Animation & Motion](implementing/ui/animation-motion/)
- [AppKit and UIKit patterns](implementing/ui/appkit-and-uikit-patterns/)
- [Apple design language and widgets](implementing/ui/apple-liquid-glass-and-widgets/)
- [Color](implementing/ui/color/)
- [Jetpack Compose performance and stability](implementing/ui/compose-performance-and-stability/)
- [Jetpack Compose side effects](implementing/ui/compose-side-effects/)
- [Jetpack Compose: state hoisting and unidirectional data flow](implementing/ui/compose-state-and-udf/)
- [Core Web Vitals and performance budgets](implementing/ui/core-web-vitals/)
- [Cross-platform token adaptation](implementing/ui/cross-platform-token-adaptation/)
- [Dashboard service is display-only](implementing/ui/dashboard-service-is-display-only/)
- [Data Display](implementing/ui/data-display/)
- [Design-Time Data](implementing/ui/design-time-data/)
- [Design token distribution](implementing/ui/design-token-distribution/)
- [Feedback Patterns](implementing/ui/feedback-patterns/)
- [Fluent Design](implementing/ui/fluent-design/)
- [Form Design](implementing/ui/form-design/)
- [High DPI / Display Scaling](implementing/ui/high-dpi-display-scaling/)
- [Iconography](implementing/ui/iconography/)
- [Layout](implementing/ui/layout/)
- [Material 3 theming on Android](implementing/ui/material3-theming/)
- [Modern CSS layout and Baseline-driven adoption](implementing/ui/modern-css/)
- [Platform Design Languages](implementing/ui/platform-design-languages/)
- [Previews](implementing/ui/previews/)
- [Progressive Web App installability](implementing/ui/progressive-web-app/)
- [Spacing](implementing/ui/spacing/)
- [State Design](implementing/ui/state-design/)
- [Theming with tokens](implementing/ui/theming-with-tokens/)
- [Theming](implementing/ui/theming/)
- [Touch & Click Targets](implementing/ui/touch-click-targets/)
- [Typography](implementing/ui/typography/)
- [Visual Hierarchy](implementing/ui/visual-hierarchy/)
- [Windows 11 materials (Mica and Acrylic)](implementing/ui/windows-11-materials/)

---

### Testing (24 guidelines)

- [Agent evaluation and safety](testing/agent-evaluation-and-safety/)
- [Contract testing for services](testing/contract-testing/)
- [Database testing](testing/database-testing/)
- [Design-Time Data](testing/design-time-data/)
- [Eval-driven development for agent behavior](testing/eval-driven-development/)
- [Flaky Test Prevention](testing/flaky-test-prevention/)
- [Flaky test quarantine lifecycle](testing/flaky-test-quarantine/)
- [Fuzz testing](testing/fuzzing/)
- [Groundedness and hallucination checks](testing/groundedness-and-hallucination/)
- [Linting from day one](testing/linting/)
- [Mutation Testing](testing/mutation-testing/)
- [Post-generation verification](testing/post-generation-verification/)
- [Previews](testing/previews/)
- [Properties of Good Tests](testing/properties-of-good-tests/)
- [Property-Based Testing](testing/property-based-testing/)
- [Security Testing](testing/security-testing/)
- [Snapshot testing discipline](testing/snapshot-testing/)
- [Test Data](testing/test-data/)
- [Test Doubles](testing/test-doubles/)
- [Test Pyramid](testing/test-pyramid/)
- [Comprehensive unit testing](testing/testing/)
- [The Testing Workflow](testing/the-testing-workflow/)
- [Tool-call evaluation](testing/tool-call-evaluation/)
- [Unit Test Patterns](testing/unit-test-patterns/)

---

### Reviewing (64 guidelines)

- [Conformance: The Criterion Walk](reviewing/conformance-criterion-walk/)
- [Writing the Review Report](reviewing/review-report-writing/)

**accessibility**
- [Accessibility from day one](reviewing/accessibility/accessibility/)

**code-quality**
- [Bulk operation verification](reviewing/code-quality/bulk-operation-verification/)
- [Code hygiene: remove the old thing](reviewing/code-quality/code-hygiene/)
- [Dependency Injection](reviewing/code-quality/dependency-injection/)
- [File paths](reviewing/code-quality/file-paths/)
- [Law of Demeter and Tell, Don't Ask](reviewing/code-quality/law-of-demeter/)
- [Naming](reviewing/code-quality/naming/)
- [No external dependencies in core libraries](reviewing/code-quality/no-external-dependencies-in-core-librari/)
- [Scope discipline](reviewing/code-quality/scope-discipline/)
- [Shell scripts](reviewing/code-quality/shell-scripts/)
- [Type hints](reviewing/code-quality/type-hints/)
- [Use roadmap_lib](reviewing/code-quality/use-roadmaplib/)
- [Visual Studio project files](reviewing/code-quality/visual-studio-project-files/)
- [Xcode project hygiene](reviewing/code-quality/xcode-project-hygiene/)
- [YAML frontmatter](reviewing/code-quality/yaml-frontmatter/)

**data**
- [Query Optimization](reviewing/data/query-optimization/)

**documentation**
- [Docs match the code](reviewing/documentation/docs-match-code/)

**infrastructure**
- [Container image security](reviewing/infrastructure/container-image-security/)

**internationalization**
- [Localizability](reviewing/internationalization/localization/)
- [RTL layout support](reviewing/internationalization/rtl-support/)

**language**
- [Objective-C](reviewing/language/objective-c/)
- [PowerShell](reviewing/language/powershell/)
- [Python](reviewing/language/python/)
- [Ruby](reviewing/language/ruby/)
- [Swift](reviewing/language/swift/)

**networking**
- [MCP server review checklist](reviewing/networking/mcp-server-checklist/)
- [Hyrum's Law: all observable behavior becomes contract](reviewing/networking/observable-behavior-contract/)
- [Rate Limiting](reviewing/networking/rate-limiting/)
- [Timeouts](reviewing/networking/timeouts/)

**observability**
- [Analytics](reviewing/observability/analytics/)
- [Instrumented logging](reviewing/observability/logging/)

**platform-integration**
- [Deep linking](reviewing/platform-integration/deep-linking/)
- [Use AppKit and UIKit, not SwiftUI](reviewing/platform-integration/prefer-explicit-apple-apis/)
- [Windows Subsystem for Linux](reviewing/platform-integration/wsl/)

**security**
- [Authentication](reviewing/security/authentication/)
- [Authorization](reviewing/security/authorization/)
- [Content Security Policy](reviewing/security/content-security-policy/)
- [CORS](reviewing/security/cors/)
- [Dependency Security](reviewing/security/dependency-security/)
- [Input Validation](reviewing/security/input-validation/)
- [LLM red teaming](reviewing/security/llm-red-teaming/)
- [Privacy and security by default](reviewing/security/privacy/)
- [Secure Storage](reviewing/security/secure-storage/)
- [Security Headers Checklist](reviewing/security/security-headers-checklist/)
- [Sensitive Data](reviewing/security/sensitive-data/)
- [Token Handling](reviewing/security/token-handling/)
- [Transport Security](reviewing/security/transport-security/)
- [Vulnerability prioritization by exploitability](reviewing/security/vulnerability-prioritization/)

**skills-and-agents**
- [Agent Lint Checklist](reviewing/skills-and-agents/agent-checklist/)
- [Codex configuration](reviewing/skills-and-agents/codex-configuration/)
- [GitHub Copilot configuration](reviewing/skills-and-agents/copilot-configuration/)
- [Kimi configuration](reviewing/skills-and-agents/kimi-configuration/)
- [Never overwrite a user's files](reviewing/skills-and-agents/never-clobber-user-files/)
- [Performance: Speed and Token Efficiency](reviewing/skills-and-agents/performance/)
- [Rule Lint Checklist](reviewing/skills-and-agents/rule-checklist/)
- [Skill Lint Checklist](reviewing/skills-and-agents/skill-checklist/)

**testing**
- [Flaky Test Prevention](reviewing/testing/flaky-test-prevention/)
- [Post-generation verification](reviewing/testing/post-generation-verification/)
- [Security Testing](reviewing/testing/security-testing/)

**ui**
- [AppKit and UIKit patterns](reviewing/ui/appkit-and-uikit-patterns/)
- [Color](reviewing/ui/color/)
- [Touch & Click Targets](reviewing/ui/touch-click-targets/)

---

### Shipping (17 guidelines)

- [A/B testing](shipping/ab-testing/)
- [Ship a privacy manifest and declare required-reason APIs](shipping/apple-privacy-manifest/)
- [Small, atomic commits](shipping/atomic-commits/)
- [Database backup and recovery](shipping/backup-and-recovery/)
- [Bulk operation verification](shipping/bulk-operation-verification/)
- [Continuous delivery](shipping/continuous-delivery/)
- [Dependency Security](shipping/dependency-security/)
- [Ephemeral preview environments](shipping/ephemeral-environments/)
- [Feature flags](shipping/feature-flags/)
- [Incident response and blameless postmortems](shipping/incident-response/)
- [MSIX Packaging](shipping/msix-packaging/)
- [Progressive delivery](shipping/progressive-delivery/)
- [Schema evolution and migrations](shipping/schema-evolution/)
- [Software supply-chain integrity](shipping/supply-chain-integrity/)
- [Transport Security](shipping/transport-security/)
- [Trunk-based development](shipping/trunk-based-development/)
- [Windows ARM64 and Native AOT](shipping/windows-arm64-and-aot/)

---

### Cookbook (16 guidelines)


**recipe-quality**
- [Behavioral Requirements](cookbook/recipe-quality/behavioral-requirements/)
- [Completeness](cookbook/recipe-quality/completeness/)
- [Cookbook Compliance](cookbook/recipe-quality/cookbook-compliance/)
- [Cross-Recipe Consistency](cookbook/recipe-quality/cross-recipe-consistency/)
- [Source Fidelity](cookbook/recipe-quality/source-fidelity/)
- [Template Conformance](cookbook/recipe-quality/template-conformance/)

**skills-and-agents**
- [Agent Lint Checklist](cookbook/skills-and-agents/agent-checklist/)
- [Agent Structure Reference](cookbook/skills-and-agents/agent-structure-reference/)
- [Authoring Skills and Rules](cookbook/skills-and-agents/authoring-skills-and-rules/)
- [Rule Lint Checklist](cookbook/skills-and-agents/rule-checklist/)
- [Rule Structure Reference](cookbook/skills-and-agents/rule-structure-reference/)
- [Skill Lint Checklist](cookbook/skills-and-agents/skill-checklist/)
- [Skill Structure Reference](cookbook/skills-and-agents/skill-structure-reference/)

**testing**
- [Properties of Good Tests](cookbook/testing/properties-of-good-tests/)
- [Unit Test Patterns](cookbook/testing/unit-test-patterns/)

**ui**
- [Platform Design Languages](cookbook/ui/platform-design-languages/)

---

### Researching (5 guidelines)


**evidence**
- [Research results document](researching/evidence/research-results-document/)
- [Verification and trust scoring](researching/evidence/verification-and-trust-scoring/)

**process**
- [Agentic research design lessons](researching/process/agentic-research-design-lessons/)
- [Research methodology and sources](researching/process/research-methodology-and-sources/)
- [Research type taxonomy](researching/process/research-type-taxonomy/)

---

### Storytelling (6 guidelines)

- [Narrative Craft](storytelling/craft/)
- [Ecosystem Narration](storytelling/ecosystem/)
- [Explaining a Project](storytelling/explanation/)
- [Grounded Synthesis](storytelling/grounded-synthesis/)
- [Narrative Arc](storytelling/narrative-arc/)
- [Positioning](storytelling/positioning/)

---

### Brainstorming (4 guidelines)

- [Convergent Techniques](brainstorming/convergent-techniques/)
- [Divergent Techniques](brainstorming/divergent-techniques/)
- [Facilitation Without Anchoring](brainstorming/facilitation-without-anchoring/)
- [Framing Techniques](brainstorming/framing-techniques/)

---

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.7.0 | 2026-07-23 | Mike Fullerton | Add PII detection and redaction guideline (implementing/security) |
| 2.6.0 | 2026-06-27 | Mike Fullerton | Add Researching use case (5 guidelines): research-results-document, verification-and-trust-scoring, research-type-taxonomy, research-methodology-and-sources, agentic-research-design-lessons |
| 2.5.0 | 2026-06-09 | Mike Fullerton | Add 43 guidelines across waves 2-4 (AI-native, security, backend, API/MCP, observability, delivery, platforms) |
| 2.4.0 | 2026-06-09 | Mike Fullerton | Add code-hygiene, completeness, value-objects, reuse-before-build (146 unique, 238 total) |
| 2.3.0 | 2026-04-09 | Mike Fullerton | Recategorize: 20→12 categories, dissolve language/platform, flatten shipping/testing |
| 2.1.0 | 2026-04-09 | Mike Fullerton | Pass 2: tailor guidelines to use cases, update counts (140 unique, 232 total) |
| 2.0.0 | 2026-04-09 | Mike Fullerton | Reorganize by use case (planning, implementing, testing, reviewing, shipping, cookbook) |
| 1.1.0 | 2026-04-04 | Mike Fullerton | Add database-design category with SQLite best practices |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
