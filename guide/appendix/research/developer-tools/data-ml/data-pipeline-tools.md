---
id: b3432143-1a99-4dda-9971-da3d411a9568
title: Data & ML Pipeline Development Tools
domain: agenticdevelopercookbook://appendix/research/developer-tools/data-ml/data-pipeline-tools
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: Data & ML Pipeline Development Tools
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# Data & ML Pipeline Development Tools

**Date:** 2026-03-29
**Context:** Tools for data engineering and ML pipeline development, integrated with Claude Code.

This catalog covers best-in-class CLI tools for data and ML pipeline development, organized by category. Each entry notes the tool's loop phase (plan, implement, verify), install command, and integration method with Claude Code.

**Integration methods:**
- **CLI shell-out** -- Claude Code runs the tool via Bash (most common)
- **MCP server** -- tool exposes a Model Context Protocol server for direct integration
- **Hook** -- Claude Code pre/post-tool hook triggers the tool automatically
- **Plugin** -- Claude Code plugin bundles MCP + hooks + skills

---

## Data Validation (verify)

Tools that validate data schemas, values, and quality. Run during the verify phase to catch data issues before they propagate downstream.

### DataFrame & Schema Validation

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Great Expectations (GX)](https://greatexpectations.io/) | Full-featured data validation framework with 300+ built-in expectations. v1.15+ (March 2026). Define expectations as verifiable assertions, run them as Checkpoints against any data source. ExpectAI (Feb 2025) auto-suggests validation rules. Supports Pandas, Spark, SQL backends. | `pip install great-expectations` | CLI shell-out: `great_expectations checkpoint run`. Claude can generate expectation suites from schema descriptions and run validations. Heavy but comprehensive. |
| [Pandera](https://pandera.readthedocs.io/) | Type-safe DataFrame validation for Pandas, Polars, PySpark, and Ibis backends. v0.25+ adds Ibis support (Snowflake, BigQuery). Declarative schemas with mypy integration, statistical hypothesis testing (t-tests, chi-square), and built-in coercion. Leverages Polars lazy API for optimization. | `pip install pandera` | CLI shell-out via pytest. Claude can write Pandera schemas as Python dataclasses that double as documentation and validation. Lighter than GX for single-DataFrame checks. |
| [Pydantic](https://docs.pydantic.dev/) | The most widely used Python data validation library. v2.12+ with Rust-powered core for speed. Validates arbitrary Python objects via type hints. Strict and lax modes. Powers FastAPI, LangChain, and most modern Python frameworks. | `pip install pydantic` | Claude generates Pydantic models directly from data descriptions. Use for API payloads, config files, and row-level record validation. Not DataFrame-native -- pair with Pandera for tabular data. |
| [Cerberus](https://docs.python-cerberus.org/) | Lightweight, extensible dictionary/document validation. Schema-driven with custom rules. Good for validating JSON configs, API payloads, and YAML-derived dicts. Less opinionated than Pydantic. | `pip install cerberus` | CLI shell-out via Python scripts. Best for projects that need simple dict validation without full Pydantic adoption. Claude can generate Cerberus schemas from sample documents. |

### SQL & dbt Validation

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [dbt tests](https://docs.getdbt.com/docs/build/data-tests) | Built-in data tests for dbt models: `unique`, `not_null`, `accepted_values`, `relationships`. Run with every `dbt build` or `dbt test`. The foundation of SQL-layer data quality. | `pip install dbt-core dbt-<adapter>` | CLI shell-out: `dbt test`, `dbt build`. Claude can add test blocks to YAML schema files. Every dbt model should have at minimum `unique` and `not_null` on its primary key. |
| [dbt-expectations](https://github.com/calogica/dbt-expectations) | Port of Great Expectations patterns to dbt macros. 60+ tests covering schema validation, regex, time-series freshness, statistical distributions, outlier detection, and cross-column logic. Maintained by Datadog. | Add to `packages.yml`: `calogica/dbt_expectations` | CLI shell-out: `dbt deps && dbt test`. Claude can select appropriate expectation macros given a column description. Extends dbt tests without leaving the dbt ecosystem. |
| [Soda](https://soda.io/) | Data quality platform with open-source CLI (Soda Core) and commercial cloud. SodaCL provides 50+ built-in checks in a YAML-based DSL. v4.0 (Jan 2026) adds AI-assisted check generation. Works with any SQL warehouse. | `pip install soda-core-<adapter>` | CLI shell-out: `soda scan`. Claude can author SodaCL YAML check files. Good for teams that want data quality monitoring without adopting dbt or GX. |

---

## Notebook Tooling (implement/verify)

Tools for managing Jupyter notebooks in professional development workflows: version control, linting, conversion, and parameterized execution.

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [nbstripout](https://github.com/kynan/nbstripout) | Git filter that strips cell outputs and metadata from notebooks before commit. Keeps diffs clean and prevents large binary outputs from bloating the repo. Install once per repo as a git filter. | `pip install nbstripout && nbstripout --install` | Hook: install as a git pre-commit filter. Claude should recommend this in any project with notebooks in version control. Zero ongoing maintenance once installed. |
| [nbqa](https://github.com/nbQA-dev/nbQA) | Run any Python linter or formatter on Jupyter notebooks. Supports ruff, black, isort, mypy, pyright, and custom tools. Extracts code cells, runs the tool, and reinjects results. | `pip install nbqa` | CLI shell-out: `nbqa ruff notebooks/`, `nbqa black notebooks/`. Claude can lint notebooks the same way it lints `.py` files. Pair with ruff for fast notebook linting. |
| [jupytext](https://jupytext.readthedocs.io/) | Bidirectional sync between `.ipynb` and plain-text formats (`.py`, `.md`, `.Rmd`). Edit notebooks as scripts, review diffs as code. Supports percent format, light format, and MyST Markdown. | `pip install jupytext` | CLI shell-out: `jupytext --to py:percent notebook.ipynb`. Claude can work with the `.py` version directly -- no JSON parsing needed. Best practice: pair jupytext with nbstripout. |
| [papermill](https://papermill.readthedocs.io/) | Parameterized notebook execution. Inject parameters into tagged cells and execute notebooks programmatically. Produces output notebooks with full execution results. Used in production ML pipelines at Netflix. | `pip install papermill` | CLI shell-out: `papermill input.ipynb output.ipynb -p param_name value`. Claude can build parameterized report pipelines. Excellent for experiment sweeps and scheduled reporting. |
| [nbconvert](https://nbconvert.readthedocs.io/) | Convert notebooks to HTML, PDF, LaTeX, Markdown, Python scripts, and more. v7.17 (2026). Can also execute notebooks during conversion. Supports custom Jinja2 templates. | `pip install nbconvert` | CLI shell-out: `jupyter nbconvert --to html notebook.ipynb`. Claude can generate documentation from executed notebooks. Use `--execute` flag to run-and-convert in one step. |
| [nbformat](https://nbformat.readthedocs.io/) | Programmatic notebook manipulation library. Create, modify, and validate `.ipynb` files from Python. The canonical API for notebook structure -- more stable than parsing JSON directly. | `pip install nbformat` | Claude can use nbformat via Python scripts to generate notebooks programmatically, inject cells, or validate notebook structure. Use when building notebook templates or CI checks. |

---

## Pipeline Orchestration & Testing (verify)

Testing utilities for the major pipeline orchestration frameworks. Each framework has its own testing patterns for validating DAG structure, task logic, and end-to-end pipeline behavior.

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Airflow test utils](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html) | DagBag import validation, `dag.test()` for local execution, task-level unit tests with pytest. Airflow 3.0 (April 2025) improved local dev experience. DagBag checks catch import errors; `dag.test()` supports regex-based task skipping for sensor bypass. | `pip install apache-airflow` | CLI shell-out: `airflow dags test <dag_id> <date>`, `pytest tests/`. Claude can write DagBag validation tests and task-level unit tests. Always test DAG imports first -- catches most common errors. |
| [Dagster testing](https://docs.dagster.io/guides/test) | First-class testing built into the framework. Test individual assets, ops, and resources with `materialize_to_memory()`. No external infrastructure needed. Components framework GA (Oct 2025), enhanced catalog in v1.7. Fastest local dev feedback loop of any orchestrator. | `pip install dagster dagster-webserver` | CLI shell-out: `dagster dev`, `pytest tests/`. Claude can write asset tests that validate output schemas inline. Dagster's testing story is its strongest differentiator -- recommend it for new projects. |
| [Prefect testing](https://docs.prefect.io/v3/how-to-guides/workflows/test-workflows) | `prefect_test_harness` context manager for testing flows against a temporary database. Call `.fn()` on tasks to test the underlying function directly. `disable_run_logger()` for clean test output. | `pip install prefect` | CLI shell-out: `pytest tests/`. Claude can write Prefect flow tests using the test harness fixture. Test tasks via `.fn()` to skip Prefect runtime overhead in unit tests. |
| [Luigi test helpers](https://luigi.readthedocs.io/) | Target-based testing: verify task output files exist and contain expected data. Tasks are plain Python classes testable with pytest. Idempotent design means completed tasks won't re-execute. Spotify no longer actively maintains Luigi; community-driven since ~2023. | `pip install luigi` | CLI shell-out: `pytest tests/`. Claude can write task tests that mock targets. Consider Luigi only for existing Luigi codebases -- for new projects, prefer Dagster or Prefect. |
| [dbt test / dbt build](https://docs.getdbt.com/docs/build/data-tests) | Run data tests after model materialization. `dbt build` runs models + tests in dependency order. `dbt test --select model_name` for targeted testing. Integrates with dbt-expectations for advanced checks. | `pip install dbt-core dbt-<adapter>` | CLI shell-out: `dbt build`, `dbt test`. Claude can add schema tests to YAML files and run targeted test suites. The standard for SQL transformation testing. |

---

## Model Testing & Validation (verify)

Tools for validating ML models, detecting data drift, profiling data distributions, and property-based testing of data transformations.

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [pytest + Hypothesis](https://hypothesis.readthedocs.io/) | Property-based testing for Python. Generates random inputs matching a specification and finds edge cases automatically. Research shows property-based tests find ~50x more mutations than average unit tests. Actively maintained with regular releases through 2026. | `pip install hypothesis pytest` | CLI shell-out: `pytest tests/`. Claude can write Hypothesis strategies for data transformation functions -- e.g., testing that a cleaning function is idempotent or that schema invariants hold across random inputs. |
| [deepchecks](https://deepchecks.com/open-source/) | ML validation suite: 40+ built-in checks for data integrity, train/test comparison, model performance, and feature drift. Automated version comparisons and root cause analysis. Separate monitoring package for production. | `pip install deepchecks` | CLI shell-out via Python scripts or pytest. Claude can select appropriate check suites for a model type (tabular, NLP, vision) and generate validation scripts. Best for pre-deployment model validation gates. |
| [Evidently](https://www.evidentlyai.com/) | Data and model monitoring framework. Drift detection (dataset, feature, target), model performance tracking, and interactive HTML reports. Strong on interpretation and usability. Open-source core with hosted dashboard option. | `pip install evidently` | CLI shell-out via Python scripts. Claude can generate Evidently report configs for drift monitoring. Use in CI to compare current data distributions against a reference baseline. |
| [whylogs](https://whylabs.ai/whylogs) | Lightweight data profiling and logging. Creates statistical profiles of datasets (approximate histograms, cardinality, distributions) without storing raw data. Privacy-preserving by design. WhyLabs platform (open-sourced under Apache 2.0, Jan 2025) adds real-time monitoring. | `pip install whylogs` | CLI shell-out via Python scripts. Claude can add whylogs profiling to data pipeline steps. Profiles are small (~KB) and can be stored alongside model artifacts for lineage. |
| [MLflow model validation](https://mlflow.org/) | Model registry with validation workflows. Tag model versions with validation status, use aliases (champion/challenger) for deployment promotion. v3.0 extends to GenAI/agents. Integrates with Unity Catalog on Databricks. | `pip install mlflow` | CLI shell-out: `mlflow models serve`, `mlflow models predict`. Claude can write validation scripts that register models and set validation tags. The standard open-source model registry. |

---

## Data & SQL Linting (implement/verify)

Linters and formatters for SQL, Python, YAML, and type checking. Run during implement (auto-format on save) and verify (CI gate).

### SQL

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [SQLFluff](https://www.sqlfluff.com/) | Modular SQL linter and auto-formatter. Supports 20+ SQL dialects, Jinja templating, and dbt. Monthly releases. Configurable rules with `.sqlfluff` config file. The standard SQL linter for data teams. | `pip install sqlfluff` | CLI shell-out: `sqlfluff lint path/`, `sqlfluff fix path/`. Hook: run as pre-commit hook. Claude can fix SQL style issues and configure rules per project. Pair with dbt for templated SQL. |
| [sqlfmt](https://sqlfmt.com/) | Opinionated SQL formatter (not a linter). Zero config beyond line length. Powers the dbt Cloud IDE "Format" button. Lexer-based, not AST-based -- fast but less precise than SQLFluff for linting. | `pip install shandy-sqlfmt` | CLI shell-out: `sqlfmt path/`. Claude can use sqlfmt for quick formatting and SQLFluff for lint rules. They complement each other -- sqlfmt formats, SQLFluff lints. |

### Python

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Ruff](https://docs.astral.sh/ruff/) | Extremely fast Python linter and formatter, written in Rust. v0.15+ (March 2026). 800+ built-in rules replacing Flake8, Black, isort, pydocstyle, pyupgrade, and autoflake. 10-100x faster than the tools it replaces. The new default for Python projects. | `pip install ruff` | CLI shell-out: `ruff check .`, `ruff format .`. Hook: pre-commit or Claude Code hook for auto-format. Claude should default to Ruff for all Python linting/formatting. Use `ruff check --fix` for auto-fixable issues. |
| [mypy](https://mypy-lang.org/) | The original Python type checker. Reference implementation for the typing spec. v1.18+ brought ~40% speed improvements. Comprehensive but slower on large codebases. Best for CI pipelines where correctness matters more than speed. | `pip install mypy` | CLI shell-out: `mypy src/`. Claude can add type annotations and run mypy to verify. By default, mypy skips unannotated functions -- use `--strict` for full coverage. Pair with pyright or ty in the editor. |
| [Pyright](https://github.com/microsoft/pyright) | Fast Python type checker written in TypeScript. Powers Pylance in VS Code. 3-5x faster than mypy on large codebases. Checks all code regardless of annotations. Implements typing features ahead of other checkers. | `pip install pyright` | CLI shell-out: `pyright src/`. Claude can use Pyright for fast type checking during development and mypy for CI. Best IDE integration of any type checker via Pylance. |
| [ty](https://docs.astral.sh/ty/) | Astral's new Python type checker, written in Rust. Beta (Dec 2025). 10-60x faster than mypy/Pyright without caching. Built-in language server with code navigation, completions, and auto-import. From the makers of Ruff and uv. Astral joined OpenAI (Codex team) in March 2026. | `pip install ty` | CLI shell-out: `ty check src/`. Currently in beta -- watch for stable release in 2026. When stable, ty + Ruff + uv will form a complete Astral-powered Python toolchain. |

### Config Files

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [yamllint](https://yamllint.readthedocs.io/) | YAML linter checking syntax validity plus cosmetic issues (line length, trailing spaces, indentation, key repetition). v1.38 (2026). Configurable rules via `.yamllint` config. | `pip install yamllint` | CLI shell-out: `yamllint .`. Hook: pre-commit hook for YAML files. Claude should run yamllint on pipeline configs, dbt YAML files, and CI/CD definitions. Essential for data projects with heavy YAML usage. |

---

## Environment Management (implement)

Tools for creating reproducible Python and ML environments. Essential for ensuring consistent behavior across development, CI, and production.

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [uv](https://docs.astral.sh/uv/) | Extremely fast Python package manager and environment tool, written in Rust by Astral. Replaces pip, virtualenv, pyenv, and pip-tools in a single binary. 10-100x faster than pip. Handles Python version management, lockfiles, and virtual environments. The new default for Python projects in 2026. | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | CLI shell-out: `uv init`, `uv add <pkg>`, `uv run <script>`. Claude should default to uv for all new Python projects. Supports `pyproject.toml`, lockfiles, and build backends. Fastest path from zero to working environment. |
| [conda / mamba](https://docs.conda.io/) | Cross-language environment manager essential for ML workloads with C/C++/CUDA dependencies that pip cannot handle. Mamba is a C++ reimplementation with parallel downloads and faster solving. Most data science teams use mamba (or micromamba for containers) instead of base conda in 2026. | `conda install mamba -c conda-forge` or `brew install micromamba` | CLI shell-out: `mamba create -n env python=3.12 pytorch`, `mamba install <pkg>`. Use conda/mamba when GPU packages (PyTorch, TensorFlow, RAPIDS) or non-Python dependencies are needed. Use uv for pure-Python packages within a conda env. |
| [Poetry](https://python-poetry.org/) | Python dependency management with lockfile support and PyPI publishing. Mature, well-documented, large ecosystem. Still the smoothest workflow for library publishing to PyPI, though uv is catching up. | `pip install poetry` | CLI shell-out: `poetry add <pkg>`, `poetry install`, `poetry build`. Claude can manage Poetry projects. For new application projects, prefer uv; for library publishing, Poetry remains a strong choice. |
| [Docker](https://www.docker.com/) | Container-based environment isolation. The standard for reproducible ML environments in 2026, with 92% developer adoption. Docker Desktop 4.60+ adds GPU acceleration and tighter AI framework integration. 35% faster deployments and 50% fewer environment bugs in CI/CD pipelines. | `brew install --cask docker` (macOS) | CLI shell-out: `docker build`, `docker run`. Claude can generate Dockerfiles for ML workloads, multi-stage builds for smaller images, and docker-compose configs for multi-service pipelines. |
| [Dev Containers](https://containers.dev/) | Standardized development container specification. Define `.devcontainer/devcontainer.json` for reproducible, IDE-integrated environments. 64% of developers use non-local environments as primary setup in 2026 (up from 36% in 2024). | Add `.devcontainer/devcontainer.json` to repo | Claude can generate devcontainer configs with Python, Jupyter, and ML tooling pre-installed. Best for teams that need identical environments across all developers. Works with VS Code, GitHub Codespaces, and JetBrains. |

---

## Experiment Tracking (implement/verify)

Tools for logging experiments, tracking metrics, versioning models, and comparing runs. Used during implement (log metrics) and verify (compare results).

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [MLflow](https://mlflow.org/) | Open-source AI/ML platform. Experiment tracking, model registry, model serving, and evaluation. v3.0 extends to GenAI agents. Backed by Databricks. The open-source standard with the largest community. Unity Catalog integration for enterprise governance. | `pip install mlflow` | CLI shell-out: `mlflow ui`, `mlflow models serve`, `mlflow run .`. Claude can add MLflow tracking calls to training scripts, configure experiments, and query run results via the CLI. Best default choice for open-source experiment tracking. |
| [Weights & Biases (W&B)](https://wandb.ai/) | Developer-first experiment tracking with best-in-class visualization. Real-time dashboards, hyperparameter sweeps, artifact versioning, and team collaboration. Vertically integrated with CoreWeave GPU cloud. The default for teams prioritizing developer experience. | `pip install wandb` | CLI shell-out: `wandb login`, `wandb sweep`. Claude can add W&B logging to training loops and configure sweep configs. Superior visualization and collaboration features compared to MLflow. Commercial product with free tier. |
| [DVC](https://dvc.org/) | "Git for data" -- version control for datasets and models alongside code. Stores data in remote storage (S3, GCS, Azure) with lightweight pointer files in Git. DVCLive for experiment tracking. Acquired by lakeFS (Nov 2025), remains open source. | `pip install dvc` | CLI shell-out: `dvc init`, `dvc add data/`, `dvc push`, `dvc repro`. Claude can set up DVC pipelines for reproducible ML workflows. Best for teams that want data versioning tightly coupled with Git. |
| [ClearML](https://clear.ml/) | All-in-one open-source MLOps platform: experiment tracking, data versioning, pipeline orchestration, and model serving in one package. Auto-logs metrics, hyperparameters, model checkpoints, stdout, and system resources with minimal code changes. | `pip install clearml` | CLI shell-out: `clearml-init`, `clearml-task`. Claude can add ClearML auto-logging to existing training scripts (often just two lines). Best for teams that want a single platform instead of stitching together separate tools. |

**Note on Neptune.ai:** Neptune was acquired by OpenAI in late 2025 and is winding down its public service (no new sign-ups, shutdown by March 2026). Do not adopt Neptune for new projects. Existing Neptune users should migrate to MLflow, W&B, or ClearML.

---

## Feature Store & Data Catalog (plan)

Tools for managing feature engineering pipelines and discovering/governing data assets. Used during plan phase to understand what data exists and how it can be used.

### Feature Stores

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Feast](https://feast.dev/) | Open-source feature store for ML. Manages feature engineering pipelines, serves features for training and inference, and ensures consistency between offline (batch) and online (real-time) feature access. Community plugins for DataHub and Amundsen integration. | `pip install feast` | CLI shell-out: `feast init`, `feast apply`, `feast materialize`. Claude can define feature views and entity definitions. Best for teams that need a standardized feature serving layer without vendor lock-in. |

### Data Catalogs

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [DataHub](https://datahubproject.io/) | The most actively maintained open-source data catalog in 2026. Metadata platform with fine-grained lineage, governance, 70+ connectors, and a modern UI. Pre-release v1.4.0. Strong roadmap and large community. Recommended over alternatives for new projects. | Docker-based: `datahub docker quickstart` | Claude can query DataHub's REST/GraphQL API to discover datasets during planning. DataHub's lineage graph helps Claude understand data dependencies. Self-hosted; requires operational investment. |
| [Amundsen](https://www.amundsen.io/) | Open-source data catalog originally from Lyft. Search-based discovery with PageRank-style relevance. Integrates with Feast. **Caution:** No active roadmap as of 2025-2026; development has stagnated. Not recommended for new production deployments. | Docker-based: `docker-compose up` | Consider only if already invested in Amundsen. For new projects, choose DataHub or OpenMetadata instead. |
| [Apache Atlas](https://atlas.apache.org/) | Metadata management and governance for Apache Hadoop ecosystem. v2.4.0 (Jan 2025), v2.5.0 planned with Trino extractor and PostgreSQL backend. Integrates with Apache Ranger for access control. Best fit for Hadoop-native stacks. | Hadoop ecosystem deployment | Specialized for HBase/Solr/Kafka environments. If your stack is Snowflake, BigQuery, or Databricks, Atlas requires significant custom work. For non-Hadoop teams, prefer DataHub. |
| [OpenMetadata](https://open-metadata.org/) | Rising open-source metadata platform with 84+ connectors, data quality, lineage, and governance. Active development and growing community. Strong alternative to DataHub with a more modern UI. | Docker-based: `docker-compose up` | Claude can query OpenMetadata's API for data discovery. Consider alongside DataHub for new catalog deployments -- both are viable in 2026. |

---

## Claude Code Integration (all phases)

Tools and servers that connect Claude Code directly to data and ML infrastructure.

### MCP Servers

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| [Jupyter MCP Server](https://github.com/datalayer/jupyter-mcp-server) | MCP server for interacting with Jupyter notebooks in any JupyterLab environment. Real-time cell control, smart execution, instant visibility of changes, and automatic error recovery. | `pip install jupyter-mcp-server` | Add to `.mcp.json`. Claude can execute notebook cells, read outputs, and modify notebooks without leaving the conversation. Essential for interactive data exploration. |
| [PostgreSQL MCP](https://github.com/aftabbs/postgresql-mcp-server) | Query databases, inspect schemas, and assist with writing migrations. Claude translates natural language to SQL and explains results. Configurable read/write permissions. | Via `.mcp.json` config | Add to `.mcp.json` with connection string. Claude can explore database schemas during planning, write and test queries, and validate migration results. |
| [Supabase MCP](https://supabase.com/docs/guides/getting-started/mcp) | MCP server for Supabase projects. Query tables, manage auth, inspect storage, and work with edge functions. | Via `.mcp.json` config | Add to `.mcp.json`. Claude can interact with Supabase as a complete backend -- useful for ML-powered applications with Supabase as the data layer. |
| [SQLite MCP](https://github.com/ergut/sqlite-mcp-server) | Lightweight MCP server for SQLite databases. Read/write access, schema inspection, and query execution. Good for local development and testing. | Via `.mcp.json` config | Add to `.mcp.json`. Claude can use SQLite for local experiment databases, feature caching, and test fixtures. |

### Language Tooling

| Tool | What it does | Install | Notes |
|------|-------------|---------|-------|
| Python LSP (Pylance/Pyright) | Language server providing completions, type checking, go-to-definition, and refactoring for Python. Claude Code's built-in Python support uses these under the hood. | Included with Claude Code | Claude Code automatically uses Python language intelligence for navigation and refactoring. No additional setup needed. Enhanced by ty when it reaches stable. |
| [Ruff LSP](https://docs.astral.sh/ruff/editors/) | Ruff's built-in language server for real-time linting and formatting feedback. Integrated into VS Code, Neovim, and other editors. | `pip install ruff` (LSP built-in) | Claude Code can shell out to `ruff check` and `ruff format`. The LSP runs in the editor for real-time feedback. Both complement each other. |

### Claude Code Workflow Patterns

**Planning with data context:**
```bash
# Discover schema via MCP
# Claude reads database schemas, data catalog entries, and feature definitions
# to understand the data landscape before writing pipeline code
```

**Implementing with validation:**
```bash
# Claude writes pipeline code, then immediately validates:
ruff check src/pipeline/          # lint Python
sqlfluff lint models/             # lint SQL
yamllint configs/                 # lint YAML
dbt build --select model_name     # run model + tests
```

**Verifying with quality gates:**
```bash
# Run the full verification suite:
pytest tests/                     # unit + property-based tests
great_expectations checkpoint run # data validation
dbt test                          # SQL-layer tests
soda scan                         # data quality monitoring
evidently report                  # drift detection
```

---

## Sources

- [Great Expectations documentation](https://docs.greatexpectations.io/)
- [Pandera documentation](https://pandera.readthedocs.io/)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [Soda Core documentation](https://docs.soda.io/)
- [dbt documentation](https://docs.getdbt.com/)
- [dbt-expectations](https://github.com/calogica/dbt-expectations)
- [nbstripout](https://github.com/kynan/nbstripout)
- [nbqa](https://github.com/nbQA-dev/nbQA)
- [jupytext documentation](https://jupytext.readthedocs.io/)
- [papermill documentation](https://papermill.readthedocs.io/)
- [nbconvert documentation](https://nbconvert.readthedocs.io/)
- [Airflow best practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Dagster documentation](https://docs.dagster.io/)
- [Prefect testing guide](https://docs.prefect.io/v3/how-to-guides/workflows/test-workflows)
- [Hypothesis documentation](https://hypothesis.readthedocs.io/)
- [deepchecks](https://deepchecks.com/open-source/)
- [Evidently AI](https://www.evidentlyai.com/)
- [whylogs / WhyLabs](https://whylabs.ai/whylogs)
- [SQLFluff documentation](https://docs.sqlfluff.com/)
- [sqlfmt](https://github.com/tconbeer/sqlfmt)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [Pyright](https://github.com/microsoft/pyright)
- [ty documentation](https://docs.astral.sh/ty/)
- [yamllint documentation](https://yamllint.readthedocs.io/)
- [uv documentation](https://docs.astral.sh/uv/)
- [conda documentation](https://docs.conda.io/)
- [Poetry documentation](https://python-poetry.org/)
- [Dev Containers specification](https://containers.dev/)
- [MLflow documentation](https://mlflow.org/)
- [Weights & Biases](https://wandb.ai/)
- [DVC documentation](https://dvc.org/)
- [ClearML documentation](https://clear.ml/)
- [Feast documentation](https://docs.feast.dev/)
- [DataHub](https://datahubproject.io/)
- [OpenMetadata](https://open-metadata.org/)
- [Apache Atlas](https://atlas.apache.org/)
- [Jupyter MCP Server](https://github.com/datalayer/jupyter-mcp-server)
- [Python data validation landscape 2025](https://aeturrell.com/blog/posts/the-data-validation-landscape-in-2025/)
- [Airflow vs Dagster vs Prefect comparison 2026](https://bix-tech.com/airflow-vs-dagster-vs-prefect-which-workflow-orchestrator-should-you-choose-in-2026/)
- [Python package managers comparison 2026](https://scopir.com/posts/best-python-package-managers-2026/)
- [MLflow vs W&B vs Neptune comparison 2026](https://reintech.io/blog/mlflow-vs-weights-and-biases-vs-neptune-experiment-tracking-comparison)
- [Best MCP servers for Claude Code 2026](https://dev.to/raxxostudios/best-mcp-servers-for-claude-code-in-2026-5e6k)
