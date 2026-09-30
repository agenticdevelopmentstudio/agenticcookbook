<!-- leaf: implement-code-quality/file-paths · source: guidelines/implementing/code-quality/file-paths.md -->

**Rules** (cite as `implement-code-quality/file-paths#<slug>`):

- `pathlib-path-used-os-path-path` MUST — pathlib.Path MUST be used, not os.path. All path manipulation MUST go through pathlib.

# File paths

`pathlib.Path` MUST be used, not `os.path`. All path manipulation MUST go through `pathlib`.

```python
from pathlib import Path

roadmap_dir = Path.home() / ".roadmaps" / project_name
```
