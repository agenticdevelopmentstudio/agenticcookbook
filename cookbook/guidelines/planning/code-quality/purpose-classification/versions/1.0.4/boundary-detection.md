
1. **Purpose-coherent groups are correctly scoped.** If every file in a candidate scope group has the same primary purpose, the group is coherent. Different purposes within the same group indicate either misclassification or a need to split.
2. **Each scope group should have one sentence purpose.** Test: can you complete "This scope group exists to ___" with a single clear answer? If the answer requires "and also", the group conflates concerns.
3. **Mixed-purpose files mark the fault line.** A file that mixes UI and networking is a symptom — the fault line is between those two purposes. Recommend splitting the file along that line.
4. **Configuration is rarely its own scope group.** Configuration files belong with the components they configure, unless they configure the entire application (in which case they belong in an application bootstrap scope group).
5. **Testing infrastructure belongs adjacent to its subject.** Test mocks and fakes belong in the same scope group as the types they mock, or in a shared test infrastructure scope group if used across multiple groups.
6. **Build tooling is always its own scope group.** Build scripts, code generators, and Gradle/Webpack configuration are not part of any runtime scope group — they form a `Build Tooling` scope group that is excluded from runtime analysis.

