# Review: cookbook-formatting

## Findings

- `cookbook/guidelines/cookbook/authoring/cookbook-formatting/` (the guideline under review): the round-3 change is in `draft.md` but was never folded back into the source folder. The folder still compiles to `draft-2.md` byte for byte (`cookr compile --out` on the folder, then `diff` against `draft-2.md`, gives no difference). All three changed lines in diff-3.md are therefore missing from the folder:
  - `rules.md` line 46, `schema-structure-kind-enum`: it still reads `- **schema-structure-kind-enum**: "kind": { ... }` without the owner's lead-in "The schema MUST type `structure.kind` as written here:". That is the round-2 `gf-named-rules` lint failure, and it still stands.
  - `a-complete-review-must-establish.md` line 4: `schema-structure-kind-enum` is still in the MAY list and not in the MUST list.
  - `a-build-must-establish.md` line 46: it still reads "`kind` is typed as the rule writes it" and not "`structure.kind` is typed as the rule writes it".
  Fix: fold `draft.md` into the folder (`cookr convert --update`, or edit the three section files to match diff-3.md), then delete any compiled doc left over.

## Checked

- `draft.md`, `schema-structure-kind-enum`: the lead-in is "The schema MUST type `structure.kind` as written here:", exactly as owner-list.md lists it under the owner ruling of 2026-11-22. The prior text after it is word for word, and the rule still ends with `(claim: schema-structure-kind-enum-prior)`, which exists in research.json.
- Strength: `schema-structure-kind-enum-prior` is not listed among the second check's refutations (it appears nowhere in second-check.md), so MUST is allowed under criterion 3. The MUST comes from the owner's lead-in, which criterion 5 accepts.
- `draft.md`, *A complete review must establish*: `schema-structure-kind-enum` has moved from the MAY list to the MUST list. That matches its new MUST strength, and each rule appears in exactly one list.
- `draft.md`, *A build must establish*: the `schema-structure-kind-enum` line now names `structure.kind`, which matches the rule's lead-in.
- diff-3.md changes nothing else, so no other text is open to review this round.
- `cookr roles check` on the folder compiles every role.

## Rulings

none (no findings were open)

## Lint

The /lint-artifact skill (lint-artifact v2.0.1, run with this checkout's cookr against the folder) returned:

```
[PASS] FM-01 … FM-13, FM-11a (frontmatter, index entry, links, Change History, no placeholders)
[PASS] GF-01: Summary paragraph follows the H1
[PASS] GF-02: Structured guidance
[PASS] GF-03: RFC 2119 keywords used (53 occurrences)
[PASS] GF-04: No Compliance section (optional)
Pass: 18 | Warn: 0 | Fail: 0
RESULT: CLEAN
```

That run did not apply the per-rule `gf-named-rules` check that round 2's lint applied. The folder still holds the same keywordless `schema-structure-kind-enum` text that failed that check in round 2 (see Findings), so that failure is counted here.

lint: fail 1

verdict: fail
