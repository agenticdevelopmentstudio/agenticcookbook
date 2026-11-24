# Research brief: issue-tracking

- **Area:** `planning/project-management`
- **Topic:** `issue-tracking` (new: no rules of its own yet; its folder holds only `research/` until stage 3)
- **Artifact:** `cookbook/guidelines/planning/project-management/issue-tracking`
- **Base commit:** `f0dd450e1188364e9e221d912d49657944ae46ad` (`base.txt`)
- **Research type:** How-to / troubleshooting (intent Do; domain issue triage and resolution; method standards bodies, tool documentation and practitioner sources).
- **Research bar:** How-to / troubleshooting, no escalation (owner approval 2026-11-24, Owner questions 1 and 4).
  Any metric claim (a review cadence, a task size or a schedule accuracy backed by a study or survey) takes the
  *Statistical* bar of `guidelines/researching/process/research-methodology-and-sources`: name the study, its
  sample, its measure and its result, and score it on that bar.

## The topic

How a team identifies, triages and tracks project issues to resolution: what an issue records, its severity (kept apart from priority), its status and owner, who triages it, when and to whom a critical issue is escalated, and what a resolved issue records about what resolved it.

The cookbook states general practice for any delivery team, not projectteam's: projectteam's `.dev-team-project/`
paths, its file formats and its specialist names stay in projectteam and are not researched.

**Not this topic's:**

- Production incidents and their severity tiers are `cookbook/guidelines/shipping/incident-response`'s ("Run production incidents with defined command roles and severity tiers"); this topic cites it where an issue is a production incident and does not restate it.
- Security vulnerability triage is `cookbook/guidelines/reviewing/security/vulnerability-prioritization`'s ("Triage CVEs by exploitability ... not raw CVSS"); this topic cites it for security issues.
- Risks that have not happened are `risk-tracking`'s; the general linking convention between records is `project-record-linking`'s.

## The four questions (verbatim)

1. **Best practices:** what is current best practice for this topic?
2. **Known solutions:** what solutions, patterns, libraries and tools already exist, and how do they compare?
3. **Platform guidelines:** what do the platform owners' own guidelines say, for each platform the topic touches (Apple, Android, Windows, web, the databases and runtimes concerned)?
4. **The expert's view:** if we hired an expert consultant in this topic, what would they tell us: what to do, what to avoid, and what people usually get wrong?

For this topic the "platforms" are the method owners and standards bodies (PMI's PMBOK Guide and its
practice standards, ISO 21502, ISO 31000 where risk is concerned, AXELOS PRINCE2, the Scrum Guide, the
Kanban Guide, and the scaled frameworks SAFe and LeSS where they speak to it) and the published guidance of
the issue trackers teams use (GitHub Issues and Projects, Jira, Linear). Apple, Android and Windows have no
bearing on this topic; say so in one line rather than researching them. Where a standard is paywalled, use
its owner's own public summary or excerpt and say so in the claim's trust basis.

## Research questions (from the area plan, verbatim)

1. Best practice: how should a team identify, triage and track project issues to resolution: what an issue records, who triages it, and how it links to the findings that raised it?
2. Known solutions: how do the triage workflows and fields of GitHub Issues, Jira and Linear compare (labels, severity, priority, states), and how does issue triage differ from incident and vulnerability triage?
3. Platform guidelines: what do the PMBOK Guide's issue log, ITIL 4's problem management and the issue-tracker vendors' own triage guides say about severity, priority and resolution?
4. The expert's view: what do triage practitioners say teams get wrong with issue trackers (everything critical, severity confused with priority, issues closed with no resolution), and what to do instead?
5. **Issue severity levels**: find the severity scales standards and trackers use and how severity differs from priority, and state the severity levels a project issue carries and what each means.
6. **Issue escalation path**: find when and to whom practitioners escalate an issue, and state the escalation rule for a critical issue.
7. **Issue resolution traceability**: find what a closed issue records in tracker practice (the resolution, the change or decision that resolved it), and state what a resolved issue references.

## Method

- Research to `cookbook/guidelines/researching/process/research-methodology-and-sources`, using its source
  catalogue for the domain. Primary sources (standards, method owners' guides, the trackers' own documentation)
  come before secondary ones (practitioner articles, books); use a secondary source only for what no primary
  source covers, and say so in the claim's trust basis.
- Score each claim 0–100 per `cookbook/guidelines/researching/evidence/verification-and-trust-scoring`,
  applying the principles `cite-the-claim-not-the-document`, `independence-before-corroboration`,
  `domain-stratified-trust`, `suppress-unsupported-confidence` and `provenance-at-generation-time`.
- Verify every rule listed below. Each is quoted **verbatim**, with the file it is in, as a claim to check,
  never as a source. Never restate or summarize a rule.
- `supported` means supported at the rule's stated strength. Every rule below is marked *no RFC keyword*: it
  states its obligation in plain words (a Verify clause reads as a check that must hold; a Worker Focus
  clause as what the worker attends to). Judge each at the strength its words carry, and say in research.md
  what strength (MUST, SHOULD or MAY) the sources support.
- A rule the research cannot support or finds against is recorded as its own `<rule-name>-prior` claim,
  `source_type` `prior cookbook text`, its one citation `title` `issue-tracking (teams/projectteam/specialities/project/issues.md)`, `author`
  `Agentic Developer Cookbook`, `publisher` `agenticcookbook`, `date` `n.d.`, `url`
  `git:736232c055d56077e7e1bc03e7e1accf7173a87f:teams/projectteam/specialities/project/issues.md` (the teams repo commit the rule is quoted at; the topic has no part files yet).
- Find what the topic is missing: practice the research finds that no rule covers. Give each a `new` verdict
  naming the kebab-case rule stage 3 will write and the strength its sources support. Each bold-named research
  question above (the plan's Missing subjects) owes at least one `new` verdict, unless a listed rule already
  covers it.
- What the research leaves to a policy choice goes in `open_questions`, one entry per question.

## The rules to verify

Each rule is quoted verbatim from `teams/projectteam/specialities/project/issues.md` in the teams repo at commit `736232c055d56077e7e1bc03e7e1accf7173a87f` (projectteam's
compiled speciality; the cookbook base commit is `f0dd450e1188364e9e221d912d49657944ae46ad`), as a claim to check, never as a source.
The file's two sections, whole, for context:

> **Worker Focus:** Problem identification, severity assessment, triage; link issues to specialist findings when applicable; track resolution status; escalate critical issues

> **Verify:** Every issue has severity and status; critical issues have an owner or are escalated; resolved issues reference what resolved them

The rules, one per clause, named here; the names are fixed from here on:

1. **identify-assess-severity-and-triage** (no RFC keyword; section *Worker Focus*): "Problem identification, severity assessment, triage"
2. **link-issues-to-findings** (no RFC keyword; section *Worker Focus*): "link issues to specialist findings when applicable"
3. **track-resolution-status** (no RFC keyword; section *Worker Focus*): "track resolution status"
4. **escalate-critical-issues** (no RFC keyword; section *Worker Focus*): "escalate critical issues"
5. **issue-has-severity-and-status** (no RFC keyword; section *Verify*): "Every issue has severity and status"
6. **critical-issue-owned-or-escalated** (no RFC keyword; section *Verify*): "critical issues have an owner or are escalated"
7. **resolved-issue-references-resolution** (no RFC keyword; section *Verify*): "resolved issues reference what resolved them"
