
A guideline's triggers, in its meta, most specific first (`schema-design` is a part of `database-operations`, and `performance-optimization` also covers rendering):

```yaml
triggers:
  - schema-design
  - database-operations
  - performance-optimization
```

An agent that is about to write tests for an API client queries two triggers at once and loads the union:

```text
writing-tests ∪ api-integration  →  every guideline tagged with either value
```

A rename kept resolvable (a sketch, in SKOS terms):

```text
prefLabel:   ui-implementation
altLabel:    ui-work            (old value; still resolves to the new one)
historyNote: 2026-11-21 renamed from ui-work
```

