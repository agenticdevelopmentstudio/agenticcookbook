
- `should-treat-high-coupling-ratio-as-candidate`: If 80% of a directory's imports are within the same directory, it is self-contained.
- `should-consider-merging-low-ratio-files`: A file that imports mostly from other directories is probably a leaf consumer or a shared utility.
- `should-separate-unidirectional-layers`: A and B are separate concerns even if they live near each other.
- `should-flag-high-fan-in-files`: A file imported by 10+ other files across multiple candidate groups is a cross-cutting dependency.
- `should-not-count-star-imports-as-full-coupling`: A `import com.example.util.*` may only use one symbol.
