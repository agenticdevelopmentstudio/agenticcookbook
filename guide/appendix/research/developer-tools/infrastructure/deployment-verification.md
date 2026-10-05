---
id: 45cd3ab2-836d-4db2-8ef8-f7addca69065
title: Deployment Verification Tools
domain: agenticdevelopercookbook://appendix/research/developer-tools/infrastructure/deployment-verification
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: Deployment Verification Tools
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# Deployment Verification Tools

**Date:** 2026-03-29
**Context:** Tools for verifying deployments are healthy and correct, integrated with Claude Code.

This catalog covers best-in-class tools for deployment verification, organized by category. Each entry notes the tool's loop phase (plan, implement, verify), install command, and integration method with Claude Code.

**Integration methods:**
- **CLI shell-out** -- Claude Code runs the tool via Bash (most common)
- **MCP server** -- tool exposes a Model Context Protocol server for direct integration
- **Hook** -- Claude Code pre/post-tool hook triggers the tool automatically
- **Plugin** -- Claude Code plugin bundles MCP + hooks + skills

---

## Health Check Tools (verify)

Tools that confirm services are alive, ready, and accepting traffic after deployment. Health checks are the first line of defense -- if the health endpoint fails, nothing else matters.

### Wait-for-Readiness Scripts

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [wait-for-it](https://github.com/vishnubob/wait-for-it) | Pure bash script that waits for a TCP host:port to become available. Zero dependencies. Used in Docker entrypoints and CI pipelines to gate dependent services. | Copy `wait-for-it.sh` into project | CLI shell-out: `./wait-for-it.sh db:5432 --timeout=30 -- echo "db ready"`. Claude Code can run this before executing integration tests or migration commands. |
| [dockerize](https://github.com/jwilder/dockerize) | Go utility that waits for services (TCP, HTTP, Unix socket) and renders templates. More capable than wait-for-it with HTTP health check support. | `brew install dockerize` or download binary from GitHub releases | CLI shell-out: `dockerize -wait http://localhost:8080/health -timeout 60s`. Supports multiple `-wait` flags for complex dependency graphs. |
| [wait-on](https://www.npmjs.com/package/wait-on) | Node.js utility that waits for files, ports, sockets, and HTTP(S) resources. Supports TCP, HTTP HEAD/GET, file existence, and socket checks. | `npm install -g wait-on` | CLI shell-out: `wait-on http://localhost:3000 tcp:localhost:5432 --timeout 30000`. Claude Code can chain this with `&&` before running smoke tests. |

### Docker Health Checks

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Docker HEALTHCHECK](https://docs.docker.com/reference/dockerfile/#healthcheck) | Built-in Docker instruction that runs a command inside the container at intervals to verify health. Combined with `depends_on: condition: service_healthy` in Compose, replaces external wait scripts entirely. | Built into Docker | Claude Code can write HEALTHCHECK instructions in Dockerfiles and `healthcheck:` blocks in docker-compose.yml. Key params: `interval`, `timeout`, `retries`, `start_period`. The modern approach over wait-for-it for Docker workflows. |

### Uptime & Endpoint Monitoring

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [UptimeRobot](https://uptimerobot.com/) | Free-tier uptime monitoring (50 monitors) with 5-minute checks. Supports HTTP, ping, port, and keyword monitoring. Status pages included. Founded 2010, one of the most established services. | SaaS -- configure via web UI or [API](https://uptimerobot.com/api/) | Claude Code can use the REST API to create monitors post-deploy: `curl -X POST https://api.uptimerobot.com/v2/newMonitor -d "api_key=...&url=..."`. Good for basic uptime; not for synthetic transactions. |
| [Better Stack](https://betterstack.com/uptime) (formerly Better Uptime) | All-in-one monitoring platform: uptime checks every 30 seconds from multiple locations, incident management, status pages, and on-call scheduling. More complete than UptimeRobot. | SaaS -- configure via web UI or [Uptime API](https://betterstack.com/docs/uptime/api/getting-started-with-uptime-api/) | CLI shell-out via API: Claude Code can create monitors and check incident status. Integrates logging + monitoring + incidents in one platform. |
| [Pingdom](https://www.pingdom.com/) | SolarWinds uptime and performance monitoring from 100+ global locations. Synthetic transaction checks simulate user journeys (login, checkout). Real User Monitoring (RUM) included. | SaaS -- configure via web UI or API | Claude Code can query Pingdom API to verify monitor status post-deploy. Transaction checks are configured in the web UI but results are queryable via API. |
| [Uptime Kuma](https://github.com/louislam/uptime-kuma) | Self-hosted open-source monitoring tool. Supports HTTP, TCP, DNS, Docker, and push monitors. Clean UI with status pages. 60k+ GitHub stars. | `docker run -d -p 3001:3001 louislam/uptime-kuma` | Claude Code can interact via the [API](https://github.com/louislam/uptime-kuma/wiki/API) or configure Docker deployments. Best for teams that need monitoring without SaaS costs. |
| [Healthchecks.io](https://healthchecks.io/) | Cron job and heartbeat monitoring. Services ping a unique URL at expected intervals; if a ping is missed, alerts fire. Open source, self-hostable. | SaaS or `docker run healthchecks/healthchecks` | Claude Code can integrate heartbeat pings into deploy scripts: `curl -fsS --retry 3 https://hc-ping.com/UUID`. Ideal for verifying scheduled jobs and background workers are running post-deploy. |

---

## Smoke Testing (verify)

Smoke tests are fast, critical-path tests that run immediately after deployment. If smoke tests fail, roll back. They answer: "Did the deploy fundamentally break anything?"

### Browser-Based Smoke Tests

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Playwright](https://playwright.dev/) | Microsoft's cross-browser automation framework. 78k+ GitHub stars, 45% adoption among QA professionals in 2026. Supports Chromium, Firefox, WebKit. Fastest execution of the major E2E frameworks. | `npm install -D @playwright/test && npx playwright install` | CLI shell-out: `npx playwright test --grep @smoke`. Claude Code can write Playwright smoke tests that hit critical paths (login, homepage, API health). Tag smoke tests with `@smoke` for selective execution. |
| [Cypress](https://www.cypress.io/) | Developer-friendly E2E framework with time-travel debugging and automatic waiting. Superior debugging experience with DOM snapshots at each step. | `npm install -D cypress` | CLI shell-out: `npx cypress run --spec "cypress/e2e/smoke/**"`. Claude Code can write Cypress smoke specs and run them headlessly in CI. Best when debugging speed matters more than browser coverage. |

### API & Script-Based Smoke Tests

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Newman](https://github.com/postmanlabs/newman) (Postman CLI) | Runs Postman collections from the command line. Export your Postman smoke test collection and run it in CI/CD. Supports environment files and test assertions. | `npm install -g newman` | CLI shell-out: `newman run smoke-tests.postman_collection.json -e production.json --reporters cli,json`. Claude Code can parse JSON output to check for failures. |
| [curl](https://curl.se/) + [httpie](https://httpie.io/) | Universal HTTP clients for scripting smoke checks. curl is pre-installed everywhere; httpie offers a more readable syntax. Both support headers, auth, timing, and response validation. | curl: pre-installed; httpie: `pip install httpie` or `brew install httpie` | Claude Code can write and execute shell smoke scripts: `curl -sf https://api.example.com/health \|\| exit 1`. Chain multiple endpoints with `&&` for a quick smoke suite. |
| [k6](https://grafana.com/docs/k6/latest/) | Grafana's load testing tool, excellent for smoke tests at low VU counts. Write tests in JavaScript, get structured metrics output. Can verify response times stay under thresholds. | `brew install k6` or `go install go.k6.io/k6@latest` | CLI shell-out: `k6 run --vus 1 --duration 10s smoke.js`. Claude Code can write k6 scripts that check response status, body content, and latency thresholds. Output integrates with Grafana dashboards. |

### Infrastructure Smoke Tests

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Pester](https://pester.dev/) | The ubiquitous test framework for PowerShell. Used for infrastructure smoke tests on Windows/Azure: verify services are running, ports are open, configs are correct. Supports the Operation Validation Framework (OVF). | `Install-Module -Name Pester -Force` (PowerShell 5.1+) | CLI shell-out: `Invoke-Pester -Path ./smoke-tests/ -Tag Smoke`. Claude Code can write Pester tests that validate infrastructure state. Use the `Simple` folder convention for quick smoke tests vs `Comprehensive` for deeper checks. |
| [Terratest](https://terratest.gruntwork.io/) | Go library for testing infrastructure code (Terraform, Packer, Docker, Kubernetes). Deploys real infrastructure, validates it, then tears it down. | `go get github.com/gruntwork-io/terratest` | Claude Code can write Go test files that use Terratest to validate deployed infrastructure. Run with `go test -v -timeout 30m ./test/`. Best for infrastructure-as-code verification. |

---

## Progressive Deployment (verify)

Tools that gradually shift traffic to new versions, monitoring health metrics along the way. If metrics degrade, traffic shifts back automatically.

### Canary Deployment

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Argo Rollouts](https://argoproj.github.io/rollouts/) | Kubernetes controller providing advanced deployment strategies: canary with analysis, blue-green, and experimentation. Integrates with ingress controllers and service meshes for traffic shaping. Queries metrics providers (Prometheus, Datadog, CloudWatch) to drive automated promotion or rollback. | `kubectl create namespace argo-rollouts && kubectl apply -n argo-rollouts -f https://github.com/argoproj/argo-rollouts/releases/latest/download/install.yaml` | CLI shell-out: `kubectl argo rollouts status my-app`, `kubectl argo rollouts promote my-app`. Claude Code can write Rollout manifests, configure AnalysisTemplates, and monitor rollout status. The most popular Kubernetes progressive delivery controller. |
| [Flagger](https://flagger.app/) | Kubernetes operator for automated canary deployments. Integrates with Istio, Linkerd, App Mesh, NGINX, Contour, and Gloo. Runs canary analysis using Prometheus, Datadog, or CloudWatch metrics to determine promotion or rollback. | `kubectl apply -k github.com/fluxcd/flagger/kustomize/istio` (varies by mesh) | CLI shell-out: `kubectl get canaries -A`. Claude Code can write Flagger Canary resources and MetricTemplates. Works well with Flux CD for GitOps workflows. |
| [AWS CodeDeploy](https://aws.amazon.com/codedeploy/) | Managed deployment service supporting canary (two-increment traffic shift), linear (fixed % every N minutes), and all-at-once strategies for EC2, ECS, and Lambda. Automatic rollback based on CloudWatch alarms. | `aws deploy create-deployment ...` (AWS CLI) | CLI shell-out: Claude Code can create deployments, check status, and trigger rollbacks via AWS CLI. Supports `CodeDeployDefault.ECSCanary10Percent5Minutes` and similar pre-built configs. |

### Feature Flags for Progressive Rollout

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [LaunchDarkly](https://launchdarkly.com/) | Enterprise feature management platform. Sub-millisecond flag evaluation, advanced targeting rules, percentage rollouts, kill switches. The most widely adopted commercial solution. | SDK per language: `npm install launchdarkly-node-server-sdk` | Claude Code can write feature flag checks in application code and configure flag rules via the [LaunchDarkly API](https://apidocs.launchdarkly.com/). Decouples deployment from feature release. |
| [Unleash](https://www.getunleash.io/) | Leading open-source feature management platform. Gradual rollouts, kill switches, user segmentation. Self-hostable with a managed cloud option. | `docker run -p 4242:4242 unleashorg/unleash-server` | CLI shell-out via API: Claude Code can create toggles and configure gradual rollout strategies. Open-source core means no vendor lock-in. |
| [Flagsmith](https://flagsmith.com/) | Open-source feature flag platform with remote configuration. Supports web, mobile, and server-side SDKs. Granular feature control with real-time updates. | `docker-compose up` (self-hosted) or SaaS | Claude Code can manage flags via the [Flagsmith API](https://docs.flagsmith.com/clients/rest). Includes A/B testing and analytics built in. |

### Blue-Green Deployment

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Argo Rollouts](https://argoproj.github.io/rollouts/) (Blue-Green mode) | Same controller as canary, but configured for blue-green: runs both versions simultaneously, switches traffic atomically after validation, keeps old version as instant rollback target. | Same as canary install above | Claude Code can write blue-green Rollout manifests with `strategy.blueGreen`. Key fields: `activeService`, `previewService`, `autoPromotionEnabled`, `scaleDownDelaySeconds`. |
| [Kubernetes Service Switching](https://kubernetes.io/docs/concepts/services-networking/service/) | Native Kubernetes blue-green via label selectors. Deploy green with new labels, update Service selector to point to green, keep blue running for rollback. No extra controllers needed. | Built into Kubernetes | Claude Code can write the deployment manifests and `kubectl patch svc` commands to switch traffic. Simplest approach but no automated analysis or rollback. |
| [AWS CodeDeploy](https://aws.amazon.com/codedeploy/) (Blue-Green mode) | Managed blue-green for ECS and Lambda. Provisions green task set, runs validation, shifts traffic, terminates blue after configurable wait. Automatic rollback on CloudWatch alarm. | AWS CLI | Claude Code can configure `appspec.yml` with lifecycle hooks (BeforeAllowTraffic, AfterAllowTraffic) for validation. Works with ECS, Lambda, and EC2. |
| [Devtron](https://devtron.ai/) | Kubernetes-native DevOps platform with UI-based blue-green deployment. Handles environment provisioning, traffic switching, and instant rollback without scripts. | Helm chart: `helm install devtron devtron/devtron-operator` | Web UI primarily, but Claude Code can interact via Devtron's API for programmatic deployments. Best for teams wanting a GUI over raw manifests. |

---

## Rollback & Recovery (verify)

When verification fails, these tools revert to the last known good state. Fast rollback is as important as the deployment itself.

### Kubernetes Rollback

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [kubectl rollout](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/) | Built-in Kubernetes rollback commands. `kubectl rollout undo` reverts to the previous revision; `--to-revision=N` targets a specific revision. `kubectl rollout history` shows revision history. `kubectl rollout status` monitors progress. | Built into kubectl | CLI shell-out: `kubectl rollout undo deployment/my-app`, `kubectl rollout status deployment/my-app --timeout=120s`. Claude Code can check history, select a revision, and monitor rollback completion. |
| [Helm rollback](https://helm.sh/docs/helm/helm_rollback/) | Rolls back a Helm release to a previous revision. Helm maintains release history with all manifests, making rollback deterministic. | `brew install helm` or binary from [releases](https://github.com/helm/helm/releases) | CLI shell-out: `helm rollback my-release 3` (roll back to revision 3). `helm history my-release` shows all revisions. Claude Code can automate: check history, select last good revision, rollback, verify. |

### Infrastructure Rollback

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Terraform](https://www.terraform.io/) (state management) | Infrastructure-as-code with state tracking. Rollback is a roll-forward: revert the code change and re-apply. `terraform state` commands allow manual state manipulation for recovery. Remote state backends (S3, GCS) provide versioning for state file recovery. | `brew install terraform` or binary from [releases](https://releases.hashicorp.com/terraform/) | CLI shell-out: `terraform plan`, `terraform apply`. Claude Code should revert the Terraform code in git, then run `terraform apply` to roll forward. Use `terraform state list` and `terraform state show` for debugging. Never use `terraform state rm` without explicit user consent. |
| [Pulumi](https://www.pulumi.com/) | Infrastructure-as-code using general-purpose languages (TypeScript, Python, Go, C#). Stack history provides full rollback: `pulumi stack history` and targeted updates. | `brew install pulumi` or `curl -fsSL https://get.pulumi.com \| sh` | CLI shell-out: `pulumi up`, `pulumi stack history`, `pulumi refresh`. Claude Code can revert code and re-apply. Pulumi's type-safe approach catches more errors at plan time. |

### Database Migration Rollback

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Flyway](https://flywaydb.org/) | SQL-based database migration tool. Undo migrations (file prefix `U`) available in Enterprise edition. Community edition supports clean + re-migrate for non-production. As of 2025, only Community and Enterprise editions exist (Teams discontinued). | `brew install flyway` or download from [flywaydb.org](https://flywaydb.org/) | CLI shell-out: `flyway migrate`, `flyway info`, `flyway undo` (Enterprise). Claude Code can write migration and undo scripts. For Community, rollback strategy is to write a new forward migration that reverses the change. |
| [Liquibase](https://www.liquibase.com/) | Database schema change management with built-in rollback support. Supports XML, YAML, JSON, and SQL changelogs. Liquibase 5.0 (September 2025) requires Java 17+. Rollback-one-changeset available in paid tiers; Community supports tag-based rollback. | `brew install liquibase` or download from [liquibase.com](https://www.liquibase.com/) | CLI shell-out: `liquibase update`, `liquibase rollback-count 1`, `liquibase rollback-to-tag release-1.0`. Claude Code can write changesets with explicit rollback blocks. |
| [Alembic](https://alembic.sqlalchemy.org/) | Migration tool for Python/SQLAlchemy. Supports upgrade and downgrade operations per revision. Each migration file has both `upgrade()` and `downgrade()` functions. | `pip install alembic` | CLI shell-out: `alembic upgrade head`, `alembic downgrade -1`, `alembic history`. Claude Code can write migrations with proper downgrade logic and execute rollbacks. |
| [Prisma Migrate](https://www.prisma.io/migrate) | Schema-first migrations for TypeScript/Node.js. Prisma 7 (late 2025) dropped the Rust engine for pure TS. No built-in rollback command; rollback strategy is creating a new migration that reverses changes, or using `prisma db execute` for manual SQL. | `npm install prisma` | CLI shell-out: `npx prisma migrate deploy`, `npx prisma migrate status`. Claude Code can generate reverse migrations. For emergencies, `npx prisma db execute --file rollback.sql`. |

---

## Synthetic Monitoring (verify)

Continuous automated tests that simulate real user behavior from external locations. Run post-deploy and on a schedule to catch regressions that internal tests miss.

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Checkly](https://www.checklyhq.com/) | Developer-focused synthetic monitoring using Playwright scripts. Monitor APIs and browser flows as code. Tests run from 20+ global locations. Integrates with CI/CD via the Checkly CLI. | `npm install -g checkly` | CLI shell-out: `npx checkly test`, `npx checkly deploy`. Claude Code can write Playwright-based check scripts, deploy them to Checkly, and verify results post-deploy. "Monitoring as code" approach fits developer workflows. |
| [Datadog Synthetic Tests](https://docs.datadoghq.com/synthetics/) | Enterprise synthetic monitoring with API tests, browser tests (no-code recorder), and multi-step API tests. AI anomaly detection, self-healing tests, 1000+ integrations. Correlates synthetic results with traces and logs. | SaaS -- configure via web UI or [Terraform provider](https://registry.terraform.io/providers/DataDog/datadog/) | Claude Code can manage synthetic tests via the Datadog API or Terraform. Tests can be triggered on-demand post-deploy via API: `curl -X POST "https://api.datadoghq.com/api/v1/synthetics/tests/trigger"`. |
| [Grafana Synthetic Monitoring](https://grafana.com/products/cloud/synthetic-monitoring/) | Built into Grafana Cloud. Supports HTTP, DNS, TCP, ping, traceroute, and scripted k6 checks. k6 scripted checks let you write JavaScript for complex transaction monitoring. Results flow into Grafana dashboards. | Enabled in Grafana Cloud; k6 scripts via `k6 run` | Claude Code can write k6 synthetic scripts and configure checks via the Grafana Cloud API. Integrates natively with Prometheus metrics and Loki logs for correlation. |
| [Pingdom Transaction Tests](https://www.pingdom.com/) | Synthetic transaction monitoring that simulates user journeys (login, checkout, form submission) from 100+ global locations. Part of the SolarWinds platform. | SaaS -- configure via web UI or API | Transaction tests are configured in the web UI; Claude Code can query results via the API to verify post-deploy behavior. Best for teams already in the SolarWinds ecosystem. |

---

## Post-Deploy Validation (verify)

After the deploy is live, these tools detect problems by analyzing logs, metrics, and system behavior. The goal is catching issues that smoke tests miss -- slow degradation, edge cases, and error spikes.

### Log Analysis

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Grafana Loki](https://grafana.com/oss/loki/) | "Prometheus for logs." Indexes metadata (labels) not full text, making it cost-effective at scale. Alerting rules can fire on log patterns (error spikes, new exception types). Pairs with Promtail or Grafana Agent for log collection. | `helm install loki grafana/loki-stack` or Grafana Cloud | Claude Code can query Loki via LogQL: `{app="my-service"} \|= "error" \| rate() > threshold`. Write alerting rules that fire when error rates spike post-deploy. |
| [Sentry](https://sentry.io/) | Error tracking platform that groups errors by root cause, shows first/last seen, and tracks error frequency. SDKs for every major language. Release tracking shows which deploy introduced which errors. | SDK per language: `npm install @sentry/node` | Claude Code can integrate Sentry SDK into application code and query the [Sentry API](https://docs.sentry.io/api/) post-deploy to check for new error groups. Release association (`SENTRY_RELEASE`) links errors to specific deploys. |
| [Datadog Log Management](https://docs.datadoghq.com/logs/) | Centralized logging with real-time search, pattern detection, and anomaly alerts. Log-based metrics let you create monitors on error rates without custom instrumentation. | Agent: `DD_API_KEY=... DD_SITE=... bash -c "$(curl -L https://install.datadoghq.com/scripts/install_mac_os.sh)"` | Claude Code can query Datadog Logs API to search for errors post-deploy. Set up log-based monitors that alert on `status:error` rate exceeding baseline. |

### Metric Monitoring & Alerting

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Prometheus](https://prometheus.io/) + [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/) | Open-source metrics collection and alerting. PromQL queries define alert conditions (latency P99, error rate, saturation). Alertmanager handles routing, grouping, silencing, and notification (Slack, PagerDuty, email). | `brew install prometheus` or Helm: `helm install prometheus prometheus-community/kube-prometheus-stack` | CLI shell-out: `promtool check rules alerts.yml`. Claude Code can write PromQL alert rules for post-deploy validation: `rate(http_requests_total{status=~"5.."}[5m]) > 0.01`. |
| [Grafana](https://grafana.com/) | Visualization and alerting dashboard. Unified alerting supports Prometheus, Loki, and other data sources. Alert rules can trigger on metric thresholds, log patterns, or composite conditions. | `brew install grafana` or `docker run -d -p 3000:3000 grafana/grafana` | Claude Code can provision dashboards and alert rules via Grafana's [HTTP API](https://grafana.com/docs/grafana/latest/developers/http_api/) or Terraform. Post-deploy, check the dashboard API for active alerts. |
| [PagerDuty](https://www.pagerduty.com/) / [Opsgenie](https://www.atlassian.com/software/opsgenie) | Incident management platforms that receive alerts from monitoring tools, manage on-call schedules, and escalate. PagerDuty supports automated runbooks for common remediation. | SaaS -- integrates via webhook or native integrations | Claude Code can check incident status via API post-deploy. PagerDuty's [Event API v2](https://developer.pagerduty.com/api-reference/) allows triggering and resolving incidents programmatically. |

### Automated Runbooks

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Rundeck](https://www.rundeck.com/) | Open-source runbook automation. Define operational procedures as jobs with steps, run them on-demand or triggered by alerts. Supports node filtering, approval workflows, and audit logging. | `brew install rundeck` or Docker | Claude Code can trigger Rundeck jobs via API: `curl -X POST https://rundeck.example.com/api/41/job/UUID/run`. Pair with Alertmanager webhooks for automated remediation (restart service, scale out, purge cache). |
| [incident.io](https://incident.io/) | Incident management with automated workflows. Can auto-detect deployment-related incidents, run diagnostic steps, and execute remediation. Integrates with Slack for collaborative response. | SaaS -- configure via web UI | Claude Code can check incident status and trigger workflows via API. Their automated runbook approach reduces MTTR by ~50% according to their benchmarks. |

---

## SSL/TLS & Certificate Verification (verify)

Verify that TLS is correctly configured, certificates are valid, and the deployment hasn't introduced security regressions.

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [testssl.sh](https://testssl.sh/) | Comprehensive bash-based TLS/SSL scanner. Tests ciphers, protocols, vulnerabilities (Heartbleed, ROBOT, CCS injection), and certificate details. Works on any port, not just 443. Runs locally -- safe for internal/staging environments. Machine-readable output (CSV, JSON, HTML). | `git clone https://github.com/testssl/testssl.sh.git` or `brew install testssl` | CLI shell-out: `testssl.sh --json-pretty https://example.com`. Claude Code can run this post-deploy and parse JSON output to check for regressions. Add to CI as: `testssl.sh --severity HIGH --json staging.example.com \|\| exit 1`. |
| [SSLyze](https://github.com/nabla-c0d3/sslyze) | Python-based SSL/TLS scanner. Tests against Mozilla's recommended TLS configurations (modern, intermediate, old). Battle-tested on hundreds of thousands of servers daily. Can run from CI/CD pipelines. | `pip install sslyze` | CLI shell-out: `sslyze --mozilla_config=intermediate www.example.com`. Claude Code can verify TLS config matches Mozilla's standards post-deploy. Also usable as a Python library for programmatic checks. |
| [SSL Labs API](https://www.ssllabs.com/ssltest/) | Qualys free SSL server test. The industry standard for public-facing TLS assessment. Grades A+ through F. API available for automation but rate-limited. | No install -- API at `https://api.ssllabs.com/api/v3/` | CLI shell-out: `curl "https://api.ssllabs.com/api/v3/analyze?host=example.com&startNew=on"`. Claude Code can poll for results and verify grade hasn't dropped. Use sparingly -- cache results and only run on TLS config changes. |
| [certbot](https://certbot.eff.org/) (verify mode) | Let's Encrypt client with certificate management. `certbot certificates` shows installed certs and expiry dates. Post-deploy, verify renewed certs are correctly served. | `brew install certbot` or `pip install certbot` | CLI shell-out: `certbot certificates` to list cert expiry. Claude Code can verify certs won't expire within N days: parse the `Expiry Date` field and alert if < 30 days. |
| [cert-manager](https://cert-manager.io/) (Kubernetes) | Kubernetes-native certificate management. Automatically provisions and renews TLS certificates from Let's Encrypt, HashiCorp Vault, Venafi, and more. Certificate resources show status. | `kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.17.0/cert-manager.yaml` | CLI shell-out: `kubectl get certificates -A`, `kubectl describe certificate my-cert`. Claude Code can verify all certificates are in `Ready=True` state post-deploy. |

---

## DNS & Network Testing (verify)

Verify DNS resolution, routing, and network performance after deployment. Catch misconfigured DNS records, routing issues, and performance regressions.

### DNS Verification

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [dig](https://man.openbsd.org/dig.1) | DNS lookup utility. Query any record type (A, AAAA, CNAME, MX, TXT, SRV) against specific nameservers. Shows full DNS response including TTL and authority section. | Pre-installed on most Unix systems; `brew install bind` on macOS if missing | CLI shell-out: `dig +short example.com A`, `dig @8.8.8.8 example.com CNAME`. Claude Code can verify DNS records point to the correct IPs post-deploy. Chain with expected value: `[ "$(dig +short example.com A)" = "1.2.3.4" ] \|\| exit 1`. |
| [nslookup](https://man.openbsd.org/nslookup.1) | Simpler DNS query tool. Less powerful than dig but available everywhere including Windows. | Pre-installed on all major OSes | CLI shell-out: `nslookup example.com`. Claude Code can use this for quick DNS verification when dig is unavailable. |
| [dog](https://github.com/ogham/dog) | Modern DNS client with colorized output, JSON support, and DNS-over-HTTPS/TLS. A friendlier alternative to dig. | `brew install dog` | CLI shell-out: `dog example.com A --json`. Claude Code can parse JSON output for automated DNS verification. |

### Network Diagnostics

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [mtr](https://github.com/traviscross/mtr) | Combines traceroute and ping in a single tool. Shows packet loss and latency at each hop. Essential for diagnosing routing issues after infrastructure changes. | `brew install mtr` or `apt install mtr` | CLI shell-out: `mtr --report --report-cycles 10 example.com`. Claude Code can run this to diagnose latency issues post-deploy. The `--report` flag gives a single summary instead of the interactive UI. |
| [curl timing](https://curl.se/) | curl's `-w` flag exposes detailed timing breakdown: DNS lookup, TCP connect, TLS handshake, time to first byte (TTFB), and total time. Essential for performance regression detection. | Pre-installed everywhere | CLI shell-out: `curl -o /dev/null -s -w "dns:%{time_namelookup} connect:%{time_connect} ttfb:%{time_starttransfer} total:%{time_total}\n" https://example.com`. Claude Code can compare TTFB before and after deploy. |

### HTTP Benchmark Tools

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [hey](https://github.com/rakyll/hey) | Simple HTTP load generator (formerly boom). Written in Go. Quick way to verify a service handles expected load after deploy. | `brew install hey` or `go install github.com/rakyll/hey@latest` | CLI shell-out: `hey -n 1000 -c 50 https://example.com/api/health`. Claude Code can run a quick load test post-deploy and verify P99 latency stays under threshold. |
| [wrk](https://github.com/wg/wrk) | High-performance HTTP benchmark tool using epoll/kqueue. Lua scripting for custom request generation. More throughput than hey for stress testing. | `brew install wrk` | CLI shell-out: `wrk -t4 -c100 -d10s https://example.com`. Claude Code can compare baseline vs post-deploy throughput. Use Lua scripts for authenticated or POST requests. |
| [bombardier](https://github.com/codesenberg/bombardier) | Fast cross-platform HTTP benchmarking tool written in Go. Uses fasthttp for maximum performance. Supports HTTP/1.x and HTTP/2.0. Clean output with latency distribution and throughput stats. | `brew install bombardier` or `go install github.com/codesenberg/bombardier@latest` | CLI shell-out: `bombardier -c 200 -d 10s -l https://example.com`. Claude Code can run quick benchmarks and verify latency distribution hasn't degraded. The `-l` flag enables latency distribution output. |
| [k6](https://grafana.com/docs/k6/latest/) (load mode) | Full-featured load testing with scenarios, thresholds, and checks. Write tests in JavaScript. Thresholds fail the test if metrics exceed limits (e.g., P95 < 200ms). | `brew install k6` | CLI shell-out: `k6 run --out json=results.json load-test.js`. Claude Code can write k6 scripts with thresholds: `http_req_duration: ['p(95)<200']`. Parse JSON output to verify performance post-deploy. |

---

## Environment Verification (verify)

Verify the deployed environment is correctly configured: required environment variables are present, secrets are accessible, dependencies are reachable, and databases are connected.

### Configuration Validation

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [dotenv-linter](https://dotenv-linter.github.io/) | Lightning-fast linter for `.env` files written in Rust. Checks for duplicates, incorrect ordering, missing values, extra blanks, and inconsistencies across `.env` files. | `brew install dotenv-linter` or `cargo install dotenv-linter` | CLI shell-out: `dotenv-linter .env .env.production`. Claude Code can run this in CI to catch env file issues before deploy. Also compares files: `dotenv-linter compare .env .env.example` to ensure all required vars are defined. |
| [envalid](https://www.npmjs.com/package/envalid) | Node.js runtime environment variable validation. Defines a schema for required vars with types, defaults, and descriptions. Fails fast at startup with clear error messages if vars are missing or malformed. | `npm install envalid` | Claude Code can write envalid schemas in application code: `cleanEnv(process.env, { DATABASE_URL: str(), PORT: port({ default: 3000 }) })`. Catches missing or invalid config at deploy time, not at first request. |
| [env-sentinel](https://www.envsentinel.dev/) | Environment variable management and validation platform. Three-layer merge (base, environment-specific, personal overrides). Startup validation with format checking. | See [docs](https://www.envsentinel.dev/) for install | Claude Code can configure validation rules that run during application startup. Prevents localhost database URLs in production and other common misconfigurations. |

### Dependency & Connectivity Checks

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [wait-for-it](https://github.com/vishnubob/wait-for-it) / [dockerize](https://github.com/jwilder/dockerize) | Also listed under Health Check Tools. Use these to verify dependent services (database, cache, message queue) are reachable before the application starts accepting traffic. | See Health Check Tools section | Claude Code can write startup scripts that check all dependencies: `dockerize -wait tcp://db:5432 -wait tcp://redis:6379 -wait http://auth:8080/health -timeout 60s`. |
| [pg_isready](https://www.postgresql.org/docs/current/app-pg-isready.html) | PostgreSQL connection checker. Returns exit code 0 if the server is accepting connections. Works with connection strings, supports timeout. | Included with PostgreSQL client: `brew install libpq` | CLI shell-out: `pg_isready -h localhost -p 5432 -U myuser`. Claude Code can use this in deploy scripts to verify database connectivity before running migrations. |
| [mysqladmin ping](https://dev.mysql.com/doc/refman/en/mysqladmin.html) | MySQL/MariaDB connectivity check. Verifies the server is alive and accepting connections. | Included with MySQL client: `brew install mysql-client` | CLI shell-out: `mysqladmin ping -h localhost -u root`. Returns `mysqld is alive` on success. |
| [redis-cli ping](https://redis.io/docs/latest/commands/ping/) | Redis connectivity and latency check. `PING` returns `PONG` if the server is responsive. | Included with Redis: `brew install redis` | CLI shell-out: `redis-cli -h localhost ping`. Claude Code can verify Redis is reachable and measure latency with `redis-cli --latency`. |
| Custom startup probes | Shell scripts that verify all required environment variables exist, secrets are readable, and external service endpoints respond. Run as a Kubernetes init container, Docker entrypoint check, or CI pipeline step. | Write as shell script | Claude Code can write comprehensive startup verification scripts: check each required env var, test database connectivity, verify API keys work with a test call, and confirm file system mounts are accessible. Fail the deploy if any check fails. |

### Secret Verification

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Vault](https://www.vaultproject.io/) (HashiCorp) | Secret management platform. Post-deploy, verify the application can read required secrets from Vault. `vault kv get` retrieves secrets; `vault status` checks server health. | `brew install vault` | CLI shell-out: `vault status`, `vault kv get -field=value secret/myapp/db-password > /dev/null`. Claude Code can verify secret paths are readable without exposing values. |
| [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) | AWS-managed secret store. Post-deploy, verify the application's IAM role can access required secrets. | AWS CLI | CLI shell-out: `aws secretsmanager get-secret-value --secret-id myapp/db-password --query SecretString > /dev/null`. Claude Code can verify secret access without printing values. |
| [1Password CLI](https://developer.1password.com/docs/cli/) | 1Password secret management for development and CI/CD. `op read` retrieves secrets; `op inject` populates templates. | `brew install 1password-cli` | CLI shell-out: `op read "op://Vault/DB Password/password" > /dev/null 2>&1 && echo "ok"`. Claude Code can verify secret access in deploy pipelines. |

---

## Sources

### Health Check Tools
- [Docker Compose Health Checks (Last9)](https://last9.io/blog/docker-compose-health-checks/)
- [Docker Health Check Best Practices (OneUptime)](https://oneuptime.com/blog/post/2026-01-30-docker-health-check-best-practices/view)
- [wait-for-it vs Healthcheck (Medium)](https://medium.com/@pavel.loginov.dev/wait-for-services-to-start-in-docker-compose-wait-for-it-vs-healthcheck-e0248f54962b)
- [Forget wait-for-it (denhox.com)](https://www.denhox.com/posts/forget-wait-for-it-use-docker-compose-healthcheck-and-depends-on-instead/)

### Uptime Monitoring
- [11 Best Uptime Monitoring Tools 2026 (UptimeRobot)](https://uptimerobot.com/knowledge-hub/monitoring/11-best-uptime-monitoring-tools-compared/)
- [Better Stack vs UptimeRobot (API Status Check)](https://apistatuscheck.com/blog/better-stack-vs-uptimerobot)
- [Better Stack Uptime API](https://betterstack.com/docs/uptime/api/getting-started-with-uptime-api/)

### Smoke Testing
- [Playwright](https://playwright.dev/)
- [Smoke Testing SaaS with Playwright (MakerKit)](https://makerkit.dev/blog/tutorials/smoke-testing-saas-playwright)
- [E2E Testing Tools 2026 (Autonoma)](https://www.getautonoma.com/blog/e2e-testing-tools)
- [Pester Framework](https://pester.dev/)
- [Infrastructure Testing with Pester (4sysops)](https://4sysops.com/archives/an-introduction-to-infrastructure-testing-with-powershell-pester/)

### Progressive Deployment
- [Argo Rollouts](https://argoproj.github.io/rollouts/)
- [Progressive Delivery: Argo Rollouts and Flagger (Calmops)](https://calmops.com/architecture/progressive-delivery-canary-argo-rollouts-flagger/)
- [Canary Releases with Kubernetes and Feature Flags (GoCodeo)](https://www.gocodeo.com/post/implementing-canary-releases-with-kubernetes-and-feature-flags)
- [Automating Blue-Green and Canary with Argo Rollouts (Akuity)](https://akuity.io/blog/automating-blue-green-and-canary-deployments-with-argo-rollouts)
- [Blue-Green Deployment in Kubernetes (Spacelift)](https://spacelift.io/blog/blue-green-deployment-kubernetes)
- [AWS CodeDeploy Blue-Green (Medium)](https://medium.com/@praneethshettyy/aws-codedeploy-blue-green-deployment-rollback-guide-229c8aed7f22)

### Rollback & Recovery
- [kubectl rollout undo (Kubernetes docs)](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_undo/)
- [Terraform State Rollback Guide (Spacelift)](https://spacelift.io/blog/terraform-state-rollback)
- [Flyway vs Liquibase 2026 (Bytebase)](https://www.bytebase.com/blog/flyway-vs-liquibase/)
- [Database Migration Testing (Yuri Kan)](https://yrkan.com/blog/database-migration-testing/)

### Synthetic Monitoring
- [Checkly](https://www.checklyhq.com/)
- [Grafana Synthetic Monitoring](https://grafana.com/products/cloud/synthetic-monitoring/)
- [k6 Synthetic Monitoring (Grafana)](https://grafana.com/docs/k6/latest/testing-guides/synthetic-monitoring/)
- [21 Best Synthetic Monitoring Tools 2026 (CTO Club)](https://thectoclub.com/tools/best-synthetic-monitoring-tools/)

### Post-Deploy Validation
- [12 Post-Deployment Validation Steps (DevOps Training Institute)](https://www.devopstraininginstitute.com/blog/12-post-deployment-validation-steps-in-cicd)
- [Automated Runbook Guide (incident.io)](https://incident.io/blog/automated-runbook-guide)
- [Observability with Prometheus, Grafana, Loki (Medium)](https://medium.com/@abhishek_pahuja/back-to-basics-observability-and-monitoring-with-prometheus-grafana-loki-and-alert-manager-bba2cdccf738)

### SSL/TLS
- [testssl.sh](https://testssl.sh/)
- [SSLyze (GitHub)](https://github.com/nabla-c0d3/sslyze)
- [SSL Labs Server Test](https://www.ssllabs.com/ssltest/)
- [Best SSL Checker Tools (Geekflare)](https://geekflare.com/cybersecurity/best-ssl-checker/)

### DNS & Network
- [HTTP Benchmark Tools (GitHub Gist)](https://gist.github.com/denji/8333630)
- [Bombardier (GitHub)](https://github.com/codesenberg/bombardier)
- [Performance Testing with Bombardier (Improve & Repeat)](https://improveandrepeat.com/2025/01/performance-testing-your-web-application-with-bombardier/)

### Environment Verification
- [dotenv-linter](https://dotenv-linter.github.io/)
- [envalid (npm)](https://www.npmjs.com/package/envalid)
- [Environment Variable Management Best Practices 2026 (Env-Sentinel)](https://www.envsentinel.dev/blog/environment-variable-management-tips-best-practices)
- [.env Validator Guide (CheckTown)](https://check.town/blog/env-validator-guide)
