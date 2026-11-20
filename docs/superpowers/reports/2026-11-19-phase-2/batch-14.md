# Phase 2 batch 14 report: roled parts

Eighteen topics converted to roled parts. Each one is committed on its own and was checked by `cookr roles lossless --base 0005775 --draft`, `cookr roles check` and `approve.py`, which printed `RESULT: APPROVED`. The conversion is format only: no research was added and no rule's substance changed. No `judged` record was written. "Promoted" means a rule named from text that had no RFC keyword.
## cookbook/guidelines/planning/data/cqrs-and-event-sourcing

Commit 9d88151. 18 rules; lossless: 14 moved, 0 obsolete. The four body parts (guardrail, triggers, costs
table, implementation guidance) are folded whole into `rules`; the intro is unchanged.

**promoted** (9 rules):
- "Default to a single model (CRUD over one datastore)." → `should-default-to-a-single-model`: "You SHOULD default to a single model (CRUD over one datastore)."
- "Adopt **CQRS** when one of these is concretely true:" (under the heading "Adopt ONLY when a trigger holds") → `should-adopt-cqrs-only-on-its-triggers`: "You SHOULD adopt **CQRS** only when one of these is concretely true:" (its two triggers kept as sub-bullets).
- "Adopt **event sourcing** when one of these is concretely true:" → `should-adopt-event-sourcing-only-on-its-triggers`: "You SHOULD adopt **event sourcing** only when one of these is concretely true:" (its two triggers kept as sub-bullets).
- The heading "Costs you take on (plan for each before adopting)" and the table's "Operational surface" row → `should-plan-for-each-cost-before-adopting`: "You SHOULD plan for each cost you take on, and what it requires, before adopting: eventual consistency, projection rebuilds, event versioning and the operational surface. Command handlers, event store, projectors, and read stores each add deployment, monitoring, and failure modes (`manage-complexity-through-boundaries`)."
- "**explicit-over-implicit**: model commands and events as named, versioned types; never overload one generic "update" event." → split:
  - `should-model-commands-and-events-as-named-versioned-types`: "Per **explicit-over-implicit**, you SHOULD model commands and events as named, versioned types."
  - `must-not-overload-a-generic-update-event` ("never" read as MUST NOT): "You MUST NOT ever overload one generic "update" event."
