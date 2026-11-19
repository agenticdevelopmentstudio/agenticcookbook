# Review: debug-mode

## Findings

- `rules.md`, `platform-access-methods` versus `access-gesture-avoids-system-gestures`: the rules contradict each other. The first says iOS (and Android) SHOULD open the panel with a shake. The second says the panel SHOULD NOT use a gesture the system binds, and names "shake is the iPhone's undo gesture". The research leaves this to the owner (open question 3, "Whether to keep shake as the iOS access gesture"), and `rationale.md` says "which the owner weighs", but `owner-list.md` names only `typescript-debug-access`. Fix: add the iOS shake question to `owner-list.md`. Or reconcile the two rules, either by naming a non-system entry point for iOS in `platform-access-methods`, or by having `access-gesture-avoids-system-gestures` state the Debug-only shake as a documented exception.
- `rules.md`, `debug-only-config-panel`: "Apps MUST include a debug-only configuration panel" is at MUST strength, but none of the six cited claims requires every app to have a panel. Research open question 2 says "No source mandates that every app MUST include a debug panel; the requirement is a cookbook policy choice", and `rationale.md` repeats it. The rule was kept for the owner, yet it is not in `owner-list.md`. Fix: add `debug-only-config-panel` (the MUST-include policy) to `owner-list.md`.
- `rules.md`, `panel-in-internal-builds`: research open question 1 ("Debug-only or also present in internal/staging/TestFlight builds … the owner decides") and `rationale.md` ("an open question for the owner") both hand this rule to the owner. It is not in `owner-list.md`. Fix: add it.
- `rules.md`, `windows-debug-settings-page`: the cited claims (`dotnet-if-debug`, `dotnet-conditional-attribute`) support only the `#if DEBUG` guard and the `[Conditional("DEBUG")]` clause. No claim supports the MUSTs that the panel be a settings page with exactly these sections, reached through a debug-only navigation menu item. The rule's section list also leaves out the A/B variant picker, which `debug-only-config-panel` requires in every panel, and `a-build-must-establish.md` repeats that gap. Fix: add the page and menu-item shape to `owner-list.md` as retained policy. Then either add the A/B variant picker to the Windows section list, or state why Windows has none.
- `rules.md`, `sdk-dev-modes-off-in-production`: the rule makes the flag-SDK dev mode (`enableDevMode`) a MUST. Its claim `sdk-dev-mode-off-in-production` quotes "we recommend setting this to `false` in production in most cases", which is a hedged recommendation. The MUST for the developer exception page is backed ("Don't enable … unless … Development"). Fix: make the SDK dev-mode clause SHOULD, keep MUST for developer exception pages, or cite a source stated at MUST strength.
- `rules.md`, `production-overrides-are-guarded`: "MUST be authenticated or cryptographically signed" cites `production-overrides-widen-attack-surface`. Its quote presents signing only as "one option to alleviate this concern" and never mentions authentication. No cited claim requires either. Fix: lower to SHOULD, or cite a source that requires authenticated or signed overrides.
- `rules.md`, `node-env-production-on-servers`: both clauses are MUST and MUST NOT, but the claim `node-env-only-production-on-servers` says servers "should always run with NODE_ENV=production". The quote calls other values "an _antipattern_", which is not a requirement. Fix: make the clauses SHOULD and SHOULD NOT, or cite a source stated at MUST strength.
- `rules.md`, `debug-impact-scales-with-permissions`: the MUST clause ("kept out of every production build") cites only `debug-feature-impact`. That claim describes harm ("can be used to circumvent … bypass paywalls") and states no requirement. Fix: add the claims that do require exclusion to the citation, `debug-features-out-of-production` and `runtime-hiding-is-not-protection`.
- `what-a-reviewer-looks-for.md`: four rules have no defect line:
  - `debug-only-config-panel`: a panel missing one of the four sections.
  - `platform-access-methods` and `windows-debug-settings-page`: an entry point or guard that differs from the listed one, with no reason given in the code.
  - `panel-in-internal-builds`: the panel enabled in the Release configuration for testers, or an internal configuration that also produces the store build.

  Fix: add one defect line for each.
