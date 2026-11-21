--- draft-2.md
+++ draft.md
@@ -122,7 +122,7 @@
   20. `## Design Decisions`
   21. `## Compliance`
   22. `## Change History` (claim: if-section-order-prior)
-- **short-required-core-labelled-optional-rest**: The ingredient format SHOULD label every section either required, carried by every ingredient, or optional, so that every optional section can be found: the required sections are those `if-section-order` does not mark "(MAY omit)" or "(MAY: …)", and the optional sections are those it marks. (claims: rfc-some-sections-required, rfc3552-security-section-required, rfc-security-considerations-required, act-required-items, act-optional-items, w3c-qa-label-optional-features)
+- **short-required-core-labelled-optional-rest**: The ingredient format SHOULD label every section either required or optional, so that every optional section can be found: the required sections are those `if-section-order` does not mark "(MAY omit)" or "(MAY: …)" (`## Appearance` and `## States` by UI ingredients only, per `if-appearance` and `if-states`), and the optional sections are those it marks. (claims: rfc-some-sections-required, rfc3552-security-section-required, rfc-security-considerations-required, act-required-items, act-optional-items, w3c-qa-label-optional-features)
 - **present-section-uses-specified-heading**: A section that is present SHOULD use its specified heading and heading level. (claim: patternfly-template-omit-but-fixed-headings)
 - **inapplicable-section-stated-not-omitted**: A section an ingredient carries that has nothing to say for it SHOULD say so in one line, as Apple's "No additional considerations for tvOS." does, rather than stand empty, so that a reader can tell a deliberate 'none' from an omission. This holds for the source, even where a published or rendered form drops the empty section, as the RFC Editor does at publication and GOV.UK's template does on its website. (claims: rfc-empty-iana-section-kept, rfc-editor-removes-empty-iana, govuk-template-empty-fields-hidden, rfc-no-actions-statement, w3c-qa-label-optional-features, apple-platform-considerations-none, play-form-even-if-no-data)
 - **informative-sections-labelled**: A section that states no requirements MAY be marked non-normative, with the line "This section is non-normative." (claim: respec-informative-marking)
@@ -164,10 +164,16 @@
 - **if-accessibility**: The ingredient MUST have a `## Accessibility` section.
 
   **Applies when:** always. (claim: wcag-name-role-value)
-- **accessibility-role**: The `## Accessibility` section MUST give the component's role or trait (for example, button, heading, text field), the role assistive technologies determine programmatically. (claim: wcag-name-role-value)
+- **accessibility-role**: The `## Accessibility` section MUST give the component's role or trait (for example, button, heading, text field), the role assistive technologies determine programmatically.
+
+  **Applies when:** UI ingredients; an infrastructure ingredient follows `accessibility-not-applicable-stated`. (claim: wcag-name-role-value)
 - **accessibility-role-from-apg**: Where the ARIA Authoring Practices Guide has a pattern for the component, the role given SHOULD be the one that pattern states (a button has role `button`). (claim: apg-button-role)
-- **accessibility-label**: The `## Accessibility` section MUST state the component's label requirements: the name assistive technologies determine programmatically for it. (claim: wcag-name-role-value)
-- **accessibility-state-announcements**: The `## Accessibility` section MUST state how each change to the component's states (for example, loading, disabled) is notified to assistive technologies. (claim: wcag-name-role-value)
+- **accessibility-label**: The `## Accessibility` section MUST state the component's label requirements: the name assistive technologies determine programmatically for it.
+
+  **Applies when:** UI ingredients; an infrastructure ingredient follows `accessibility-not-applicable-stated`. (claim: wcag-name-role-value)
+- **accessibility-state-announcements**: The `## Accessibility` section MUST state how each change to the component's states (for example, loading, disabled) is notified to assistive technologies.
+
+  **Applies when:** UI ingredients; an infrastructure ingredient follows `accessibility-not-applicable-stated`. (claim: wcag-name-role-value)
 - **accessibility-min-target-size**: The `## Accessibility` section SHOULD give the component's minimum target size. (claims: apple-strive-min-control-size, android-touch-target-48dp, wcag-target-size-minimum-24)
 - **accessibility-not-applicable-stated**: An infrastructure ingredient's `## Accessibility` section SHOULD say that accessibility is out of scope for it, and why, rather than stand empty. (claims: rfc3552-out-of-scope-stated, rfc-empty-iana-section-kept)
 - **accessibility-keyboard-interaction**: The `## Accessibility` section SHOULD describe the component's keyboard interaction, beside its role, states and properties. (claim: apg-keyboard-interaction-section)