- "Keep CQRS **without** event sourcing as a valid stopping point: …" → `should-keep-cqrs-without-event-sourcing-as-a-stopping-point`: "You SHOULD keep CQRS **without** event sourcing as a valid stopping point: separating read/write models in one database is far cheaper than a full event store, and often enough."
- "Start in-process and single-store; introduce separate read stores or message infrastructure **only** when the triggering requirement demands it." → `should-start-in-process-and-single-store`: "You SHOULD start in-process and single-store, and introduce separate read stores or message infrastructure **only** when the triggering requirement demands it."
- "Define the consistency contract per use case (…) and surface it in the API." → `should-define-the-consistency-contract-per-use-case`: "You SHOULD define the consistency contract per use case (which reads may be stale, which must be strongly consistent) and surface it in the API."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none. (The trigger rules are SHOULD while `must-not-adopt-without-a-trigger` is MUST NOT; both levels are the source's own, and the MUST NOT is the stronger reading of the same requirement, so they agree.)

**unfinished**: none.

## cookbook/guidelines/planning/data/datastore-selection

Commit 6bc0b2eb. 11 rules; lossless: 3 moved, 0 obsolete. The `strong-default` bullets and the existing
`rules` bullets are named in `rules`; `decision-criteria` (its table) is `how-to`; `why-relational-is-the-default`
is `rationale`, and a new `rationale` part carries the "advocacy, not consensus" caveat.

**promoted** (3 rules):
- "Treat the relational default as a strong starting point that a real requirement can override — not as a universal law." → `should-treat-the-relational-default-as-overridable`: "The agent SHOULD treat the relational default as a strong starting point that a real requirement can override — not as a universal law."
- "Pick the store from data shape, query patterns, and measured scale." (intro) → `should-pick-the-store-from-shape-patterns-and-scale`: "The agent SHOULD pick the store from data shape, query patterns, and measured scale."
- "Choose a specialist primary store **only** when a requirement below is concrete and, where possible, measured:" → `should-choose-a-specialist-store-only-on-a-concrete-requirement`: "The agent SHOULD choose a specialist primary store **only** when a requirement in the decision criteria below is concrete and, where possible, measured."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/planning/data/swiftdata-vs-core-data

Commit 6ee42724. 15 rules; lossless: 6 moved, 0 obsolete. The existing `rules` bullets are named; the
decision-rule's lead-in and closing SHOULD, and the requirements in the SwiftData, Core Data and
interoperability notes, move into `rules`. `decision-rule` (its table) is `how-to`; what is left of the three
note parts (facts, no requirement) is `rationale`.

**promoted** (6 rules):
- "Make this a **deliberate decision**, not a reach for the newest API." (intro) → `should-make-the-choice-deliberately`: "The choice SHOULD be a **deliberate decision**, not a reach for the newest API."
- "Apply these in order; the first matching row decides." → `should-apply-the-decision-rows-in-order`: "You SHOULD apply the decision rule's rows in order; the first matching row decides."
- "Preferred for fine-grained fetch tuning, batch operations at scale, and predictable performance on large datasets." (Core Data notes) → `should-prefer-core-data-for-tuning-and-scale`: "Core Data SHOULD be preferred for fine-grained fetch tuning, batch operations at scale, and predictable performance on large datasets."
- "Define models with the `@Model` macro on a Swift class — …" → `should-define-models-with-the-model-macro`: "You SHOULD define SwiftData models with the `@Model` macro on a Swift class — no `.xcdatamodeld` file or `NSManagedObject` subclass required."
- "Use `@ModelActor` for background work; …" → `should-use-modelactor-for-background-work`: "You SHOULD use `@ModelActor` for background work; it gives clearer actor-isolation boundaries under Swift 6 strict concurrency than Core Data's `perform` closures."
- "Commonly requested items (…) did **not** ship — treat them as unavailable, not roadmap guarantees." → `should-treat-unshipped-swiftdata-features-as-unavailable`: "Commonly requested items (shared/public CloudKit sync, dynamic predicate adjustment) did **not** ship — you SHOULD treat them as unavailable, not roadmap guarantees."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none. (`should-use-swiftdata-for-greenfield-ios-17-plus` and `should-use-core-data-for-controlled-migrations` can both match one greenfield app; the decision rule's row order, kept as `should-apply-the-decision-rows-in-order`, settles it for Core Data.)

**unfinished**: none.

## cookbook/guidelines/planning/data/vector-search-and-retrieval

Commit f1a8a625. 21 rules; lossless: 13 moved, 0 obsolete. The pgvector-default, chunking, metadata-filtering
and verification parts fold whole into `rules`. `indexing` keeps the HNSW defaults and the operator list as
`how-to`; `prefer-hybrid-retrieval-over-pure-ann` keeps its four steps as `how-to`. A new `rationale` part
holds the reasons (one store, HNSW's tradeoff, why pure ANN is not enough, rerank latency), and a new
`references` part holds the "(Source: pgvector README, 2026.)" citation.

**promoted** (10 rules):
- "Treat that migration as a reversible, scale-triggered decision, not a default." → `should-treat-the-vector-database-migration-as-reversible`: "You SHOULD treat that migration to a dedicated vector database as a reversible, scale-triggered decision, not a default."
- "Use an **HNSW** index as the default." → `should-default-to-hnsw`: "You SHOULD use an **HNSW** index as the default."
- "Raise `ef_search` to trade latency for recall." → `should-raise-ef-search-for-recall`: "You SHOULD raise `ef_search` to trade latency for recall." (A tuning knob; a judge may read it as MAY.)
- "Verify current defaults against the pinned pgvector version before relying on them." → `should-verify-index-defaults-against-the-pinned-version`: "You SHOULD verify current defaults against the pinned pgvector version before relying on them."
- "Pick the distance operator that matches how the embedding model was trained — …" → `should-match-the-distance-operator-to-the-model`: "You SHOULD pick the distance operator that matches how the embedding model was trained — cosine (`<=>`) for most normalized text embeddings, inner product (`<#>`) or L2 (`<->`) when the model specifies it."
- "The dense-vs-lexical balance is workload-dependent and contested — treat fusion weights and whether to rerank as things to measure on your own eval set, not as fixed constants." → `should-measure-fusion-weights-and-reranking`: "The dense-vs-lexical balance is workload-dependent and contested — you SHOULD treat fusion weights and whether to rerank as things to measure on your own eval set, not as fixed constants."
- "Chunk documents before embedding; chunk size and overlap directly determine retrieval quality." → `should-chunk-before-embedding`: "You SHOULD chunk documents before embedding; chunk size and overlap directly determine retrieval quality."
- "There is no universal best size — start with a moderate window with small overlap and tune against a retrieval eval set." → `should-tune-the-chunk-window-against-an-eval-set`: "There is no universal best size — you SHOULD start with a moderate window with small overlap and tune against a retrieval eval set."
- "Prefer chunking on semantic/structural boundaries (…) over fixed character counts where the source structure allows it." → `should-chunk-on-semantic-boundaries`: "You SHOULD prefer chunking on semantic/structural boundaries (headings, paragraphs, code blocks) over fixed character counts where the source structure allows it."
- "Store filterable attributes (…) as ordinary columns alongside the vector, and filter on them in the same query." → `should-store-filterable-attributes-as-columns`: "You SHOULD store filterable attributes (tenant, source, document type, timestamp, access scope) as ordinary columns alongside the vector, and filter on them in the same query."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none. `should-default-to-pgvector`/`should-adopt-a-dedicated-vector-database-only-when-forced` and `should-start-with-pgvector-and-hybrid-retrieval` (from *Verification*) say much the same thing twice; both kept, as the source has both.

**unfinished**: none.

## cookbook/guidelines/planning/infrastructure/immutable-infrastructure

Commit 979516ed. 16 rules; lossless: 8 moved, 0 obsolete. All six bullet parts fold into `rules`; their three
explanatory bullets (configuration drift, containers vs. VM images, no orchestrator needed) go to a new
`rationale` part. The intro is unchanged.

**promoted** (9 rules):
- "Never patch a running server in place." (intro, kept there as the statement) → `must-not-patch-a-running-server-in-place`: "You MUST NOT ever patch a running server in place."
- "Servers are **cattle, not pets** — interchangeable and disposable, never hand-tuned and irreplaceable." → `must-treat-servers-as-cattle` ("never" read as MUST): "Servers MUST be treated as **cattle, not pets** — interchangeable and disposable, never hand-tuned and irreplaceable."
- "Keep prior image versions retained and addressable (immutable tags or digests, e.g. `app@sha256:...`) so any past release can be restored deterministically." → `should-retain-addressable-prior-images`: "You SHOULD keep prior image versions retained and addressable (…) so any past release can be restored deterministically."
- "Avoid mutable tags like `latest` for what is actually deployed; pin to an immutable digest or version tag." → `should-not-deploy-mutable-tags`: "You SHOULD avoid mutable tags like `latest` for what is actually deployed; pin to an immutable digest or version tag."
- "Pair this with **infrastructure-as-code** (see related): the artifact is built from version-controlled definitions …" → `should-build-from-version-controlled-definitions`: "You SHOULD pair this with **infrastructure-as-code** (see related): the artifact is built from version-controlled definitions (`Dockerfile`, Packer template) so builds are reproducible and reviewable."
- "Bake application code and dependencies **into** the image at build time." → `should-bake-code-and-dependencies-into-the-image`: "You SHOULD bake application code and dependencies **into** the image at build time."
- "Inject environment-specific config at **deploy/runtime** … — do not bake secrets or per-environment values into the image." → `should-inject-environment-config-at-runtime` ("do not" read as SHOULD NOT): "You SHOULD inject environment-specific config at **deploy/runtime** via environment variables or a config service, and SHOULD NOT bake secrets or per-environment values into the image."
- "Adopt heavier machinery — … — only **when a measured need justifies it** (…), not as a default." → `should-adopt-heavier-machinery-only-on-measured-need`: "You SHOULD adopt heavier machinery — Kubernetes, managed image pipelines, blue-green or canary rollout infrastructure — only **when a measured need justifies it** (scale, zero-downtime SLAs, fleet size), not as a default."
- "Faster iteration: optimize image builds (…) so rebuild-to-deploy stays quick enough that no one is tempted to patch in place." → `should-keep-image-builds-fast`: "For faster iteration, you SHOULD optimize image builds (layer caching, small base images) so rebuild-to-deploy stays quick enough that no one is tempted to patch in place."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: `should-inject-environment-config-at-runtime` is SHOULD NOT on baking secrets into the image (the source's "do not", a plain imperative). Secrets in an image are usually held to MUST NOT elsewhere in the cookbook; the level is kept as the wording carries it, for the owner to raise if wanted.

**unfinished**: none.

## cookbook/guidelines/planning/infrastructure/infrastructure-as-code

Commit 59014ea1. 27 rules; lossless: 17 moved, 0 obsolete. All six bullet parts fold into `rules`; "Floating versions break reproducibility." and the not-legal-advice note go to a new `rationale` part. The intro is unchanged; its MUST sentence is also rule `must-define-infrastructure-as-declarative-code`.

**promoted** (16 rules):
- "Reach for managed IaC platforms, Kubernetes operators, or multi-account orchestration **only when a measured need justifies the operational weight** — not as a default." → `should-adopt-heavy-iac-platforms-only-on-measured-need`: "You SHOULD reach for managed IaC platforms, Kubernetes operators, or multi-account orchestration **only when a measured need justifies the operational weight** — not as a default."
- "Start with the smallest backend and module layout that works and grow deliberately (small, reversible decisions)." → `should-start-with-the-smallest-layout-that-works`: "You SHOULD start with the smallest backend and module layout that works and grow deliberately (small, reversible decisions)."
- "Confirm data-residency and credential-handling obligations with qualified counsel." → `should-confirm-obligations-with-counsel`: "You SHOULD confirm data-residency and credential-handling obligations with qualified counsel."
- "Describe the **desired end state**, not the steps to reach it." → `should-describe-the-desired-end-state`: "You SHOULD describe the **desired end state**, not the steps to reach it."
- "Pin tool and provider versions explicitly (e.g. a `.terraform.lock.hcl` / lockfile committed to the repo)." → `should-pin-tool-and-provider-versions`: "You SHOULD pin tool and provider versions explicitly (e.g. a `.terraform.lock.hcl` / lockfile committed to the repo)."
- "Prefer mature, declarative tooling: **OpenTofu** or **Terraform** (HCL), or **Pulumi** (general-purpose languages) when programmable abstractions justify the added surface area." → `should-prefer-mature-declarative-tooling`: "You SHOULD prefer mature, declarative tooling: **OpenTofu** or **Terraform** (HCL), or **Pulumi** (general-purpose languages) when programmable abstractions justify the added surface area."
- "Run scheduled drift detection (e.g. a periodic `plan`, `pulumi refresh` + preview, or a platform's drift feature) so manual changes are caught in hours, not at the next unrelated apply when a `destroy` appears unexpectedly." → `should-run-scheduled-drift-detection`: "You SHOULD run scheduled drift detection (e.g. a periodic `plan`, `pulumi refresh` + preview, or a platform's drift feature) so manual changes are caught in hours, not at the next unrelated apply when a `destroy` appears unexpectedly."
- "When drift is real and intended, encode it in the configuration and re-apply; do not leave the divergence in place." → `should-encode-intended-drift`: "When drift is real and intended, you SHOULD encode it in the configuration and re-apply, and SHOULD NOT leave the divergence in place."
- "Factor repeated patterns into **modules** with explicit inputs/outputs; pin module versions." → `should-factor-repeated-patterns-into-modules`: "You SHOULD factor repeated patterns into **modules** with explicit inputs/outputs, and pin module versions."
- "Keep environments (dev/stage/prod) as separate state with shared modules — avoid copy-paste." → `should-keep-environments-as-separate-state`: "You SHOULD keep environments (dev/stage/prod) as separate state with shared modules — avoid copy-paste."
- "Do not emit secrets as outputs; write them directly to a secrets manager during apply and have apps fetch at runtime." → `should-not-emit-secrets-as-outputs`: "You SHOULD NOT emit secrets as outputs; write them directly to a secrets manager during apply and have apps fetch at runtime."
- "Pulumi encrypts values marked `secret` in state, but restrict state read access regardless." → `should-restrict-state-read-access`: "Pulumi encrypts values marked `secret` in state, but you SHOULD restrict state read access regardless."
- "Run `plan` in CI on every pull request and surface the diff in the PR." → `should-run-plan-in-ci-on-every-pull-request`: "You SHOULD run `plan` in CI on every pull request and surface the diff in the PR."
- "Be wary of resources marked for replacement — confirm the underlying cause (a deliberate change vs. drift vs. a provider upgrade) before applying." → `should-confirm-the-cause-of-replacements`: "You SHOULD be wary of resources marked for replacement, and confirm the underlying cause (a deliberate change vs. drift vs. a provider upgrade) before applying."
- "For the S3 backend, prefer native S3 lockfile-based locking (`use_lockfile = true`, available since 2025); a DynamoDB lock table remains valid and can run alongside it during migration." → `should-prefer-native-s3-lockfile-locking`: "For the S3 backend, you SHOULD prefer native S3 lockfile-based locking (`use_lockfile = true`, available since 2025); a DynamoDB lock table remains valid and can run alongside it during migration."
- "Use a consistent state key convention (`<env>/<component>/terraform.tfstate`) so IAM policies can scope per environment." → `should-use-a-consistent-state-key-convention`: "You SHOULD use a consistent state key convention (`<env>/<component>/terraform.tfstate`) so IAM policies can scope per environment."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: `should-not-emit-secrets-as-outputs` is SHOULD NOT (the source's "Do not", a plain imperative), yet it is the means of keeping `must-not-expose-secrets-in-plaintext-state` (MUST NOT): the source says state stores outputs in plaintext for HCL tools, so a secret emitted as an output breaks the MUST NOT. Source: "**Secrets MUST NOT be exposed in plaintext state.** State files store resource attributes (including outputs) in plaintext for HCL tools. Do not emit secrets as outputs; …". Levels left as worded.

**unfinished**: none.

## cookbook/guidelines/planning/networking/api-design-first

Commit 5cc3a6a5. 21 rules; lossless: 9 moved, 0 obsolete. *When this applies*, *Core requirements*, *Pin the version*, *Lint in CI*, *Contract checks both ways* and *Anti-patterns* fold into `rules` (the two scope bullets become sub-bullets of `should-define-non-trivial-apis-contract-first`). The derivatives table stays as `how-to`; the OpenAPI 3.2.0 release note is `rationale`; the 3.1.0 spec link is `references`. The anti-patterns are MUST NOT requirements, so they became rules, not review-focus text.

**promoted** (7 rules):
- "Lint with a spec linter (e.g." → `should-lint-with-a-spec-linter`: "You SHOULD lint with a spec linter (e.g. **Spectral**) using a checked-in `.spectral.yaml` ruleset; extend the built-in OpenAPI ruleset and add house rules (naming, required `operationId`, error-schema presence)."
- "Consider adding security-focused rules (e.g. an OWASP API Security ruleset) to catch missing auth and unconstrained inputs at design time." → `should-consider-security-lint-rules`: "You SHOULD consider adding security-focused rules (e.g. an OWASP API Security ruleset) to catch missing auth and unconstrained inputs at design time."
- "Add a breaking-change diff check (e.g." → `should-add-a-breaking-change-diff-check`: "You SHOULD add a breaking-change diff check (e.g. `oasdiff`) so backward-incompatible edits are caught before merge."
- "Use **OpenAPI 3.1.x** as the baseline (full JSON Schema 2020-12 alignment)." → `should-use-openapi-3-1-as-the-baseline`: "You SHOULD use **OpenAPI 3.1.x** as the baseline (full JSON Schema 2020-12 alignment)."
- "Adopt it **only** when your toolchain — generators, linters, mock servers — fully supports it; otherwise stay on 3.1.x." → `should-adopt-openapi-3-2-only-with-full-tool-support`: "You SHOULD adopt OpenAPI 3.2 **only** when your toolchain — generators, linters, mock servers — fully supports it; otherwise stay on 3.1.x."
- "Verify tool support before relying on 3.2-only features." → `should-verify-tool-support-before-3-2-features`: "You SHOULD verify tool support before relying on 3.2-only features."
- "Skip the full ceremony only for throwaway prototypes you will delete." → `should-skip-the-ceremony-only-for-throwaway-prototypes`: "You SHOULD skip the full ceremony only for throwaway prototypes you will delete."

- Also promoted, from the intro (kept there as the statement): "Write the OpenAPI specification before implementing any endpoint, and treat that document as the single source of truth." → `should-write-the-spec-before-any-endpoint`: "You SHOULD write the OpenAPI specification before implementing any endpoint, and treat that document as the single source of truth."
- Not promoted but re-levelled: "Always state the `openapi:` version explicitly in the document; **MUST NOT** leave it implicit or mixed across files." → `must-state-the-openapi-version-explicitly`: "You MUST always state the `openapi:` version explicitly in the document; **MUST NOT** leave it implicit or mixed across files." ("Always" read as MUST.)

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none. (`should-define-non-trivial-apis-contract-first` is SHOULD while `must-treat-the-spec-as-the-source-of-truth` and `must-not-generate-the-spec-from-code` are MUST/MUST NOT; the source has these levels, and they do not conflict: the MUSTs bind whenever a spec exists or a new API is built.)

**unfinished**: none.

## cookbook/guidelines/planning/networking/api-style-selection

Commit 0e17b4ac. 14 rules; lossless: 9 moved, 0 obsolete. *Decision factors*, the choose-when and requirement bullets of *REST*, *gRPC* and *GraphQL*, and *Mixing styles* fold into `rules`. The REST and gRPC strengths and trade-offs stay in their own parts as `how-to`. The three *Anti-patterns* bullets were reviewer text, so they open `look-for` verbatim, each labelled with the rule it checks.

**promoted** (6 rules):
- "Use when clients drive aggregation across many resources and over/under-fetching with REST is a measured problem." → `should-choose-graphql-for-measured-aggregation-needs`: "You SHOULD use GraphQL when clients drive aggregation across many resources and over/under-fetching with REST is a measured problem: choose GraphQL when first-party clients need to compose data from several sources in one round trip and field-level shape varies by screen."
- "**Choose GraphQL when** first-party clients need to compose data from several sources in one round trip and field-level shape varies by screen." → `should-choose-graphql-for-measured-aggregation-needs`: "You SHOULD use GraphQL when clients drive aggregation across many resources and over/under-fetching with REST is a measured problem: choose GraphQL when first-party clients need to compose data from several sources in one round trip and field-level shape varies by screen."
- "Caching is field-level and client-driven, not HTTP-intermediary; do not assume CDN caching applies." → `should-not-assume-cdn-caching-for-graphql`: "GraphQL caching is field-level and client-driven, not HTTP-intermediary; you SHOULD NOT assume CDN caching applies."
- "Treat the schema as a versioned contract; prefer additive evolution and field deprecation over breaking changes." → `should-treat-the-graphql-schema-as-a-versioned-contract`: "You SHOULD treat the GraphQL schema as a versioned contract, and prefer additive evolution and field deprecation over breaking changes."
- "Use for low-latency internal service-to-service calls and streaming, per the official model (RPC over HTTP/2 with Protocol Buffers as the IDL and serialization; see references)." → `should-choose-grpc-for-internal-low-latency-calls`: "You SHOULD use gRPC for low-latency internal service-to-service calls and streaming, per the official model (RPC over HTTP/2 with Protocol Buffers as the IDL and serialization; see references): choose gRPC when callers are internal services, latency/throughput matter, you want generated client/server stubs across languages, or you need uni-/bi-directional streaming."
- "**Choose gRPC when** callers are internal services, latency/throughput matter, you want generated client/server stubs across languages, or you need uni-/bi-directional streaming." → `should-choose-grpc-for-internal-low-latency-calls`: "You SHOULD use gRPC for low-latency internal service-to-service calls and streaming, per the official model (RPC over HTTP/2 with Protocol Buffers as the IDL and serialization; see references): choose gRPC when callers are internal services, latency/throughput matter, you want generated client/server stubs across languages, or you need uni-/bi-directional streaming."
- "**Choose REST when** consumers are diverse/external, resources map cleanly to URLs, and HTTP caching (`ETag`, `Cache-Control`, CDN) adds value." → `should-choose-rest-for-diverse-consumers-and-http-caching`: "You SHOULD choose REST when consumers are diverse/external, resources map cleanly to URLs, and HTTP caching (`ETag`, `Cache-Control`, CDN) adds value."
- "Pin contracts to a dated OpenAPI revision; version the API (`/v1`) per `api-design`." → `should-pin-rest-contracts-and-version-the-api`: "You SHOULD pin contracts to a dated OpenAPI revision and version the API (`/v1`) per `api-design`."

- Also promoted, from the intro (kept there as the statement): "Pick the API style from who consumes the endpoint and the shape of its traffic, not from fashion." → `should-pick-the-style-from-consumer-and-traffic`: "You SHOULD pick the API style from who consumes the endpoint and the shape of its traffic, not from fashion."

**bars**: `look-for` moved (the three anti-patterns bullets) plus 11 authored lines for the rules they do not cover; `a-complete-review-must-establish` authored; `a-build-must-establish` authored.

**contradictions**: the anti-pattern "Exposing internal gRPC contracts directly to untrusted/public clients." reads as a flat prohibition, while its rule `should-not-expose-raw-grpc-publicly` is "You **SHOULD NOT** expose raw gRPC as a public third-party API without a REST/Connect façade." Left at SHOULD NOT, as the source states it.

**unfinished**: none.

## cookbook/guidelines/planning/networking/api-versioning-and-deprecation

Commit 862240f5. 18 rules; lossless: 7 moved, 0 obsolete. *Evolve additively first*, the scheme requirements and the *Deprecation lifecycle* steps and bullets fold into `rules`. The scheme table (with its lead-in kept verbatim) is the `how-to` part `versioning-schemes`; the header block is the `examples` part `deprecation-headers-example`. The four *Anti-patterns* bullets were reviewer text, so they open `look-for` verbatim, each labelled with its rule.

**promoted** (7 rules):
- "Pick ONE scheme and apply it consistently across the whole surface." → `should-pick-one-scheme-for-the-whole-surface`: "You SHOULD pick ONE versioning scheme (URI path, media-type / header, or query param) and apply that ONE scheme consistently across the whole surface."
- "When retiring a version or endpoint, run this sequence and publish the timeline before the first signal ships:" → `should-run-the-deprecation-sequence`: "When retiring a version or endpoint, you SHOULD run this sequence (announce, set a removal date, document, honor a migration window) and publish the timeline before the first signal ships."
- "**Announce** — set the `Deprecation` response header (RFC 9745, published March 2025) on affected responses." → `should-announce-with-the-deprecation-header`: "**Announce**: you SHOULD set the `Deprecation` response header (RFC 9745, published March 2025) on affected responses. Value is the deprecation timestamp or `true`."
- "**Set a removal date** — add the `Sunset` header (RFC 8594) with the HTTP-date after which behavior is undefined." → `should-set-a-removal-date-with-sunset`: "**Set a removal date**: you SHOULD add the `Sunset` header (RFC 8594) with the HTTP-date after which behavior is undefined."
- "**Document** — record the change, replacement, and dates in a public changelog and the OpenAPI/spec (`deprecated: true`)." → `should-document-the-deprecation`: "**Document**: you SHOULD record the change, replacement, and dates in a public changelog and the OpenAPI/spec (`deprecated: true`)."
- "**Honor a migration window** — give consumers a published, generous window before removal; do not shorten it after announcement." → `should-honor-a-migration-window`: "**Honor a migration window**: you SHOULD give consumers a published, generous window before removal, and SHOULD NOT shorten it after announcement."
- "Per the observable-behavior-contract guideline (Hyrum's Law), assume consumers depend on *every* observable detail — undocumented field order, error text, timing — so changing those can break someone even when the spec did not." → `should-assume-consumers-depend-on-every-observable-detail`: "Per the observable-behavior-contract guideline (Hyrum's Law), you SHOULD assume consumers depend on *every* observable detail — undocumented field order, error text, timing — so changing those can break someone even when the spec did not."


**bars**: `look-for` moved (the four anti-patterns bullets) plus 14 authored lines for the rules they do not cover; `a-complete-review-must-establish` authored; `a-build-must-establish` authored.

**contradictions**:
- `must-version-breaking-changes` ("You **MUST** treat these as breaking and requiring a version: …") and `must-not-ship-breaking-changes-in-place` ("Breaking changes **MUST** be versioned, never shipped in place.") state the same requirement twice; both kept, as the source has both.
- `must-pair-deprecation-headers-with-documentation` carries two levels in one sentence: "Deprecations **SHOULD** use `Deprecation` + `Sunset` headers plus a changelog entry; headers are hints, so they **MUST** be paired with documentation, not used alone." Kept as one rule, as the source wrote it.

**unfinished**: none.

## cookbook/guidelines/planning/security/data-privacy-regulations

Commit 6a32ae0b. 16 rules; lossless: 7 moved, 0 obsolete. The regime bullets, *Shared principles to encode*, the controller/processor requirements and *Before you collect* fold into `rules`. The regimes table and the controller/processor definitions stay as `how-to` parts; the injunction forecast and the "build to them once" reason go to `rationale`. The "These appear across GDPR …:" lead-in maps to three of the six principle rules (the most that one entry allows), and `rationale` names all six.

**promoted** (7 rules):
- "Determine applicable regimes from **user geography** and **data types** (special-category/sensitive data raises the bar)." → `should-determine-applicable-regimes-before-collecting`: "Before you collect, you SHOULD determine applicable regimes from **user geography** and **data types** (special-category/sensitive data raises the bar)."
- "Confirm a lawful basis or required notice/opt-out posture — and record it." → `should-confirm-the-lawful-basis-before-collecting`: "Before you collect, you SHOULD confirm a lawful basis or required notice/opt-out posture — and record it."
- "Confirm minimization, retention, and a deletion path exist for each field." → `should-confirm-minimization-retention-and-deletion-per-field`: "Before you collect, you SHOULD confirm minimization, retention, and a deletion path exist for each field."
- "These appear across GDPR and most US state laws, so build to them once:" → split:
  - `must-record-a-lawful-basis`: "**lawful basis**: You **MUST** establish and record a lawful basis (GDPR) or required notice/opt-out posture (US) before collection."
  - `must-collect-only-needed-data`: "**data minimization**: You **MUST** collect only data needed for the stated purpose."
  - `must-limit-use-to-disclosed-purposes`: "**purpose limitation**: You **MUST** use data only for the purposes disclosed at collection. New purpose requires new basis/notice."
- "Default to *not* collecting." → `should-default-to-not-collecting`: "You SHOULD default to *not* collecting."


**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: the *Before you collect* steps had no keyword, so they were promoted to SHOULD. Two of them restate MUST rules at a weaker level:
- `should-confirm-the-lawful-basis-before-collecting` ("Confirm a lawful basis or required notice/opt-out posture — and record it.") against `must-record-a-lawful-basis` ("You **MUST** establish and record a lawful basis (GDPR) or required notice/opt-out posture (US) before collection.").
- `should-confirm-minimization-retention-and-deletion-per-field` against `must-collect-only-needed-data` and `must-define-retention-per-data-type`.

Both levels were left as found.

**unfinished**: none.

## cookbook/guidelines/planning/security/privacy-by-design

Commit c9dc163e. 18 rules; lossless: 4 moved, 0 obsolete. The requirements of all five sections fold into `rules`. The data-flow map table becomes the `how-to` part `data-flow-map-dimensions`, and its "For each category of personal data, record:" lead-in becomes a sub-bullet of `must-produce-a-maintained-data-flow-map`, so it carries that rule's MUST and is not promoted. The cost sentence of *Adopt heavier controls only when justified* goes to `rationale`.

**promoted** (3 rules):
- "Per YAGNI, adopt these **only when a measured need justifies them** — driven by data sensitivity, regulatory scope, or DPIA findings — not as a reflexive default." → `should-adopt-heavier-controls-only-when-justified`: "Per YAGNI, you SHOULD adopt privacy-enhancing infrastructure (dedicated tokenization vaults, differential-privacy pipelines, confidential-compute enclaves, per-tenant key management) **only when a measured need justifies them** — driven by data sensitivity, regulatory scope, or DPIA findings — not as a reflexive default."
- "Start with minimization and de-identification; escalate to specialized tooling when the risk profile demands it." → `should-start-with-minimization-and-de-identification`: "You SHOULD start with minimization and de-identification, and escalate to specialized tooling when the risk profile demands it."
- "For each category of personal data, record:" → `must-produce-a-maintained-data-flow-map`: "Before writing code, you **MUST** produce a personal-data flow map and treat it as a maintained artifact, not a throwaway sketch."

- Also promoted, from the intro (kept there as the statement): "Build privacy into the system from the first design decision, not as a later bolt-on." → `should-build-privacy-in-from-the-first-design-decision`: "You SHOULD build privacy into the system from the first design decision, not as a later bolt-on."
- Also promoted, from the intro: "This guidance is engineering practice, **NOT** legal advice — consult counsel for jurisdiction-specific obligations." → `should-consult-counsel-for-jurisdiction-specific-obligations`: "This guidance is engineering practice, **NOT** legal advice; you SHOULD consult counsel for jurisdiction-specific obligations."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: `must-delete-or-de-identify-when-purpose-ends` ("Define retention up front and **MUST** delete or de-identify data when its purpose ends.") gives "Define retention up front" no keyword of its own, so its level is ambiguous. It was kept verbatim under the rule's MUST.

**unfinished**: none.

## cookbook/guidelines/planning/security/threat-modeling

Commit c81f3e01. 10 rules; lossless: 4 moved, 0 obsolete. *The four questions*, the STRIDE requirements and *Make it continuous* fold into `rules`. The four numbered questions are kept verbatim as sub-bullets of `should-anchor-sessions-on-the-four-questions`; their step imperatives (Diagram, Mark, Enumerate, Decide, Validate) are that rule's detail and were not promoted separately. The STRIDE table is the `how-to` part `stride-categories`, and the Manifesto quote goes to `rationale`. The four *Anti-patterns* bullets were reviewer text, so they open `look-for` verbatim, each labelled with its rule.

**promoted** (3 rules):
- "Keep each session lightweight: a focused diagram and a short threat list per feature beats an exhaustive enterprise-wide model done once." → `should-keep-each-session-lightweight`: "You SHOULD keep each session lightweight: a focused diagram and a short threat list per feature beats an exhaustive enterprise-wide model done once."
- "Use STRIDE to drive question 2 systematically." → `should-use-stride-for-question-two`: "You SHOULD use STRIDE to drive question 2 systematically, applying each category to elements touching a trust boundary."
- "Apply each category to elements touching a trust boundary:" → `should-use-stride-for-question-two`: "You SHOULD use STRIDE to drive question 2 systematically, applying each category to elements touching a trust boundary."
- "Anchor every modeling session on the four questions from the Threat Modeling Manifesto (threatmodelingmanifesto.org):" → `should-anchor-sessions-on-the-four-questions`: "You SHOULD anchor every modeling session on the four questions from the Threat Modeling Manifesto (threatmodelingmanifesto.org)."


**bars**: `look-for` moved (the four anti-patterns bullets) plus 6 authored lines for the rules they do not cover; `a-complete-review-must-establish` authored; `a-build-must-establish` authored.

**contradictions**: the "Controls without threats" anti-pattern faults a control with no recorded threat. The nearest rule, `should-map-each-threat-to-a-linked-control` ("Each identified threat **SHOULD** map to a concrete control …"), runs the other way, threat to control, and no rule states "every control MUST name the threat it addresses". The gap was left as found; only the intro implies that direction.

**unfinished**: none.

## cookbook/guidelines/planning/testing/test-pyramid

Commit 7110d85e. 9 rules; lossless: 7 moved, 0 obsolete. The intro keeps its H1 and its ratio statement. Its bullets split three ways: the descriptions go to the `how-to` part `test-kinds`, and the instructions become rules. The two near-duplicate *The shape is context-dependent* parts fold into three rules and a `rationale` part. The base is hard-wrapped and lossless reads it line by line, so the rules and rationale keep the source's line breaks verbatim. That is why the intro's wrapped fragments are the only moved entries.

**promoted** (5 rules):
- "Use real databases, real / file systems, real HTTP where practical." → `should-use-real-dependencies-in-integration-tests`: "Integration tests SHOULD use real databases, real file systems, real HTTP where practical."
- "Reserve for critical user journeys." → `should-reserve-e2e-for-critical-journeys`: "You SHOULD reserve E2E tests for critical user journeys."
- "If you're unsure what kind of test to write, write a unit test." → `should-default-to-a-unit-test`: "If you're unsure what kind of test to write, you SHOULD write a unit test."
- "If the unit test can't / cover the behavior (e.g., database queries, UI rendering), escalate to integration." → `should-escalate-to-integration-when-unit-cannot-cover`: "If the unit test can't cover the behavior (e.g., database queries, UI rendering), you SHOULD escalate to integration."
- Not promoted but reworded: "E2E tests — … Expensive, brittle, SHOULD be used sparingly." → `should-use-e2e-tests-sparingly`: "E2E tests SHOULD be used sparingly." (The keyword was in the source; "Expensive, brittle." stays in `test-kinds`.)

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**:
- `should-follow-the-80-15-5-ratio` ("Projects SHOULD follow the Google SWE Book ratio: **80% unit / 15% integration / 5% E2E**.") conflicts with `should-choose-the-distribution-per-system` ("Teams SHOULD choose the test distribution per system based on where risk actually lives, not a fixed ratio."). Left unfixed.
- `should-choose-the-distribution-per-system` holds two near-identical sentences, one from each base part ("…not a fixed ratio." / "…rather than forcing a fixed ratio."). Both kept, as the source had both.

**unfinished**: none.

## cookbook/guidelines/planning/ui/design-tokens

Commit 5f01b732. 16 rules; lossless: 2 moved, 0 obsolete. *Single source of truth*, *Three tiers*, *Theming and modes* and *Accessibility and validation* fold into `rules`, keeping their wording verbatim. The tier table is the `how-to` part `token-tiers`. The three *Anti-patterns* "Do **NOT**" bullets were reviewer text restating MUST rules, so they open `look-for` verbatim, each labelled with its rule. The stray privacy note goes to `rationale`.

**promoted** (2 rules):
- "Pin to a dated revision (e.g." → `should-pin-a-dated-dtcg-revision`: "You SHOULD pin to a dated revision (e.g. `2025.10`) rather than tracking the living draft, which carries a do-not-implement notice."
- "Use three layers so values change in one place and intent stays stable:" → `should-use-three-layers`: "You SHOULD use three layers (primitive, semantic, component) so values change in one place and intent stays stable across the three."

- Also promoted, from the intro (kept there as the statement): "Express every UI design decision — color, spacing, typography, radius, motion, elevation, opacity — once as a named **design token** in a single platform-agnostic source of truth, then generate platform artifacts from it." → `should-express-every-decision-as-a-token`: "You SHOULD express every UI design decision — … — once as a named **design token** in a single platform-agnostic source of truth, then generate platform artifacts from it."

**bars**: `look-for` moved (the three anti-patterns bullets) plus 13 authored lines for the rules they do not cover; `a-complete-review-must-establish` authored; `a-build-must-establish` authored.

**contradictions**:
- `should-generate-platform-outputs` ("Platform outputs … **SHOULD** be generated by a build step (e.g. Style Dictionary) — never hand-maintained copies.") pairs SHOULD with "never". Kept at SHOULD as worded.
- `should-express-every-decision-as-a-token` (SHOULD, promoted from the intro) sits beside `must-keep-one-shared-source` ("Design decisions **MUST** live in one shared source"), which covers the same single-source requirement at MUST.
- The note "> Privacy/compliance note: this is engineering guidance, not legal advice." looks misplaced in a design-tokens topic. Kept, in `rationale`.

**unfinished**: none.

## cookbook/guidelines/planning/ui/rendering-strategy

Commit 6effbfbe. 15 rules; lossless: 4 moved, 0 obsolete. *Core principle*, the strategy bullets, the RSC note and *Decision hygiene* fold into `rules`. The route-type table is the `how-to` part `strategy-by-route-type`. The decision-variable framing, the INP/FID note and the RSC background (default for React, framework-only, Next.js maturity, complexity) go to `rationale`, each labelled with its rule.

**promoted** (4 rules):
- "Frame rendering as an architecture-selection decision, not a framework choice." → `should-frame-rendering-as-architecture-selection`: "You SHOULD frame rendering as an architecture-selection decision, not a framework choice."
- "Optimize for INP and LCP; do **not** target FID." → `should-optimize-for-inp-and-lcp`: "You SHOULD optimize for INP and LCP, and SHOULD **not** target FID."
- "**React Router v7 RSC support is newer and less stable** — treat it as evolving, and pin to a tested release before relying on it." → `should-pin-react-router-rsc-to-a-tested-release`: "**React Router v7 RSC support is newer and less stable**; you SHOULD treat it as evolving, and pin to a tested release before relying on it."
- "Adopt it deliberately, not reflexively." → `should-adopt-rsc-deliberately`: "You SHOULD adopt RSC deliberately, not reflexively."

- Also promoted, from the intro (kept there as the statement): "Choose the strategy per route based on that route's job, and default to shipping less client JS." → `should-default-to-less-client-js`: "You SHOULD choose the strategy per route based on that route's job, and default to shipping less client JS."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none found.

**unfinished**: none.

## cookbook/guidelines/planning/ui/state-management

Commit ba3f7c32. 9 rules; lossless: 3 moved, 0 obsolete. The *Requirements* part already held named rules, so it became `rules.md` verbatim and keeps its existing rule names, which have no must-/should- prefix. The decision-order list became the sub-items of one promoted rule, `choose-a-mechanism-in-decision-order`; its step imperatives are that rule's detail. The state table is `how-to` (`two-kinds-of-state`), and the library list, without its three instruction sentences, is `examples` (`example-libraries`). *Anti-patterns to flag in review* became `look-for` verbatim, each bullet labelled with its rule.

**promoted** (3 rules):
- "These are deliberate, swappable choices — name the role, not the brand." → `name-the-role-not-the-brand`: "State libraries are deliberate, swappable choices; you SHOULD name the role, not the brand."
- "Libraries in this space churn; treat the pattern as durable and the tool as an implementation detail." → `treat-the-tool-as-an-implementation-detail`: "Libraries in this space churn; you SHOULD treat the pattern as durable and the tool as an implementation detail."
- "Reach for one only when local state and lifting genuinely fall short (see YAGNI)." → `client-store-only-when-local-state-falls-short`: "You SHOULD reach for one client-store library only when local state and lifting genuinely fall short (see YAGNI)."

- Also promoted: the *How to choose a mechanism (decision order)* list (no keyword) → `choose-a-mechanism-in-decision-order`: "You SHOULD choose a state mechanism by asking, in order:", followed by the five numbered questions verbatim.

**bars**: `look-for` moved (*Anti-patterns to flag in review*, its four bullets) plus 5 authored lines for `local-state-for-client-state` and the four promoted rules; `a-complete-review-must-establish` authored; `a-build-must-establish` authored.

**contradictions**: `separate-server-and-client` holds "Do not store fetched server data in the same construct used for UI toggles." under its MUST, while `no-hand-cached-server-state` puts the nearby case, hand-caching server data in a global client store, at SHOULD NOT. Both were left at their source levels.

**unfinished**: none.

## cookbook/guidelines/researching/evidence/research-results-document

Commit 5d4db00a. 4 rules; lossless: 0 moved, 0 obsolete. Every base sentence survives verbatim. *Per-claim record* becomes one rule whose sub-bullets are the seven fields, word for word. *Document container* becomes one rule, and *Provenance standards to align with* is the `references` part.

**promoted** (2 rules):
- "Capture provenance, not prose." (intro, kept there) → `should-capture-provenance-not-prose`: "You SHOULD capture provenance, not prose."
- The heading "Provenance standards to align with" (a heading, no sentence) → `should-align-with-provenance-standards`: "The record SHOULD align with the provenance standards listed under *Provenance standards to align with*." The heading is the only place the topic states this instruction. It is reported here because it has no source sentence.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none found.

**unfinished**: none.

## cookbook/guidelines/researching/evidence/verification-and-trust-scoring

Commit 6681b43e. 4 rules; lossless: 0 moved, 0 obsolete. Every base sentence survives verbatim. The intro keeps its statement, and its SHOULD/MUST clauses are restated as `should-verify-with-the-domain-framework`, `should-score-on-the-common-scale` and `must-apply-the-domain-ceiling`. The domain-ceiling sentence moves from *Scoring* into `rules`, and the *False-positive catalog* sentence becomes `should-score-false-positive-patterns-low`. *Verification frameworks*, *Domain bars* and the score blend stay as `how-to` parts.

**promoted**: none. Every rule carries the source's own keyword.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none found.

**unfinished**: none.
