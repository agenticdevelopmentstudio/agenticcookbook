---
id: 6a81c776-d327-4ea6-9814-585e5cf85bc7
title: Web Backend Development Tools
domain: agenticdevelopercookbook://appendix/research/developer-tools/web/backend-tools
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: Web Backend Development Tools
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# Web Backend Development Tools

**Date:** 2026-03-29
**Context:** Backend development tools that integrate with Claude Code for the plan/implement/verify loop.

This catalog covers best-in-class CLI tools for web backend development, organized by category. Each entry notes the tool's loop phase (plan, implement, verify), install command, and integration method with Claude Code.

**Integration methods:**
- **CLI shell-out** -- Claude Code runs the tool via Bash (most common)
- **MCP server** -- tool exposes a Model Context Protocol server for direct integration
- **Hook** -- Claude Code pre/post-tool hook triggers the tool automatically
- **Plugin** -- Claude Code plugin bundles MCP + hooks + skills

---

## Server Frameworks (implement)

Frameworks Claude Code can scaffold, configure, and develop against. All integrate via CLI shell-out for project creation and `dev` server commands.

### Node.js

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Express](https://expressjs.com/) | The most widely used Node.js web framework. Mature ecosystem, extensive middleware, massive community. Battle-tested since 2010. | `npm install express` | Largest middleware ecosystem; Claude knows Express patterns deeply due to training data volume. |
| [Fastify](https://fastify.dev/) | High-performance Node.js framework with built-in schema validation, JSON serialization, and logging. 2-3x faster than Express for JSON APIs. | `npm install fastify` | Built-in JSON Schema validation generates types automatically; excellent for API-first development. |
| [Hono](https://hono.dev/) | Ultralight, cross-runtime framework (Node, Deno, Bun, Cloudflare Workers, AWS Lambda). Minimal bundle, fast cold starts. | `npm install hono` | Best for edge/serverless; same code runs on every runtime. Growing fast in 2025-2026. |
| [Koa](https://koajs.com/) | Lightweight middleware framework by the Express team. Uses async/await natively with a minimal core. | `npm install koa` | Smaller ecosystem than Express; good for developers who want fine-grained middleware control. |

### Python

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [FastAPI](https://fastapi.tiangolo.com/) | Modern async Python framework with automatic OpenAPI docs and Pydantic validation. Handles 20k+ req/s with Uvicorn. Adoption grew 40% YoY through 2025. | `pip install "fastapi[standard]"` | Auto-generates OpenAPI spec; Claude can read the spec to understand endpoints during planning. |
| [Django](https://www.djangoproject.com/) | Batteries-included full-stack framework with ORM, admin, auth, and migrations built in. The mature Python choice for complex applications. | `pip install django` | `manage.py` CLI is excellent for Claude shell-out (migrations, shell, test, runserver). |
| [Flask](https://flask.palletsprojects.com/) | Lightweight WSGI micro-framework for rapid prototyping. Flexible and simple, with extensions for anything you need. | `pip install flask` | Best for small APIs and prototypes; less opinionated than Django. |

### Ruby

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Ruby on Rails](https://rubyonrails.org/) | Full-stack convention-over-configuration framework. Fastest time-to-ship for CRUD apps. Strong CLI generators. | `gem install rails` | `rails` CLI generates models, controllers, migrations; Claude can drive the full scaffold workflow. |

### Go

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Gin](https://gin-gonic.com/) | Most popular Go web framework (used by 48% of Go developers). Fast routing, middleware support, JSON rendering. | `go get github.com/gin-gonic/gin` | Best default choice for Go APIs; huge community and documentation. |
| [Echo](https://echo.labstack.com/) | Structured Go framework with type safety, middleware chaining, and enterprise patterns. Slightly edges Gin in raw throughput. | `go get github.com/labstack/echo/v4` | Better for enterprise API gateways; steeper learning curve than Gin. |
| [Fiber](https://gofiber.io/) | Express-inspired Go framework built on fasthttp. Exceptional performance at the cost of some net/http compatibility. | `go get github.com/gofiber/fiber/v2` | Familiar to Express developers; fastest Go framework in many benchmarks. |

### Java

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Spring Boot](https://spring.io/projects/spring-boot) | Enterprise Java framework used by JPMorgan, PayPal, Stripe. Auto-configuration, embedded servers, production-ready features. | `sdk install springboot` (SDKMAN) or [start.spring.io](https://start.spring.io) | `spring` CLI and Maven/Gradle integration; Claude can generate and modify `application.properties`. |

### C#

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [ASP.NET Core](https://dotnet.microsoft.com/apps/aspnet) | Cross-platform, high-performance .NET framework. Strong typed tooling, integrated with .NET 8+ ecosystem. | `dotnet new webapi` | `dotnet` CLI is comprehensive; Claude drives project creation, build, run, and publish. |

---

## Database Tools

### Migration & Schema Management (implement)

| Tool | What it does | Install | Integration |
|------|-------------|---------|-------------|
| [Prisma Migrate](https://www.prisma.io/migrate) | Declarative schema-first migrations for TypeScript/Node.js. Prisma 7 (late 2025) dropped the Rust engine for pure TS -- 3.4x faster queries, 9x faster cold starts. | `npm install prisma` | CLI shell-out: `npx prisma migrate dev`, `npx prisma db push` |
| [Drizzle Kit](https://orm.drizzle.team/kit-docs/overview) | Code-first TypeScript migration generator. Minimal bundle (~7.4KB), SQL-like control. v1.0 beta landed early 2025. | `npm install drizzle-kit` | CLI shell-out: `npx drizzle-kit generate`, `npx drizzle-kit migrate` |
| [Knex](https://knexjs.org/) | SQL query builder with migration support for PostgreSQL, MySQL, SQLite, MSSQL, Oracle, and more. Mature and stable. | `npm install knex` | CLI shell-out: `npx knex migrate:latest`, `npx knex seed:run` |
| [Alembic](https://alembic.sqlalchemy.org/) | Migration tool for SQLAlchemy. v1.17.2 released January 2026. The standard for Python/SQLAlchemy projects. | `pip install alembic` | CLI shell-out: `alembic upgrade head`, `alembic revision --autogenerate` |
| [Django Migrations](https://docs.djangoproject.com/en/5.1/topics/migrations/) | Built-in migration framework for Django ORM. Auto-detects model changes and generates migration files. | Included with Django | CLI shell-out: `python manage.py makemigrations`, `python manage.py migrate` |
| [ActiveRecord Migrations](https://guides.rubyonrails.org/active_record_migrations.html) | Built-in Rails migration system. Convention-driven, supports reversible migrations with rollback. | Included with Rails | CLI shell-out: `rails db:migrate`, `rails generate migration` |
| [Entity Framework Migrations](https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/) | .NET migration system with code-first and database-first workflows. Integrated with `dotnet` CLI. | `dotnet tool install --global dotnet-ef` | CLI shell-out: `dotnet ef migrations add`, `dotnet ef database update` |

### ORMs & Query Builders (implement)

| Tool | What it does | Install | Integration |
|------|-------------|---------|-------------|
| [Prisma](https://www.prisma.io/) | Type-safe ORM with declarative schema, auto-generated client, and visual Studio. Prisma 7 is pure TypeScript with 85-90% smaller bundle. | `npm install @prisma/client` | CLI shell-out: `npx prisma generate`, `npx prisma studio` |
| [Drizzle ORM](https://orm.drizzle.team/) | Lightweight TypeScript ORM with SQL-like syntax. Zero dependencies, full type safety, optimal for serverless. | `npm install drizzle-orm` | CLI shell-out (via drizzle-kit); code-level integration |
| [TypeORM](https://typeorm.io/) | Decorator-based ORM for TypeScript supporting Active Record and Data Mapper patterns. Supports MySQL, PostgreSQL, SQLite, MSSQL, Oracle. | `npm install typeorm` | CLI shell-out: `npx typeorm migration:run` |
| [Sequelize](https://sequelize.org/) | Promise-based Node.js ORM for PostgreSQL, MySQL, SQLite, MSSQL. Established ecosystem with large community. | `npm install sequelize` | CLI shell-out: `npx sequelize-cli db:migrate` |
| [SQLAlchemy](https://www.sqlalchemy.org/) | The dominant Python SQL toolkit and ORM. Supports both high-level ORM and low-level Core patterns. Standard for FastAPI and data engineering. | `pip install sqlalchemy` | Code-level integration; pairs with Alembic for migrations |
| [Django ORM](https://docs.djangoproject.com/en/5.1/topics/db/) | Built-in Django ORM with model definitions, querysets, and admin integration. Best for Django projects. | Included with Django | CLI shell-out: `python manage.py shell`, `python manage.py dbshell` |

### Database CLIs & Inspection (plan/verify)

| Tool | What it does | Install | Integration |
|------|-------------|---------|-------------|
| [psql](https://www.postgresql.org/docs/current/app-psql.html) | PostgreSQL interactive terminal. Query, inspect schemas (`\dt`, `\d+`), manage databases. The standard Postgres CLI. | Included with PostgreSQL | CLI shell-out: `psql -c "SELECT ..."` |
| [mysql](https://dev.mysql.com/doc/refman/en/mysql.html) | MySQL command-line client. Query execution, schema inspection, database administration. | Included with MySQL | CLI shell-out: `mysql -e "SHOW TABLES"` |
| [sqlite3](https://www.sqlite.org/cli.html) | SQLite command-line shell. Dot-commands for schema inspection (`.tables`, `.schema`), query execution. | Included with SQLite / OS | CLI shell-out: `sqlite3 db.sqlite ".tables"` |
| [mongosh](https://www.mongodb.com/docs/mongodb-shell/) | Modern MongoDB shell. JavaScript-based, query execution, collection inspection, aggregation pipelines. | `npm install -g mongosh` | CLI shell-out: `mongosh --eval "db.collection.find()"` |
| [PostgreSQL MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres) | Anthropic's official Postgres MCP server. Read-only schema inspection and SELECT queries directly from Claude. | `npm install @modelcontextprotocol/server-postgres` | MCP server (read-only); add to `.mcp.json` |
| [Supabase MCP](https://supabase.com/docs/guides/getting-started/mcp) | Official Supabase MCP server (v0.7.0, March 2026). 20+ tools for database, auth, storage, edge functions. 832k+ downloads since April 2025 launch. | `npx supabase mcp` | MCP server; OAuth 2.1 auth (cloud-hosted since Oct 2025). Dev/test only -- never connect to production. |

### Schema Visualization (plan)

| Tool | What it does | Install | Integration |
|------|-------------|---------|-------------|
| [SchemaSpy](https://schemaspy.org/) | Java CLI that analyzes database metadata and generates browsable HTML/SVG entity-relationship diagrams. Supports 12+ database types. | `java -jar schemaspy.jar` (or Docker) | CLI shell-out: `java -jar schemaspy.jar -t pgsql -db mydb` |
| [dbdiagram.io](https://dbdiagram.io/) | Web tool using DBML DSL for quick schema visualization. Export DDL for multiple engines. | Browser-based; DBML CLI: `npm install -g @dbml/cli` | CLI shell-out: `dbml2sql schema.dbml`; Claude can generate DBML from schema descriptions |
| [tbls](https://github.com/k1LoW/tbls) | CLI tool that generates database documentation (Markdown, PlantUML, Mermaid) from live databases. | `brew install k1LoW/tap/tbls` | CLI shell-out: `tbls doc postgres://...` |

### Query Analyzers (verify)

| Tool | What it does | Install | Integration |
|------|-------------|---------|-------------|
| [EXPLAIN / EXPLAIN ANALYZE](https://www.postgresql.org/docs/current/sql-explain.html) | Built-in PostgreSQL query plan analysis. Shows execution plan, actual timing, row estimates vs actuals. | Built into PostgreSQL | CLI shell-out: `psql -c "EXPLAIN ANALYZE SELECT ..."` |
| [pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html) | PostgreSQL extension tracking execution statistics for all queries -- time, calls, rows, I/O. Essential for production query analysis. | Enable in `postgresql.conf` | CLI shell-out: query via `psql -c "SELECT * FROM pg_stat_statements ORDER BY total_exec_time DESC"` |
| [pg_stat_monitor](https://github.com/percona/pg_stat_monitor) | Percona's enhanced alternative to pg_stat_statements. Includes actual query plans and more detailed grouping. PostgreSQL 14+. | Enable in `postgresql.conf` | CLI shell-out: query via psql |
| [auto_explain](https://www.postgresql.org/docs/current/auto-explain.html) | Logs execution plans for slow queries automatically in production. No application code changes needed. | Enable in `postgresql.conf` | Configuration-based; Claude can analyze log output |

---

## API Development

### API Testing & HTTP Clients (verify)

| Tool | What it does | Install | Integration |
|------|-------------|---------|-------------|
| [curl](https://curl.se/) | The universal HTTP client. Available everywhere, supports every protocol. Verbose but complete. | Pre-installed on most systems | CLI shell-out: `curl -X POST -H "Content-Type: application/json" -d '{}' http://...` |
| [HTTPie](https://httpie.io/) | Modern, human-readable HTTP client for the terminal. Intuitive syntax, colorized output, JSON support by default. Free and open-source CLI. | `pip install httpie` or `brew install httpie` | CLI shell-out: `http POST api.example.com/users name=John` |
| [Bruno](https://www.usebruno.com/) | Open-source API client storing collections as plain-text `.bru` files on your filesystem. Git-friendly, no cloud sync, no account required. | `npm install -g @usebruno/cli` | CLI shell-out: `bru run --env production`; collections commit to Git alongside code |
| [Newman](https://github.com/postmanlabs/newman) | Postman collection runner for the command line. Run Postman collections in CI/CD pipelines. | `npm install -g newman` | CLI shell-out: `newman run collection.json -e environment.json` |

### API Documentation (plan/implement)

| Tool | What it does | Install | Integration |
|------|-------------|---------|-------------|
| [Redocly CLI](https://redocly.com/docs/cli) | All-in-one OpenAPI utility: lint, bundle, preview, and generate docs. Supports OpenAPI 3.2/3.1/3.0/2.0, AsyncAPI 3.0, Arazzo 1.0. Replaced the deprecated swagger-cli. | `npm install -g @redocly/cli` | CLI shell-out: `redocly lint openapi.yaml`, `redocly build-docs openapi.yaml` |
| [Redoc](https://redocly.com/docs/redoc) | Open-source three-panel API documentation renderer from OpenAPI specs. Beautiful, responsive output. | `npm install redoc-cli` | CLI shell-out: `redoc-cli build openapi.yaml` |
| [GraphQL Inspector](https://the-guild.dev/graphql/inspector) | Schema diffing, breaking change detection, coverage analysis, and document validation for GraphQL. Modular CLI -- install only what you need. | `npm install @graphql-inspector/cli` | CLI shell-out: `graphql-inspector diff old.graphql new.graphql`, `graphql-inspector validate documents/*.graphql schema.graphql` |

### API Mocking (implement/verify)

| Tool | What it does | Install | Integration |
|------|-------------|---------|-------------|
| [Prism](https://stoplight.io/open-source/prism) | CLI mock server that generates responses from OpenAPI v2/v3 specs. Validates requests against the spec automatically. | `npm install -g @stoplight/prism-cli` | CLI shell-out: `prism mock openapi.yaml` (serves on localhost:4010) |
| [Mock Service Worker (MSW)](https://mswjs.io/) | API mocking library that intercepts network requests at the browser/Node.js level using Service Workers. Industry standard for JS testing. | `npm install msw` | Code-level integration; used in test suites with Vitest/Jest |
| [json-server](https://github.com/typicode/json-server) | Zero-config REST API from a JSON file. Instant fake server for prototyping. | `npm install -g json-server` | CLI shell-out: `json-server db.json` |
| [WireMock](https://wiremock.org/) | Heavyweight API mock/stub server for JVM ecosystems. Standalone server or JUnit integration. Enterprise-grade. | `docker run -p 8080:8080 wiremock/wiremock` or Java jar | CLI shell-out: `java -jar wiremock-standalone.jar` |

---

## Testing Frameworks

### Unit & Integration Testing (verify)

| Tool | What it does | Install | Integration |
|------|-------------|---------|-------------|
| [Vitest](https://vitest.dev/) | Fast test runner for Vite projects. Native ESM/TypeScript, 4x faster cold runs and 30% less memory than Jest. 400% adoption growth in 2023-2024. | `npm install -D vitest` | CLI shell-out: `npx vitest run`, `npx vitest --reporter=verbose` |
| [Jest](https://jestjs.io/) | Established JavaScript testing framework. 35M+ weekly downloads, massive ecosystem. Required for React Native. | `npm install -D jest` | CLI shell-out: `npx jest --verbose`, `npx jest --coverage` |
| [pytest](https://pytest.org/) | The dominant Python testing framework. Rich plugin ecosystem, fixtures, parametrize, assertion introspection. | `pip install pytest` | CLI shell-out: `pytest -v`, `pytest --tb=short` |
| [unittest](https://docs.python.org/3/library/unittest.html) | Python's built-in test framework. No install needed; xUnit-style with class-based test organization. | Built into Python | CLI shell-out: `python -m unittest discover` |
| [RSpec](https://rspec.info/) | BDD testing framework for Ruby. Expressive DSL, rich matchers, widely used with Rails. | `gem install rspec` | CLI shell-out: `rspec --format documentation` |
| [JUnit 5](https://junit.org/junit5/) | Standard Java testing framework. Annotations, parameterized tests, extensions. | Maven/Gradle dependency | CLI shell-out: `mvn test`, `gradle test` |
| [xUnit.net](https://xunit.net/) | Modern .NET testing framework. Clean, extensible, used by the .NET team itself. | `dotnet add package xunit` | CLI shell-out: `dotnet test --verbosity normal` |
| [Go testing](https://pkg.go.dev/testing) | Go's built-in test package. Table-driven tests, benchmarks, subtests. No external dependency needed. | Built into Go | CLI shell-out: `go test ./... -v`, `go test -bench=.` |

### API & E2E Testing (verify)

| Tool | What it does | Install | Integration |
|------|-------------|---------|-------------|
| [Supertest](https://github.com/ladjs/supertest) | HTTP assertion library for Node.js. Test Express/Fastify/Koa endpoints without starting a server. Pairs with Jest or Vitest. | `npm install -D supertest` | Code-level integration; run via `npx vitest` or `npx jest` |
| [httpx](https://www.python-httpx.org/) | Modern Python HTTP client with async support. Used for API testing with pytest. Drop-in replacement for requests with HTTP/2 support. | `pip install httpx` | Code-level integration; run via `pytest` |
| [requests](https://docs.python-requests.org/) | The most popular Python HTTP library. Simple API for making HTTP requests in test scripts. | `pip install requests` | Code-level integration; run via `pytest` |
| [REST Assured](https://rest-assured.io/) | Java DSL for REST API testing. v6.0.0 (December 2025) requires Java 17+, supports Spring 7 + Jackson 3. | Maven/Gradle dependency | CLI shell-out: `mvn test` (tests written as JUnit) |

### Load & Performance Testing (verify)

| Tool | What it does | Install | Integration |
|------|-------------|---------|-------------|
| [k6](https://k6.io/) | Developer-friendly load testing tool by Grafana Labs (29.9k GitHub stars). Tests written in JavaScript/TypeScript. v1.0 (May 2025) added native TS, extension framework. v1.6.1 released Feb 2026. | `brew install k6` or `go install go.k6.io/k6@latest` | CLI shell-out: `k6 run script.js --vus 50 --duration 30s` |
| [Locust](https://locust.io/) | Python-based load testing with code-defined user behavior. Distributed, scalable, web UI for monitoring. 27.5k GitHub stars. | `pip install locust` | CLI shell-out: `locust -f locustfile.py --headless -u 100 -r 10` |
| [Artillery](https://www.artillery.io/) | YAML-defined load testing for HTTP, WebSocket, Socket.io. Quick setup, CI/CD friendly. | `npm install -g artillery` | CLI shell-out: `artillery run scenario.yml`, `artillery quick --count 100 -n 50 http://localhost:3000` |
| [autocannon](https://github.com/mcollina/autocannon) | Fast HTTP/1.1 benchmarking tool for Node.js. Produces more load than wrk. Both CLI and programmatic API. | `npm install -g autocannon` | CLI shell-out: `autocannon -c 100 -d 10 http://localhost:3000` |

---

## Security Scanning (verify)

### Dependency Scanning

| Tool | What it does | Install | Integration |
|------|-------------|---------|-------------|
| [npm audit](https://docs.npmjs.com/cli/commands/npm-audit) | Built-in Node.js dependency vulnerability scanner. Checks packages against the npm advisory database. | Included with npm | CLI shell-out: `npm audit`, `npm audit fix` |
| [Snyk](https://snyk.io/) | Developer security platform covering SCA, SAST, containers, and IaC. Monitors 15M+ packages, provides fix PRs, reachability analysis. Proprietary vulnerability database. | `npm install -g snyk` | CLI shell-out: `snyk test`, `snyk monitor`; also available as MCP server |
| [Socket](https://socket.dev/) | Supply-chain threat detection at install time. Detects malicious packages, typosquatting, and install scripts. Pairs with Dependabot or Snyk. | `npm install -g socket` | CLI shell-out: `socket scan`; GitHub App integration |
| [Dependabot](https://github.com/dependabot) | GitHub's built-in dependency management. Auto-detects vulnerable dependencies and creates fix PRs. Free for all GitHub repos. | Configure via `.github/dependabot.yml` | GitHub-native; Claude can review Dependabot PRs via `gh` CLI |
| [pip-audit](https://github.com/pypa/pip-audit) | Python dependency vulnerability scanner using the OSV database. Official PyPA project. | `pip install pip-audit` | CLI shell-out: `pip-audit` |

### Static Analysis (SAST)

| Tool | What it does | Install | Integration |
|------|-------------|---------|-------------|
| [Semgrep](https://semgrep.dev/) | Fast, open-source SAST with YAML rules that mirror source code syntax. 30+ languages, thousands of pre-written checks. Scans in 10-30 seconds. Used by Dropbox, Figma, Snowflake, HashiCorp. | `pip install semgrep` or `brew install semgrep` | **Plugin** (MCP + hooks + skills): Semgrep Claude Code plugin bundles scanning into every file Claude generates. Also CLI shell-out: `semgrep scan --config=auto` |
| [CodeQL](https://codeql.github.com/) | GitHub's query-based SAST engine. Write custom queries to inspect code behavior across multiple languages. Free for public repos; private repos require GitHub Advanced Security. | `gh codeql` (via GitHub CLI extension) | CLI shell-out: `codeql database create`, `codeql database analyze`; GitHub Actions integration |
| [Bandit](https://bandit.readthedocs.io/) | Python-specific security linter with 47 built-in checks. Finds common security issues in Python source files. Outputs SARIF for GitHub code scanning. | `pip install bandit` | CLI shell-out: `bandit -r ./src` |
| [Brakeman](https://brakemanscanner.org/) | Ruby on Rails security scanner. Static analysis for Rails-specific vulnerabilities. v8.0.3 released February 2026. | `gem install brakeman` | CLI shell-out: `brakeman -A` |
| [SonarQube](https://www.sonarqube.org/) | Comprehensive code quality and security platform. 30+ languages, quality gates, technical debt tracking. Community and commercial editions. | Docker: `docker run sonarqube` | CLI shell-out: `sonar-scanner`; analyzes on CI push |
| [gosec](https://github.com/securego/gosec) | Go security checker. Inspects Go source for security problems. Produces SARIF output. | `go install github.com/securego/gosec/v2/cmd/gosec@latest` | CLI shell-out: `gosec ./...` |

### Secret Detection

| Tool | What it does | Install | Integration |
|------|-------------|---------|-------------|
| [Gitleaks](https://gitleaks.io/) | Fast regex-based secret scanner for Git repos. Best as a pre-commit hook -- blocks secrets in milliseconds. Lightweight and simple. | `brew install gitleaks` or `go install github.com/gitleaks/gitleaks/v8@latest` | CLI shell-out: `gitleaks detect`; Hook: pre-commit hook for automatic scanning |
| [TruffleHog](https://trufflesecurity.com/trufflehog) | Deep secret scanner that verifies whether detected credentials are still active. 800+ secret types. Scans Git, S3, Docker, Slack. | `brew install trufflehog` or `pip install trufflehog` | CLI shell-out: `trufflehog git file://.`; best in CI/CD for depth |
| [detect-secrets](https://github.com/Yelp/detect-secrets) | Yelp's baseline-driven secret scanner. Lower false positive rates via curated approach. Focuses on preventing new secret exposure. | `pip install detect-secrets` | CLI shell-out: `detect-secrets scan`, `detect-secrets audit .secrets.baseline` |

**Recommended combo:** Gitleaks pre-commit for speed, TruffleHog in CI/CD for depth.

---

## Monitoring & Observability (verify)

Tools for verifying backend behavior in development and staging environments.

### Log Analysis

| Tool | What it does | Install | Integration |
|------|-------------|---------|-------------|
| [pino](https://getpino.io/) | High-performance Node.js JSON logger. Structured output ideal for machine parsing. Pairs with pino-pretty for development. | `npm install pino` | Code-level integration; `pino-pretty` for CLI-readable output |
| [structlog](https://www.structlog.org/) | Structured logging for Python. Key-value pairs, processors, integration with stdlib logging. | `pip install structlog` | Code-level integration; structured JSON output for analysis |
| [jq](https://jqlang.github.io/jq/) | Lightweight CLI JSON processor. Essential for parsing structured log output, API responses, and configuration files. | `brew install jq` or `apt install jq` | CLI shell-out: `cat logs.json \| jq '.level == "error"'` |
| [lnav](https://lnav.org/) | Log file navigator for the terminal. Auto-detects log formats, SQL queries on log data, timeline view. | `brew install lnav` | CLI shell-out: `lnav /var/log/app.log` |

### Health Check & Uptime

| Tool | What it does | Install | Integration |
|------|-------------|---------|-------------|
| [wait-on](https://github.com/jeffbski/wait-on) | CLI utility that waits for files, ports, HTTP(s) resources. Essential for CI/CD: wait for server before running tests. | `npm install -g wait-on` | CLI shell-out: `wait-on http://localhost:3000 && npm test` |
| [healthcheck (Docker)](https://docs.docker.com/reference/dockerfile/#healthcheck) | Docker's built-in health check directive. Verifies container readiness via CLI commands. | Built into Docker | Dockerfile directive; Claude can generate and verify HEALTHCHECK instructions |
| [curl health checks](https://curl.se/) | Simple HTTP health check via curl. Universal, zero-dependency health verification. | Pre-installed on most systems | CLI shell-out: `curl -f http://localhost:3000/health` |

### Metrics & Tracing (reference)

These are typically production infrastructure rather than CLI tools, but Claude Code can help configure and verify their setup:

| Tool | What it does | Install | Integration |
|------|-------------|---------|-------------|
| [Prometheus](https://prometheus.io/) | Open-source metrics collection and alerting. CNCF graduated project, de facto standard for Kubernetes monitoring. | Docker or binary | Claude can generate `prometheus.yml` config and verify metrics endpoints |
| [Grafana](https://grafana.com/) | Multi-platform visualization for metrics, logs, and traces. Sits on top of Prometheus, Loki, and many other data sources. | Docker or binary | Claude can generate dashboard JSON and datasource configurations |
| [OpenTelemetry](https://opentelemetry.io/) | Vendor-neutral instrumentation framework for traces, metrics, and logs. The emerging standard for observability. | Language-specific SDKs | Claude can add OTel instrumentation to application code |

---

## MCP Servers Summary

Tools with dedicated MCP servers that give Claude Code direct access (beyond CLI shell-out):

| MCP Server | Purpose | Install |
|------------|---------|---------|
| [PostgreSQL MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/postgres) | Read-only schema inspection and queries | `npm install @modelcontextprotocol/server-postgres` |
| [Supabase MCP](https://supabase.com/docs/guides/getting-started/mcp) | Full Supabase backend (DB, auth, storage, functions) | `npx supabase mcp` |
| [Semgrep Plugin](https://semgrep.dev/docs/mcp) | Security scanning on every generated file | MCP + hooks + skills bundle |
| [GitHub MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/github) | Issues, PRs, repo search, workflow automation | `npm install @modelcontextprotocol/server-github` |

---

## Sources

- [Claude Code MCP Documentation](https://code.claude.com/docs/en/mcp)
- [Fastify vs Express vs Hono -- Better Stack](https://betterstack.com/community/guides/scaling-nodejs/fastify-vs-express-vs-hono/)
- [Node.js Application Servers in 2026 -- DeployHQ](https://www.deployhq.com/blog/node-application-servers-in-2025-from-express-to-modern-solutions)
- [Flask vs FastAPI vs Django 2026 -- WebAndCrafts](https://webandcrafts.com/blog/django-vs-flask-vs-fastapi)
- [Python Framework Comparison 2026 -- DasRoot](https://dasroot.net/posts/2026/02/python-flask-fastapi-django-framework-comparison-2026/)
- [Go Web Frameworks Comparison 2026 -- DEV Community](https://dev.to/mahdi0shamlou/go-web-frameworks-comparison-2026-top-5-picks-gin-fiber-echo-chi-beego-mahdi-shamlo-57d4)
- [Best Go Backend Frameworks 2026 -- Encore](https://encore.dev/articles/best-go-backend-frameworks)
- [12 Best Backend Frameworks 2026 -- Index.dev](https://www.index.dev/blog/best-backend-frameworks-ranked)
- [Drizzle vs Prisma 2026 -- Bytebase](https://www.bytebase.com/blog/drizzle-vs-prisma/)
- [Prisma vs Drizzle Performance -- Design Revision](https://designrevision.com/blog/prisma-vs-drizzle)
- [Best Node.js ORMs 2025 -- Nihar Daily](https://www.nihardaily.com/173-the-best-nodejs-orms-in-2025-a-brutally-honest-review)
- [Top 5 ORMs for Developers 2026 -- Strapi](https://strapi.io/blog/orms-for-developers)
- [Redocly CLI -- GitHub](https://github.com/Redocly/redocly-cli)
- [GraphQL Inspector -- The Guild](https://the-guild.dev/graphql/inspector)
- [MSW Comparison -- Mock Service Worker](https://mswjs.io/docs/comparison/)
- [10 Best API Testing Tools 2025 -- DEV Community](https://dev.to/_d7eb1c1703182e3ce1782/10-best-free-api-testing-tools-in-2025-postman-alternatives-included-583d)
- [Bruno GitHub](https://github.com/usebruno/bruno)
- [Vitest vs Jest -- Better Stack](https://betterstack.com/community/guides/scaling-nodejs/vitest-vs-jest/)
- [Load Testing Tools 2026 -- Vervali](https://www.vervali.com/blog/best-load-testing-tools-in-2026-definitive-guide-to-jmeter-gatling-k6-loadrunner-locust-blazemeter-neoload-artillery-and-more/)
- [k6 vs Artillery vs Locust PoC -- Medium](https://medium.com/@dorangao/load-testing-poc-k6-vs-artillery-vs-locust-vs-gatling-node-js-express-target-f056094ffbef)
- [Snyk vs Semgrep 2026 -- DEV Community](https://dev.to/rahulxsingh/snyk-vs-semgrep-sca-platform-vs-custom-sast-rules-in-2026-3047)
- [Best SAST Tools 2026 -- AppSec Santa](https://appsecsanta.com/sast-tools)
- [TruffleHog vs Gitleaks -- Jit](https://www.jit.io/resources/appsec-tools/trufflehog-vs-gitleaks-a-detailed-comparison-of-secret-scanning-tools)
- [Best Secret Scanning Tools 2026 -- SentinelOne](https://www.sentinelone.com/cybersecurity-101/cloud-security/secret-scanning-tools/)
- [Code Security MCP Servers -- DEV Community](https://dev.to/grove_chatforest/code-security-mcp-servers-snyk-sonarqube-semgrep-trivy-codeql-and-beyond-4nln)
- [Semgrep Plugin MCP Docs](https://semgrep.dev/docs/mcp)
- [Supabase MCP Docs](https://supabase.com/docs/guides/getting-started/mcp)
- [15 Best Observability Tools 2026 -- Spacelift](https://spacelift.io/blog/observability-tools)
- [Top 10 Open Source Monitoring Tools 2026 -- OpenObserve](https://openobserve.ai/blog/top-10-open-source-monitoring-tools/)
- [PostgreSQL EXPLAIN Tools -- Bytebase](https://www.bytebase.com/blog/top-open-source-postgres-explain-tool/)
- [pg_stat_statements Documentation](https://www.postgresql.org/docs/current/pgstatstatements.html)
- [50+ Best MCP Servers for Claude Code 2026 -- ClaudeFast](https://claudefa.st/blog/tools/mcp-extensions/best-addons)
