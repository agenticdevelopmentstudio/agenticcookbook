
- `should-separate-into-sequential-phases`: whether correctness, design quality, and performance were handled as sequential phases
- `should-first-make-it-work`: whether a working solution for the common case exists before later phases began
- `should-then-make-it-right`: whether the working solution was refactored for clarity, its edge cases handled and its design cleaned up
- `should-optimize-only-measured-slowness`: whether every optimization is backed by a measurement proving the code slow
- `must-not-skip-make-it-right`: whether phase 2 (make it right) was done before any phase 3 optimization