@@ -358,7 +364,7 @@
 - `if-type-field`: the `type` field is `ingredient`
 - `if-title-heading`: the first H1 is the frontmatter `title`, exactly
 - `if-section-order`: the sections appear in the 22-entry order, every section not marked MAY is present, and none is out of order
-- `short-required-core-labelled-optional-rest`: every section of the format is either required (unmarked in `if-section-order`) or labelled optional (marked MAY there)
+- `short-required-core-labelled-optional-rest`: every section of the format is either required (unmarked in `if-section-order`; `## Appearance` and `## States` by UI ingredients only) or labelled optional (marked MAY there)
 - `present-section-uses-specified-heading`: each present section uses its specified heading and heading level
 - `inapplicable-section-stated-not-omitted`: no section the ingredient carries is empty: each with nothing to say says so in one line
 - `informative-sections-labelled`: any section marked non-normative states no requirement
@@ -380,10 +386,10 @@
 - `tmpl-states-table`: `## States` is a `| State | Appearance change |` table with a row for each state the component takes
 - `states-include-hover-and-selected`: a component that can be hovered or selected has Hover and Selected rows
 - `if-accessibility`: a `## Accessibility` section is present
-- `accessibility-role`: `## Accessibility` gives the component's role or trait
+- `accessibility-role`: a UI ingredient's `## Accessibility` gives the component's role or trait
 - `accessibility-role-from-apg`: where APG has a pattern for the component, the role given is that pattern's
-- `accessibility-label`: `## Accessibility` states the component's label requirements
-- `accessibility-state-announcements`: `## Accessibility` states how each change to the component's states is notified to assistive technologies
+- `accessibility-label`: a UI ingredient's `## Accessibility` states the component's label requirements
+- `accessibility-state-announcements`: a UI ingredient's `## Accessibility` states how each change to the component's states is notified to assistive technologies
 - `accessibility-min-target-size`: `## Accessibility` gives a minimum target size
 - `accessibility-not-applicable-stated`: an infrastructure ingredient's `## Accessibility` says accessibility is out of scope for it, and why
 - `accessibility-keyboard-interaction`: `## Accessibility` describes the component's keyboard interaction
@@ -434,7 +440,7 @@
 - `overview-states-when-to-use`, `overview-states-when-not-to-use`, `overview-states-why-to-use`: GOV.UK's template asks when to use a component and when not to, and PatternFly's asks how it is used, when and why, so a reader can choose the right component before reading its rules. Only the description is required by GOV.UK; the rest are prompts, hence SHOULD.
 - `behavioral-requirements-named`: OASIS gives each test assertion a unique identifier that maps it to the statement it tests; a unique name does that for a requirement and its test vectors. SHOULD, since the Committee Note only recommends universal uniqueness.
 - `appearance-contrast-in-all-states`: Fluent requires 4.5:1 text and 3:1 icon contrast in every interactive state, because a state change that drops contrast makes the control unreadable in that state. SHOULD, since it is one design system's requirement for its own buttons.
