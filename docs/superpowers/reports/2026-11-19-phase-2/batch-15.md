# Phase 2 batch 15 report

Twenty topics converted to roled parts: three research-process guidelines, ten shipping guidelines, six storytelling guidelines and one testing guideline. No topic had text written for a reviewer, so in every topic all three bar parts (`look-for`, `a-complete-review-must-establish`, `a-build-must-establish`) are **authored**, one line per rule, from the topic's own rules.

## Where this batch differs from the brief

- **A clause holding two keywords cannot be split.** When one clause carries MUST and SHOULD ("a red pipeline **MUST** block release and **SHOULD** be treated as a stop-the-line event"), `cookr roles lossless` refuses to map it to two rules, with "the matched clause drops its MUST". The clause stays whole in one rule. `continuous-delivery` needed a fix commit for this (see its section).
- **A base sentence is never obsolete.** An old `###` sub-heading in the topic's own base cannot be marked obsolete ("a sentence of the topic's own base is never obsolete; only a folded copy's may be"). It is mapped as moved to the part that now carries it. No obsolete entries were written in this batch.
- **A colon lead-in maps to its rules.** Where a lead-in ending in ":" was removed, it maps to the rules it introduced, and a `rationale` bullet naming those rules holds its words verbatim.
- **Embedded imperatives.** A plain imperative sentence inside a keyword bullet ("Audit `runtimes/` folders before shipping.") was split out as its own SHOULD rule wherever it was a separate sentence. An imperative inside the same clause as a keyword stays with that rule.

## Summary

| Topic | Commit | Rules | Moved | Obsolete | Promoted |
|---|---|---|---|---|---|
| `researching/process/agentic-research-design-lessons` | `c44ee784` | 18 | 16 | 0 | 18 |
| `researching/process/research-methodology-and-sources` | `493201ea` | 10 | 0 | 0 | 8 |
| `researching/process/research-type-taxonomy` | `cbcc5fc3` | 6 | 1 | 0 | 3 |
| `shipping/apple-privacy-manifest` | `ae03565f` | 18 | 6 | 0 | 11 |
| `shipping/bulk-operation-verification` | `5e35ca57` | 8 | 7 | 0 | 5 |
| `shipping/continuous-delivery` | `711bce08` + `ca23a021` | 16 | 3 | 0 | 6 |
| `shipping/ephemeral-environments` | `62cc1c86` | 22 | 10 | 0 | 7 |
| `shipping/incident-response` | `0fb54d92` | 22 | 7 | 0 | 6 |
| `shipping/msix-packaging` | `0ceebe87` | 4 | 4 | 0 | 1 |
| `shipping/progressive-delivery` | `2608b670` | 17 | 6 | 0 | 6 |
| `shipping/supply-chain-integrity` | `e0cbc601` | 19 | 16 | 0 | 12 |
| `shipping/trunk-based-development` | `6138f245` | 22 | 5 | 0 | 13 |
| `shipping/windows-arm64-and-aot` | `47578bd3` | 18 | 6 | 0 | 6 |
| `storytelling/craft` | `cccf9131` | 3 | 0 | 0 | 0 |
| `storytelling/ecosystem` | `dc7fc357` | 3 | 0 | 0 | 0 |
| `storytelling/explanation` | `fd7772b2` | 3 | 0 | 0 | 0 |
| `storytelling/grounded-synthesis` | `316596a6` | 4 | 0 | 0 | 0 |
| `storytelling/narrative-arc` | `83efc3b6` | 3 | 0 | 0 | 0 |
| `storytelling/positioning` | `db82263a` | 3 | 0 | 0 | 0 |
| `testing/agent-evaluation-and-safety` | `3d01e5c7` | 21 | 5 | 0 | 7 |

## cookbook/guidelines/researching/process/agentic-research-design-lessons

The section parts held unlabelled lesson bullets; every bullet became a named rule and the section parts were removed. Parts are now intro, rules and the three bars.

**promoted** (18 rules):
- "The orchestrator **plans and synthesizes; it never does ground research itself.**" → `must-not-do-ground-research-in-orchestrator`: "The orchestrator SHOULD plan and synthesize; it MUST NOT do ground research itself." ("never" read as MUST NOT; "plans and synthesizes" as SHOULD.)
- "Budget per-subtopic specialists with isolated context." → `should-budget-isolated-subtopic-specialists`: "SHOULD budget per-subtopic specialists with isolated context."
- "**Outline before searching;** reflect at both supervisor and worker level." → split in 2:
  - `should-outline-before-searching`: "SHOULD outline before searching."
  - `should-reflect-at-supervisor-and-worker-level`: "SHOULD reflect at both supervisor and worker level."
- "Stop on **coverage** (two independent sources, or one authoritative one), not on a loop count." → `should-stop-on-coverage`: "SHOULD stop on coverage (two independent sources, or one authoritative one), not on a loop count."
- "Multi-engine, domain-routed sources; **rerank and quality-gate before the LLM sees them.**" → split in 2:
  - `should-use-multi-engine-domain-routed-sources`: "Sources SHOULD be multi-engine and domain-routed."
  - `should-rerank-and-quality-gate-sources`: "Sources SHOULD be reranked and quality-gated before the LLM sees them."
