
These examples are informative.

A rules part with two named rules, each citing its claims at its end:

```markdown
## Rules

- **index-foreign-keys**: Every foreign-key column MUST have an index. (claims: fk-index-postgres, fk-index-sqlite)
- **name-indexes-by-columns**: An index SHOULD be named for the table and columns it covers. (claim: index-naming-convention)
```

The build-bar lines that go with them, one per rule:

```markdown
## A build must establish

- `index-foreign-keys`: every foreign-key column has an index.
- `name-indexes-by-columns`: every index is named for its table and columns.
```

A rule that is not named, and one whose citation is not at its end, both of which `cookr roles check` reports:

```markdown
- Every foreign-key column MUST have an index. (claim: fk-index-postgres)
- **index-foreign-keys**: Every foreign-key column MUST have an index (claim: fk-index-postgres), on every table.
```

A change history row:

```markdown
| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-11-21 | Mike Fullerton | Initial creation |
```

