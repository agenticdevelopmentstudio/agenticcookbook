# Review: feature-flags

## Findings

- `examples.md`, the Kotlin `DataStoreFlagProvider` (`context.flagStore.data.first()[booleanPreferencesKey(key)] ?: default`, with the comment "anything else, CancellationException included, propagates"). DataStore's `Preferences.get` does an unchecked cast, and `Preferences.Key` equality is by name only. So a value stored under the same key with a different type (for example a string written by a sync) makes the elvis unbox throw `ClassCastException`, and the example lets that exception escape. This breaks `evaluation-takes-a-default-and-never-throws` ("MUST NOT throw: when ... evaluation fails, it MUST return that default") and `how-to-keep-the-rules.md` ("a flag that is missing, mistyped or unreachable at runtime returns its default and logs"). Fix: read the raw value and check its type, for example `val raw = context.flagStore.data.first().asMap()[booleanPreferencesKey(key)]; (raw as? Boolean) ?: default.also { if (raw != null) Log.w("FeatureFlags", "Flag $key is not a Boolean; using default $default") }`. Keep the `IOException` catch. Change the comment so it says only `CancellationException` propagates.
- `examples.md`, the TypeScript `LocalStorageFlagProvider` (`return raw === null ? defaultValue : raw === "true";`). A stored value that is neither `"true"` nor `"false"` (`"1"`, `"yes"`, garbage) comes back as `false`, not as the default. A flag whose default is `true` is silently switched off by a malformed value. This contradicts the how-to ("a flag that is missing, mistyped ... returns its default and logs") and `typescript-localstorage-default`'s "parse them on read". Fix: `if (raw === "true") return true; if (raw === "false") return false; if (raw !== null) console.warn(\`Flag ${key} malformed; using default ${defaultValue}\`); return defaultValue;`.
- `rules.md`, `local-flag-store-is-untrusted` ("flag stores and flag contexts MUST NOT hold secrets or personal data"). For flag *contexts*, the only cited support is `client-side-override-risk`, whose Unleash half is vendor best practice ("ensuring that all ... PII remains confined to your application"). The claim itself is worded "flag systems should not hold PII". `apple-userdefaults-not-sensitive` ("Don't store personal or sensitive information") supports MUST NOT for a client-side flag *store* such as `UserDefaults`, but it says nothing about evaluation contexts sent to a flag service. The context clause is therefore stated at MUST from a SHOULD-strength claim. Fix: split the clause. "Flag stores MUST NOT hold secrets or personal data; flag contexts SHOULD NOT carry personal data." Align the build-bar line (`local-flag-store-is-untrusted`), the review bar and the review focus to match.
- `rationale.md`, `feature-flag-provider-interface` ("The rule no longer fixes the signature `isEnabled(key) -> Bool` ... ; the owner decides the final signature"). The rule's verdict is `supported`, but its wording changed from the prior text: the `isEnabled(key) -> Bool` signature was dropped. The rationale also hands the signature to the owner, yet the rule is not in owner-list.md. The guideline therefore defers a decision that the owner list does not record, and the owner never sees it. Fix: either add `feature-flag-provider-interface` to owner-list.md (prior signature `isEnabled(key) -> Bool`; against: `openfeature-default-required-no-throw`, `openfeature-typed-evaluation`), or drop "the owner decides the final signature" from the rationale and state that the call-site default and typed values are the rule's shape.
- `what-a-reviewer-looks-for.md`. Every platform local-store rule has a review-focus item except `swift-userdefaults-default`. Kotlin and TypeScript share a line, and C# has its own. A Swift local default that is not a protocol with a `UserDefaults`-backed implementation is never named as something to look for, although the review bar checks it. Fix: add "A Swift local default that is not a protocol with a `UserDefaults`-backed implementation, with no reason given".

Not reported:
- The owner-list rules `gate-all-features`, `fail-fast-on-missing-config`, `kotlin-sharedpreferences-default` and `spec-lists-flag-keys` keep the exact wording in owner-list.md.
- The rules in owner-list.md's "also flagged by validate" section are the owner's to confirm. One of them, `kotlin-datastore-default`, has "a DataStore file of its own for flags", which is stronger than its quote; the quote asks only that non-sensitive preferences be kept apart from sensitive data.
- Version, `modified` and Change History are left for stage 5's `cookr bump`, as the write brief says.

