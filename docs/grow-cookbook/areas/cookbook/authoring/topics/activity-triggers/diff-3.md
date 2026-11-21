--- draft-2.md
+++ draft.md
@@ -145,6 +145,7 @@
 ### Measuring selection
 
 - **measure-trigger-selection-with-labelled-tasks**: Trigger selection SHOULD be measured against a test collection of three parts: the guidelines, a set of tasks (a mix that should and should not load a given guideline), and for each task the guidelines it needs, judged against the task and not against the trigger word; little published work tests controlled vocabularies, so the cookbook builds its own set. (claims: ev-test-collection-three-parts, ev-relevance-to-need-not-query, ks-skill-trigger-eval-set, ev-little-research-vocab-evaluation)
+- **task-set-size-reference-point**: The labelled task set's size SHOULD be weighed against the IR rule of thumb that 50 information needs has usually been found a sufficient minimum; the size the cookbook adopts is the owner's to set. (claim: ev-fifty-information-needs)
 - **evaluation-before-trigger-text**: The selection evaluation SHOULD be built before the trigger values and scope notes it tests are written. (claim: pg-skills-evaluations-first)
 - **evaluation-is-source-of-truth**: Whether trigger selection works SHOULD be judged by the selection evaluation, as its source of truth. (claim: pg-skills-evaluations-source-of-truth)
 - **hold-out-part-of-task-set**: Part of the labelled task set SHOULD be held out from any tuning of trigger values or scope notes. (claim: ks-skill-trigger-train-test-split)
@@ -285,6 +286,7 @@
 - `validate-trigger-values-mechanically`: tooling fails on a value outside the table.
 - `reject-unparseable-frontmatter`: tooling fails on a guideline whose frontmatter does not parse.
 - `measure-trigger-selection-with-labelled-tasks`: selection is measured on a labelled task set of guidelines, tasks that should and should not load them, and the guidelines each task needs.
+- `task-set-size-reference-point`: the task set's size was weighed against the IR rule of thumb of a minimum of 50 information needs.
 - `evaluation-before-trigger-text`: the selection evaluation existed before the trigger values and scope notes it tests were written.
 - `evaluation-is-source-of-truth`: claims that selection works rest on the evaluation's results.
 - `hold-out-part-of-task-set`: part of the task set was held out from tuning.
