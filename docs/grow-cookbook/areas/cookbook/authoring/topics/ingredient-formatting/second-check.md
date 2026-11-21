## earl-outcome-values
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: EARL 1.0 recommends exactly these five earl:OutcomeValue instances ("where applicable it is recommended"), and none of them is "partial". The word "partial" appears only in the TestCase and semiAuto definitions.

## act-outcome-types
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: ACT 1.1 lists five outcome types (inapplicable, passed, failed, cantTell, untested). The recorded quote stops after three of them, but the source is contiguous and holds those words.

## apple-min-control-size-per-platform
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- note: I read the HIG through its JSON data endpoint. The table cells match the quote and the claim exactly: iOS/iPadOS 44/28, macOS 28/20, tvOS 66/56, visionOS 60/28, watchOS 44/28. Only the formatting differs.
- result: confirmed

## android-touch-target-48dp
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source says "we recommend ... at least 48dpx48dp. Larger is even better."

## windows-touch-target-40
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source says "In general, set your touch target size to 7.5mm square range (40x40 pixels on a 135 PPI display at a 1.0x scaling plateau)."

## wcag-target-size-minimum-24
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is SC 2.5.8 Target Size (Minimum), which is marked Level AA.

## apple-universal-links-recommended
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The JSON splits the sentence at the "universal links" link run, so the difference is formatting only. The wording matches.

## apple-url-scheme-attack-vector
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Apple calls it a "potential attack vector" and goes on to "validate all URL parameters and discard any malformed URLs". The claim's "is an attack vector" drops the word "potential", but it is still fair as a warning.

## firebase-event-name-charset
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The charset rule means a dotted name is invalid. The page also reserves the "firebase_", "google_" and "ga_" prefixes.

## rfc-empty-iana-section-kept
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is RFC 8126 §9.1. It adds "This is a change from the prior practice of requesting that such sections be removed by the RFC Editor".

## rfc-no-actions-statement
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: RFC 8126 §9.1 is specifically about the IANA Considerations section. It says such documents "should ... include an IANA Considerations section that states: This document has no IANA actions." The claim widens this to any mandated section, which the source does not say.
- correction: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST

## w3c-qa-label-optional-features
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source is QA Framework Good Practice 16, "Clearly identify optional features". It is a good practice, which fits the claim's "should".

## apple-platform-considerations-none
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Under the Buttons page's "Platform considerations" heading, the italic line "No additional considerations for tvOS." comes before the per-platform subsections (iOS/iPadOS and the rest).

## play-form-even-if-no-data
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: "Must complete this form", and the form "can indicate that no user data is collected or shared."

## rfc-editor-removes-empty-iana
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: RFC 7322 §4.8.3 says exactly this. However, RFC 8126 §9.1 (2017, later than 7322) calls removal "the prior practice", and IANA now prefers that the empty section be kept in the RFC. The practice may therefore be out of date.

## govuk-template-empty-fields-hidden
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is Step 3 of the template: "Any fields without any data points will not be displayed on the website." The "opposite convention" part is the research's own interpretation.

## md043-enforces-heading-structure
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source says this, word for word.

## md043-wildcards-only
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The doc lists the `*`, `+` and `?` wildcards, plus `%` regex headings and `^` loops. It never says a named heading cannot be optional or that a custom rule is needed. The "only" and "cannot" parts are inference. Also, `?` means exactly one heading, not an optional one.
- correction: refuted (quote-found yes, supports-claim partly); trust 80 -> 60; a rule citing it cannot carry MUST

## markdownlint-custom-rules
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: "Custom rules can do everything the built-in rules can". The claim's example uses follow directly from that.

## vale-occurrence-min-flags-absence
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The doc says "`min` makes absence a violation: a scope with fewer than `min` matches is flagged", and the check is evaluated once per scope. The required-heading example is illustration only.

## vale-script-arbitrary-rules
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The doc's own example script message is about inserting a section heading.

## json-schema-required-properties
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is Validation §6.5.3 `required`.

## json-schema-prefixitems-positional
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is Core §10.3.1.1. The "only if modelled as an ordered array" consequence fits the same document's data model, where only arrays are ordered.

## json-schema-objects-unordered
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The data model defines an object as "An unordered set of properties ..." and an array as "An ordered list of instances".

## respec-privsec-lint
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is the `privsec-section` lint. It is off by default but on by default for W3C specs.

