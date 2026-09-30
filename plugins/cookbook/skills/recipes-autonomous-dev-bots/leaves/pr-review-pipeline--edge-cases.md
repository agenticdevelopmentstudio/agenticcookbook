<!-- leaf: recipes-autonomous-dev-bots/pr-review-pipeline--edge-cases · source: recipes/autonomous-dev-bots/pr-review-pipeline.md -->

# PR Review Pipeline

## Edge Cases

- **PR with multiple recipes**: run the pipeline once per changed recipe file, aggregate results into a single review per phase
- **PR modifying existing content only**: skip Phase 2 overlap detection for sections that didn't change; still check that modifications don't introduce new overlap
- **PR touching non-recipe files** (guidelines, principles): run Phase 1 and Phase 3 only; skip Phase 2 (scoping/refactoring is recipe-specific)
- **Contributor pushes during pipeline run**: cancel current run, restart from Phase 1 on the latest commit
- **GitHub App rate limits**: implement exponential backoff; if rate-limited during review posting, retry up to 3 times then log failure
- **OpenClaw goes offline**: GitHub webhook delivery retries for up to 8 hours; pending PRs will be picked up by the cron fallback when the Mac comes back online