- `a-complete-review-must-establish.md`: five rules are absent from the review bar:
  - `platform-access-methods`: each platform's entry method and guard checked against the list.
  - `panel-in-internal-builds`: any internal configuration confirmed not to produce the store build.
  - `node-env-production-on-servers`: the deployed `NODE_ENV` checked.
  - `debug-impact-scales-with-permissions`: debug controls checked for payment, subscription or authentication bypass and for their permissions.
  - `complement-platform-devtools`: the panel checked for rebuilt devtools and for Flipper dependence.

  Fix: add one line for each, or state in the part why one cannot be established from a review.
- `artifact.json`, `meta.related` is empty (cookbook compliance, referencing; cross-recipe consistency, cross-references). The panel's flag overrides and variant picker rest on the sibling guidelines `feature-flags` and `ab-testing`, and the `ab-testing` review asks that guideline to reference this one. Fix: add `ac616d81-16c2-4f33-9ae4-139d5c24318d` (feature-flags) and `d991b992-07aa-47b9-9d36-4fd1ca81435f` (ab-testing) to `related`.
- `artifact.json`, `meta.summary` is 179 characters. Template conformance requires 160 or fewer. Fix: shorten it, for example "Apps MUST include a debug-only panel (flag overrides, analytics event log, A/B variant picker, environment info) compiled out of release builds." (139 characters).

## Lint

`/lint-artifact cookbook/guidelines/implementing/feature-management/debug-mode`. `cookr` is not on PATH, so the linter ran it through a wrapper. `cookr validate` returned "Validation passed".

```
[PASS] FM-01 / gf-frontmatter-complete: all required fields present (including approved-by and approved-date)
[PASS] FM-02: id is a valid UUID
[PASS] FM-03: index.json entry matches the folder (rdid adc.guideline.implementing.feature-management.debug-mode), no domain field
[PASS] FM-04 / gf-type-field: type is guideline
[PASS] FM-05: version 1.0.3 is valid semver
[PASS] FM-07: license is MIT
[PASS] FM-08: copyright is "2026 Mike Fullerton"
[PASS] FM-09: created and modified are ISO dates
[PASS] FM-10: summary is non-empty
[PASS] FM-11 / gf-title-heading: H1 "Debug mode" matches the title
[PASS] FM-11a: no unresolved links (depends-on and related are empty)
[PASS] FM-12 / gf-change-history: Change History table is present with 4 rows
[PASS] FM-13: no TODO, TBD, FIXME or placeholder text
[PASS] GF-01 / gf-summary-statement: the statement follows the H1
[PASS] GF-02 / gf-structured-guidance: bulleted rules, sections and code examples
[PASS] GF-03 / gf-rfc-keywords: all 18 rules carry MUST, SHOULD or MAY
[PASS] gf-triggers-field: triggers are feature-flags and logging
[PASS] gf-roled-parts: rules, review-focus, review-bar and build-bar parts are present; no routes or hosts
[PASS] gf-roled-parts (build-bar): one line per rule, and the 18 names match the rules exactly
[PASS] gf-named-rules: 18 named rules, unique names
[PASS] gf-research-folder: research.json and research.md both exist; four headings in order; 45 claims, none duplicated, all fields present; every cited claim has a verdict naming it
[PASS] gf-rule-cites-research: every rule ends with one (claim: ...) or (claims: ...) citation, and every id resolves to a claim in research.json
[WARN] GF-04 / gf-compliance-section: no ## Compliance section (optional)
[WARN] gf-research-folder (owner-decides): rule typescript-debug-access has a "contradicted" verdict; kept as written for the owner, as the Rationale notes
```

Pass: 22 | Warn: 2 | Fail: 0. RESULT: CLEAN.

verdict: fail
