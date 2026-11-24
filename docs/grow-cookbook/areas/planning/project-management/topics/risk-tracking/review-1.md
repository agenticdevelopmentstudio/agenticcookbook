# Review: risk-tracking

## Findings

- `rules.md`, bundled rules (behavioral-requirements must-not-bundle-behaviors-into-one-requirement; guideline-formatting one-requirement-per-rule): each of these rules joins two or more behaviours that can each be tested on its own, so one part can pass while another fails:
  - `risk-identification-and-attention-flagging`: identify risks whatever their source; surface new risks and impediments as they appear; record each one as soon as it is identified, whoever raised it.
  - `distinguish-immediate-action-from-monitoring`: evaluate each risk as needing action now or being watched; record its proximity (already two SHOULDs in one bullet).
  - `link-concerns-to-related-elements`: a unique identifier; the product or process it concerns (two SHOULDs).
  - `concern-has-status-and-raiser`: the raiser is named; a status is carried; the status history is kept (two SHOULDs plus the history clause).
  - `risk-review-cadence`: reviews are planned, with responsibility defined, inside the normal management flow; the register is checked for new or revised risks at each review (two SHOULDs).
  - `owner-most-capable-and-not-overloaded`: the owner is the person most capable; no one holds too many risks (two SHOULDs).
  - `risk-response-triage`: the response comes from a defined set of options; it is chosen by weighing benefit against cost (the build line checks the two separately).
  - `escalate-risks-beyond-tolerance`: escalation criteria are agreed; a risk beyond tolerance is escalated rather than accepted (two SHOULDs).
  - `describe-risk-as-cause-event-effect`: the description gives cause, event and effect; no entry duplicates another (the build line checks the two separately).

  Fix: split each into one rule per behaviour. The prior rule name stays on one half, because verdict names are fixed, and the other half gets a fresh name. Each new rule carries its own citation (the claims that support that half), its own line in `a-build-must-establish.md`, and an entry in the SHOULD list of `a-complete-review-must-establish.md`.
- `rules.md`, the list as a whole (guideline-formatting keep-rule-lists-short; template/sibling structure): the 17 rules are one flat list, but a list SHOULD have no more than seven items where possible. The siblings group their rules under `###` subsections (`issue-tracking` has "Recording issues" and "Triage"; `dependency-tracking` has three to six rules per subsection). Fix: group the rules, including the new ones from the split above, under `###` subsections of seven or fewer. Possible groups are recording a risk, ownership, review, response and escalation, and tooling.
- `rules.md`, `risk-becomes-issue-when-it-happens`, "SHOULD leave the risk register": this rests on the part of the claims that the second check refuted. `pmbok8-issue-already-happened` is refuted because "the source never says an issue no longer belongs in the risk register". `orange-book-contingency-if-risks-crystallise` is refuted because Principle D9 "does not say that crystallising is the point where something stops being a risk". `prince2-issue-is-event-that-happened` and `atlassian-raid-issues-need-immediate-attention` define an issue and set it apart from a risk, but neither says the risk leaves the register. The wording also contradicts the guideline itself in three places:
  - `concern-has-status-and-raiser` keeps each risk's status (active or closed) and its history in the register.
  - `keeping-a-risk-register.md` step 7 says to "close the risk and raise an issue".
  - The build-bar line says "is closed and raised as an issue".

  Fix: "A risk whose event has happened SHOULD be closed in the risk register and raised as an issue, which needs management action now." Add `prince2-risk-status-field` (active or closed; named by the `concern-has-status-and-raiser` verdict) to its citation.
