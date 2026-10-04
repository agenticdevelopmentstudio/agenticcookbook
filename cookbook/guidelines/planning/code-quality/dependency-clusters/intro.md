
# Dependency Clusters

The import graph is the most objective structural signal in a codebase. Files that frequently import each other form clusters with high internal cohesion. Files with few internal imports and many external imports are loosely coupled and may be candidates for separate scope groups. This lens builds a coarse import graph and identifies clusters with high internal coupling density — these are natural scope group candidates.

