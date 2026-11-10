
- **Missing frontmatter fields.** A recipe omits `summary` or `platforms` because the author considered them optional. The parser fails validation with a missing-key error.
- **Scalar platforms field.** `platforms: ios` instead of `platforms:\n  - ios`. The YAML type is wrong; tooling that iterates platforms breaks.
- **Invalid semver.** `version: 1.0` or `version: v1.0.0` — neither is valid semver. The correct form is `1.0.0`.
- **Empty required sections.** A recipe contains `## Accessibility` with no content and no `NEEDS REVIEW` marker. This silently passes structural checks while hiding an unfilled gap.
- **Wrong section order.** "Edge Cases" appears before "Conformance Test Vectors." Automated diffing tools and reviewers expect a fixed order; misordering signals the recipe was authored without consulting the template.
- **Title mismatch.** The frontmatter `title` is `"Submit Button"` but the document heading reads `# Primary Action Button`. These must be identical.
- **Multi-line summary.** The `summary` field uses a YAML literal block scalar (`summary: |`) and spans two lines. Parsers that expect a string scalar may coerce or truncate it unexpectedly.
- **Duplicate `id`.** A recipe is copy-pasted from an existing one and the `id` is never regenerated. The cookbook now has two artifacts with the same identity.