- `rules.md`, `flag-project-at-risk`, "alongside a record for each risk rather than in place of one", and its `a-build-must-establish.md` line, "beside its per-risk records": none of the cited claims supports the clause. `linear-health-at-risk` was refuted on exactly the per-risk part ("Nothing in the quote or the page supports 'no per-risk record type'"), and its quote supports only the project-level health indicator. The clause also decides part of the owner's open question on tracker mapping, which lists "a project health flag such as Linear's 'At risk'" as one candidate mapping for a small team, because it rules that flag out as the mapping. Fix: end the rule at the indicator: "A team MAY mark a project its risks threaten with a health indicator such as on track, at risk or off track. (claim: linear-health-at-risk)". Make the build line read "where used, a threatened project carries a health indicator". The other rules already ask for a record for each risk, so nothing is lost.
- `artifact.json` `related` and `intro.md`, the scope paragraph (criterion 6; cross-recipe-consistency must-reference-siblings-by-uuid): `related` is `[]`, but the text hands every risk that has happened to issue tracking, and sibling guidelines it overlaps already exist:
  - `issue-tracking` (`f77eeffe-2699-4028-9195-4bfc23c75e91`, in `cookbook/index.json`). Its own intro sends "risks that have not happened" to this topic.
  - `dependency-tracking` (`3f978ba7-c8c1-4b53-8fda-12e5a6966b75`). Its `at-risk-dependency-logged-as-risk` rule feeds this register, and its round-1 review already asked that guideline to add this one to its `related`.

  The intro also names issue tracking in free prose, not by link. Fix: add both UUIDs to `related`, and in the intro link issue tracking as `[adc.guideline.planning.project-management.issue-tracking](cookbook:f77eeffe-2699-4028-9195-4bfc23c75e91)`, the form `issue-tracking`'s intro uses for its existing siblings. `project-record-linking` has no guideline yet, so it stays a topic mention.

## Checked

- Verdict coverage: all 14 verdict rules (5 `supported`, 9 `new`) are named rules in `rules.md` under their fixed names. The three added rules (`flag-overdue-risk-reviews`, `owner-most-capable-and-not-overloaded`, `flag-project-at-risk`) are new names, which is allowed. No `supported` or `new` verdict is left without a rule.
- Citations: every one of the 17 rules ends with exactly one `(claim: …)` or `(claims: …)` citation with nothing after it. Every cited id is a claim in research.json and is named by some verdict (checked by script). The only verdict-named claim no rule cites is `scrum-controls-risk-by-iteration` (refuted, trust 58), which the rationale uses to explain why a Scrum team may keep a lighter register.
- Strength rule: no rule carries MUST. All 15 refuted claims are cited only by SHOULD or MAY rules. No claim is under "citation dropped". The MAY rules (`flag-overdue-risk-reviews`, `keep-risk-scoring-simple`, `track-risks-in-the-team-tracker`, `flag-project-at-risk`) rest on vendor or practitioner claims stated as options. The SHOULD rules rest on ISO 31000 "should", PRINCE2 "recommends"/"should", Orange Book and NAO guidance, and the ILX and ROAM practitioner points, as research.md's summary ("All five listed rules hold at SHOULD strength") supports.
- Rules follow their claims, apart from the two findings above:
  - identification whatever the source (ISO 6.4.2), capture on identification by anyone (PRINCE2), impediments at the Daily Scrum;
  - evaluation deciding action, definite action now, plans prepared now and acted on at a trigger (ISO, PRINCE2, PMBOK 8 errata), proximity;
  - a unique identifier and the product concerned;
  - author, active/closed status, response complete/ongoing/pending (ILX), status history;
  - ongoing review of untreatable risks, an up-to-date register;
  - a planned review with defined responsibility in the normal management flow, and a register check at each progress review;
  - one owner per risk, including complex cross-organisation risks (NAO "particularly important" kept at SHOULD), with responsibility for management and escalation (ILX);
  - most capable owner, not overloaded;
  - an actionee who may or may not be the owner;
  - ISO's treatment options and cost-benefit selection, with escalation as a PMBOK 8 option;
  - escalation criteria, escalation when tolerance is threatened, no acceptance beyond tolerance;
  - cause, event and effect, specific and distinct;
  - probability times impact, simple scoring;
  - custom issue types and fields, or the integrated register PRINCE2 lists.