- "Filter by freshness and authority / venue reputation." → `should-filter-by-freshness-and-authority`: "SHOULD filter sources by freshness and authority / venue reputation."
- "**Read full pages, not snippets.**" → `should-read-full-pages`: "SHOULD read full pages, not snippets."
- "A **dedicated reviewer** with explicit acceptance criteria." → `should-use-dedicated-reviewer`: "SHOULD use a dedicated reviewer with explicit acceptance criteria."
- "**Cross-source corroboration** is the primary anti-hallucination defense." → `should-corroborate-across-sources`: "Claims SHOULD be corroborated across sources; cross-source corroboration is the primary anti-hallucination defense."
- "Check URL health / citation existence — even top tools hallucinate 3-13% of URLs." → `should-check-url-health`: "SHOULD check URL health / citation existence — even top tools hallucinate 3-13% of URLs."
- "Perspective diversity is structural anti-hallucination." → `should-build-in-perspective-diversity`: "Perspective diversity SHOULD be built into the research structure; perspective diversity is structural anti-hallucination."
- "**Attach citation metadata at retrieval time, not after generation** — pre-embedding citations gave the best observed accuracy (~92% in Perplexity)." → `should-attach-citations-at-retrieval`: "Citation metadata SHOULD be attached at retrieval time, not after generation — pre-embedding citations gave the best observed accuracy (~92% in Perplexity)."
- "Cite at the claim / sentence level with the supporting quote." → `should-cite-at-claim-level-with-quote`: "SHOULD cite at the claim / sentence level with the supporting quote."
- "Keep stable, numbered citations through summarization." → `should-keep-stable-numbered-citations`: "SHOULD keep stable, numbered citations through summarization."
- "Outline-driven report with a **confidence / coverage indicator per section.**" → `should-report-confidence-per-section`: "The report SHOULD be outline-driven, with a confidence / coverage indicator per section."
- "Keep intermediate artifacts (outline, mind-map) for human review." → `should-keep-intermediate-artifacts`: "SHOULD keep intermediate artifacts (outline, mind-map) for human review."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions** (left unfixed):
- The topic's top-level `informational` field says it is "offered as evidence for design choices rather than as rules", but the topic now carries named rules. `meta` and top-level fields were not hand-edited, so the field stands as it was.

**unfinished**: none.

## cookbook/guidelines/researching/process/research-methodology-and-sources

`workflow`, `source-catalogue` and `agentic-access` stay verbatim as how-to; rules restate their requirements. The intro's MUST NOT sentence moved verbatim into `must-not-stop-at-search-results`; the intro keeps "Web search is the start, not the method." as its statement.

**promoted** (8 rules):
- "1. **Orient and classify** the topic's domain." → `should-orient-and-classify-domain`: "SHOULD first orient and classify the topic's domain."
- "2. **Identify authoritative sources** for that domain (catalogue below)." → `should-identify-authoritative-sources`: "SHOULD identify the authoritative sources for that domain (see the source catalogue) and go to them."
- "3. **Search** with Boolean or controlled vocabulary (e.g. MeSH for medicine)." → `should-search-with-controlled-vocabulary`: "SHOULD search with Boolean or controlled vocabulary (e.g. MeSH for medicine)."
- "4. **Chain citations** — backward and forward snowballing — to saturation." → `should-chain-citations-to-saturation`: "SHOULD chain citations — backward and forward snowballing — to saturation."
- "5. **Corroborate** across genuinely independent sources." → `should-corroborate-across-independent-sources`: "SHOULD corroborate across genuinely independent sources."
- "6. **Record provenance** at generation time. Use PRISMA when systematic rigor is required." → split in 2:
  - `should-record-provenance-at-generation-time`: "SHOULD record provenance as you go, at generation time."
  - `should-use-prisma-for-systematic-rigor`: "SHOULD use PRISMA when systematic rigor is required."
- "**Academic:** OpenAlex (free, no key — a strong default), ..." → `should-default-to-openalex`: "For academic sources, OpenAlex (free, no key) SHOULD be the default." ("a strong default" read as SHOULD; a judge should check it.)

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/researching/process/research-type-taxonomy

Intro kept verbatim (its SHOULD restated as `should-classify-before-search`). `three-lenses` and `the-types` stay as how-to; `routing-and-escalation` folded into rules.

**promoted** (3 rules):
- "Apply three lenses — intent, domain, method — then let the type pick the sources, the method, and the bar." → split in 2: (The intro keeps the sentence verbatim.)
  - `should-apply-three-lenses`: "SHOULD apply three lenses — intent, domain, method — to classify it."
  - `should-let-type-pick-sources-method-and-bar`: "SHOULD let the type pick the sources, the method, and the bar."
