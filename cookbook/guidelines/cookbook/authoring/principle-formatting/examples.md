
A short principle, shown as its compiled doc with the frontmatter cut to the fields the rules name (`#` marks the title and `##` the history; every other required field is present in the real file):

```text
---
title: "Explicit Over Implicit"
type: principle
summary: "Make behaviour visible in code and config; apply it when choosing between a convention and a declaration."
---

# Explicit Over Implicit

State what code does where a reader looks for it. Hidden behaviour is the
behaviour nobody reviews, so it is the first to break unnoticed.

- Declare a dependency where it is used instead of resolving it from a global.
- Name a default in configuration instead of burying it in a constructor.
- Link the dependency-injection guideline for how; this principle says only why.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.0 | 2026-11-21 | Name | Adds the configuration bullet |
| 1.0.0 | 2026-04-04 | Name | Initial creation |
```

The title and the H1 match, the statement opens the body and says why, each bullet is a full sentence, the third links the detail rather than copying it, and the history has a dated row per version, newest first.

