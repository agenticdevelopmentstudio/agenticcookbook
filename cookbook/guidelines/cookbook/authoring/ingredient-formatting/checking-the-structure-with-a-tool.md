
| Check | Tool | Limit |
|---|---|---|
| Frontmatter comes first | Any front-matter reader (Jekyll and its kin) | It must be the first thing in the file, valid YAML between triple-dashed lines |
| Required frontmatter fields | JSON Schema `required` | Checks presence only; key order cannot be checked, since objects are unordered |
| `type: ingredient` | JSON Schema `const` | |
| UI-only sections for UI ingredients | JSON Schema `if` / `then` / `else` | One schema applies the UI checks and skips them for infrastructure ingredients |
| Section order | JSON Schema `prefixItems` | Only once the sections are parsed into an ordered array |
| Heading list | markdownlint MD043 | Unspecified headings as wildcards: `*` zero or more, `+` one or more, `?` exactly one |
| Named optional sections, H1 equals the title | markdownlint custom rule, Vale `script` | Custom code |
| A required heading is present | Vale `occurrence` with `min` | |
| RFC 2119 keywords with no `## Behavioral Requirements` | A custom rule, as ReSpec does for a conformance section | |
| The document starts with an H1 | markdownlint MD041 | Does not compare the H1 with the front-matter `title` |
| One top-level heading | markdownlint MD025 | Treats a front-matter `title` as the H1, so by default flags the `# Title` after it |

