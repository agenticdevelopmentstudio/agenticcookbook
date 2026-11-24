--- draft-1.md
+++ draft.md
@@ -82,8 +82,8 @@
 - **every-failure-gets-one-disposition**: Every failure put to triage MUST receive exactly one disposition: no failure is left without one, and no disposition is given for a failure that was not in the input. (claims: ks-treeherder-classification-set, bp-failure-classes-flaky-bug-obsolete)
 - **disposition-from-fixed-set**: Each disposition MUST be one value from a fixed set that covers a product bug, a flake, an environment fault, a test made stale by an intended behavior change, and uncertain. (claims: ks-treeherder-classification-set, bp-failure-classes-flaky-bug-obsolete, pg-firebase-inconclusive-vs-failure, ks-trunk-broken-vs-flaky)
 - **never-force-a-verdict**: Where the evidence does not settle which disposition a failure has, the triager SHOULD give it the uncertain disposition rather than force it into another. (claims: bp-rerun-same-code-separates-flake, ks-treeherder-classification-set, ks-datadog-flaky-categories, ks-meta-pfs-posterior-uncertainty, bp-explain-uncertainty-and-gaps)
-- **evidence-states-what-was-observed**: A verdict's evidence MUST state what was observed and where, kept apart from what is inferred from it; an argument from what is likely is not evidence. (claims: bp-bug-report-observed-vs-expected, bp-failure-record-copies-log, bp-separate-information-from-judgment, ev-get-data-first)
-- **bug-names-observed-misbehavior**: A product-bug verdict MUST name the misbehavior observed, the actual result against the expected one, and where in the system under test it was observed. (claims: bp-bug-report-observed-vs-expected, bp-failure-message-desired-actual)
+- **evidence-states-what-was-observed**: A verdict's evidence MUST state what was observed and where, kept apart from what is inferred from it; an argument from what is likely is not evidence. (claims: bp-bug-report-observed-vs-expected, bp-failure-record-copies-log)
+- **bug-names-observed-misbehavior**: A product-bug verdict MUST name the misbehavior observed, the actual result against the expected one, and where in the system under test it was observed. (claim: bp-bug-report-observed-vs-expected)
 - **flake-cites-history-or-race**: A flake verdict MUST cite the test's outcome history on unchanged code, such as a pass on retry or both a failure and a pass on the same revision, or a race visible in the error; that a failure seems intermittent is not a flake verdict. (claims: pg-ci-flaky-same-code-history, pg-playwright-flaky-status, pg-surefire-flaky-counted, bp-rerun-same-code-separates-flake, ks-luo-flaky-root-causes, ks-datadog-flaky-categories)
 - **environment-cites-cross-test-signal**: This MUST hold: An **environment** verdict cites a signal spanning unrelated sites or tests, or a probe/status observation. A single failing test never establishes it. (claim: environment-cites-cross-test-signal-prior)
 - **spec-rot-names-new-assertion**: This MUST hold: A **spec-rot** verdict carries a non-empty `suggested_fix` naming what the spec should assert now. A suggested_fix that restates the failure, or says the spec needs updating without saying to what, is a fail. (claim: spec-rot-names-new-assertion-prior)
@@ -137,11 +137,14 @@
 
 ```text
 Disposition: flake
-Observed: checkout total test failed on revision a1b2c3d with "expected 3 items, got 2"
-  (log lines copied below); the same test passed on rerun of a1b2c3d in the same CI job.
+Observed: checkout total test failed on revision a1b2c3d; the same test passed on rerun
+  of a1b2c3d in the same CI job. Log lines copied from the failing run:
+    AssertionError: expected 3 items, got 2
+      at tests/checkout/total.spec.ts:42
+      at CheckoutPage.assertItemCount (tests/pages/checkout.ts:88)
 History: failed 4 times and passed 120 times on the main branch in the last 14 days, all on unchanged code.
 Cause category: asynchronous wait (the assertion runs before the cart update request completes).
-Confidence: likely. Rests on the same-revision pass and the history; not yet reproduced
+Confidence: 6 (1-10). Rests on the same-revision pass and the history; not yet reproduced
   on demand, so a product-side race in the cart update is not ruled out.
 ```
 
@@ -152,6 +155,7 @@
 Observed: login test timed out once on revision 9f8e7d6; no trace was recorded and the rerun passed.
 Missing: a trace or screenshot of the failing run, and whether other tests on the same runner
   failed in that window. Either would separate a flake from an environment fault.
+Confidence: 3 (1-10). One timeout and one passing rerun; no trace and no runner-wide signal.
 ```
 
 ## What a reviewer looks for