- "Classify by keywords and intent." → `should-classify-by-keywords-and-intent`: "SHOULD classify by keywords and intent."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/shipping/apple-privacy-manifest

How-to kept verbatim: `what-the-manifest-is`, `required-reason-api-categories` (lead-in and table) and `finding-required-reason-usage-in-code`. `required-practice` and `notes` folded into rules; the notes' reasons went to `rationale`.

**promoted** (11 rules):
- "Treat a missing or incomplete `PrivacyInfo.xcprivacy` as a build-breaking error, not a warning." → `should-treat-missing-manifest-as-build-breaking`: "A missing or incomplete `PrivacyInfo.xcprivacy` SHOULD be treated as a build-breaking error, not a warning." (Plain imperative, so SHOULD, although the intro calls the manifest an enforced gate; a judge should check it.)
- "A property-list resource named exactly **`PrivacyInfo.xcprivacy`**, added to the app target (and to each framework/SDK target that needs its own)." → `should-name-and-target-manifest`: "The manifest SHOULD be a property-list resource named exactly **`PrivacyInfo.xcprivacy`**, added to the app target (and to each framework/SDK target that needs its own)."
- "For an app, place it at the top level of the app bundle. For a framework or SDK, place it inside the bundle so it ships with the binary." → `should-place-manifest-in-bundle`: "For an app, it SHOULD be placed at the top level of the app bundle. For a framework or SDK, it SHOULD be placed inside the bundle so it ships with the binary."
- "**`NSPrivacyTrackingDomains`** (array) — internet domains the app connects to for tracking; required if `NSPrivacyTracking` is `true`." → `must-declare-tracking-domains-when-tracking`: "**`NSPrivacyTrackingDomains`** (the internet domains the app connects to for tracking) MUST be declared if `NSPrivacyTracking` is `true`." ("required" read as MUST (RFC 2119 treats REQUIRED as MUST).)
- "If a pinned SDK lacks one, update to a version that includes it or remove the dependency." → `should-update-or-remove-sdk-lacking-manifest`: "If a pinned SDK lacks one, you SHOULD update to a version that includes it or remove the dependency."
- "Search the source and dependencies for the trigger symbols, e.g. `cc-grep` (or `grep -rE`) for: ..." → `should-search-for-trigger-symbols`: "SHOULD search the source and dependencies for the trigger symbols (see *Finding required-reason usage in code*)."
- "Inspect compiled SDKs: a manifest's reasons must cover transitively linked binaries, so scan vendored `.framework`/`.xcframework` symbols, not just first-party Swift." → `must-cover-transitively-linked-binaries`: "A manifest's reasons MUST cover transitively linked binaries, so compiled SDKs SHOULD be inspected: scan vendored `.framework`/`.xcframework` symbols, not just first-party Swift." (Lowercase "must" read as MUST.)
- "After a clean Archive build, confer the **Privacy Report** in Xcode's Organizer (or `xcrun` privacy tooling) to aggregate manifests across the app and its bundles, and reconcile gaps before submitting." → `should-reconcile-privacy-report-before-submitting`: "After a clean Archive build, SHOULD confer the **Privacy Report** in Xcode's Organizer (or `xcrun` privacy tooling) to aggregate manifests across the app and its bundles, and reconcile gaps before submitting."
- "The manifest is additive and durable: declaring an unused category or a missing reason both cause rejection, so keep it minimal and accurate." → `should-keep-manifest-minimal-and-accurate`: "The manifest SHOULD be kept minimal and accurate."
- "Apple may extend the required-reason API list over time; re-check the official docs when adding new low-level Foundation calls." → `should-recheck-docs-for-new-foundation-calls`: "SHOULD re-check the official docs when adding new low-level Foundation calls."
- "Treat any not-yet-published category change as a **forecast** until it appears in Apple's documentation." → `should-treat-unpublished-category-changes-as-forecast`: "Any not-yet-published category change SHOULD be treated as a **forecast** until it appears in Apple's documentation."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions** (left unfixed):
- The intro calls a missing manifest an enforced gate, and `must-ship-privacy-manifest` is MUST, but "Treat a missing or incomplete `PrivacyInfo.xcprivacy` as a build-breaking error, not a warning." has no keyword, so `should-treat-missing-manifest-as-build-breaking` is only SHOULD.
- "confer the **Privacy Report**" in `should-reconcile-privacy-report-before-submitting` reads as a slip for "consult". Left as written.

**notes**: Split: "You **MUST** match `NSPrivacyCollectedDataTypes` to the data the app actually collects; it **SHOULD** stay consistent with the App Store Connect privacy "nutrition label"." became `must-match-collected-data-types` and `should-match-nutrition-label`, keywords kept.

**unfinished**: none.

## cookbook/guidelines/shipping/bulk-operation-verification

Intro kept verbatim (its MUST statement repeated as a rule). Every section folded into rules.

