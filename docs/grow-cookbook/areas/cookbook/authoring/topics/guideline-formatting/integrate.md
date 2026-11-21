# Integrate: guideline-formatting

## For the owner

Rules standing as they were until you decide each (`cookr validate` owner-decides):

- rule 'gf-title-heading' cites 'gf-title-heading-prior', which the research rules unsupported
- rule 'gf-rfc-keywords' cites 'gf-rfc-keywords-prior', which the research rules unsupported
- rule 'gf-roled-parts' cites 'gf-roled-parts-prior', which the research rules unsupported
- rule 'conv-roled-artifact-complete' cites 'conv-roled-artifact-complete-prior', which the research rules unsupported
- rule 'conv-role-values' cites 'conv-role-values-prior', which the research rules unsupported
- rule 'conv-no-roles-under-reviewing' cites 'conv-no-roles-under-reviewing-prior', which the research rules unsupported
- rule 'conv-four-skills' cites 'conv-four-skills-prior', which the research rules unsupported
- rule 'conv-skill-names' cites 'conv-skill-names-prior', which the research rules unsupported
- rule 'conv-legacy-keeps-working' cites 'conv-legacy-keeps-working-prior', which the research rules unsupported
- rule 'gf-research-folder' cites 'gf-research-folder-prior', which the research rules unsupported
- rule 'gf-rule-cites-research' cites 'gf-rule-cites-research-prior', which the research rules unsupported
- rule 'gf-compliance-section' cites 'gf-compliance-section-prior', which the research rules unsupported
- rule 'gf-triggers-field' cites 'gf-triggers-field-prior', which the research rules unsupported

Open questions from the owner list:

- Whether gf-research-folder and gf-rule-cites-research stay MUST: the strongest outside sources (IOM Standard 5.1, AGREE II) phrase per-recommendation evidence as 'should be provided' or as an appraisal criterion; the owner decides whether the cookbook's research-first ruling justifies MUST.
- Whether gf-rfc-keywords stays MUST: the W3C QA Framework requires a consistent, distinguishable style for requirements (Requirement 7) and gives RFC 2119 keywords only as a technique; the owner decides whether the cookbook requires the keywords themselves (keyword case belongs to requirement-keywords).
- Whether gf-roled-parts stays MUST: outside sources support labelling normative and informative content and separating reference, how-to and explanation at SHOULD/good-practice strength; the specific role vocabulary and the four required roles are the cookbook's own design.
- Whether gf-title-heading (H1 equals the frontmatter title) is kept: no source requires it, and markdownlint's default (MD025 with front_matter_title) treats a frontmatter title as the document's top-level heading, so a title plus an H1 is reported as a second top-level heading unless the option is disabled.
- Whether gf-compliance-section is kept: no outside source speaks to a section listing evaluated compliance checks; the W3C's conformance clause is a different element (what conformance requires), proposed as the new rule conformance-and-scope-statement.
- Whether examples-are-non-normative is written as MUST NOT: the W3C Manual of Style says 'document editors must not make any figure, example or note normative' but also says 'No requirements for W3C publications are in this document.'
- Whether normative-keywords-only-where-required belongs to this topic or to requirement-keywords: it is about when a rule carries an obligation at all (structure), but it is RFC 2119's own keyword guidance.
- Whether keep-rule-lists-short applies to a rules part: Microsoft's seven-item limit is for lists in general ('if possible'), not for a rule-bearing document's rule count.
- Whether the change history is ordered newest-first (Keep a Changelog) or oldest-first (the conventions.md example has one row, so the order is not stated).
- Whether conv-* rules that state tool behaviour (conv-legacy-keeps-working, conv-role-values, conv-no-roles-under-reviewing, conv-roled-artifact-complete, conv-four-skills, conv-skill-names) remain in conventions.md as design statements without outside research, per owner ruling Q12.

Disputed findings the author left for you:

- requirement-keywords R1.8: gf-rfc-keywords is on this topic's owner list and is kept word for word (claim: gf-rfc-keywords-prior), and the brief lists "whether normative-keywords-only-where-required belongs here or in requirement-keywords" as an open owner question; replacing them with a citation of requirement-keywords would settle that question, and would leave the `new`-verdict claim rfc2119-use-sparingly cited by no rule. The draft links requirement-keywords in its intro and `related` instead.

## Lossless

New topic: its text was never in the cookbook at the base commit (it came from tbd/compliance/, which owner-list.md carries word for word), so `cookr roles lossless` has no base text to check.

## Validate

`cookr validate` passed; its owner-decides rows are listed under For the owner. Bumped to 1.0.1; /add-artifact approved it (lint 24 pass, 0 fail).

integrated: 2026-11-21
