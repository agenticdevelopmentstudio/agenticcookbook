
**Burn rate** is how fast you are consuming the error budget relative to the SLO window: burn rate `1` exhausts the budget exactly at the window's end; burn rate `14.4` exhausts it in ~2 hours for a 30-day window.

- **alert-on-symptom-not-cause**: Alerting MUST target budget burn (the user-visible symptom), not resource thresholds (CPU > 80%, queue depth). Threshold alerts are noisy proxies that fire without user impact and miss impact that doesn't touch the watched resource.
- **use-multi-window-multi-burn-rate**: Burn-rate alerts SHOULD require BOTH a long and a short window to exceed the threshold. The long window gives recall (catches sustained burn); the short window cuts reset time so the alert clears soon after the burn stops, reducing false positives.
- **tier-by-severity**: Page on fast burn; open a ticket on slow burn. A common starting set for a 99.9% SLO (per Google SRE; tune to your window and tolerance):

  | Severity | Long window | Short window | Burn rate | Budget consumed |
  |----------|-------------|--------------|-----------|-----------------|
  | Page     | 1 hour      | 5 minutes    | 14.4      | ~2%             |
  | Page     | 6 hours     | 30 minutes   | 6         | ~5%             |
  | Ticket   | 3 days      | 6 hours      | 1         | ~10%            |

- **scale-windows-to-your-SLO**: These windows and rates assume a 30-day, 99.9% SLO. You MUST recompute them when your window or target differs — the burn-rate-to-time mapping changes with the window length.

