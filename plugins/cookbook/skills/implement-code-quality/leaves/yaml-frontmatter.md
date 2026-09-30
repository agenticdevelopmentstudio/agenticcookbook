<!-- leaf: implement-code-quality/yaml-frontmatter · source: guidelines/implementing/code-quality/yaml-frontmatter.md -->

**Rules** (cite as `implement-code-quality/yaml-frontmatter#<slug>`):

- `parser-roadmap-lib-used-parsing-yaml-frontmatter` MUST — The built-in frontmatter parser in roadmap_lib MUST be used for parsing YAML frontmatter. A PyYAML dependency MUST NOT …

# YAML frontmatter

The built-in frontmatter parser in `roadmap_lib` MUST be used for parsing YAML frontmatter. A PyYAML dependency MUST NOT be added. The parser handles the `---` delimited frontmatter block at the top of markdown files.
