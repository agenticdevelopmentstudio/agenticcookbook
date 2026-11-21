# Review: principle-formatting

## Findings

none

## Checked

- `artifact.json` now carries `"names_hosts": "Cites agent hosts' published instruction budgets and guidance as the evidence for its rules."`. `cookr validate` exits 0, and its Neutrality section reports "No artifact names a host without saying why (32 say why)". This folder is no longer listed.
- `cookr roles check` on the folder is ok: 39 rules, no findings, and all four skills compile (builder, build-verifier, reviewer, review-verifier). `cookr validate` Roles reports that every build bar cites exactly its rules.
- All 27 verdict names still have a rule of that name. No prior rule was renamed, and each split kept the prior name on one part.
- Every one of the 39 rules ends with one citation. Every cited id is a claim in research.json that some verdict names. No claim from a `supported` or `new` verdict is left uncited after the splits.
- `a-build-must-establish.md` has exactly one line per rule, in rule order, including a line for each new split rule.
- New split rules, checked against their cited claims:
  - `pf-no-domain-field` (MUST NOT): `pep-preamble-required` gives a fixed, required header set stated with "must", and `astro-frontmatter-schema` errors on a schema violation. Together they support a fixed field set. Neither claim was refuted.
  - The `pf-statement-before-bullets`, `pf-key-guidance-first`, `pf-actionable-guidance`, `pf-bullet-right-altitude`, `pf-bullet-full-sentence`, `pf-bullet-list-shape`, `pf-no-copied-conventions`, `pf-bullet-for-a-repeated-mistake`, `pf-history-row-per-version`, `pf-history-dated`, `pf-history-newest-first`, `pf-text-holds-untooled-guidance`, `standard-link-detail-not-copy`, `standard-research-kept` and `standard-research-cited` rules each follow from the subset they cite, at SHOULD or SHOULD NOT.
- Strength rule: the refuted claims `ifscale-earlier-instructions`, `adr-motivation-lost`, `skill-only-new-context`, `docs-as-code`, `md043-required-headings` and `vale-metric-formulas` are cited only by SHOULD rules.
- `pf-key-guidance-first` now says only that models "favour earlier instructions". It no longer ties the bias to instruction density, so it matches what the second check confirmed.
- Owner list: `pf-title-heading`, `pf-statement`, `pf-change-history`, `pf-brevity` and `roles-*` are unchanged. Each still cites only its `-prior` claim, and each carries the listed lead-ins.
- Rationale: every new rule name appears in a rationale line, so every SHOULD has its reason. The merged lines state the strength each rule takes.
- The changed review-focus and review-bar lines each match the rule they serve. These cover statement before bullets, bullets for a statement that is not self-evident, altitude, full sentences, list shape, text spent on what a tool checks, and the research folder and citations.
- `summary` is 152 characters and describes the new text.
- The intro matches the draft's new text and keeps the always-loaded condition.

## Rulings

- R1.1: fixed — `names_hosts` is set in `artifact.json` with a reason of more than 16 characters, and `cookr validate` no longer lists this folder under Neutrality. The author's dispute was that the draft cannot set the key and the fix belongs to integration. That dispute is moot, because the key is now in the folder.
- R1.2: fixed — `rationale.md` drops "at high instruction density" from the IFScale clause. It now says "one of the hardest things to track", matching the `adr-motivation-lost` quote.
- R1.3: fixed — the three parts now say "typically" one to three sentences:
  - review-focus says "runs well past the typical one to three sentences";
  - review-bar says "in typically one to three sentences";
  - how-to says "typically in one to three sentences".
- R1.4: fixed — all four parts restore the condition that a principle loads on every task:
  - build-bar: "a principle that loads on every task was sized …";
  - review-bar: "for a principle that loads on every task, its share …";
  - how-to: "When the principle loads on every task, count it with the others that do";
  - intro: "size it against the always-loaded budget when it loads on every task".
- R1.5: fixed — each of the eight bundled rules is now split into single-behaviour rules:
  - `pf-frontmatter-complete` and `pf-no-domain-field`;
  - `pf-statement-before-bullets` and `pf-key-guidance-first`;
  - `pf-actionable-guidance`, `pf-bullet-right-altitude`, `pf-bullet-full-sentence` and `pf-bullet-list-shape`;
  - `pf-only-what-the-agent-lacks`, `pf-no-copied-conventions` and `pf-bullet-for-a-repeated-mistake`;
  - `pf-history-row-per-version`, `pf-history-dated` and `pf-history-newest-first`;
  - `pf-format-checks-tool-enforced` and `pf-text-holds-untooled-guidance`;
  - `standard-one-source-per-topic` and `standard-link-detail-not-copy`;
  - `standard-research-kept` and `standard-research-cited`.

  Each new rule cites a subset of the original claims at the right strength, keeps a prior name on one part, and has its own build-bar line.
- R1.6: fixed — the intro now reads "its core idea first with the reason it holds, then specific bullets". The summary reads "its main point and why first, actionable bullets". Neither asks every bullet to give a reason.

## Lint

/lint-artifact on the compiled doc (type guideline, compliance `tbd/compliance/artifact-formatting/guideline-formatting.md`): Pass 29, Warn 1, Fail 0. RESULT: CLEAN.

- [PASS] FM-01 to FM-13, including:
  - FM-03: the index entry matches the folder at `guidelines/cookbook/authoring/principle-formatting`;
  - FM-11: the H1 matches the title;
  - FM-11a: the links resolve.
- [PASS] GF-01 statement after H1, GF-02 structured guidance (39 bullet rules), GF-03 RFC keywords, and gf-triggers-field.
- [PASS] gf-roled-parts, gf-named-rules (39 unique, each with a keyword), gf-research-folder (75 claims, valid verdicts), gf-rule-cites-research, and build-bar (39 lines, one per rule).
- [WARN] GF-04: no Compliance section. This only matters if a compliance check references the guideline, and roled guidelines have no such section.
- The example principle's `# Explicit Over Implicit` heading and its `## Change History` sit inside a fenced block, so they do not count as extra headings.

lint: clean

verdict: pass
