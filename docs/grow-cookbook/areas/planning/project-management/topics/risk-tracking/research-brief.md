# Research brief: risk-tracking

- **Area:** `planning/project-management`
- **Topic:** `risk-tracking` (new: no rules of its own yet; its folder holds only `research/` until stage 3)
- **Artifact:** `cookbook/guidelines/planning/project-management/risk-tracking`
- **Base commit:** `f0dd450e1188364e9e221d912d49657944ae46ad` (`base.txt`)
- **Research type:** How-to / troubleshooting (intent Do; domain project risk management; method standards bodies and practitioner sources).
- **Research bar:** How-to / troubleshooting, no escalation (owner approval 2026-11-24, Owner questions 1 and 4).
  Any metric claim (a review cadence, a task size or a schedule accuracy backed by a study or survey) takes the
  *Statistical* bar of `guidelines/researching/process/research-methodology-and-sources`: name the study, its
  sample, its measure and its result, and score it on that bar.

## The topic

How a delivery team identifies, records, reviews, responds to and closes project risks and open concerns: the risk register (or RAID log) and its fields, the owner and raiser of each risk, its review cadence, the response options and how one is chosen, and when a risk becomes an issue.

The cookbook states general practice for any delivery team, not projectteam's: projectteam's `.dev-team-project/`
paths, its file formats and its specialist names stay in projectteam and are not researched.

**Not this topic's:**

- Issues (a risk that has happened) are `issue-tracking`'s; this topic says when a risk becomes an issue and hands it over, and never rules issue severity or triage.
- How a risk links to milestones, tasks and other records in general is `project-record-linking`'s (the linking convention the record topics share); research here only what a risk record itself carries.
- Technical risks of one practice (backup-and-recovery, feature-flags, authorization) are their own guidelines' and have no bearing here.

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

1. Best practice: how should a delivery team identify, record and monitor project risks and open concerns: a risk register's fields (description, likelihood, impact, owner, status, raiser), its review, and when a risk becomes an issue?
2. Known solutions: how do RAID logs, risk registers, probability-impact matrices and the risk features of GitHub Projects, Jira and Linear compare for a small software team, and which fields does each keep?
3. Platform guidelines: what do ISO 31000, the PMBOK Guide's risk performance domain and PRINCE2's risk theme say about recording, owning, reviewing and closing a risk?
4. The expert's view: what do delivery leads and risk practitioners say teams get wrong with risk registers (stale entries, no owner, risks never closed, issues logged as risks), and what to do instead?
5. **Risk review cadence**: find how often standards and practitioners review open risks, who reviews them and what closes one, and state the review rule a register follows so no risk stays open without review.
6. **Risk response triage**: find the response options standards name (avoid, mitigate, transfer, accept, escalate, monitor) and how one is chosen, and state how a worker decides that a risk needs action now or is monitored.

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
  `source_type` `prior cookbook text`, its one citation `title` `risk-tracking (teams/projectteam/specialities/project/concerns.md)`, `author`
  `Agentic Developer Cookbook`, `publisher` `agenticcookbook`, `date` `n.d.`, `url`
  `git:736232c055d56077e7e1bc03e7e1accf7173a87f:teams/projectteam/specialities/project/concerns.md` (the teams repo commit the rule is quoted at; the topic has no part files yet).
- Find what the topic is missing: practice the research finds that no rule covers. Give each a `new` verdict
  naming the kebab-case rule stage 3 will write and the strength its sources support. Each bold-named research
  question above (the plan's Missing subjects) owes at least one `new` verdict, unless a listed rule already
  covers it.
- What the research leaves to a policy choice goes in `open_questions`, one entry per question.

## The rules to verify

Each rule is quoted verbatim from `teams/projectteam/specialities/project/concerns.md` in the teams repo at commit `736232c055d56077e7e1bc03e7e1accf7173a87f` (projectteam's
compiled speciality; the cookbook base commit is `f0dd450e1188364e9e221d912d49657944ae46ad`), as a claim to check, never as a source.
The file's two sections, whole, for context:

> **Worker Focus:** Risk identification, attention flagging; distinguish between concerns that need immediate action and those that need monitoring; link concerns to related project elements

> **Verify:** Every concern has a status and a raiser; no concern sits in open status indefinitely without review

The rules, one per clause, named here; the names are fixed from here on:

1. **risk-identification-and-attention-flagging** (no RFC keyword; section *Worker Focus*): "Risk identification, attention flagging"
2. **distinguish-immediate-action-from-monitoring** (no RFC keyword; section *Worker Focus*): "distinguish between concerns that need immediate action and those that need monitoring"
3. **link-concerns-to-related-elements** (no RFC keyword; section *Worker Focus*): "link concerns to related project elements"
4. **concern-has-status-and-raiser** (no RFC keyword; section *Verify*): "Every concern has a status and a raiser"
5. **no-concern-open-without-review** (no RFC keyword; section *Verify*): "no concern sits in open status indefinitely without review"
