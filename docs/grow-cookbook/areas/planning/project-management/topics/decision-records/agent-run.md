I've written both research files for `decision-records`, and validation prints `Research passed.` The research supports all six rules, though alternatives and the decider are supported at SHOULD, not MUST. I also added 11 `new` verdicts.

**Files**
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/decision-records/research/research.json`
- `/Users/mfullerton/Development/projects/myagenticteams/teamtesting/.claude/worktrees/teams-cookbook-grounding-phase-3/external/teams/external/agenticcookbook/cookbook/guidelines/planning/project-management/decision-records/research/research.md`

**Claims per question (46 in total)**
- best-practices: 18
- known-solutions: 9
- platform-guidelines: 8
- experts-view: 11

**Verdicts**
- record-decisions-with-full-context: supported. Claims: record-context-of-decision, record-rationale-justification, record-consequences-good-and-bad.
- capture-rationale-alternatives-and-decider: supported. Claims: record-rationale-justification, record-alternatives-considered, record-who-decided.
- decisions-findable-and-linked: supported. Claims: store-openly-findable, store-with-the-code, link-decisions-to-work, github-issue-pr-linking.
- decision-has-rationale-and-decider: supported, but only at SHOULD for the decider. Claims: record-rationale-justification, record-who-decided, zimmermann-identify-decision-makers.
- alternatives-are-recorded: supported at SHOULD. Claims: record-alternatives-considered, proposal-processes-record-alternatives, zimmermann-dummy-alternative-and-sprint.
- acknowledge-contradicted-decisions: supported. Claims: supersede-and-link, records-prevent-relitigation, cloud-providers-agree-on-supersession, gds-way-supersede-must.
- supersede-never-edit-accepted-records: new. Claims: accepted-records-immutable, adr-tools-supersede-command, clarifications-may-amend.
- supersession-links-both-ways: new; this is the one owed to the Decision supersession question. Claims: supersede-and-link, supersession-header-fields, gds-way-supersede-must.
- record-status-lifecycle: new. Claim: status-lifecycle.
- record-decision-date: new. Claim: record-decision-date.
- record-consequences-good-and-bad: new. Claims: record-consequences-good-and-bad, zimmermann-anti-patterns.
- one-decision-per-short-record: new. Claims: one-decision-short-record, zimmermann-mega-adr.
- record-significant-decisions-only: new. Claim: record-significant-decisions.
- record-rejected-proposals: new. Claim: record-rejected-decisions.
- record-confidence-level: new. Claim: record-confidence-level.
- backfill-undocumented-decisions: new. Claim: backfill-undocumented.
- no-dummy-alternatives: new. Claim: zimmermann-dummy-alternative-and-sprint.

No rule was unsupported or contradicted, so there are no `-prior` claims.

**Things you should know**
- **Weaker support for two rules.** Nygard's original template has no decider field, and it and the GOV.UK template both omit alternatives. MADR marks its decision-makers field as optional. Whether to make the decider a MUST is in `open_questions` for the owner.
- **Disagreement on editing accepted records.** The GDS Way and Henderson's ADR collection allow a clarification to edit an accepted record. Microsoft, AWS and Fowler say every change must be a new superseding record. This is also in `open_questions`.
- **Gaps in `limitations`.** I could not reach the primary texts for PMBOK, ISO 21502, ISO 31000, PRINCE2, SAFe and LeSS, so their positions are not established. Linear is cited from its page heading only.
- **Verification exceptions.** The AWS quotes come from the fetched page's markdown, not a text check with curl. The one adoption study was read as its abstract only, and it supports no rule.