-- `tmpl-states-table`, `states-include-hover-and-selected`: Apple requires a press state so a button does not feel unresponsive, and Flutter's, Material's and Fluent's state lists include hover and selected; a row per state lets a builder style each one. SHOULD, because which states apply depends on the component.
+- `tmpl-states-table`, `states-include-hover-and-selected`: Apple requires a press state so a button does not feel unresponsive, and Flutter's and Material's state lists include hover and selected, and Fluent's includes selected; a row per state lets a builder style each one. SHOULD, because which states apply depends on the component.
 - `accessibility-role-from-apg`: APG states the role for each pattern, so the role need not be invented; SHOULD, since a component may have no APG pattern or a platform name for the role.
 - `accessibility-min-target-size`, `per-platform-target-sizes`, `tmpl-accessibility-min-tap-target`, `tmpl-platform-notes-platforms`: Apple asks for each platform's recommended minimum control size so controls are comfortable to tap and click; the platforms disagree on the value (Apple by platform, Android 48dp, Windows 40px, WCAG 24px at AA and 44px at AAA), so one value is wrong for most of them and each targeted platform needs its own entry. They are SHOULD because Apple and Android recommend rather than require their sizes. `tmpl-accessibility-min-tap-target` keeps the template's 44×44pt word for word; which default the template should give is the owner's open question.
 - `accessibility-keyboard-interaction`: APG's Button pattern documents keyboard interaction beside roles, states and properties, so a keyboard user's path is specified with the rest; SHOULD, since that is one APG page's layout.
@@ -447,12 +453,12 @@
 - `tmpl-accessibility-options`: Apple asks apps to respond to Reduce Motion and Increase Contrast and not to convey information by color alone, and WCAG forbids color as the only means; the web reads the same settings through media features, so one table covers every platform. SHOULD, because which options apply depends on the component.
 - `tmpl-analytics-events`, `analytics-event-names-fit-platform-limits`: the template's table is kept word for word for the owner, who decides whether its names should use dots or underscores; where events go to Firebase Analytics, which accepts only letters, digits and underscores, the MUST rule governs, so `tmpl-analytics-events` is a SHOULD such an ingredient departs from.
 - `tmpl-privacy-fields`, `privacy-states-encryption-in-transit`: Apple counts data as collected only when it leaves the device and is kept longer than the request needs, and Google Play defines ephemeral processing and asks whether data is encrypted in transit, so these fields answer the stores' privacy questions. SHOULD, since `## Privacy` is itself optional in `if-section-order`.
-- `tmpl-logging-subsystem-category`: Apple defines subsystem and category so that log messages can be filtered by functional area; SHOULD, since both are optional on Apple's Logger and other platforms name them differently.
+- `tmpl-logging-subsystem-category`: Apple defines subsystem and category so that each message carries the context of its functional area; SHOULD, since both are optional on Apple's Logger and other platforms name them differently.
 - `tmpl-design-decisions-approved`: a decision record carries its status, proposed until the stakeholders agree and accepted after (Nygard), so a reader can tell an agreed decision from a proposal. SHOULD, since the source is one practitioner's practice.
 - `tmpl-approval-fields`: kept word for word as the template has it, for the owner, who decides whether the template keeps them; no source and no required-field list prescribes them, hence SHOULD.
 - `tmpl-compliance-link-form`: a test assertion names the precise statement it tests (OASIS), and a UUID is unique across space and time (RFC 9562), so a link by UUID survives a check's rename. SHOULD, since a link by rdid still resolves.
 - `change-history-iso-dates`: Keep a Changelog recommends ISO 8601 dates, an international standard, so every reader reads a date the same way. SHOULD, as Keep a Changelog's own recommendation.
-- `section-structure-machine-checked`: a structural check a tool can decide (headings, required fields, order) need not be left to a reader; MD043's wildcards stand only for unspecified headings, so named optional sections take a custom rule.
+- `section-structure-machine-checked`: a structural check a tool can decide (headings, required fields, order) need not be left to a reader; MD043's wildcards `*`, `+` and `?` stand for unspecified headings; a custom rule can name an optional section.
 - `released-version-immutable`: Semantic Versioning forbids changing a released version, so every reader of a version sees the same text.
 
 ## References