## respec-headingless-lint
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is the `no-headingless-sections` lint, which is on by default.

## rfc-some-sections-required
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: RFC 7322 §4 marks some sections [Required] (Security Considerations, for one), marks IANA as "[Required in I-D]", and leaves others unmarked.

## rfc-security-considerations-required
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote backs only the RFC half ("All RFCs must contain a section that discusses the security considerations"). Nothing in the source supports the general rule that "a long-lived specification template keeps a short list of always-required sections".
- correction: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST

## rfc3552-security-section-required
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: RFC 3552 cites RFC 2223, which is now obsolete. RFC 7322 §4.8.5 carries the same requirement today.

## act-required-items
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The full list goes on past the quote: Rule Input, Applicability, Expectations, Background, Assumptions, Accessibility Support, Examples, Rule Versions, ACT Rules Format Version and Glossary.

## act-optional-items
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: "An ACT Rule MAY also contain", followed by five items marked optional, Implementations among them.

## patternfly-template-omit-but-fixed-headings
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source says this, word for word, under "Design guidelines sections".

## act-examples-pass-fail-inapplicable
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: "Each rule must have one or more examples for passed, failed, and inapplicable outcomes."

## govuk-when-not-to-use
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The template has a "When not to use this component" field next to the "when to use" field.

## patternfly-usage-when-to-use
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote is the description of the "Usage (H2)" section, but the template does not open with Usage. It opens with "Elements (H2)", the annotated image of the component's parts, and Usage comes second.
- correction: refuted (quote-found yes, supports-claim partly); trust 74 -> 54; a rule citing it cannot carry MUST

## apple-strive-min-control-size
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: "Strive to meet the recommended minimum control size for each platform", followed by the per-platform table.

## apple-button-hit-region-44
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source says this, word for word, on the Buttons page.

## android-touch-target-spacing
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The source's wording is "Consider making touch targets at least 48x48dp, separated by 8dp of space or more". That is advisory, which matches "asks for".

## wcag-target-size-enhanced-44
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is SC 2.5.5 Target Size (Enhanced), Level AAA.

## wcag-resize-text
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is SC 1.4.4 Resize Text, Level AA.

## apple-dynamic-type
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The Typography page supports Dynamic Type on iOS, iPadOS, tvOS, visionOS and watchOS. It never mentions Reduce Motion or Increase Contrast, so the "display option next to" part is unsupported.
- correction: refuted (quote-found yes, supports-claim partly); trust 86 -> 66; a rule citing it cannot carry MUST

## flutter-hover-state
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is the definition of `WidgetState.hovered`.

## flutter-selected-state
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is the definition of `WidgetState.selected`, for toggleable or selectable items.

## material-states-list
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The source is the Checkbox doc of material-components-android only. It lists those states for checkboxes, but one component's doc does not show that Material's component documentation in general lists states this way.
- correction: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST

## fluent-rest-selected-states
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The sentence is in the Toggle button behavior section of the Fluent 2 Button usage page.

## fluent-contrast-in-all-states
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: "Must pass 4.5:1 ... 3:1 ... in all interactive states."

## apg-keyboard-interaction-section
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: Only the Button pattern page is cited. It does have "Keyboard Interaction" next to "WAI-ARIA Roles, States, and Properties", but one page does not establish "each APG pattern page".
- correction: refuted (quote-found yes, supports-claim partly); trust 78 -> 58; a rule citing it cannot carry MUST

## android-app-links-recommended
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: "For deep links to your website, App Links is a recommended approach." The page describes App Links as verified links.

## play-encryption-in-transit
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: It appears as a question under "Encryption in transit", in the list of practices the Data safety section lets developers highlight.

## act-assumptions-listed
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is ACT §4.8.1 Assumptions, which uses "must".

## rfc3552-out-of-scope-stated
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: RFC 3552 §5 says "Authors MUST describe 1. which attacks are out of scope (and why!) 2. which attacks are in-scope".

## respec-informative-marking
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is ReSpec's `.informative` class (§9.6).

## semver-released-immutable
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: This is SemVer 2.0.0 item 3, which uses MUST NOT and MUST.

## kac-iso-dates
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Keep a Changelog recommends dates like 2017-07-17 (YYYY-MM-DD, ISO 8601) for changelog entries. It is a recommendation, which matches "should".
