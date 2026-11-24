# Research brief: task-breakdown

- **Area:** `planning/project-management`
- **Topic:** `task-breakdown` (new: no rules of its own yet; its folder holds only `research/` until stage 3)
- **Artifact:** `cookbook/guidelines/planning/project-management/task-breakdown`
- **Base commit:** `f0dd450e1188364e9e221d912d49657944ae46ad` (`base.txt`)
- **Research type:** How-to / troubleshooting (intent Do; domain work decomposition and task assignment; method standards bodies and practitioner sources).
- **Research bar:** How-to / troubleshooting, no escalation (owner approval 2026-11-24, Owner questions 1 and 4).
  Any metric claim (a review cadence, a task size or a schedule accuracy backed by a study or survey) takes the
  *Statistical* bar of `guidelines/researching/process/research-methodology-and-sources`: name the study, its
  sample, its measure and its result, and score it on that bar.

## The topic

How work is broken into tasks: what makes a task specific and actionable, how large a task may be, one owner (assignee), a priority, acceptance or done criteria, the link from each task to its milestone, and how a blocked task names what it waits on.

The cookbook states general practice for any delivery team, not projectteam's: projectteam's `.dev-team-project/`
paths, its file formats and its specialist names stay in projectteam and are not researched.

**Not this topic's:**

- `cookbook/guidelines/planning/code-quality/spec-driven-development` rules writing a self-contained spec before code ("write a self-contained spec before code, separating planning from execution and ending with a verification step"); this topic rules how the planned work is split into owned, actionable tasks, and cites it.
- `cookbook/principles/steel-thread-first` ("Build the thinnest end-to-end slice through every boundary before breadth") is a principle for ordering slices; this topic cites it for slicing and does not restate it.
- Milestones themselves are `milestone-scheduling`'s; the general linking convention between records is `project-record-linking`'s.

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

1. Best practice: how should work be broken into tasks: the size of a task, one owner, a priority, acceptance criteria, and the link from each task to its milestone?
2. Known solutions: how do work breakdown structures, user story splitting, INVEST, task checklists and the task fields of GitHub Issues, Jira and Linear compare?
3. Platform guidelines: what do the PMBOK Guide's WBS guidance, the Scrum Guide's sprint backlog and the Kanban Guide's work items say about breaking down and assigning work?
4. The expert's view: what do practitioners say teams get wrong with task lists (vague tasks, tasks too large, no owner, blocked tasks that never say why), and what to do instead?
5. **Actionable task wording**: find what practitioners require of an actionable task (a verb and an object, a done condition, a size limit), and state what a task's text says and how large a task may be.
6. **Task blocker naming**: find how trackers and practitioners record what a blocked task waits on, and state how a blocked task names its blocker.

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
  `source_type` `prior cookbook text`, its one citation `title` `task-breakdown (teams/projectteam/specialities/project/todos.md)`, `author`
  `Agentic Developer Cookbook`, `publisher` `agenticcookbook`, `date` `n.d.`, `url`
  `git:736232c055d56077e7e1bc03e7e1accf7173a87f:teams/projectteam/specialities/project/todos.md` (the teams repo commit the rule is quoted at; the topic has no part files yet).
- Find what the topic is missing: practice the research finds that no rule covers. Give each a `new` verdict
  naming the kebab-case rule stage 3 will write and the strength its sources support. Each bold-named research
  question above (the plan's Missing subjects) owes at least one `new` verdict, unless a listed rule already
  covers it.
- What the research leaves to a policy choice goes in `open_questions`, one entry per question.

## The rules to verify

Each rule is quoted verbatim from `teams/projectteam/specialities/project/todos.md` in the teams repo at commit `736232c055d56077e7e1bc03e7e1accf7173a87f` (projectteam's
compiled speciality; the cookbook base commit is `f0dd450e1188364e9e221d912d49657944ae46ad`), as a claim to check, never as a source.
The file's two sections, whole, for context:

> **Worker Focus:** Task breakdown, assignment, prioritization; ensure tasks are specific and actionable; link tasks to milestones; identify blocked tasks and their blockers

> **Verify:** Every todo has an assignee and priority; blocked todos reference a specific blocker; no todo is assigned to a nonexistent milestone

The rules, one per clause, named here; the names are fixed from here on:

1. **break-down-assign-and-prioritize-tasks** (no RFC keyword; section *Worker Focus*): "Task breakdown, assignment, prioritization"
2. **tasks-specific-and-actionable** (no RFC keyword; section *Worker Focus*): "ensure tasks are specific and actionable"
3. **link-tasks-to-milestones** (no RFC keyword; section *Worker Focus*): "link tasks to milestones"
4. **identify-blocked-tasks-and-blockers** (no RFC keyword; section *Worker Focus*): "identify blocked tasks and their blockers"
5. **task-has-assignee-and-priority** (no RFC keyword; section *Verify*): "Every todo has an assignee and priority"
6. **blocked-task-references-blocker** (no RFC keyword; section *Verify*): "blocked todos reference a specific blocker"
7. **task-milestone-must-exist** (no RFC keyword; section *Verify*): "no todo is assigned to a nonexistent milestone"