**promoted** (5 rules):
- "**Cross-reference integrity**: Verify that every file that references a renamed/moved entity has been updated." → `should-verify-cross-reference-integrity`: "After the bulk operation finishes, SHOULD verify that every file that references a renamed/moved entity has been updated. Common miss points:"
- "**Completeness**: Confirm the operation covered all intended files. List what was changed and compare against what should have been changed." → `should-confirm-completeness`: "After the bulk operation finishes, SHOULD confirm the operation covered all intended files: list what was changed and compare against what should have been changed."
- "When to run: "After any rename (files, directories, functions, variables across files)" / "After migrating content between directories or repos" / "After restructuring a directory layout" / "After updating a convention across multiple files (e.g., frontmatter format)"" → `should-verify-after-bulk-changes`: "The verification pass SHOULD run:"
- "Verify each repo independently." → `should-verify-each-repo-independently`: "For cross-repo operations, SHOULD verify each repo independently."
- "Then run a cross-repo check to confirm consistency — the same identifier should resolve correctly in every repo that references it." → `should-run-cross-repo-check`: "For cross-repo operations, SHOULD then run a cross-repo check to confirm consistency — the same identifier should resolve correctly in every repo that references it."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions** (left unfixed):
- The intro makes verification a MUST for an operation touching more than 5 files, while the when-to-run list (now `should-verify-after-bulk-changes`) has no threshold and no keyword, so it is SHOULD.

**unfinished**: none.

## cookbook/guidelines/shipping/continuous-delivery

The delivery-vs-deployment table stays as how-to, the pre-PR checklist stays verbatim as how-to, and the J-curve paragraph is `rationale`.

**promoted** (6 rules):
- "These are distinct practices; do not conflate them." → `should-not-conflate-delivery-and-deployment`: "Continuous delivery and continuous deployment are distinct practices; they SHOULD NOT be conflated." (SHOULD NOT.)
- "Expect a temporary performance dip when adopting CD; plan for the recovery rather than abandoning the effort at the bottom of the curve." → `should-plan-for-the-j-curve-dip`: "Teams SHOULD expect a temporary performance dip when adopting CD, and plan for the recovery rather than abandoning the effort at the bottom of the curve. (Caveat: the J-curve is an observed pattern, not a guarantee; depth and duration vary by team.)"
- "1. Confirm CI runs the full automated pipeline on this branch and is green before marking the PR ready." → `should-confirm-ci-green-before-pr-ready`: "Before marking a PR ready, an agent SHOULD confirm CI runs the full automated pipeline on the branch and is green."
- "2. Confirm the change does not require a manual step to become releasable." → `should-confirm-no-manual-release-step`: "Before marking a PR ready, an agent SHOULD confirm the change does not require a manual step to become releasable."
- "3. Confirm risky behavior is gated behind a flag so merge does not force a release." → `should-confirm-risky-behavior-flagged`: "Before marking a PR ready, an agent SHOULD confirm risky behavior is gated behind a flag so merge does not force a release."
- "4. Confirm a rollback or roll-forward path exists for the change." → `should-confirm-rollback-path`: "Before marking a PR ready, an agent SHOULD confirm a rollback or roll-forward path exists for the change."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**notes**: Fix commit `ca23a021` ("fix(cookbook): continuous-delivery red-pipeline rule kept whole"). The first commit, `711bce08`, split "a red pipeline **MUST** block release and **SHOULD** be treated as a stop-the-line event" into two rules. `cookr roles lossless` refused that split with "the matched clause drops its MUST", but my finish script did not yet gate on lossless, so the commit went in. The fix merges the clause back into one rule, `must-block-release-on-red-pipeline`, carrying both keywords. Lossless and roles check exit 0 after the fix. The fix commit was not bumped again.

**unfinished**: none.

## cookbook/guidelines/shipping/ephemeral-environments

Intro kept verbatim (its SHOULD restated as `should-give-every-pr-a-preview`). The old labels `created-automatically`, `isolated` and `destroyed-automatically` became one named rule per sentence. The database-strategy sentence stays verbatim as how-to ("Database strategy"); the "To prevent drift" lead-in maps to its three rules, which a `rationale` part names.

**promoted** (7 rules):
- "No environment may outlive its PR." → `must-not-outlive-pr`: "No environment may outlive its PR: an environment MUST NOT outlive it." ("may not" (no environment may outlive) read as MUST NOT.)
- "Seed each environment with synthetic or anonymized fixtures (per *test-data-management*)." → `should-seed-with-synthetic-fixtures`: "SHOULD seed each environment with synthetic or anonymized fixtures (per *test-data-management*)."
- "Pick fresh-provision by default and adopt branching only when spin-up latency is a measured bottleneck (per *yagni*)." → `should-default-to-fresh-provision`: "SHOULD choose a database strategy deliberately: pick fresh-provision by default and adopt branching only when spin-up latency is a measured bottleneck (per *yagni*)."
- "Run E2E/smoke suites and contract tests (see ...) against the live URL, and post the preview link plus check results back as a PR comment for human review." → split in 2:
  - `should-run-e2e-against-live-url`: "SHOULD run E2E/smoke suites and contract tests (see `[adc.guideline.testing.contract-testing](cookbook:abdcd282-5b81-4ab2-ab1e-3ed288a4aee5)`) against the live URL."
  - `should-post-preview-link-and-results`: "SHOULD post the preview link plus check results back as a PR comment for human review."
