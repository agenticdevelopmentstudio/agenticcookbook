---
title: Input validation
type: guideline
summary: Validate untrusted input at the boundary.
---
# Input validation

Validate at the boundary.

- **validate-at-boundary**: Every handler MUST validate its input before use.
- **reject-unknown-fields** (api): Parsers SHOULD reject fields they do not know.
- Error messages MUST NOT echo raw input back to the caller.

| ID | Requirements |
|----|--------------|
| iv-1 | `validate-at-boundary` |
| iv-2 | `reject-unknown-fields`, `validate-at-boundary` |

## Change History

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-01-01 | Initial |
