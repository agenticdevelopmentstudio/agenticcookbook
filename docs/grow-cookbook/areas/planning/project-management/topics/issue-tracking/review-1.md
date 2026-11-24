# Review: issue-tracking

## Findings

- `rationale.md`, third paragraph, "Mozilla and Linear raise a notice beyond the assignee": wrong for Linear. The cited claim `critical-notifies-beyond-assignee` quotes Linear as "When an issue is marked as Urgent, Linear notifies the assignee and, if email notifications are enabled, also sends an urgent email notification": Linear notifies the assignee itself, not anyone beyond it. Only Mozilla (Release Management and the component's triage owner for S1 and S2) notifies beyond the assignee. This is the only instance; the rule `escalate-critical-issues` says "a notice beyond the triage queue", which both sources do support. Fix: reword to something like "Mozilla notifies Release Management beyond the assignee, and Linear sends the assignee an urgent notice", or "Mozilla and Linear raise a notice beyond the triage queue".

## Checked

- Citations (source fidelity, criteria 2 and 4): all 29 named rules end with exactly one `(claim: …)` or `(claims: …)` citation with nothing after it; every cited id is a claim in research.json and is named by some verdict.
- Coverage: every claim named by a `supported` or `new` verdict is cited by at least one rule; all 29 verdict rule names appear as named rules, and no rule is unaccounted for.
- Strength rule (criterion 3): no rule other than the owner-list `issue-has-severity-and-status` carries MUST. The four refuted claims (`google-issue-tracker-priority-and-severity` in `severity-kept-apart-from-priority`, `link-fix-to-issue` in `link-fix-change-to-issue`, `duplicates-refiled` in `close-duplicates-linking-canonical`, `spolsky-three-things` in `issue-records-minimum-fields`) are cited only by SHOULD rules. MAY rules match the research's MAY findings (`issue-covers-more-than-defects`, `severity-change-needs-rationale`, `flag-stale-issues`, `communicate-resolution-to-stakeholders`); the remaining rules are SHOULD, as research.md and the trust bases support (single-source 50-55 claims such as `escalation-procedure-documented` and `keep-closed-as-history` stay at SHOULD, `communicate-resolution` at MAY).
- `defect-has-severity-every-issue-has-status` is SHOULD for both halves, the strength of its weakest cited claim (`triage-sets-severity-on-every-defect`), per the strength rule.
- Second-check corrections applied in wording: `link-fix-change-to-issue` drops the unsupported "Jira pull requests carry the key" and names only the GitHub closing keyword, the Jira commit-message key and the Jira Service Management problem-to-change link.
- Rules follow their claims: e.g. `triage-new-issues-promptly` (Mozilla's one week, needs-triage label or inbox), `critical-issue-owned-or-escalated` (two business days), `flag-stale-issues` (Kubernetes 90 days), `record-resolution-reason` (fixed set incl. ITIL known error), `verify-resolution-before-close` (reporter, verifier or test), `close-duplicates-linking-canonical` (link original, tell reporter).
- Owner list (criterion 5): `link-issues-to-findings` reads "A team SHOULD do this: link issues to specialist findings when applicable (claim: link-issues-to-findings-prior)" and `issue-has-severity-and-status` reads "This MUST hold: Every issue has severity and status (claim: issue-has-severity-and-status-prior)": prior text word for word, the listed lead-in, the `-prior` citation.
- Open questions are left open: no rule picks a severity scale (examples call Mozilla's scale one choice and name Atlassian's), the escalation time and target are "stated"/"agreed" by the project, who confirms a fix names all three options, whether priority is required is not settled (the minimum-fields rule omits priority), and the rationale lists all six as the owner's.
- Frontmatter (criterion 6): summary is 153 characters and describes the new text; tags (`issue-tracking`, `triage`, `severity`, `project-management`) share the family's `project-management` tag; `platforms` is `[]` like every sibling; `related` holds the incident-response and vulnerability-prioritization UUIDs that the intro links by rdid.
- Cross-references: the intro links the two existing out-of-scope guidelines by `[rdid](cookbook:uuid)`; `risk-tracking` and `project-record-linking` are named as topics only, since no guideline exists for them yet in `planning/project-management/`.
- Template and roles: intro, Rules, two how-to parts, Examples, What a reviewer looks for, A complete review must establish, A build must establish, Rationale, References and Change History, in that order with Change History last; `cookr roles check` passes (`ok: true`, 29 rules, no findings), with one build-bar line per named rule and none naming a non-rule.
- RFC keywords are uppercase and normative statements use them; informative parts (Examples, Rationale, References) are marked informative.
- How-to steps, review focus, review bar and build bar agree with the rules (e.g. severity judged regardless of reporter or regression, critical issue owned in the stated time or escalated, confirm the fix before closing).
- Examples: the Mozilla S1-S4 table matches the `severity-levels-defined` quote; the record keeps severity and priority in separate fields; `Fixes #412` is GitHub's closing keyword.
- Rationale, other statements: triage owners (Mozilla, Linear, Chromium), the severity/priority field split (Mozilla, Atlassian), tracker differences (Bugzilla, Google, Jira, GitHub, Linear), resolution reasons (Jira, GitHub, Google, FogBugz), verifiers (Spolsky, Jira, Google, Atlassian) and duplicates (Kubernetes, Linear, GitHub, Google) all match their claims' citations.
- No sibling-topic findings.

## Lint

/lint-artifact (v2.0.1, cookr from this checkout) on the compiled guideline: Pass 28, Warn 2, Fail 0, RESULT: CLEAN.

- PASS: FM-01 to FM-13 (frontmatter, UUID, index entry, type, version, required fields, license, copyright, dates, summary, H1 matches title, `related` and in-text `cookbook:` links resolve, Change History, no placeholders); GF-01 to GF-04; gf-roled-parts (one build-bar line per rule); gf-named-rules; gf-research-folder; gf-rule-cites-research; gf-triggers-field.
- WARN: gf-rule-cites-research, `issue-has-severity-and-status` cites `issue-has-severity-and-status-prior`, which research marks contradicted (owner decides; on the owner list).
- WARN: gf-rule-cites-research, `link-issues-to-findings` cites `link-issues-to-findings-prior`, which research marks unsupported (owner decides; on the owner list).
- `cookr validate` reports "Validation failed" only for three other topics (`milestone-scheduling`, `project-record-linking`, `risk-tracking`: their `research/research.md` has no YAML frontmatter); nothing in this artifact.

lint: clean

verdict: fail
