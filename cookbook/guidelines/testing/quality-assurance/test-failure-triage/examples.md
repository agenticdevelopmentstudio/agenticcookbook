
This section is informative; the verdicts below are illustrations, not a required format.

A flake verdict:

```text
Disposition: flake
Observed: checkout total test failed on revision a1b2c3d; the same test passed on rerun
  of a1b2c3d in the same CI job. Log lines copied from the failing run:
    AssertionError: expected 3 items, got 2
      at tests/checkout/total.spec.ts:42
      at CheckoutPage.assertItemCount (tests/pages/checkout.ts:88)
History: failed 4 times and passed 120 times on the main branch in the last 14 days, all on unchanged code.
Cause category: asynchronous wait (the assertion runs before the cart update request completes).
Confidence: 6 (1-10). Rests on the same-revision pass and the history; not yet reproduced
  on demand, so a product-side race in the cart update is not ruled out.
```

An uncertain verdict:

```text
Disposition: uncertain
Observed: login test timed out once on revision 9f8e7d6; no trace was recorded and the rerun passed.
Missing: a trace or screenshot of the failing run, and whether other tests on the same runner
  failed in that window. Either would separate a flake from an environment fault.
Confidence: 3 (1-10). One timeout and one passing rerun; no trace and no runner-wide signal.
```

