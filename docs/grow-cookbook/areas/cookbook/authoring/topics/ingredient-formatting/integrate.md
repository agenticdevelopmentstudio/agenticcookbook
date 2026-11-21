# Integrate: ingredient-formatting

## Lossless

New topic: its text was never in the cookbook at the base commit (it came from tbd/compliance/, which owner-list.md carries word for word), so `cookr roles lossless` has no base text to check.

## Validate

`cookr validate` passed; its owner-decides rows are listed under For the owner. Bumped to 1.0.1; /add-artifact approved it (lint 24 pass, 0 fail).

## For the owner

Rules standing as they were until you decide each (`cookr validate` owner-decides):

- rule 'if-applicability' cites 'if-applicability-prior', which the research rules unsupported
- rule 'if-frontmatter-complete' cites 'if-frontmatter-complete-prior', which the research rules unsupported
- rule 'tmpl-approval-fields' cites 'tmpl-approval-fields-prior', which the research rules unsupported
- rule 'if-type-field' cites 'if-type-field-prior', which the research rules unsupported
- rule 'if-title-heading' cites 'if-title-heading-prior', which the research rules unsupported
- rule 'if-section-order' cites 'if-section-order-prior', which the research rules unsupported
- rule 'component-recipe-sections-in-order' cites 'component-recipe-sections-in-order-prior', which the research rules unsupported
- rule 'if-appearance' cites 'if-appearance-prior', which the research rules unsupported
- rule 'if-states' cites 'if-states-prior', which the research rules unsupported
- rule 'tmpl-accessibility-min-tap-target' cites 'tmpl-accessibility-min-tap-target-prior', which the research rules contradicted
- rule 'if-edge-cases' cites 'if-edge-cases-prior', which the research rules unsupported
- rule 'if-configuration' cites 'if-configuration-prior', which the research rules unsupported
- rule 'tmpl-deep-linking-patterns' cites 'tmpl-deep-linking-patterns-prior', which the research rules contradicted
- rule 'tmpl-analytics-events' cites 'tmpl-analytics-events-prior', which the research rules contradicted
- rule 'if-logging' cites 'if-logging-prior', which the research rules unsupported
- rule 'if-platform-notes' cites 'if-platform-notes-prior', which the research rules unsupported
- rule 'if-reference-implementations' cites 'if-reference-implementations-prior', which the research rules unsupported
- rule 'if-design-decisions' cites 'if-design-decisions-prior', which the research rules unsupported
- rule 'if-compliance' cites 'if-compliance-prior', which the research rules contradicted
- rule 'if-change-history' cites 'if-change-history-prior', which the research rules unsupported

Open questions from the owner list:

- Should an inapplicable section be omitted, or kept with a one-line 'not applicable' note in the source (IETF/W3C practice) and hidden only in a rendered form (GOV.UK practice)?
- Should ingredients split into UI and infrastructure variants with their own section lists, or keep one schema that applies UI-only sections conditionally (JSON Schema if/then)?
- Which of the formatting checks should become a schema or lint rule rather than prose: the section order, the frontmatter fields, the H1-equals-title check?
- Should the template's tap-target default be one value, a per-platform table (Apple per platform, Android 48dp, Windows 40px) or the WCAG 2.2 AA 24px floor with 44px as the enhanced target?
- Should analytics event names use dots, or underscores to fit Firebase's naming limits?
- Should the Apple deep-linking row show a universal link instead of a custom URL scheme?
- Should the compliance status vocabulary keep 'partial', or adopt EARL's passed/failed/cantTell/inapplicable/untested?
- Should the section-order and section-presence rules stay MUST where the sources support only recommended strength?
- Should the template keep approved-by and approved-date, which no source and no required-field list prescribes?
- Should 'loading' stay among the default states, given that no platform's state list includes it?
- Should the H1 duplicate the frontmatter title, given that markdownlint's default treats a front-matter title as the top-level heading?

Notes:

- accessibility-options-include-text-size requires `## Accessibility Options` for any ingredient that shows text, while if-section-order, kept word for word, marks that section (MAY omit). Deciding if-section-order settles it.
- component-recipe-sections-in-order carries the prior rule word for word, so its text still opens with the prior rule's own name (`- **must-contain-template-sections-in-order**: The recipe MUST ...`), a second rule name nested inside the first. Deciding the rule settles its wording.
- if-compliance (kept word for word, research contradicted) fixes the status values as passed, failed, partial, while compliance-status-includes-inapplicable says they SHOULD include inapplicable; conventions.md's "Only list checks that are applicable" sides with if-compliance. conventions.md's status values were left as they were until you decide.

integrated: 2026-11-21
