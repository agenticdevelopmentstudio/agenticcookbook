---
id: af8d7c30-f595-4d2d-b780-bdcbd1cb5962
title: "File paths"
domain: agenticdevelopercookbook://guidelines/reviewing/code-quality/file-paths
type: guideline
version: 1.0.2
status: accepted
language: en
created: 2026-03-27
modified: 2026-04-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Use `pathlib.Path`, not `os.path`. All path manipulation should go through `pathlib`."
platforms:
  - python
languages:
  - python
tags:
  - file-paths
  - language
  - python
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
triggers:
  - new-module
---

# File paths

`pathlib.Path` MUST be used, not `os.path`. All path manipulation MUST go through `pathlib`.

```python
from pathlib import Path

roadmap_dir = Path.home() / ".roadmaps" / project_name
```

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
