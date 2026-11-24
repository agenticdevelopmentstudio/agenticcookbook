
This section is informative; the entries below are illustrations, not a format the guideline requires.

A Playwright spec that keeps the rules:

```typescript
import { test, expect } from '@playwright/test';

test('a signed-in user sees their saved address at checkout', {
  annotation: { type: 'source', description: 'docs/features/checkout.md#saved-addresses' },
}, async ({ page }) => {
  // Hermetic: the address API returns synthetic data.
  await page.route('**/api/addresses', route =>
    route.fulfill({ json: [{ id: 'a1', line1: '1 Test Street', city: 'Exampleton' }] }));

  await page.goto('/checkout');
  await page.getByRole('button', { name: 'Use saved address' }).click();

  // A web-first assertion waits until the text appears; no fixed timeout.
  await expect(page.getByText('1 Test Street')).toBeVisible();
});
```

The same wait, written against the rules and then kept:

| Breaks a rule | Keeps it |
|---|---|
| `await page.waitForTimeout(2000)` | `await expect(page.getByRole('alert')).toHaveText('Saved')` |
| `page.locator('div.form > div:nth-child(3) > button')` | `page.getByRole('button', { name: 'Save' })` |
| `const password = 'hunter2'` | `const password = process.env.TEST_USER_PASSWORD` |

A rationale for a new assertion:

> Asserts that the saved address is offered at checkout, as `docs/features/checkout.md#saved-addresses` specifies for signed-in users.

