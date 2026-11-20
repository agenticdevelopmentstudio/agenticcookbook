
- `must-use-pathlib-not-os-path`: no code uses `os.path`; paths are `pathlib.Path`
- `must-route-all-path-manipulation-through-pathlib`: every path manipulation goes through `pathlib`