Source fidelity checks that passed:
- All 27 rules end with a citation, and every cited claim exists in research.json.
- All 48 claims are cited, and every `supported` and `new` verdict has its rule.
- The `FeatureGateAttribute` exception from round 3 is now in all three bars.
- The `related` links are bidirectional with `ab-testing` and `debug-mode`.
- The summary is 160 characters.

## Lint

The /lint-artifact skill ran on `cookbook/guidelines/implementing/feature-management/feature-flags`. Its environment had no `cookr`, so it linted the source folder directly. I then ran `cookr validate` separately with the worktree `.venv` python (`PYTHONPATH=skills/cookr/cli .venv/bin/python -m cookr validate`). It reported "✓ All 485 artifacts passed deterministic checks." and "✓ Validation passed."

```
Type: guideline | Compliance: tbd/compliance/artifact-formatting/guideline-formatting.md
[PASS] FM-01/gf-frontmatter-complete: all meta fields present in artifact.json, no domain field
[PASS] FM-02: id ac616d81-16c2-4f33-9ae4-139d5c24318d is a valid UUID
[PASS] FM-03: index.json maps the id to guidelines/implementing/feature-management/feature-flags, rdid adc.guideline.implementing.feature-management.feature-flags
[PASS] FM-04/gf-type-field: guideline
[PASS] FM-05: version 1.0.4
[PASS] FM-06: id through references, plus approved-by and approved-date, all present
[PASS] FM-07: license MIT
[PASS] FM-08: copyright "2026 Mike Fullerton"
[PASS] FM-09: created 2026-03-27, modified 2026-11-07
[PASS] FM-10: summary is non-empty
[PASS] FM-11/gf-title-heading: intro H1 "Feature flags" matches the title
[PASS] FM-11a: both related UUIDs are in the index, and the one in-text cookbook: link uses the format-2 UUID form
[PASS] FM-12/gf-change-history: 5 rows, the last one at 1.0.4 (matching version) and 2026-11-07 (matching modified)
[PASS] FM-13: no TODO, TBD, FIXME or "fill in"; the {{app_prefix}} in the examples is a code template token, not a placeholder
[PASS] GF-01/gf-summary-statement: the summary paragraph follows the H1
[PASS] GF-02/gf-structured-guidance: 27 bulleted rules
[PASS] GF-03/gf-rfc-keywords: every rule carries MUST, SHOULD or MAY
[PASS] GF-04/gf-compliance-section: optional, and nothing references it
[PASS] gf-triggers-field: triggers [feature-flags, new-module]
[PASS] gf-roled-parts: rules, review-focus, review-bar, build-bar, how-to, examples, rationale and references are all present; the build-bar has exactly one line per rule, in the same order as the rules
[PASS] gf-named-rules: 27 unique kebab-case names, each with an RFC 2119 keyword
[PASS] gf-research-folder: research.json and research.md both exist
       - The four ## headings are in the right order.
       - All 48 claims have the required fields, valid question and independence values, and citations with all six fields.
       - Every rule has a verdict naming at least one claim, and every cited claim is covered by a verdict.
[PASS] gf-rule-cites-research: all 27 rules end with one (claim: ...) or (claims: ...) citation, and every id exists in research.json
[WARN] gf-research-folder (owner-decides): 4 rules are kept for the owner despite the research. They are gate-all-features, fail-fast-on-missing-config and kotlin-sharedpreferences-default (verdict contradicted) and spec-lists-flag-keys (verdict unsupported). The rationale records each as kept for the owner to decide.
       -> The owner needs to rule on these, or the rules need to change. This is the expected `cookr validate` warning, not a structural failure.

=== LINT SUMMARY ===
Artifact: feature-flags (guideline)
Type: guideline
Pass: 22 | Warn: 1 | Fail: 0

RESULT: CLEAN — artifact passes all checks.
```

The lint's one warning is on the owner-list rules, and their wording matches owner-list.md.

verdict: fail
