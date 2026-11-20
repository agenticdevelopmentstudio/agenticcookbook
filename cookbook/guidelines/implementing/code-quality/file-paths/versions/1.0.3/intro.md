
# File paths

`pathlib.Path` MUST be used, not `os.path`. All path manipulation MUST go through `pathlib`.

```python
from pathlib import Path

roadmap_dir = Path.home() / ".roadmaps" / project_name
```

