
- **Add a delegating method**: replace `order.getCustomer().getAddress().getZip()` with `order.shippingZip()`.
- **Move behavior (Tell, Don't Ask)**: replace `if (account.getBalance() < amt) ...` with `account.withdraw(amt)` that enforces the rule internally.

