
1. **High internal coupling ratio (>0.6) = strong scope group candidate.** If 80% of a directory's imports are within the same directory, it is self-contained.
2. **Low coupling ratio (<0.3) = likely belongs elsewhere.** A file that imports mostly from other directories is probably a leaf consumer or a shared utility — consider merging it into the scope group it depends on most.
3. **Unidirectional dependency = separate scope groups.** If layer A only imports layer B (never the reverse), A and B are separate concerns even if they live near each other.
4. **High fan-in files are shared infrastructure.** A file imported by 10+ other files across multiple candidate groups is a cross-cutting dependency — flag it for `cross-cutting-detection` rather than assigning it to one group.
5. **Circular dependencies force co-location.** Files in a cycle must remain in the same scope group until the cycle is resolved. Document the cycle as a refactoring target.
6. **Star imports inflate apparent coupling.** A `import com.example.util.*` may only use one symbol — do not count star imports as full coupling without verifying symbol usage.

