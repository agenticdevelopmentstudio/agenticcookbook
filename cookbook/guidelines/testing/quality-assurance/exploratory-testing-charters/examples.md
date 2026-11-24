
This section is informative; the charter, finding and report below are illustrations, not a required format.

A charter:

```text
Explore the checkout flow
With saved payment methods, a slow network profile and a second browser tab
To discover how the order total and payment state hold up when the cart changes mid-checkout

Scope: cart review, payment entry and order confirmation
Duration: 60 minutes (the time budgeted, not an estimate)
Focus, in priority order: 1. order total  2. payment retries  3. confirmation page
Out of scope: account settings, promotional banners
Limitation: the product never charges a card twice for one order
```

A finding:

```text
Where: /checkout/confirmation
Observed: after removing an item in a second tab and returning, the confirmation page showed
  the old total (3 items, 42.00); the receipt email showed the new total (2 items, 30.00).
Expected: the confirmation page shows the current cart total, 2 items, 30.00.
Oracle: the confirmation page and the receipt disagree for the same order.
Steps: 1. add three items to the cart  2. open the cart in a second tab and remove one item
  3. return to the first tab and confirm the order
Environment: build 2.14.0, Firefox 133 on macOS 15
Repeatability: retried four times with the same steps; reproduced three times.
```

A session report with no problems found:

```text
Result: no problems found.
Covered: cart review and payment entry with saved cards and a slow network profile,
  operated in two browser tabs; observed the totals, the network log and the receipt emails.
Not tested: the confirmation page on mobile browsers (no device available this session).
Good enough because: the order total, the highest-priority focus area, was checked on every
  path the charter names.
Time: 50 minutes on charter, 10 on opportunity (the order-history page linked from the confirmation).
New charter noted: explore the order-history page for orders whose cart changed mid-checkout.
```

