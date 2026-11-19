# Review: feature-flags

## Findings

- `rules.md`, `typescript-localstorage-default`: "...which MUST store values as strings, parse them on read, and return the defaults when `localStorage` is unavailable or throws. (claims: sdks-cache-in-local-storage, web-localstorage-semantics)". The rule does not follow from its cited claims at the strength it states. `web-localstorage-semantics` (MDN) establishes that `localStorage` holds only strings and can throw `SecurityError`, and `sdks-cache-in-local-storage` says vendor SDKs cache flags there. Neither source says an implementation MUST return the default when storage throws. That MUST comes from OpenFeature's "MUST NOT throw ... must always return the `default value`" (`openfeature-default-required-no-throw`), which the rule does not cite. Its rationale entry does not name `evaluation-takes-a-default-and-never-throws` either. Compare `csharp-missing-flag-returns-default`, whose rationale names "the call-site default the evaluation rule requires". Fix: change the citation to `(claims: sdks-cache-in-local-storage, web-localstorage-semantics, openfeature-default-required-no-throw)`. Also extend the `typescript-localstorage-default` entry in `rationale.md` to "...so the implementation parses and guards every read, returning the call-site default that `evaluation-takes-a-default-and-never-throws` requires; LaunchDarkly's web SDK caches flags there."

Checked with no finding:
- The four owner-list rules (`gate-all-features`, `fail-fast-on-missing-config`, `kotlin-sharedpreferences-default`, `spec-lists-flag-keys`) match `owner-list.md` word for word.
- All 37 rules end with a `(claim:/claims:)` citation, and every cited id is one of the 48 claims in `research.json`.
- Every claim is cited by at least one rule, so no claim under a `supported` or `new` verdict is left without a rule.
- Every other rule's RFC strength follows from its claims' quotes, or from the derivation its `rationale.md` entry gives. Examples: the MUST in `no-dependency-on-flag-service` rests on OpenFeature's MUST; the MUSTs in `unique-never-reused-flag-names` rest on the SEC order and Unleash's "Ensure"; the MUST in `remove-code-before-archive` rests on archive-serves-the-fallback across vendors; vendor-only and single-source practice is held to SHOULD.
- The review focus, review bar and build bar cover every MUST and MUST NOT. The build bar has one line per rule, in rule order.
- The five findings from the previous round are fixed: the long-lived off path and error reporting are now in the review bar, there is a review-focus bullet for unreported fallbacks, and the "flag failure" qualifier is back in both the build bar and the review bar.
- `references.md` lists exactly the 30 research sources.
- `related` is bidirectional with ab-testing and debug-mode.
- The tags, the author format and the provider terminology are consistent with the siblings.
- The examples are correct for their APIs and follow the rules: call-site defaults, no throws, errors logged, and coroutine cancellation rethrown.

## Lint

/lint-artifact on cookbook/guidelines/implementing/feature-management/feature-flags. `cookr` is not installed in the lint agent's environment, so it read `artifact.json` and the parts directly, checked links and the index by hand, and did not run `cookr validate`.

```
lint-artifact v2.0.0
Type: guideline | Compliance: tbd/compliance/artifact-formatting/guideline-formatting.md
Artifact: cookbook/guidelines/implementing/feature-management/feature-flags (Feature flags, 1.0.4)

[PASS] FM-01: Frontmatter present (meta block in artifact.json)
[PASS] FM-02: id is a valid UUID (ac616d81-16c2-4f33-9ae4-139d5c24318d)
[PASS] FM-03: cookbook/index.json has this id, path guidelines/implementing/feature-management/feature-flags, rdid adc.guideline.implementing.feature-management.feature-flags, and no domain field
[PASS] FM-04: type is guideline
[PASS] FM-05: version 1.0.4 is valid semver
[PASS] FM-06: all required fields present
[PASS] FM-07: license is MIT
[PASS] FM-08: copyright is "2026 Mike Fullerton"
[PASS] FM-09: created and modified are ISO dates
[PASS] FM-10: summary is non-empty
[PASS] FM-11: H1 "Feature flags" matches title
[PASS] FM-11a: both related UUIDs resolve in index.json; the in-text cookbook:e446ee3e link is a UUID link and resolves
[PASS] FM-12: Change History has 5 rows
[PASS] FM-13: no TODO, TBD, FIXME, placeholder or fill-in text
[PASS] gf-type-field
[PASS] gf-title-heading
[PASS] GF-01 / gf-summary-statement: the intro paragraph follows the H1
[PASS] GF-02 / gf-structured-guidance: named bullets, tables and sections
[PASS] GF-03 / gf-rfc-keywords: all 37 rules carry MUST, SHOULD or MAY
[PASS] gf-change-history: columns Version, Date, Author, Summary
[PASS] gf-triggers-field: triggers [feature-flags, new-module]
[PASS] gf-roled-parts: rules, review-focus, review-bar and build-bar parts present; no routes or hosts
[PASS] gf-named-rules: 37 unique kebab-case names, each with an RFC keyword
[PASS] gf-rule-cites-research: each rule ends with one citation, and all 57 cited claim ids exist in research.json
[PASS] gf-roled-parts (build-bar): one line per rule, 37 lines, exactly matching the rule names
[PASS] gf-research-folder: research.json and research.md exist, the four headings are in the right order, every claim has all required fields with valid question values, and every cited claim is named by a verdict
[WARN] GF-04 / gf-compliance-section: there is no ## Compliance section
       -> It is optional. Add one only if other compliance checks reference this guideline.
[WARN] gf-research-folder (verdict coverage): 10 of the 37 rules have no verdict of their own
       -> The rules are ship-a-local-default-provider, backend-provider-is-swappable, plan-flag-removal-at-creation, remove-code-before-archive, review-live-flags-regularly, csharp-missing-flag-returns-default, csharp-feature-gate, no-secrets-in-userdefaults, no-secrets-in-client-flag-store and no-personal-data-in-flag-service. The spec says each rule checked gets a verdict, and `cookr validate` may flag this. I left GF-04 and this one as warnings because I could not run it.
[WARN] gf-triggers-field: I could not confirm the trigger names against the taxonomy
       -> guide/introduction/trigger-guide.md does not exist at that path.

=== LINT SUMMARY ===
Artifact: feature-flags
Type: guideline
Pass: 24 | Warn: 3 | Fail: 0
RESULT: CLEAN — artifact passes all checks.
```

verdict: fail
