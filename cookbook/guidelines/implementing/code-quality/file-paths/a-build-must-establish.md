
- `must-use-pathlib-not-os-path`: a search of the new code finds no `os.path`
- `must-route-all-path-manipulation-through-pathlib`: every path the new code joins, splits or inspects is a `pathlib.Path`, with no string path manipulation
