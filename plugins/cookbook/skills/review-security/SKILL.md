---
name: review-security
description: "Review code for security. Covers: Authentication, Authorization, CORS, Dependency Security, Privacy and security by default, Secure Storage, Security Headers Checklist, Transport Security, Content Security Policy, Input Validation, LLM red …"
---

# review-security

Review the change against the rules in the leaves that apply to it.

1. Read `index.md` and pick the leaves whose summary, platforms and triggers
   match the files under review. Read only those.
2. Each leaf opens with its rule checklist. For **every** rule in every leaf
   you read, report exactly one status:
   - `violated` — with `file:line` evidence and what the rule requires;
   - `clean` — the change complies;
   - `n/a` — with the reason it does not apply.
3. Cite a rule as `<leaf-id>#<slug>`, e.g. `implement-security/authentication#<slug>`.

Leaves: [index.md](index.md) — one line per leaf. Leaves are plain files, not skills; read them with the Read tool.
