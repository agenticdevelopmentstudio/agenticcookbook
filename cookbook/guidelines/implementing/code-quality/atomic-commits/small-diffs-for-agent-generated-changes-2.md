
The decision to keep a change reviewable happens before code is written, not after. Work **SHOULD** be split into small, independently reviewable pull requests up front — plan the slices first, then implement one slice at a time. Large diffs degrade reviewers regardless of who reads them: humans skim past detail and AI reviewers lose precision as context grows.

Agent-generated output **SHOULD** receive more per-line scrutiny than hand-written code, because plausible-looking code can hide subtle defects. That makes small, frequent diffs matter more here, not less — a reviewer (human or AI) can hold a 50-line change fully in view, but not a 1,000-line one. When an agent produces a large change, it **SHOULD** be decomposed into smaller commits or PRs before review rather than reviewed as one block.

