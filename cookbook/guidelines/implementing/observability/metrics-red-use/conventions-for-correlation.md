
- **naming-convention**: Metric names **SHOULD** follow one consistent scheme across services (the cookbook default is OpenTelemetry semantic conventions, e.g. `http.server.request.duration`) so the same query works everywhere and dashboards compose.
- **unit-discipline**: Durations **SHOULD** be recorded in seconds and sizes in bytes (base units), with the unit stated in metric metadata; mixing `ms` and `s` for the same concept breaks aggregation.
- **shared-labels**: Cross-cutting labels (`service`, `environment`, `version`) **SHOULD** be applied uniformly so RED and USE signals from the same deployment join cleanly during incident analysis.

