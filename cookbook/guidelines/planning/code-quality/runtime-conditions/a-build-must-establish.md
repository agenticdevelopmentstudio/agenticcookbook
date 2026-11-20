
- `should-group-permission-gated-code`: every permission in the findings lists its files, and they sit in one recommended group, or the findings say why not
- `should-separate-entitlement-groups`: every entitlement in the findings lists the files needing it, and a group needing one the others lack is its own candidate
- `should-flag-version-gated-features`: every OS version gate is listed with its files and guarded code
- `may-give-large-version-gated-code-own-group`: every version-gated candidate group is shown to make up a large portion of its source group
- `should-group-environment-specific-code`: every environment or configuration prerequisite's files sit in one configuration infrastructure group, or the findings say why not
- `should-document-feature-flags`: every feature flag is listed with its system and what it guards
- `should-not-group-unenabled-code-paths`: no recommended group is built around an unenabled code path
- `should-note-remote-config-ordering`: every remote config dependency appears as an ordering constraint in the findings