- Second-check corrections reach the text: the owner rule does not claim the ROAM "owner owns the conversation" point or Atlassian's four components; the actionee rule makes no timing claim from ISO; the tracker rule does not call PRINCE2's integrated register a "RAID log" (the how-to does so only as a description of the shape); the response rule names no SAFe origin for ROAM.
- Owner list: it lists no prior rules, so no `-prior` citation or lead-in is needed. The other open questions are left open: `risk-review-cadence` names no interval and gives stage boundaries, progress reviews or team reviews only as examples; `risk-response-triage` says "such as" across ISO, PRINCE2 and PMBOK 8 terms without adopting one vocabulary; opportunities are neither included nor excluded; the actionee rule keeps PRINCE2's "may or may not be the risk's owner". `rationale.md` lists all five questions as the owner's.
- Frontmatter: `summary` is 153 characters, one line, and describes the new text. `tags` include the topic slug `risk-tracking` and the family tag `project-management`, as every sibling does. `platforms` is `[]`, matching research ("Apple, Android and Windows have no bearing") and every sibling. `references` matches the 15 research sources and `references.md`. Version, modified and history are left for `cookr bump`.
- Structure (gf-roled-parts): intro, Rules, how-to, Examples, What a reviewer looks for, A complete review must establish, A build must establish, Rationale, References, then Change History last. Every part except intro and history has a role. `cookr roles check` reports `ok: true`, 17 rules, no findings, four skills compiled.
- `a-build-must-establish.md` has exactly one line per named rule (17), and every line names a rule. `a-complete-review-must-establish.md` lists the 13 SHOULD rules and 4 MAY rules, each once at its own strength.
- The informative parts (how-to, examples, review focus, rationale, references) say so at their start. RFC keywords are uppercase, and the rules are the only normative text.
- The intro gives a summary, a scope (issues, record linking and practice-specific technical risks excluded) and a conformance statement ("keeping each SHOULD rule below or stating why a register departs from it"), and puts no rules in the scope.
- The how-to steps and the example entry match the rules and claims: GitHub's task, bug and feature defaults and up to 25 types (on the page per the trust basis), PRINCE2's register formats, PRINCE2's proximity values, Atlassian's probability times impact, and Linear's indicator described as marking a project. The example has an id, cause/event/effect, raiser, owner, actionee, proximity, score, response, status and next review.
- Rationale explains the SHOULD defaults (behavioral-requirements must-explain-rationale-for-should-requirements) and matches the research's limitations: third-party copies of ISO 31000 and PRINCE2, PMBOK 8 only through errata and a secondary summary, and no outcome study.
- `cookr validate` reports nothing for this artifact. Its one frontmatter issue is in `project-record-linking/research/research.md`, and its index drift is cookbook-wide.
- No sibling-topic findings beyond the `related` note above. The `dependency-tracking` side of that link is already routed in that topic's review.

## Lint

I ran /lint-artifact (v2.0.1, using this checkout's cookr) on the compiled guideline. Result: Pass 21, Warn 0, Fail 1, RESULT: NOT CLEAN.

- PASS: FM-01, FM-02, FM-04 to FM-13 (frontmatter, UUID, type, semver, required fields, MIT license, copyright, dates, summary, H1 matching the title, links, Change History, no placeholders); GF-01 to GF-04; gf-triggers-field; gf-roled-parts (17 build-bar lines, one per rule); gf-named-rules; gf-research-folder; gf-rule-cites-research (every cited claim exists and has a verdict).
- FAIL: FM-03, index entry matches folder. `cookbook/index.json` has no entry for `a55182ef-3144-407c-b64a-6377f37f5c63` and no `risk-tracking` path. Fix: run `cookr update`, which adds the entry. The sibling `milestone-scheduling` is unindexed in the same way.
- `cookr validate` shows nothing for this artifact. It fails only on `project-record-linking/research/research.md` (no frontmatter) and on cookbook-wide index drift.

lint: fail 1

verdict: fail
