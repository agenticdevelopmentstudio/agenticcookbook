<!-- leaf: review-general/conformance-criterion-walk · source: guidelines/reviewing/conformance-criterion-walk.md -->

**Rules** (cite as `review-general/conformance-criterion-walk#<slug>`):

- `conformance-explicit-contract` MUST
- `conformance-per-criterion-verdict` MUST
- `conformance-divergent-distinct` MUST
- `conformance-full-walk` MUST
- `conformance-demand-evidence` MUST

# Conformance: The Criterion Walk

Conformance review asks a different question than quality review: did the change do what it was asked to do, completely? It judges a diff against an explicit acceptance contract.

## Acceptance Contracts
- **conformance-explicit-contract**: Conformance MUST be judged against an explicit, criterion-by-criterion acceptance contract, not an implicit sense of "done".

## Met / Unmet / Divergent
- **conformance-per-criterion-verdict**: Each acceptance criterion MUST be judged individually as met, unmet, or divergent.
- **conformance-divergent-distinct**: Divergent — built, but in a way that conflicts with the intent ("built right but wrong") — MUST be distinguished from unmet (not built at all); they have different fixes.

## Coverage Backstop
- **conformance-full-walk**: An always-on reviewer MUST walk every criterion as a coverage backstop, so no criterion is silently skipped when the diff does not obviously touch it.

## Demand Evidence
- **conformance-demand-evidence**: A "met" verdict MUST cite evidence in the diff; absence of evidence is not "met".
