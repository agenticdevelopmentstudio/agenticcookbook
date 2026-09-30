<!-- leaf: implement-code-quality/use-roadmaplib · source: guidelines/implementing/code-quality/use-roadmaplib.md -->

**Rules** (cite as `implement-code-quality/use-roadmaplib#<slug>`):

- `from-roadmap-lib-used-roadmap-operations-reading` MUST — Functions from roadmap_lib MUST be used for all roadmap operations (reading state, parsing frontmatter, finding steps, …

# Use roadmap_lib

Functions from `roadmap_lib` MUST be used for all roadmap operations (reading state, parsing frontmatter, finding steps, etc.). Functionality that already exists in the library MUST NOT be reimplemented.
