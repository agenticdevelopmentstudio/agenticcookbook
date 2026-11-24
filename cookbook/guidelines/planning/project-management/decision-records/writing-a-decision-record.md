
This section is informative: it shows one way to keep the rules, not a required method.

1. Decide whether the choice is significant: it shapes the system's structure or key quality attributes, or it would be hard to reverse. Spotify's teams reach such decisions through RFCs or engineering meetings and write the record of the outcome.
2. Pick one template and keep to it. Nygard's has Title, Status, Context, Decision and Consequences. MADR adds Decision Drivers, Considered Options with pros and cons, and optional decision-makers, consulted and informed metadata. A Y-statement puts the context, the requirement, the chosen option, the rejected options and the accepted downside in one sentence.
3. Fill in the context, the decision, the rationale, the options that lost and why, the decision-makers, the date, the status and every consequence, good and bad. Add a confidence level and what would trigger a revisit where it helps.
4. Keep the record to one decision and a page or two.
5. Store it with the log, openly, and link it to the issues that carry it out. On GitHub a pull request links to its issues by a keyword in its description or a commit message, across repositories. Jira's link types are configurable and none of its defaults expresses supersession; Linear relates issues as related, blocking or blocked.
6. Share the record once it is reviewed, so the people it affects hear of it.
7. When a decision changes, write a new record. Mark the old one superseded, with a "Status: superseded" line directly under its heading and a link to the new record, and name the old record in the new one. adr-tools does both with `adr new -s <number>`; PEPs carry the same pair as the `Superseded-By` and `Replaces` headers.

Tools that keep a log: adr-tools creates numbered records in the repository; log4brains publishes repository records as a searchable static site with a timeline, uses MADR by default and needs no sequential file numbers; Confluence's Decisions blueprint indexes a space's decisions as a decision log.