- "Note: managed-platform feature names and DB-branching capabilities evolve quickly — verify current behavior against the vendor's docs before relying on a specific guarantee." → `should-verify-vendor-behavior`: "Managed-platform feature names and DB-branching capabilities evolve quickly, so SHOULD verify current behavior against the vendor's docs before relying on a specific guarantee."
- "FORECAST: treat any "instant branch" or per-PR-cost claim as vendor-specific and unverified until measured in your own pipeline." → `should-treat-vendor-claims-as-unverified`: "FORECAST: SHOULD treat any "instant branch" or per-PR-cost claim as vendor-specific and unverified until measured in your own pipeline."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**notes**: "manual hotfixes to a live preview are forbidden" stays verbatim inside `must-recreate-state-from-iac`, under that bullet's MUST.

**unfinished**: none.

## cookbook/guidelines/shipping/incident-response

The original labels `incident-commander`, `communications-lead` and `operations-lead` are kept as rule names. The severity table is `examples` ("Severity ladder"); "The role/severity/postmortem structure is the durable part." went to `rationale`.

**promoted** (6 rules):
- "Classify severity at declaration to scale the response, and **MUST** re-evaluate as understanding changes." → `should-classify-severity-at-declaration`: "Severity SHOULD be classified at declaration to scale the response." (The sentence's MUST stays on `must-reevaluate-severity`.)
- "Use a small fixed ladder; exact thresholds are org-specific." → `should-use-small-fixed-ladder`: "SHOULD use a small fixed severity ladder; exact thresholds are org-specific."
- "Tie thresholds to SLO error budgets where they exist (see related) rather than to gut feel." → `should-tie-thresholds-to-slos`: "Severity thresholds SHOULD be tied to SLO error budgets where they exist (see related) rather than to gut feel."
- "Separate *coordinating* the response from *doing* the work so neither starves the other. The roles below follow the established Incident Management At Google (IMAG) model; adapt names to your org but keep the separation." → `should-separate-coordinating-from-doing`: "SHOULD separate *coordinating* the response from *doing* the work so neither starves the other. The roles follow the established Incident Management At Google (IMAG) model; adapt names to your org but keep the separation."
- "Specific tooling (paging vendors, ChatOps incident bots, AI-assisted triage and summarization) evolves quickly — treat any named product as an example, not a requirement." → `should-treat-named-tools-as-examples`: "Specific tooling (paging vendors, ChatOps incident bots, AI-assisted triage and summarization) evolves quickly — any named product SHOULD be treated as an example, not a requirement."
- "AI-assisted incident summarization and correlation are increasingly common as of 2026; treat their output as a draft for a human responder, not as the authority — keep a human IC accountable." → `should-treat-ai-output-as-draft`: "AI-assisted incident summarization and correlation are increasingly common as of 2026; their output SHOULD be treated as a draft for a human responder, not as the authority — keep a human IC accountable."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/shipping/msix-packaging

The statement paragraph stays in intro; the bullets became rules.

**promoted** (1 rules):
- "Use the single-project MSIX packaging model" → `should-use-single-project-msix`: "SHOULD use the single-project MSIX packaging model."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/shipping/progressive-delivery

The decoupling, rollout, rollback and guardrail bullets became rules. The mechanism table stays as how-to ("Rollout mechanisms"); the FORECAST sentence on changing controller versions went to `rationale`.

**promoted** (6 rules):
- "Pick the lightest mechanism that fits the risk; do not stack all of them." → `should-pick-lightest-mechanism`: "SHOULD pick the lightest rollout mechanism that fits the risk, and SHOULD NOT stack all of them." (SHOULD and SHOULD NOT.)
- "Flags introduced purely to gate a rollout are temporary. Remove the flag and the dead branch once the change is at 100% and stable, to avoid permanent branching debt (`design-for-deletion`, `yagni`)." → `should-remove-rollout-flags`: "Flags introduced purely to gate a rollout are temporary. The flag and the dead branch SHOULD be removed once the change is at 100% and stable, to avoid permanent branching debt (`design-for-deletion`, `yagni`)."
- "Pause new progressive rollouts during an active incident or when the error budget is exhausted." → `should-pause-rollouts-during-incidents`: "New progressive rollouts SHOULD be paused during an active incident or when the error budget is exhausted."
- "Prefer the platform/orchestrator's native progressive-delivery support (e.g. Kubernetes-native canary controllers, or a managed flag service) before building bespoke traffic-shifting (`native-controls`, `open-source-preference`)." → `should-prefer-native-progressive-delivery`: "SHOULD prefer the platform/orchestrator's native progressive-delivery support (e.g. Kubernetes-native canary controllers, or a managed flag service) before building bespoke traffic-shifting (`native-controls`, `open-source-preference`)."
- "Pin the tool and its version in your runbook rather than encoding vendor specifics here, and treat single-vendor adoption stats as marketing, not fact." → split in 2:
  - `should-pin-tool-version-in-runbook`: "SHOULD pin the tool and its version in your runbook rather than encoding vendor specifics here."
  - `should-treat-vendor-adoption-stats-as-marketing`: "SHOULD treat single-vendor adoption stats as marketing, not fact."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/shipping/supply-chain-integrity

The SLSA table and its spec sentence stay as how-to ("SLSA Build levels (v1.0, Build track L0–L3)"). The regulatory-drivers part is `rationale`; its "confirm applicability" clause became a rule. The two lead-ins are in `rationale`, naming their rules.

**promoted** (12 rules):
- "Use **CycloneDX** or **SPDX** — both are widely tooled; pick one and stay consistent." → `should-use-one-sbom-format`: "The SBOM SHOULD use **CycloneDX** or **SPDX** — both are widely tooled; pick one and stay consistent."
- "Sign artifacts and attestations. Keyless signing tied to CI workload identity (e.g. Sigstore/cosign with OIDC) avoids long-lived private keys; managed KMS keys are an acceptable alternative." → `should-sign-artifacts-and-attestations`: "Artifacts and attestations SHOULD be signed. Keyless signing tied to CI workload identity (e.g. Sigstore/cosign with OIDC) avoids long-lived private keys; managed KMS keys are an acceptable alternative."
- "Pin the toolchain and base images by digest so the build is reproducible enough to attest." → `should-pin-toolchain-by-digest`: "The toolchain and base images SHOULD be pinned by digest so the build is reproducible enough to attest."
- "Target **L2** as a realistic baseline; reach for L3 where the threat model justifies it." → `should-target-slsa-l2`: "SHOULD target SLSA Build **L2** as a realistic baseline, and reach for L3 where the threat model justifies it."
- "Store SBOMs and attestations as immutable release evidence for incident response and audits." → `should-store-release-evidence`: "SBOMs and attestations SHOULD be stored as immutable release evidence for incident response and audits."
- "Commit lockfiles; install with the frozen/locked flag in CI so resolution is deterministic." → `should-commit-lockfiles`: "SHOULD commit lockfiles, and install with the frozen/locked flag in CI so resolution is deterministic."
- "Pin dependencies (and CI actions) by version, ideally by digest/hash, not floating tags." → `should-pin-dependencies-by-digest`: "SHOULD pin dependencies (and CI actions) by version, ideally by digest/hash, not floating tags."
- "Keep scanning for known-vulnerable components — it answers a different question (*is this version exploitable?*) than provenance (*did this come from where I think?*)." → `should-keep-scanning-for-vulnerable-components`: "SHOULD keep scanning for known-vulnerable components — it answers a different question (*is this version exploitable?*) than provenance (*did this come from where I think?*)."
- "Do not ship a release build with no SBOM and no provenance." → `must-not-ship-without-sbom-and-provenance`: "MUST NOT ship a release build with no SBOM and no provenance." (MUST NOT: listed under the "MUST NOT" heading.)
- "Do not treat an unsigned or unverifiable attestation as passing." → `must-not-pass-unverifiable-attestation`: "MUST NOT treat an unsigned or unverifiable attestation as passing." (MUST NOT, same heading.)
- "Do not generate provenance from a fully build-author-controlled step and claim hosted-build (L2) trust." → `must-not-claim-hosted-trust-for-author-controlled-provenance`: "MUST NOT generate provenance from a fully build-author-controlled step and claim hosted-build (L2) trust." (MUST NOT, same heading.)
- "These are *drivers*, not engineering requirements; confirm current applicability for your jurisdiction and sector." → `should-confirm-regulatory-applicability`: "SHOULD confirm the regulatory drivers' current applicability for your jurisdiction and sector."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions** (left unfixed):
- `must-not-ship-without-sbom-and-provenance` ("Do not ship a release build with no SBOM and no provenance.") forbids only a build with neither, while `must-produce-sbom` and `must-produce-signed-provenance` ("Every release build **MUST** produce ...") require both.
- `should-verify-provenance-before-deploy` ("The deploy step **SHOULD** verify provenance") is SHOULD, while `must-block-promotion-on-failed-check` ("A failed signature or provenance check **MUST** block promotion") is MUST for a failed provenance check.

**unfinished**: none.

## cookbook/guidelines/shipping/trunk-based-development

The `core-practices` and `required-protections` bullets moved verbatim into rules, keeping their names. `how-an-agent-should-work-on-trunk` stays verbatim as how-to, with a rule restating each step. `why-frequency-beats-branch-isolation` and `caveats` are `rationale`.

**promoted** (13 rules):
- "1. **Branch small.** Cut a short-lived branch from current `main` for one logical change." → `should-branch-small`: "The agent SHOULD cut a short-lived branch from current `main` for one logical change."
- "2. **Keep work shippable.** If the change is partial, gate the new behavior behind a feature flag (default off). Add code paths that are inert until the flag is enabled." → `should-flag-partial-change`: "If the change is partial, the agent SHOULD gate the new behavior behind a feature flag (default off), adding code paths that are inert until the flag is enabled."
- "3. **Commit atomically.** One logical change per commit (see atomic-commits), running the build and tests before each commit." → `should-commit-atomically`: "The agent SHOULD make one logical change per commit (see atomic-commits), running the build and tests before each commit."
- "5. **Merge fast.** Open the PR, get checks green, and merge within a day. Prefer squash merges to keep trunk history linear and each merge a single revertible unit." → split in 2:
  - `should-merge-within-a-day`: "The agent SHOULD open the PR, get checks green, and merge within a day."
  - `should-prefer-squash-merges`: "The agent SHOULD prefer squash merges to keep trunk history linear and each merge a single revertible unit."
- "Land enabling-but-disabled increments instead." → `must-not-sit-on-work`: "The agent MUST NOT accumulate days of work on a branch "until it's complete." Land enabling-but-disabled increments instead." (Kept as the second sentence of the MUST NOT rule it follows.)
- "**DO NOT** open a branch and let it diverge from trunk for a week, then attempt a large merge." → `must-not-let-branch-diverge`: "MUST NOT open a branch and let it diverge from trunk for a week, then attempt a large merge." ("DO NOT" read as MUST NOT.)
- "**DO NOT** use a `develop` branch as a staging trunk that periodically merges into `main`; this is GitFlow, not trunk-based development, and reintroduces batched integration." → `must-not-use-develop-as-staging-trunk`: "MUST NOT use a `develop` branch as a staging trunk that periodically merges into `main`; this is GitFlow, not trunk-based development, and reintroduces batched integration."
- "**DO NOT** hold finished-but-unreleased code on a branch — merge it disabled behind a flag." → `must-not-park-finished-code-on-branch`: "MUST NOT hold finished-but-unreleased code on a branch — merge it disabled behind a flag."
- "**DO NOT** disable or bypass required checks to land a merge faster." → `must-not-bypass-required-checks`: "MUST NOT disable or bypass required checks to land a merge faster."
- "Establish green-trunk gating first." → `should-establish-green-trunk-gating-first`: "Trunk-based development assumes strong automated checks and a fast CI feedback loop; without them, frequent merges to a shared trunk amplify breakage. Green-trunk gating SHOULD be established first."
- "Heavily regulated contexts may require a release branch for a tagged, audited build." → `may-cut-release-branch-for-audited-build`: "Heavily regulated contexts MAY require a release branch for a tagged, audited build. That is a release artifact cut *from* trunk, not a long-lived integration branch — trunk remains the single integration point." (Lowercase "may" read as MAY; it may mean possibility rather than permission, so a judge should check it. The caveat stays verbatim in `rationale`.)
- "Treat this as a validated *correlation with* delivery performance, not a guarantee; ..." → `should-treat-dora-as-correlation`: "The DORA finding SHOULD be treated as a validated *correlation with* delivery performance, not a guarantee." (The paragraph stays verbatim in `rationale`.)

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions** (left unfixed):
- `integrate-daily` ("Work SHOULD be integrated into trunk at least once per day") against `short-lived-branches` ("Branches SHOULD live no more than 1-2 days") and `must-not-let-branch-diverge` ("diverge from trunk for a week"): three different time limits.

**unfinished**: none.

## cookbook/guidelines/shipping/windows-arm64-and-aot

Intro kept verbatim. The keyword bullets moved verbatim into rules; the plain imperatives inside them became rules of their own. The YAGNI framing and the forecast's first sentence are `rationale`.

**promoted** (6 rules):
- "Audit `runtimes/` folders before shipping." → `should-audit-runtimes-folders`: "The `runtimes/` folders SHOULD be audited before shipping, so no x64-only native dependency forces the process into emulation."
- "Mark this as a transitional state, not an end goal." → `should-mark-arm64ec-transitional`: "Arm64EC use SHOULD be marked as a transitional state, not an end goal."
- "Adopt them ONLY when a concrete measurement justifies the added constraints (faster cold start, smaller download, no-runtime self-contained deploy)." → `should-adopt-aot-only-on-measured-need`: "Teams SHOULD adopt AOT and trimming ONLY when a concrete measurement justifies the added constraints (faster cold start, smaller download, no-runtime self-contained deploy)." (Plain imperative, so SHOULD; the capital ONLY might be read as MUST, so a judge should check it.)
- "Use source generators or AOT-safe APIs instead." → `should-use-source-generators-or-aot-safe-apis`: "Reflection-heavy and dynamic-codegen paths SHOULD use source generators or AOT-safe APIs instead."
- "Prefer it when the measured need is startup latency alone." → `should-prefer-readytorun-for-startup-only`: "ReadyToRun SHOULD be preferred when the measured need is startup latency alone."
- "Pin to the .NET and CsWinRT versions you build against and re-verify AOT/trim compatibility on each upgrade rather than assuming prior results hold." → `should-pin-and-reverify-on-upgrade`: "Teams SHOULD pin to the .NET and CsWinRT versions they build against and re-verify AOT/trim compatibility on each upgrade rather than assuming prior results hold."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions** (left unfixed):
- `should-publish-native-arm64` ("Apps targeting Windows on ARM **SHOULD** publish a native `win-arm64` build") against `must-not-ship-on-x64-emulation` ("Builds **MUST NOT** rely on x64 emulation as the shipping plan for ARM hardware when native ARM64 is achievable").

**unfinished**: none.

## cookbook/guidelines/storytelling/craft

Every section part held rules that already had names and MUST/SHOULD keywords. They were merged verbatim into one `rules` part and the section parts removed.

**promoted**: none.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/storytelling/ecosystem

Every section part held rules that already had names and MUST/SHOULD keywords. They were merged verbatim into one `rules` part and the section parts removed.

**promoted**: none.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/storytelling/explanation

Every section part held rules that already had names and MUST/SHOULD keywords. They were merged verbatim into one `rules` part and the section parts removed.

**promoted**: none.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/storytelling/grounded-synthesis

Every section part held rules that already had names and MUST/SHOULD keywords. They were merged verbatim into one `rules` part and the section parts removed.

**promoted**: none.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/storytelling/narrative-arc

Every section part held rules that already had names and MUST/SHOULD keywords. They were merged verbatim into one `rules` part and the section parts removed.

**promoted**: none.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/storytelling/positioning

Every section part held rules that already had names and MUST/SHOULD keywords. They were merged verbatim into one `rules` part and the section parts removed.

**promoted**: none.

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions**: none.

**unfinished**: none.

## cookbook/guidelines/testing/agent-evaluation-and-safety

Intro kept verbatim. The gate table stays as how-to ("The two gates"). The first sentence of `adopt-when-measured` and the not-legal-advice blockquote are `rationale`. The SLO, CI, red-team and regression bullets moved verbatim into rules.

**promoted** (7 rules):
- "Treat both as release-gating, run in CI on every model, prompt, tool, or retrieval change — not as a post-launch afterthought." → `should-treat-both-gates-as-release-gating`: "Both gates SHOULD be treated as release-gating, run in CI on every model, prompt, tool, or retrieval change — not as a post-launch afterthought." (The intro keeps the sentence verbatim.)
- "For how to build graders, calibrate an LLM judge, and report `pass@k` vs `pass^k` consistency, follow **eval-driven-development**." → `should-follow-eval-driven-development`: "For how to build graders, calibrate an LLM judge, and report `pass@k` vs `pass^k` consistency, you SHOULD follow **eval-driven-development**."
- "For prompt injection, untrusted-output handling, and tool-agency constraints, follow **llm-application-security** (mapped to the OWASP Top 10 for LLM Applications **2025** revision — pin that edition)." → split in 2:
  - `should-follow-llm-application-security`: "For prompt injection, untrusted-output handling, and tool-agency constraints, you SHOULD follow **llm-application-security** (mapped to the OWASP Top 10 for LLM Applications **2025** revision)."
  - `should-pin-owasp-llm-2025-edition`: "You SHOULD pin the OWASP Top 10 for LLM Applications **2025** revision that llm-application-security is mapped to."
- "Confirm regulatory obligations (e.g., data-residency, consent) with qualified counsel." → `should-confirm-regulatory-obligations-with-counsel`: "You SHOULD confirm regulatory obligations (e.g., data-residency, consent) with qualified counsel."
- "Heavy evaluation infrastructure (managed eval platforms, dedicated red-team services, continuous online scoring) is justified **when a measured need warrants it** — scale, regulated risk, or a real incident — not by default (per YAGNI)." → `should-adopt-heavy-eval-infra-on-measured-need`: "Heavy evaluation infrastructure (managed eval platforms, dedicated red-team services, continuous online scoring) SHOULD be adopted **when a measured need warrants it** — scale, regulated risk, or a real incident — not by default (per YAGNI)." (The sentence also stays verbatim in `rationale`.)
- "Start with a small versioned dataset and CI gates; add platform weight when the gate cost or coverage demands it." → `should-start-small`: "You SHOULD start with a small versioned dataset and CI gates, and add platform weight when the gate cost or coverage demands it."

**bars**: `look-for` authored, `a-complete-review-must-establish` authored, `a-build-must-establish` authored.

**contradictions** (left unfixed):
- `should-pass-both-gates`: "A change to an agent system **SHOULD** pass both gates before release; either gate failing blocks the deploy." The keyword is SHOULD, but "blocks the deploy" is unconditional, and the intro says to "Treat both as release-gating".

**unfinished**: none.
