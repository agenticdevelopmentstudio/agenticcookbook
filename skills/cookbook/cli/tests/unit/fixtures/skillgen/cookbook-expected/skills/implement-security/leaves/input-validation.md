<!-- leaf: implement-security/input-validation · source: guidelines/implementing/security/input-validation.md -->

**Rules** (cite as `implement-security/input-validation#<slug>`):

- `validate-at-boundary` MUST
- `reject-unknown-fields` SHOULD (api)
- `error-messages-not-echo-raw-input-back` MUST — Error messages MUST NOT echo raw input back to the caller.

# Input validation

Validate at the boundary.

- **validate-at-boundary**: Every handler MUST validate its input before use.
- **reject-unknown-fields** (api): Parsers SHOULD reject fields they do not know.
- Error messages MUST NOT echo raw input back to the caller.

| ID | Requirements |
|----|--------------|
| iv-1 | `validate-at-boundary` |
| iv-2 | `reject-unknown-fields`, `validate-at-boundary` |
