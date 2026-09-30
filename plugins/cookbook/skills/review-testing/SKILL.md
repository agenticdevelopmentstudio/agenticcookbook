---
name: review-testing
description: "Review code for testing. Covers: Flaky Test Prevention, Post-generation verification, Security Testing."
---

# review-testing

Review the change against the rules in the leaves that apply to it.

1. Read `index.md` and pick the leaves whose summary, platforms and triggers
   match the files under review. Read only those.
2. Each leaf opens with its rule checklist. For **every** rule in every leaf
   you read, report exactly one status:
   - `violated` — with `file:line` evidence and what the rule requires;
   - `clean` — the change complies;
   - `n/a` — with the reason it does not apply.
3. Cite a rule as `<leaf-id>#<slug>`, e.g. `review-testing/flaky-test-prevention#<slug>`.

Leaves: [index.md](index.md) — one line per leaf. Leaves are plain files, not skills; read them with the Read tool.
