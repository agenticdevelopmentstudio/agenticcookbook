---
id: eb0764d5-aeac-40cc-9aa4-d84e4eaa652d
title: Guidelines Index
domain: agenticdevelopercookbook://guidelines/INDEX
type: reference
version: 2.7.0
status: accepted
language: en
created: 2026-03-27
modified: '2026-10-09'
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
| [Implementing](#implementing-175-guidelines) | 175 | Writing new code |
| [Testing](#testing-24-guidelines) | 24 | Writing and structuring tests |
| [Reviewing](#reviewing-57-guidelines) | 57 | Checking code quality, security, accessibility |
| [Shipping](#shipping-17-guidelines) | 17 | Pre-commit, pre-PR, packaging |
| [Cookbook](#cookbook-16-guidelines) | 16 | Writing cookbook content (recipes, skills, agents) |
| [Researching](#researching-5-guidelines) | 5 | Gathering, verifying, and recording trustworthy research |

268 unique guidelines, 357 total (with duplicates across use cases).

---

### Planning (63 guidelines)


**code-quality**
- [Agent instruction files (AGENTS.md / CLAUDE.md)](planning/code-quality/agent-instruction-files.md)
- [Algorithmic Complexity](planning/code-quality/algorithmic-complexity.md)
- [App Interactions](planning/code-quality/app-interactions.md)
- [Architecture](planning/code-quality/architecture.md)
- [Cross-Cutting Detection](planning/code-quality/cross-cutting-detection.md)
- [Dependency Clusters](planning/code-quality/dependency-clusters.md)
- [Choosing a .NET target framework](planning/code-quality/dotnet-target-framework.md)
- [Essential vs accidental complexity](planning/code-quality/essential-vs-accidental-complexity.md)
- [Framework Conventions](planning/code-quality/framework-conventions.md)
- [Interface Cohesion](planning/code-quality/interface-cohesion.md)
- [Kotlin Multiplatform](planning/code-quality/kotlin-multiplatform.md)
- [Lifecycle Patterns](planning/code-quality/lifecycle-patterns.md)
- [Module Boundaries](planning/code-quality/module-boundaries.md)
- [Purpose Classification](planning/code-quality/purpose-classification.md)
- [Search for existing solutions before building](planning/code-quality/reuse-before-build.md)
- [Runtime Conditions](planning/code-quality/runtime-conditions.md)
- [Scope discipline](planning/code-quality/scope-discipline.md)
- [Spec-driven development (plan before code)](planning/code-quality/spec-driven-development.md)
- [System Dependencies](planning/code-quality/system-dependencies.md)
- [System Interactions](planning/code-quality/system-interactions.md)
- [Choosing a Windows UI framework and deployment model](planning/code-quality/windows-ui-framework-and-deployment.md)

**data**
- [Access Pattern Analysis](planning/data/access-pattern-analysis.md)
- [Clock Systems for Sync](planning/data/clock-systems.md)
- [Conflict Resolution](planning/data/conflict-resolution.md)
- [CQRS and event sourcing](planning/data/cqrs-and-event-sourcing.md)
- [Database](planning/data/database.md)
- [Choosing a primary datastore](planning/data/datastore-selection.md)
- [Indexing](planning/data/indexing.md)
- [JSON columns and generated columns](planning/data/json-columns.md)
- [Normalization and denormalization](planning/data/normalization-and-denormalization.md)
- [Offline-First Architecture](planning/data/offline-first-architecture.md)
- [Primary key strategies](planning/data/primary-keys.md)
- [Relationship patterns](planning/data/relationships.md)
- [Choose SwiftData vs Core Data](planning/data/swiftdata-vs-core-data.md)
- [Sync Engine Design](planning/data/sync-engine-design.md)
- [Sync Protocol](planning/data/sync-protocol.md)
- [Sync Schema Design](planning/data/sync-schema-design.md)
- [SQLite Sync Tooling](planning/data/sync-tooling.md)
- [Transactions and Concurrency](planning/data/transactions-and-concurrency.md)
- [Vector search and retrieval](planning/data/vector-search-and-retrieval.md)

**feature-management**
- [Feature flags](planning/feature-management/feature-flags.md)

**infrastructure**
- [Immutable infrastructure](planning/infrastructure/immutable-infrastructure.md)
- [Infrastructure as code](planning/infrastructure/infrastructure-as-code.md)

**networking**
- [Design-first API development with OpenAPI](planning/networking/api-design-first.md)
- [API Design](planning/networking/api-design.md)
- [Choosing an API style (REST, gRPC, GraphQL)](planning/networking/api-style-selection.md)
- [API versioning and deprecation](planning/networking/api-versioning-and-deprecation.md)
- [Caching](planning/networking/caching.md)
- [Offline and Connectivity](planning/networking/offline-and-connectivity.md)
- [Pagination](planning/networking/pagination.md)
- [Real-Time Communication](planning/networking/real-time-communication.md)

**security**
- [Authentication](planning/security/authentication.md)
- [Data privacy regulations](planning/security/data-privacy-regulations.md)
- [Privacy by design](planning/security/privacy-by-design.md)
- [Privacy and security by default](planning/security/privacy.md)
- [Threat modeling](planning/security/threat-modeling.md)

**testing**
- [Test Pyramid](planning/testing/test-pyramid.md)

**ui**
- [Dashboard service is display-only](planning/ui/dashboard-service-is-display-only.md)
- [Data Display](planning/ui/data-display.md)
- [Design tokens](planning/ui/design-tokens.md)
- [Platform Design Languages](planning/ui/platform-design-languages.md)
- [Choose a rendering strategy per route, minimize client JS](planning/ui/rendering-strategy.md)
- [Separate server state from client state](planning/ui/state-management.md)

---

### Implementing (175 guidelines)


**accessibility**
- [Accessibility from day one](implementing/accessibility/accessibility.md)
- [Dynamic Type](implementing/accessibility/dynamic-type.md)
- [Font Scaling](implementing/accessibility/font-scaling.md)

**code-quality**
- [Architecture](implementing/code-quality/architecture.md)
- [Small, atomic commits](implementing/code-quality/atomic-commits.md)
- [Writing code for the AI reader](implementing/code-quality/code-for-the-ai-reader.md)
- [Completeness: finish the work, don't defer by default](implementing/code-quality/completeness.md)
- [Delete what you supersede](implementing/code-quality/delete-what-you-supersede.md)
- [Dependency Injection](implementing/code-quality/dependency-injection.md)
- [File paths](implementing/code-quality/file-paths.md)
- [Hilt dependency injection for Android](implementing/code-quality/hilt-dependency-injection.md)
- [Linting before the first PR](implementing/code-quality/linting.md)
- [Naming](implementing/code-quality/naming.md)
- [No external dependencies in core libraries](implementing/code-quality/no-external-dependencies-in-core-librari.md)
- [Nullable Reference Types](implementing/code-quality/nullable-reference-types.md)
- [Scope discipline](implementing/code-quality/scope-discipline.md)
- [Shared components and tiers](implementing/code-quality/shared-components-and-tiers.md)
- [Shell scripts](implementing/code-quality/shell-scripts.md)
- [Type hints](implementing/code-quality/type-hints.md)
- [TypeScript strictness configuration](implementing/code-quality/typescript-strictness.md)
- [Use roadmap_lib](implementing/code-quality/use-roadmaplib.md)
- [Value objects over primitive obsession](implementing/code-quality/value-objects.md)
- [Verification harnesses as agent guardrails](implementing/code-quality/verification-harness.md)
- [Xcode project hygiene](implementing/code-quality/xcode-project-hygiene.md)
- [YAML frontmatter](implementing/code-quality/yaml-frontmatter.md)

**concurrency**
- [No blocking the main thread](implementing/concurrency/concurrency.md)
- [Immutability](implementing/concurrency/immutability.md)
- [Kotlin Flow and StateFlow: lifecycle-aware state exposure](implementing/concurrency/kotlin-flow-stateflow.md)
- [Adopt Swift 6 strict concurrency incrementally](implementing/concurrency/swift6-strict-concurrency.md)

**data**
- [Access Pattern Analysis](implementing/data/access-pattern-analysis.md)
- [Advanced database indexing](implementing/data/advanced-indexing.md)
- [Database backup and recovery](implementing/data/backup-and-recovery.md)
- [Clock Systems for Sync](implementing/data/clock-systems.md)
- [Conflict Resolution](implementing/data/conflict-resolution.md)
- [Connection pooling for server and serverless backends](implementing/data/connection-pooling.md)
- [Constraints and validation](implementing/data/constraints-and-validation.md)
- [Data retention and deletion](implementing/data/data-retention-and-deletion.md)
- [Data types and type affinity](implementing/data/data-types.md)
- [Database](implementing/data/database.md)
- [Deterministic IDs](implementing/data/deterministic-ids.md)
- [Foreign keys and referential integrity](implementing/data/foreign-keys.md)
- [Indexing](implementing/data/indexing.md)
- [JSON columns and generated columns](implementing/data/json-columns.md)
- [Database naming conventions](implementing/data/naming-conventions.md)
- [Normalization and denormalization](implementing/data/normalization-and-denormalization.md)
- [Offline-First Architecture](implementing/data/offline-first-architecture.md)
- [Table partitioning and time-series data](implementing/data/partitioning-and-time-series.md)
- [Primary key strategies](implementing/data/primary-keys.md)
- [Query Optimization](implementing/data/query-optimization.md)
- [Relationship patterns](implementing/data/relationships.md)
- [Room persistence on Android](implementing/data/room-persistence.md)
- [Schema evolution and migrations](implementing/data/schema-evolution.md)
- [Sync Engine Design](implementing/data/sync-engine-design.md)
- [Sync Protocol](implementing/data/sync-protocol.md)
- [Sync Schema Design](implementing/data/sync-schema-design.md)
- [SQLite Sync Tooling](implementing/data/sync-tooling.md)
- [Transaction isolation and serialization-failure retry](implementing/data/transaction-isolation.md)
- [Transactions and Concurrency](implementing/data/transactions-and-concurrency.md)
- [Zero-downtime migrations: expand and contract](implementing/data/zero-downtime-migrations.md)

**documentation**
- [Writing comments and docs](implementing/documentation/writing-comments-and-docs.md)

**feature-management**
- [A/B testing](implementing/feature-management/ab-testing.md)
- [Debug mode](implementing/feature-management/debug-mode.md)
- [Feature flags](implementing/feature-management/feature-flags.md)

**infrastructure**
- [Containerization](implementing/infrastructure/containerization.md)
- [Kubernetes configuration and secrets](implementing/infrastructure/kubernetes-configuration.md)
- [Kubernetes workloads](implementing/infrastructure/kubernetes-workloads.md)
- [Twelve-factor configuration](implementing/infrastructure/twelve-factor-config.md)

**internationalization**
- [Localizability](implementing/internationalization/localization.md)
- [RTL layout support](implementing/internationalization/rtl-support.md)

**language**
- [Objective-C](implementing/language/objective-c.md)
- [Python](implementing/language/python.md)
- [Ruby](implementing/language/ruby.md)
- [Swift](implementing/language/swift.md)

**networking**
- [AI Cost Management](implementing/networking/ai-cost-management.md)
- [API Design](implementing/networking/api-design.md)
- [Caching](implementing/networking/caching.md)
- [Error Responses](implementing/networking/error-responses.md)
- [HTTP conditional requests and optimistic concurrency](implementing/networking/http-conditional-requests.md)
- [Idempotency keys for write APIs](implementing/networking/idempotency-keys.md)
- [MCP server design](implementing/networking/mcp-server-design.md)
- [Offline and Connectivity](implementing/networking/offline-and-connectivity.md)
- [Pagination](implementing/networking/pagination.md)
- [Rate Limiting](implementing/networking/rate-limiting.md)
- [Real-Time Communication](implementing/networking/real-time-communication.md)
- [Retry and Resilience](implementing/networking/retry-and-resilience.md)
- [Be strict and maintain: Postel reconsidered (RFC 9413)](implementing/networking/robust-protocol-maintenance.md)
- [Timeouts](implementing/networking/timeouts.md)
- [Web services](implementing/networking/web-services.md)

**observability**
- [AI Provider Observability](implementing/observability/ai-provider-observability.md)
- [Analytics](implementing/observability/analytics.md)
- [Continuous profiling](implementing/observability/continuous-profiling.md)
- [Distributed tracing and context propagation](implementing/observability/distributed-tracing.md)
- [Instrumented logging](implementing/observability/logging.md)
- [Metrics instrumentation: RED and USE](implementing/observability/metrics-red-use.md)
- [Service-level objectives and error budgets](implementing/observability/service-level-objectives.md)

**platform-integration**
- [App Intents](implementing/platform-integration/app-intents.md)
- [Background tasks](implementing/platform-integration/background-tasks.md)
- [Deep linking](implementing/platform-integration/deep-linking.md)
- [Handoff and continuity](implementing/platform-integration/handoff-and-continuity.md)
- [Notifications](implementing/platform-integration/notifications.md)
- [Use AppKit and UIKit, not SwiftUI](implementing/platform-integration/prefer-explicit-apple-apis.md)
- [Search integration](implementing/platform-integration/search-integration.md)
- [Share and inter-app data flow](implementing/platform-integration/share-and-inter-app-data.md)
- [Scriptable and automatable](implementing/platform-integration/shortcuts-and-automation.md)
- [Widgets and glanceable surfaces](implementing/platform-integration/widgets-and-glanceable-surfaces.md)

**security**
- [Agent guardrails](implementing/security/agent-guardrails.md)
- [Authentication](implementing/security/authentication.md)
- [Authorization](implementing/security/authorization.md)
- [Consent management](implementing/security/consent-management.md)
- [Content Security Policy](implementing/security/content-security-policy.md)
- [CORS](implementing/security/cors.md)
- [Data subject rights (DSAR)](implementing/security/data-subject-rights.md)
- [Dependency Security](implementing/security/dependency-security.md)
- [Input Validation](implementing/security/input-validation.md)
- [LLM and agentic application security](implementing/security/llm-application-security.md)
- [MCP tool input validation](implementing/security/mcp-input-validation.md)
- [MCP server security](implementing/security/mcp-server-security.md)
- [Passkeys and WebAuthn](implementing/security/passkeys-and-webauthn.md)
- [PII detection and redaction](implementing/security/pii-detection-and-redaction.md)
- [PII handling and classification](implementing/security/pii-handling.md)
- [Privacy and security by default](implementing/security/privacy.md)
- [Secure Storage](implementing/security/secure-storage.md)
- [Security Headers Checklist](implementing/security/security-headers-checklist.md)
- [Sender-constrained access tokens](implementing/security/sender-constrained-tokens.md)
- [Sensitive Data](implementing/security/sensitive-data.md)
- [Token Handling](implementing/security/token-handling.md)
- [Transport Security](implementing/security/transport-security.md)

**skills-and-agents**
- [Agent Structure Reference](implementing/skills-and-agents/agent-structure-reference.md)
- [Authoring Skills and Rules](implementing/skills-and-agents/authoring-skills-and-rules.md)
- [Context and memory management for agents](implementing/skills-and-agents/context-and-memory-management.md)
- [Performance: Speed and Token Efficiency](implementing/skills-and-agents/performance.md)
- [Rule Structure Reference](implementing/skills-and-agents/rule-structure-reference.md)
- [Skill Structure Reference](implementing/skills-and-agents/skill-structure-reference.md)

**testing**
- [Property-Based Testing](implementing/testing/property-based-testing.md)
- [Swift Testing](implementing/testing/swift-testing.md)
- [Test Data](implementing/testing/test-data.md)
- [Test Doubles](implementing/testing/test-doubles.md)
- [Comprehensive unit testing](implementing/testing/testing.md)
- [Unit Test Patterns](implementing/testing/unit-test-patterns.md)

**ui**
- [Always show progress](implementing/ui/always-show-progress.md)
- [Android edge-to-edge and window insets](implementing/ui/android-edge-to-edge.md)
- [Android navigation in Compose](implementing/ui/android-navigation.md)
- [Android predictive back](implementing/ui/android-predictive-back.md)
- [Animation & Motion](implementing/ui/animation-motion.md)
- [AppKit and UIKit patterns](implementing/ui/appkit-and-uikit-patterns.md)
- [Apple design language and widgets](implementing/ui/apple-liquid-glass-and-widgets.md)
- [Color](implementing/ui/color.md)
- [Jetpack Compose performance and stability](implementing/ui/compose-performance-and-stability.md)
- [Jetpack Compose side effects](implementing/ui/compose-side-effects.md)
- [Jetpack Compose: state hoisting and unidirectional data flow](implementing/ui/compose-state-and-udf.md)
- [Core Web Vitals and performance budgets](implementing/ui/core-web-vitals.md)
- [Cross-platform token adaptation](implementing/ui/cross-platform-token-adaptation.md)
- [Dashboard service is display-only](implementing/ui/dashboard-service-is-display-only.md)
- [Data Display](implementing/ui/data-display.md)
- [Design-Time Data](implementing/ui/design-time-data.md)
- [Design token distribution](implementing/ui/design-token-distribution.md)
- [Feedback Patterns](implementing/ui/feedback-patterns.md)
- [Fluent Design](implementing/ui/fluent-design.md)
- [Form Design](implementing/ui/form-design.md)
- [High DPI / Display Scaling](implementing/ui/high-dpi-display-scaling.md)
- [Iconography](implementing/ui/iconography.md)
- [Layout](implementing/ui/layout.md)
- [Material 3 theming on Android](implementing/ui/material3-theming.md)
- [Modern CSS layout and Baseline-driven adoption](implementing/ui/modern-css.md)
- [Platform Design Languages](implementing/ui/platform-design-languages.md)
- [Previews](implementing/ui/previews.md)
- [Progressive Web App installability](implementing/ui/progressive-web-app.md)
- [Spacing](implementing/ui/spacing.md)
- [State Design](implementing/ui/state-design.md)
- [Theming with tokens](implementing/ui/theming-with-tokens.md)
- [Theming](implementing/ui/theming.md)
- [Touch & Click Targets](implementing/ui/touch-click-targets.md)
- [Typography](implementing/ui/typography.md)
- [Visual Hierarchy](implementing/ui/visual-hierarchy.md)
- [Windows 11 materials (Mica and Acrylic)](implementing/ui/windows-11-materials.md)

---

### Testing (24 guidelines)

- [Agent evaluation and safety](testing/agent-evaluation-and-safety.md)
- [Contract testing for services](testing/contract-testing.md)
- [Database testing](testing/database-testing.md)
- [Design-Time Data](testing/design-time-data.md)
- [Eval-driven development for agent behavior](testing/eval-driven-development.md)
- [Flaky Test Prevention](testing/flaky-test-prevention.md)
- [Flaky test quarantine lifecycle](testing/flaky-test-quarantine.md)
- [Fuzz testing](testing/fuzzing.md)
- [Groundedness and hallucination checks](testing/groundedness-and-hallucination.md)
- [Linting from day one](testing/linting.md)
- [Mutation Testing](testing/mutation-testing.md)
- [Post-generation verification](testing/post-generation-verification.md)
- [Previews](testing/previews.md)
- [Properties of Good Tests](testing/properties-of-good-tests.md)
- [Property-Based Testing](testing/property-based-testing.md)
- [Security Testing](testing/security-testing.md)
- [Snapshot testing discipline](testing/snapshot-testing.md)
- [Test Data](testing/test-data.md)
- [Test Doubles](testing/test-doubles.md)
- [Test Pyramid](testing/test-pyramid.md)
- [Comprehensive unit testing](testing/testing.md)
- [The Testing Workflow](testing/the-testing-workflow.md)
- [Tool-call evaluation](testing/tool-call-evaluation.md)
- [Unit Test Patterns](testing/unit-test-patterns.md)

---

### Reviewing (57 guidelines)

- [Conformance: The Criterion Walk](reviewing/conformance-criterion-walk.md)
- [Writing the Review Report](reviewing/review-report-writing.md)

**accessibility**
- [Accessibility from day one](reviewing/accessibility/accessibility.md)

**code-quality**
- [Bulk operation verification](reviewing/code-quality/bulk-operation-verification.md)
- [Code hygiene: remove the old thing](reviewing/code-quality/code-hygiene.md)
- [Dependency Injection](reviewing/code-quality/dependency-injection.md)
- [File paths](reviewing/code-quality/file-paths.md)
- [Law of Demeter and Tell, Don't Ask](reviewing/code-quality/law-of-demeter.md)
- [Naming](reviewing/code-quality/naming.md)
- [No external dependencies in core libraries](reviewing/code-quality/no-external-dependencies-in-core-librari.md)
- [Scope discipline](reviewing/code-quality/scope-discipline.md)
- [Shell scripts](reviewing/code-quality/shell-scripts.md)
- [Type hints](reviewing/code-quality/type-hints.md)
- [Use roadmap_lib](reviewing/code-quality/use-roadmaplib.md)
- [Xcode project hygiene](reviewing/code-quality/xcode-project-hygiene.md)
- [YAML frontmatter](reviewing/code-quality/yaml-frontmatter.md)

**data**
- [Query Optimization](reviewing/data/query-optimization.md)

**documentation**
- [Docs match the code](reviewing/documentation/docs-match-code.md)

**infrastructure**
- [Container image security](reviewing/infrastructure/container-image-security.md)

**internationalization**
- [Localizability](reviewing/internationalization/localization.md)
- [RTL layout support](reviewing/internationalization/rtl-support.md)

**language**
- [Objective-C](reviewing/language/objective-c.md)
- [Python](reviewing/language/python.md)
- [Ruby](reviewing/language/ruby.md)
- [Swift](reviewing/language/swift.md)

**networking**
- [MCP server review checklist](reviewing/networking/mcp-server-checklist.md)
- [Hyrum's Law: all observable behavior becomes contract](reviewing/networking/observable-behavior-contract.md)
- [Rate Limiting](reviewing/networking/rate-limiting.md)
- [Timeouts](reviewing/networking/timeouts.md)

**observability**
- [Analytics](reviewing/observability/analytics.md)
- [Instrumented logging](reviewing/observability/logging.md)

**platform-integration**
- [Deep linking](reviewing/platform-integration/deep-linking.md)
- [Use AppKit and UIKit, not SwiftUI](reviewing/platform-integration/prefer-explicit-apple-apis.md)

**security**
- [Authentication](reviewing/security/authentication.md)
- [Authorization](reviewing/security/authorization.md)
- [Content Security Policy](reviewing/security/content-security-policy.md)
- [CORS](reviewing/security/cors.md)
- [Dependency Security](reviewing/security/dependency-security.md)
- [Input Validation](reviewing/security/input-validation.md)
- [LLM red teaming](reviewing/security/llm-red-teaming.md)
- [Privacy and security by default](reviewing/security/privacy.md)
- [Secure Storage](reviewing/security/secure-storage.md)
- [Security Headers Checklist](reviewing/security/security-headers-checklist.md)
- [Sensitive Data](reviewing/security/sensitive-data.md)
- [Token Handling](reviewing/security/token-handling.md)
- [Transport Security](reviewing/security/transport-security.md)
- [Vulnerability prioritization by exploitability](reviewing/security/vulnerability-prioritization.md)

**skills-and-agents**
- [Agent Lint Checklist](reviewing/skills-and-agents/agent-checklist.md)
- [Performance: Speed and Token Efficiency](reviewing/skills-and-agents/performance.md)
- [Rule Lint Checklist](reviewing/skills-and-agents/rule-checklist.md)
- [Skill Lint Checklist](reviewing/skills-and-agents/skill-checklist.md)

**testing**
- [Flaky Test Prevention](reviewing/testing/flaky-test-prevention.md)
- [Post-generation verification](reviewing/testing/post-generation-verification.md)
- [Security Testing](reviewing/testing/security-testing.md)

**ui**
- [AppKit and UIKit patterns](reviewing/ui/appkit-and-uikit-patterns.md)
- [Color](reviewing/ui/color.md)
- [Touch & Click Targets](reviewing/ui/touch-click-targets.md)

---

### Shipping (17 guidelines)

- [A/B testing](shipping/ab-testing.md)
- [Ship a privacy manifest and declare required-reason APIs](shipping/apple-privacy-manifest.md)
- [Small, atomic commits](shipping/atomic-commits.md)
- [Database backup and recovery](shipping/backup-and-recovery.md)
- [Bulk operation verification](shipping/bulk-operation-verification.md)
- [Continuous delivery](shipping/continuous-delivery.md)
- [Dependency Security](shipping/dependency-security.md)
- [Ephemeral preview environments](shipping/ephemeral-environments.md)
- [Feature flags](shipping/feature-flags.md)
- [Incident response and blameless postmortems](shipping/incident-response.md)
- [MSIX Packaging](shipping/msix-packaging.md)
- [Progressive delivery](shipping/progressive-delivery.md)
- [Schema evolution and migrations](shipping/schema-evolution.md)
- [Software supply-chain integrity](shipping/supply-chain-integrity.md)
- [Transport Security](shipping/transport-security.md)
- [Trunk-based development](shipping/trunk-based-development.md)
- [Windows ARM64 and Native AOT](shipping/windows-arm64-and-aot.md)

---

### Cookbook (16 guidelines)


**recipe-quality**
- [Behavioral Requirements](cookbook/recipe-quality/behavioral-requirements.md)
- [Completeness](cookbook/recipe-quality/completeness.md)
- [Cookbook Compliance](cookbook/recipe-quality/cookbook-compliance.md)
- [Cross-Recipe Consistency](cookbook/recipe-quality/cross-recipe-consistency.md)
- [Source Fidelity](cookbook/recipe-quality/source-fidelity.md)
- [Template Conformance](cookbook/recipe-quality/template-conformance.md)

**skills-and-agents**
- [Agent Lint Checklist](cookbook/skills-and-agents/agent-checklist.md)
- [Agent Structure Reference](cookbook/skills-and-agents/agent-structure-reference.md)
- [Authoring Skills and Rules](cookbook/skills-and-agents/authoring-skills-and-rules.md)
- [Rule Lint Checklist](cookbook/skills-and-agents/rule-checklist.md)
- [Rule Structure Reference](cookbook/skills-and-agents/rule-structure-reference.md)
- [Skill Lint Checklist](cookbook/skills-and-agents/skill-checklist.md)
- [Skill Structure Reference](cookbook/skills-and-agents/skill-structure-reference.md)

**testing**
- [Properties of Good Tests](cookbook/testing/properties-of-good-tests.md)
- [Unit Test Patterns](cookbook/testing/unit-test-patterns.md)

**ui**
- [Platform Design Languages](cookbook/ui/platform-design-languages.md)

---

### Researching (5 guidelines)


**evidence**
- [Research results document](researching/evidence/research-results-document.md)
- [Verification and trust scoring](researching/evidence/verification-and-trust-scoring.md)

**process**
- [Agentic research design lessons](researching/process/agentic-research-design-lessons.md)
- [Research methodology and sources](researching/process/research-methodology-and-sources.md)
- [Research type taxonomy](researching/process/research-type-taxonomy.md)

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
