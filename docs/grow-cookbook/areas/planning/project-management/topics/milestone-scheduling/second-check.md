## milestones-are-zero-duration-key-events
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: The quote is split across the two sources. GAO-16-89G holds the first two fragments (zero-duration milestones; every schedule includes start and finish), and Linear holds "Project milestones represent different stages in a project's lifecycle."

## standard-milestones-documented-with-criteria
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: GAO gives this as a footnoted example ("For example, Federal Aviation Administration (FAA) service organizations employ standard program milestones..."). It describes one agency's practice, not a general statement about organizations that standardize milestones.
- correction: refuted (quote-found yes, supports-claim partly); trust 62 -> 42; a rule citing it cannot carry MUST

## too-many-milestones-mask-work
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: GAO Best Practice 1 holds the quote verbatim, and it matches both halves of the claim.

## sequence-with-logic
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- citation 2: holds-quote
- result: refuted
- note: GAO holds the Best Practice 2 fragment and APM holds "verify that the project schedule is built on complete and defensible logic". Neither fragment says logic sequencing lets "progress be measured", so that part of the claim has no quoted support.
- correction: refuted (quote-found yes, supports-claim partly); trust 86 -> 66; a rule citing it cannot carry MUST

## missing-logic-justified
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Both fragments are in GAO. The claim's exception for the start and finish milestones is narrower than the quoted general rule, and GAO states that exception in the very next sentence.

## avoid-hard-date-constraints
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: GAO holds the quote verbatim, and it matches the claim's scope and strength.

## hard-constraints-defeat-cpm
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: GAO says that using hard constraints to fix dates "immediately convolutes critical path calculations" and defeats CPM. Neither the quote nor the passage around it calls this a "common error".
- correction: refuted (quote-found yes, supports-claim partly); trust 74 -> 54; a rule citing it cannot carry MUST

## topological-order-iff-acyclic
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The Python graphlib docs hold both fragments. They also state that CycleError is raised and that it reports one cycle, with the first and last node the same.

## assess-network-for-circular-logic
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: GAO holds the quote verbatim.

## ms-project-refuses-circular-dependency
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The Planning Wizard offers a choice. One option cancels the action; the other, "Continue the operation", creates the circular dependency and stops calculation. The page never says cancelling is the default.
- correction: refuted (quote-found yes, supports-claim partly); trust 84 -> 64; a rule citing it cannot carry MUST

## jira-cyclic-links-detected-after
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The Atlassian KB holds all three fragments; my first raw-HTML match failed only because of markup. The article assumes regular "soft" links can form cycles, which it says break apps that traverse links (StackOverflowError). It detects them afterwards from a database export.

## critical-path-is-longest-path
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: GAO holds the first two fragments and APM holds "determines the overall duration of the identified work based on estimates and logical dependencies".

## critical-path-is-dag-longest-path
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- result: confirmed
- note: GAO holds "the path of longest duration through the sequence of activities" and NetworkX holds "Returns the longest path in a directed acyclic graph (DAG)".

## critical-path-vs-critical-chain
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote covers the activity focus of critical path and the resource-utilisation focus of critical chain, but not the claim's "protects chains with buffers". APM's text "protects critical chains of activities with buffers" is on the same page but not in this claim's quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST

## status-date-separates-actual-from-remaining
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: GAO Best Practice 9 holds both fragments.

## update-regularly-track-finer-than-report
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: GAO holds all three fragments.

## status-date-not-view-date
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: GAO says the viewing date or the latest save date "should not be used as a substitute for a valid status date" and gives one case study. It does not call this a "common error".
- correction: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST

## linear-project-health-updates
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Linear's Updates page holds all three fragments; the health-indicator list is italic in the source, which is only formatting. The reminder frequency is configurable, for example weekly or biweekly.

## schedule-contingency-is-explicit
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- citation 2: holds-quote
- citation 3: holds-quote
- result: confirmed
- note: The quote is split across the sources: GAO holds the schedule-contingency definition, Spolsky holds "Ideally, you have a bunch of buffer for this", and APM holds the critical-chain buffer sentence. GAO alone supports the claim.

## risk-margin-not-padding
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: GAO holds the quote verbatim.

## schedule-risk-analysis-sizes-contingency
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote supports sizing contingency for a confidence level and identifying high-priority risks. It does not say the analysis starts from the risk register and a sound CPM schedule; GAO says "A schedule risk analysis starts with a good critical path method schedule" in the preceding sentence, outside the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 70 -> 50; a rule citing it cannot carry MUST

## baseline-and-variance
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: GAO holds both fragments.

## schedule-narrative-explains-changes
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: GAO holds all three fragments, and its checklist adds that "A schedule narrative accompanies each status update".

## github-status-updates
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote supports status, start and target dates, and a Markdown message, but not the example values "On track" or "At risk". The page does say: You can set a status, such as "On track" or "At risk". That sentence is not in the quote.
- correction: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST

## prince2-issue-includes-concern
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The PeopleCert article holds both fragments.

## kanban-sle-forecast
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The Kanban Guide holds both fragments, and the sentence before them defines the SLE as "a forecast of how long it should take a work item to flow from started to finished."

## scrum-forecasting-practices
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The 2020 Scrum Guide holds both sentences verbatim.

## evidence-based-scheduling
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The quote supports Monte Carlo simulation of many futures and a probability for each ship date. It does not say the simulation draws on historical estimate accuracy (velocity history) or replaces a single date. The source says both nearby ("fake history with a wide range of velocities"; "Rather than just adding up estimates to get a single ship date").
- correction: refuted (quote-found yes, supports-claim partly); trust 62 -> 42; a rule citing it cannot carry MUST

## commit-after-cone-narrows
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The Construx white paper holds all three fragments, including the source's misspelling "inadvertantly".

## schedules-are-halfhearted
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: Spolsky says most schedules are halfhearted and stored on a file share and forgotten. Separately, he says developers won't make schedules because "nobody believes the schedule is realistic". He does not say schedules go unbelieved because they are not kept as working tools; the claim's causal link is not in the source.
- correction: refuted (quote-found yes, supports-claim partly); trust 45 -> 25; a rule citing it cannot carry MUST

## fixed-time-variable-scope
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: Shape Up chapter 3 holds both fragments, and it adds "Estimates start with a design and end with a number. Appetites start with a number and end with a design."

## scrum-sprint-fixed-length
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: The 2020 Scrum Guide holds the sentence verbatim.

## scrum-product-goal-target
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: The Scrum Guide holds both fragments. It does not contrast the Product Goal with dated milestones, so "rather than dated milestones" is the author's own framing.
- correction: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST

## linear-cycles-not-releases
- quote-found: yes
- supports-claim: partly
- citation 1: holds-quote
- result: refuted
- note: Linear says cycles are time-boxed and "Unlike sprints, cycles are not tied to releases". The conclusion "so a cycle is not a milestone" is the author's inference; Linear does not say it.
- correction: refuted (quote-found yes, supports-claim partly); trust 85 -> 65; a rule citing it cannot carry MUST

## safe-roadmap-commit-near-forecast-far
- quote-found: yes
- supports-claim: yes
- citation 1: holds-quote
- result: confirmed
- note: SAFe's Roadmap page holds the sentence. The sentence before it qualifies the claim: "Typically a PI roadmap covers 3 PIs."
