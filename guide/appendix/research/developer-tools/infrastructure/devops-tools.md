---
id: a7bf2e35-f66d-4dd2-a900-89c4edae6ef9
title: DevOps & Infrastructure Tools
domain: agenticdevelopercookbook://appendix/research/developer-tools/infrastructure/devops-tools
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: DevOps & Infrastructure Tools
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# DevOps & Infrastructure Tools

**Date:** 2026-03-29
**Context:** Infrastructure-as-code and DevOps tools that integrate with Claude Code for plan, implement, and verify workflows.

---

## Terraform & OpenTofu (plan/implement/verify)

### [TFLint](https://github.com/terraform-linters/tflint)
- **What:** Pluggable linter for Terraform and OpenTofu. Catches deprecated syntax, provider-specific errors, naming convention violations, and enforces best practices via rulesets.
- **Loop phase:** verify
- **Install:** `brew install tflint` / `choco install tflint` / `curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash`
- **Claude Code usage:** Run `tflint --init && tflint` after editing `.tf` files. Parse JSON output (`tflint -f json`) for structured feedback. Provider-specific plugins (e.g., `tflint-ruleset-aws`) catch cloud-specific mistakes.

### [Trivy (IaC scanning)](https://github.com/aquasecurity/trivy)
- **What:** Comprehensive security scanner that subsumes the former tfsec project. Scans Terraform, CloudFormation, Kubernetes manifests, Dockerfiles, and more for misconfigurations and CVEs. Trivy is the recommended successor to tfsec.
- **Loop phase:** verify
- **Install:** `brew install trivy` / `apt-get install trivy` / `curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh`
- **Claude Code usage:** Run `trivy config .` on IaC directories. Use `--severity HIGH,CRITICAL` to focus on actionable findings. JSON output (`trivy config -f json .`) enables structured analysis. Can also scan container images (`trivy image myapp:latest`).

### [terraform validate](https://developer.hashicorp.com/terraform/cli/commands/validate)
- **What:** Built-in Terraform command that checks configuration syntax and internal consistency (references, types, required attributes) without accessing remote state or providers.
- **Loop phase:** verify
- **Install:** Included with `terraform` CLI. `brew install terraform` / `brew install opentofu`
- **Claude Code usage:** Run `terraform init -backend=false && terraform validate` as a fast pre-flight check. Returns machine-readable JSON with `-json` flag. Should run before `tflint` or `trivy` to catch basic errors first.

### [terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan)
- **What:** Generates an execution plan showing what Terraform will create, modify, or destroy. Critical for reviewing infrastructure changes before apply.
- **Loop phase:** plan / verify
- **Install:** Included with `terraform` CLI.
- **Claude Code usage:** Run `terraform plan -out=tfplan` to generate a saved plan. Use `terraform show -json tfplan` to get machine-readable output for analysis. Claude Code can review the plan diff to catch unintended resource destruction or drift.

### [terraform-docs](https://github.com/terraform-docs/terraform-docs)
- **What:** Generates documentation from Terraform modules in various formats (Markdown, JSON, AsciiDoc). Auto-generates input/output tables and module descriptions.
- **Loop phase:** implement
- **Install:** `brew install terraform-docs` / `go install github.com/terraform-docs/terraform-docs@latest`
- **Claude Code usage:** Run `terraform-docs markdown table . > README.md` after module changes. Integrate as a pre-commit hook to keep docs in sync. Claude Code can verify generated docs match the actual module interface.

### [Checkov](https://github.com/bridgecrewio/checkov)
- **What:** Open-source static analysis tool by Bridgecrew with 1000+ built-in policies. Scans Terraform, CloudFormation, Kubernetes, Dockerfiles, Helm, Kustomize, Ansible, ARM, Bicep, and CI/CD workflow files (GitHub Actions, GitLab CI, Azure Pipelines, CircleCI). Context-aware graph-based scanning detects cross-resource issues.
- **Loop phase:** verify
- **Install:** `pip install checkov` / `brew install checkov`
- **Claude Code usage:** Run `checkov -d . --output json` for structured results. Use `--framework terraform` to scope scanning. Skip specific checks with `--skip-check CKV_AWS_123`. Claude Code can triage findings by severity and suggest fixes.

### [Infracost](https://github.com/infracost/infracost)
- **What:** Cloud cost estimation for Terraform. Shows cost impact of infrastructure changes before deployment. Supports AWS, Azure, GCP. Integrates with pull requests to show cost diffs.
- **Loop phase:** plan / verify
- **Install:** `brew install infracost` / `curl -fsSL https://raw.githubusercontent.com/infracost/infracost/master/scripts/install.sh | sh`
- **Claude Code usage:** Run `infracost breakdown --path .` for current cost estimate. Run `infracost diff --path .` to see cost delta from changes. JSON output (`--format json`) enables programmatic analysis. Requires API key (`infracost auth login`).

### [Terragrunt](https://github.com/gruntwork-io/terragrunt)
- **What:** Thin wrapper around Terraform/OpenTofu that keeps configurations DRY, manages remote state, and orchestrates multi-module deployments. Provides dependency management between modules and environment-specific variable injection.
- **Loop phase:** implement / verify
- **Install:** `brew install terragrunt` / `choco install terragrunt`
- **Claude Code usage:** Run `terragrunt validate-all` to check all modules. `terragrunt plan-all` previews changes across the dependency graph. `terragrunt hclfmt` formats Terragrunt HCL files for consistency.

### [OpenTofu](https://github.com/opentofu/opentofu)
- **What:** Community-driven, open-source fork of Terraform under the Linux Foundation. Drop-in compatible with Terraform 1.5.x. All major Terraform ecosystem tools (TFLint, Checkov, Infracost, Terragrunt) work with OpenTofu.
- **Loop phase:** all phases
- **Install:** `brew install opentofu` / `snap install opentofu`
- **Claude Code usage:** Same workflow as Terraform. Use `tofu init`, `tofu validate`, `tofu plan`, `tofu apply`. Claude Code should detect `*.tofu` or `opentofu` references and use the `tofu` binary accordingly.

---

## Docker & Containers (implement/verify)

### [Hadolint](https://github.com/hadolint/hadolint)
- **What:** Dockerfile linter written in Haskell. Checks Dockerfiles against best practices from the official Docker documentation and uses ShellCheck to lint `RUN` instruction shell code. Does not detect CVEs (use Trivy or Scout for that).
- **Loop phase:** verify
- **Install:** `brew install hadolint` / `scoop install hadolint` / `docker pull hadolint/hadolint`
- **Claude Code usage:** Run `hadolint Dockerfile` after any Dockerfile edit. Use `hadolint --format json Dockerfile` for structured output. Supports `.hadolint.yaml` config for custom rule severity and ignored rules.

### [Dive](https://github.com/wagoodman/dive)
- **What:** Interactive CLI tool for exploring Docker image layers. Visualizes filesystem changes per layer (green=added, yellow=modified, red=deleted), calculates wasted space, and identifies optimization opportunities.
- **Loop phase:** verify
- **Install:** `brew install dive` / `snap install dive` / download from GitHub releases
- **Claude Code usage:** Run `dive <image-tag>` for interactive analysis. For CI, set `CI=true dive <image-tag>` to get a pass/fail based on configurable thresholds (wasted space percentage, image efficiency). Build and analyze in one step: `dive build -t myapp:latest .`

### [Dockle](https://github.com/goodwithtech/dockle)
- **What:** Container image linter focused on security, based on CIS Docker Benchmarks. Scans built images (not Dockerfiles) for security issues like running as root, exposed secrets, and missing health checks.
- **Loop phase:** verify
- **Install:** `brew install goodwithtech/r/dockle` / download from GitHub releases
- **Claude Code usage:** Run `dockle <image-tag>` after building an image. Use `dockle --format json <image-tag>` for structured output. Complements Hadolint (which checks Dockerfiles) by checking the built image.

### [Docker Scout](https://docs.docker.com/scout/)
- **What:** Docker's built-in vulnerability scanning and supply chain security platform. Generates SBOMs, matches against CVE databases, provides EPSS scores (exploit probability), and supports policy-based evaluation.
- **Loop phase:** verify
- **Install:** Bundled with Docker Desktop 4.17+. Standalone: `curl -fsSL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh`
- **Claude Code usage:** Run `docker scout quickview <image>` for a summary. `docker scout cves <image> --only-severity critical,high` for actionable vulnerabilities. `docker scout cves <image> --only-fixed` to find fixable issues. SARIF export available for CI integration. Requires Docker Hub authentication.

### [Trivy (container scanning)](https://github.com/aquasecurity/trivy)
- **What:** Also scans container images for OS package and application dependency vulnerabilities. Comprehensive alternative to Docker Scout with broader ecosystem support.
- **Loop phase:** verify
- **Install:** Same as above (Trivy covers IaC and containers).
- **Claude Code usage:** Run `trivy image <image-tag>` for vulnerability scan. `trivy image --severity HIGH,CRITICAL <image-tag>` for focused results. `trivy image -f json <image-tag>` for structured output.

### [Snyk Container](https://snyk.io/product/container-vulnerability-management/)
- **What:** Commercial container vulnerability scanner with developer-focused remediation guidance. Provides base image upgrade recommendations and monitors running containers for new vulnerabilities.
- **Loop phase:** verify
- **Install:** `npm install -g snyk` / `brew install snyk`
- **Claude Code usage:** Run `snyk container test <image-tag>` for vulnerability scan. `snyk container monitor <image-tag>` for ongoing monitoring. Requires Snyk account and authentication (`snyk auth`).

### [docker compose](https://docs.docker.com/compose/)
- **What:** Tool for defining and running multi-container Docker applications via `compose.yaml`. Manages service dependencies, networks, volumes, and environment configuration.
- **Loop phase:** implement / verify
- **Install:** Bundled with Docker Desktop. Standalone: `apt-get install docker-compose-plugin`
- **Claude Code usage:** Run `docker compose config` to validate and resolve the compose file. `docker compose up -d` to start services. `docker compose ps` to verify running state. `docker compose logs <service>` to inspect output.

---

## CI/CD Linting & Validation (verify)

### [actionlint](https://github.com/rhysd/actionlint)
- **What:** Static checker for GitHub Actions workflow files. Validates YAML syntax against the GitHub Actions schema, checks expression types, verifies action input/output usage, detects script injection vulnerabilities, and validates reusable workflow references.
- **Loop phase:** verify
- **Install:** `brew install actionlint` / `go install github.com/rhysd/actionlint/cmd/actionlint@latest`
- **Claude Code usage:** Run `actionlint` in the repo root to check all `.github/workflows/*.yml` files. Use `actionlint -format '{{json .}}'` for structured output. Catches common mistakes like invalid `runs-on` values, incorrect `if` expressions, and deprecated action versions.

### [yamllint](https://github.com/adrienverge/yamllint)
- **What:** YAML linter that checks syntax, formatting, indentation, key duplication, line length, and trailing spaces. Works on any YAML file (CI configs, Kubernetes manifests, Ansible playbooks).
- **Loop phase:** verify
- **Install:** `pip install yamllint` / `brew install yamllint` / pre-installed on GitHub Actions Ubuntu runners
- **Claude Code usage:** Run `yamllint .` or `yamllint -d relaxed <file>`. Custom config via `.yamllint.yml`. Useful as a first-pass validator before domain-specific tools (actionlint, kubeval, ansible-lint).

### [circleci config validate](https://circleci.com/docs/how-to-use-the-circleci-local-cli/)
- **What:** CircleCI CLI command that validates `.circleci/config.yml` against the CircleCI schema. Catches syntax errors, invalid orb references, and misconfigured workflows.
- **Loop phase:** verify
- **Install:** `brew install circleci` / `curl -fLSs https://raw.githubusercontent.com/CircleCI-Public/circleci-cli/master/install.sh | bash`
- **Claude Code usage:** Run `circleci config validate` in the repo root. Also supports `circleci config process .circleci/config.yml` to expand orbs and see the resolved config.

### [Checkov (CI/CD scanning)](https://github.com/bridgecrewio/checkov)
- **What:** In addition to IaC, Checkov scans CI/CD configuration files for security issues: GitHub Actions, GitLab CI, Azure Pipelines, BitBucket Pipelines, CircleCI, and Argo Workflows. Detects insecure permissions, missing pinned versions, and credential exposure patterns.
- **Loop phase:** verify
- **Install:** Same as Terraform section.
- **Claude Code usage:** Run `checkov -d .github/ --framework github_actions` to scan only CI configs. Also works on `.gitlab-ci.yml`, `azure-pipelines.yml`, etc.

---

## Infrastructure Testing (verify)

### [Terratest](https://github.com/gruntwork-io/terratest)
- **What:** Go library for writing automated tests against real infrastructure. First-class support for Terraform, Packer, Docker, Kubernetes, AWS, GCP, Azure. Deploys real resources, validates behavior, then tears them down. End-to-end acceptance testing, not unit testing.
- **Loop phase:** verify
- **Install:** `go get github.com/gruntwork-io/terratest/modules/terraform` (Go module dependency)
- **Claude Code usage:** Run `go test -v -timeout 30m ./test/` in the test directory. Claude Code can generate Terratest boilerplate: deploy module, validate outputs, HTTP-check endpoints, then `defer terraform.Destroy()`. Tests are Go code, so standard Go tooling applies.

### [InSpec](https://github.com/inspec/inspec)
- **What:** Chef's infrastructure testing framework for security compliance and system state verification. Write human-readable tests ("describe" blocks) that assert properties of OS packages, files, services, ports, cloud resources, and more. Supports AWS, Azure, GCP resource packs.
- **Loop phase:** verify
- **Install:** `gem install inspec` / `brew install chef/chef/inspec` / Chef Workstation bundle
- **Claude Code usage:** Run `inspec exec <profile-path> -t ssh://user@host` for remote testing. `inspec exec <profile-path> -t aws://` for cloud resource compliance checks. JSON output: `inspec exec --reporter json`.

### [ServerSpec](https://serverspec.org/)
- **What:** Ruby-based RSpec framework for testing server state. Verifies packages, services, ports, files, commands, and users on remote servers via SSH. Predecessor to InSpec (simpler but less feature-rich).
- **Loop phase:** verify
- **Install:** `gem install serverspec`
- **Claude Code usage:** Run `rake spec` to execute all server specs. Tests live in `spec/<hostname>/` directories. Claude Code can generate spec files that verify expected server state after provisioning.

### [Test Kitchen](https://github.com/test-kitchen/test-kitchen)
- **What:** Ruby-based integration testing harness from the Chef ecosystem. Creates VMs or containers, converges configuration code, then runs test suites (InSpec, ServerSpec, BATS). Supports Vagrant, Docker, EC2, Azure, GCP drivers.
- **Loop phase:** verify
- **Install:** `gem install test-kitchen` / included in Chef Workstation
- **Claude Code usage:** Run `kitchen test` for full create-converge-verify-destroy cycle. `kitchen converge` to provision without testing. `kitchen verify` to run tests against existing instances. Config lives in `.kitchen.yml`.

### [Molecule](https://github.com/ansible/molecule)
- **What:** Testing framework for Ansible roles. Creates ephemeral instances (Docker, Podman, Vagrant, cloud providers), applies roles, then runs verification (Ansible assertions, Testinfra, InSpec). Supports multiple scenarios per role.
- **Loop phase:** verify
- **Install:** `pip install molecule` / `pip install molecule[docker]` for Docker driver
- **Claude Code usage:** Run `molecule test` for full create-converge-idempotence-verify-destroy cycle. `molecule converge` to apply the role. `molecule verify` to run tests. `molecule login` to SSH into the test instance for debugging.

### [BATS (Bash Automated Testing System)](https://github.com/bats-core/bats-core)
- **What:** TAP-compliant testing framework for Bash scripts. Each test case is a function with standard shell commands; all commands must exit 0 for the test to pass. Includes setup/teardown hooks. Helper libraries (bats-assert, bats-support) provide richer assertions.
- **Loop phase:** verify
- **Install:** `brew install bats-core` / `apt-get install bats` / `npm install -g bats`
- **Claude Code usage:** Run `bats test/*.bats` to execute tests. Claude Code can generate `.bats` files that test shell scripts, CLI tools, or infrastructure provisioning scripts. Useful for testing wrapper scripts around terraform, kubectl, etc.

---

## Kubernetes (implement/verify)

### [kubectl](https://kubernetes.io/docs/reference/kubectl/)
- **What:** Official Kubernetes CLI. Manages all cluster resources: pods, deployments, services, configmaps, secrets, etc. Supports declarative (`apply`) and imperative commands, dry-run validation, and JSON/YAML output.
- **Loop phase:** implement / verify
- **Install:** `brew install kubectl` / `curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/$(uname -s | tr A-Z a-z)/amd64/kubectl"`
- **Claude Code usage:** `kubectl apply --dry-run=server -f manifest.yaml` to validate without deploying. `kubectl diff -f manifest.yaml` to see what would change. `kubectl get pods -o json` for structured cluster state. `kubectl describe pod <name>` for debugging.

### [kubeconform](https://github.com/yannh/kubeconform)
- **What:** Fast Kubernetes manifest validator inspired by kubeval. Validates YAML/JSON against Kubernetes OpenAPI schemas with multi-goroutine processing. Supports CRD schema validation via configurable schema locations. Kubeval is deprecated; kubeconform is the recommended replacement.
- **Loop phase:** verify
- **Install:** `brew install kubeconform` / `go install github.com/yannh/kubeconform/cmd/kubeconform@latest`
- **Claude Code usage:** Run `kubeconform -summary manifests/` to validate all manifests. Use `-kubernetes-version 1.29.0` to target a specific cluster version. `-output json` for structured output. Pipe from kustomize: `kustomize build . | kubeconform`.

### [kube-linter](https://github.com/stackrox/kube-linter)
- **What:** Static analysis tool by StackRox/Red Hat that checks Kubernetes YAML files and Helm charts against production readiness and security best practices. Detects missing resource limits, running as root, missing liveness probes, etc.
- **Loop phase:** verify
- **Install:** `brew install kube-linter` / `go install golang.stackrox.io/kube-linter/cmd/kube-linter@latest`
- **Claude Code usage:** Run `kube-linter lint manifests/` for all manifests. `kube-linter lint chart/` for Helm charts. Configurable via `.kube-linter.yml` to enable/disable specific checks. JSON output with `--format json`.

### [Polaris](https://github.com/FairwindsOps/polaris)
- **What:** Best practices and policy enforcement engine for Kubernetes. Runs as CLI, dashboard, admission controller, or CI validator. Covers security, efficiency, and reliability categories with configurable severity levels.
- **Loop phase:** verify
- **Install:** `brew install FairwindsOps/tap/polaris` / `kubectl apply -f https://github.com/FairwindsOps/polaris/releases/latest/download/dashboard.yaml`
- **Claude Code usage:** Run `polaris audit --audit-path manifests/` for CLI validation. `polaris audit --audit-path manifests/ --format json` for structured results. Use `--set-exit-code-on-danger` for CI gates.

### [Kustomize](https://kustomize.io/)
- **What:** Template-free Kubernetes configuration customization tool. Composes, patches, and transforms YAML manifests using overlays without forking base configurations. Built into kubectl (`kubectl apply -k`).
- **Loop phase:** implement
- **Install:** `brew install kustomize` / built into `kubectl` (use `kubectl kustomize`)
- **Claude Code usage:** Run `kustomize build overlays/production/` to render final manifests. Pipe to kubeconform: `kustomize build . | kubeconform`. `kubectl apply -k overlays/staging/ --dry-run=server` for validation.

### [Helm (lint)](https://helm.sh/)
- **What:** Kubernetes package manager. `helm lint` validates chart structure, template rendering, and values. `helm template` renders charts locally for inspection without a cluster.
- **Loop phase:** implement / verify
- **Install:** `brew install helm` / `curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash`
- **Claude Code usage:** Run `helm lint chart/` to validate chart structure. `helm template myrelease chart/ --values values-prod.yaml` to render and inspect. Pipe to kubeconform: `helm template chart/ | kubeconform`. `helm install --dry-run --debug` for full simulation.

### [kubectx / kubens](https://github.com/ahmetb/kubectx)
- **What:** Power tools for kubectl context and namespace switching. `kubectx` switches between clusters; `kubens` switches between namespaces. Interactive fuzzy selection with fzf integration.
- **Loop phase:** implement
- **Install:** `brew install kubectx` (installs both kubectx and kubens)
- **Claude Code usage:** `kubectx staging` to switch to staging cluster before running verification commands. `kubens kube-system` to inspect system namespace. Useful for multi-cluster workflows where Claude Code needs to verify resources across environments.

### [k9s](https://github.com/derailed/k9s)
- **What:** Terminal-based Kubernetes dashboard. Provides real-time cluster resource views, pod logs, exec into containers, port-forwarding, and resource editing. Keyboard-driven interface with vim-like navigation.
- **Loop phase:** verify (interactive)
- **Install:** `brew install derailed/k9s/k9s` / `snap install k9s` / `choco install k9s`
- **Claude Code usage:** Primarily an interactive tool for human operators. Claude Code can reference k9s as a recommendation for developers who need live cluster debugging. For automated use, prefer `kubectl` commands directly.

### [stern](https://github.com/stern/stern)
- **What:** Multi-pod and multi-container log tailing for Kubernetes. Matches pods by regex, color-codes output per pod/container, and follows logs in real time. Essential for debugging distributed services.
- **Loop phase:** verify
- **Install:** `brew install stern` / `go install github.com/stern/stern@latest`
- **Claude Code usage:** Run `stern <pod-name-prefix>` to tail logs matching the prefix. `stern . --namespace staging` to tail all pods in a namespace. `stern deployment/<name> --since 5m` for recent logs. Useful for verifying application behavior after deployment.

---

## Configuration Management (implement/verify)

### [Ansible](https://docs.ansible.com/) + [ansible-lint](https://ansible.readthedocs.io/projects/lint/)
- **What:** Agentless configuration management via YAML playbooks. `ansible-lint` checks playbooks, roles, and collections against best practices: task naming, FQCN usage, deprecated modules, idempotency issues, and formatting.
- **Loop phase:** implement (Ansible) / verify (ansible-lint)
- **Install:** `pip install ansible ansible-lint` / `brew install ansible ansible-lint`
- **Claude Code usage:** Run `ansible-lint playbook.yml` after edits. `ansible-lint -f json` for structured output. `ansible-playbook --check --diff playbook.yml` for dry-run mode that shows what would change. `ansible-lint --fix` to auto-fix some issues.

### [Molecule](https://github.com/ansible/molecule)
- **What:** (Also listed under Infrastructure Testing.) The standard testing framework for Ansible roles. Creates test instances, applies the role, checks idempotence, runs verifiers, and destroys instances. Supports Docker, Podman, Vagrant, and cloud drivers.
- **Loop phase:** verify
- **Install:** `pip install molecule[docker]`
- **Claude Code usage:** Run `molecule test` in the role directory. Claude Code can generate `molecule/default/molecule.yml` scenarios and `molecule/default/verify.yml` assertion playbooks.

### [Chef](https://www.chef.io/) + [Cookstyle](https://docs.chef.io/workstation/cookstyle/) + [ChefSpec](https://github.com/chefspec/chefspec)
- **What:** Ruby-based configuration management with a rich testing ecosystem. Cookstyle is a RuboCop-based linter for Chef cookbooks. ChefSpec runs unit tests against Chef recipes in-memory without converging real nodes. InSpec and Test Kitchen handle integration testing.
- **Loop phase:** implement (Chef) / verify (Cookstyle, ChefSpec)
- **Install:** `chef gem install cookstyle` / `gem install chefspec` / Chef Workstation bundle
- **Claude Code usage:** Run `cookstyle --auto-correct` to fix style issues. `chef exec rspec` to run ChefSpec unit tests. `kitchen test` for integration tests. Claude Code can generate ChefSpec examples for recipe coverage.

### [Puppet](https://puppet.com/) + [puppet-lint](https://github.com/puppetlabs/puppet-lint)
- **What:** Declarative configuration management with its own DSL. `puppet-lint` checks Puppet manifests against the official style guide: indentation, quoting, resource ordering, and deprecated syntax.
- **Loop phase:** implement (Puppet) / verify (puppet-lint)
- **Install:** `gem install puppet-lint` / `puppet module install puppetlabs-lint`
- **Claude Code usage:** Run `puppet-lint manifests/` to check all manifests. `puppet-lint --fix manifests/` to auto-fix issues. `puppet parser validate manifests/*.pp` for syntax validation before linting.

---

## Cloud Provider CLIs (all phases)

### [AWS CLI](https://aws.amazon.com/cli/)
- **What:** Official CLI for Amazon Web Services. Covers every AWS service API. Essential for verifying deployed infrastructure state, querying resources, and debugging.
- **Loop phase:** all phases
- **Install:** `brew install awscli` / `pip install awscli` / `curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o awscliv2.zip && unzip awscliv2.zip && sudo ./aws/install`
- **Claude Code usage:** Verification examples: `aws ec2 describe-instances --filters "Name=tag:Environment,Values=production" --output json`, `aws s3 ls s3://bucket-name/`, `aws sts get-caller-identity` (confirm active credentials), `aws cloudformation describe-stacks --stack-name mystack`. Use `--output json` for structured parsing.

### [Google Cloud CLI (gcloud)](https://cloud.google.com/sdk/gcloud)
- **What:** Official CLI for Google Cloud Platform. Manages Compute Engine, GKE, Cloud Storage, IAM, and all GCP services. Includes `gsutil` for storage and `bq` for BigQuery.
- **Loop phase:** all phases
- **Install:** `brew install google-cloud-sdk` / `curl https://sdk.cloud.google.com | bash`
- **Claude Code usage:** Verification examples: `gcloud compute instances list --format=json`, `gcloud container clusters get-credentials <cluster>`, `gcloud projects get-iam-policy <project> --format=json`. Auth: `gcloud auth application-default login`.

### [Azure CLI (az)](https://learn.microsoft.com/en-us/cli/azure/)
- **What:** Official CLI for Microsoft Azure. Manages VMs, AKS, Storage, Entra ID (formerly AAD), and all Azure services.
- **Loop phase:** all phases
- **Install:** `brew install azure-cli` / `curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash`
- **Claude Code usage:** Verification examples: `az vm list --output json`, `az aks get-credentials --resource-group rg --name cluster`, `az account show` (confirm identity), `az group list --output table`. Use `--output json` throughout for structured parsing.

### [Pulumi CLI](https://www.pulumi.com/docs/iac/cli/)
- **What:** Infrastructure-as-code using real programming languages (TypeScript, Python, Go, C#, Java). The CLI manages stacks, deploys changes, and provides drift detection. Uses cloud provider CLIs for authentication.
- **Loop phase:** all phases
- **Install:** `brew install pulumi` / `curl -fsSL https://get.pulumi.com | sh`
- **Claude Code usage:** `pulumi preview` for plan-equivalent output. `pulumi up` to deploy. `pulumi stack output --json` to read outputs. `pulumi refresh` to detect drift. Auth delegates to underlying cloud CLI (aws, gcloud, az).

---

## Monitoring & Observability Setup (verify)

### [promtool (Prometheus)](https://prometheus.io/docs/prometheus/latest/command-line/promtool/)
- **What:** Official Prometheus CLI tool for config and rule validation. Validates `prometheus.yml` syntax, checks alerting/recording rule files, and runs unit tests against rules with simulated time-series data. Essential for CI pipelines that manage Prometheus configs.
- **Loop phase:** verify
- **Install:** Bundled with Prometheus. `brew install prometheus` / download from GitHub releases.
- **Claude Code usage:** `promtool check config prometheus.yml` to validate main config. `promtool check rules alerts.yml` to validate alerting rules. `promtool test rules test.yml` to run unit tests against rules. Unit test YAML defines input series, evaluation intervals, and expected alert outputs.

### [Grafana Dashboard Validation](https://grafana.com/docs/grafana/latest/)
- **What:** Grafana dashboards are JSON files that can be validated for structure, datasource references, and panel configuration. Grafana's provisioning system allows dashboards-as-code.
- **Loop phase:** verify
- **Install:** `brew install grafana` / `docker pull grafana/grafana`
- **Claude Code usage:** Validate dashboard JSON structure programmatically. Use Grafana's HTTP API (`/api/dashboards/validate`) against a running instance. For provisioned dashboards, `grafana-cli` or API calls verify datasource bindings. Grafana 12+ supports bulk import of Prometheus-style alerting rules.

### [Grafana Synthetic Monitoring](https://grafana.com/docs/grafana-cloud/testing/synthetic-monitoring/)
- **What:** Proactive endpoint monitoring using Prometheus Blackbox exporter probes. Pre-configured sensitivity tiers: High (5% probe failure for 5m), Medium (10%), Low (25%). Available in Grafana Cloud with configurable check types (HTTP, DNS, TCP, ping).
- **Loop phase:** verify
- **Install:** Grafana Cloud service (managed). Self-hosted: deploy Blackbox exporter + recording rules.
- **Claude Code usage:** Claude Code can generate Blackbox exporter configuration and Prometheus recording rules for synthetic checks. Validate probe configs with `promtool check config`. Review alerting thresholds against SLO targets.

### [Alertmanager Configuration](https://prometheus.io/docs/alerting/latest/configuration/)
- **What:** Prometheus Alertmanager routes, groups, and silences alerts. Its config (`alertmanager.yml`) defines notification routing trees, receivers (Slack, PagerDuty, email), and inhibition rules.
- **Loop phase:** verify
- **Install:** Bundled with Prometheus ecosystem. `brew install alertmanager`
- **Claude Code usage:** `amtool check-config alertmanager.yml` to validate config syntax. `amtool config routes test` to test routing against sample alerts. Claude Code can review routing trees for missing catch-all routes or overly broad silences.

---

## Claude Code Integration (all phases)

### [Terraform MCP Server (HashiCorp)](https://github.com/hashicorp/terraform-mcp-server)
- **What:** Official HashiCorp MCP server providing seamless integration with Terraform Registry APIs. Enables Claude Code to query provider documentation, resource schemas, module interfaces, and best practices directly from the Terraform ecosystem during planning and implementation.
- **Loop phase:** plan / implement
- **Install:** `claude mcp add terraform -- npx @hashicorp/terraform-mcp-server`
- **Claude Code usage:** Query provider resource schemas before writing HCL. Look up module documentation. Validate resource attribute types against the registry. Supports both Terraform and OpenTofu workflows.

### [Kubernetes MCP Server](https://github.com/containers/kubernetes-mcp-server)
- **What:** Go-based native MCP server that interacts directly with the Kubernetes API server (not a kubectl wrapper). Provides 40+ tools for managing cluster resources. Supports multi-cluster management, read-only mode for safe inspection, and natural language cluster queries.
- **Loop phase:** implement / verify
- **Install:** `claude mcp add kubernetes -- npx mcp-server-kubernetes`
- **Claude Code usage:** Query pod status, deployment health, service endpoints. Create and update resources via natural language. Read-only mode prevents accidental mutations during verification. Alternative implementations: [Flux159/mcp-server-kubernetes](https://github.com/Flux159/mcp-server-kubernetes), [containers/kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server).

### [AWS MCP Servers](https://github.com/awslabs/mcp)
- **What:** Official AWS Labs MCP server collection with 45+ tools for Claude Code. Covers documentation lookup, CDK infrastructure, CloudFormation, DynamoDB (read-only), Lambda management, cost analysis, Bedrock knowledge bases, and more. Requires Core MCP Server as orchestrator.
- **Loop phase:** all phases
- **Install:** `claude mcp add aws-docs -- npx @awslabs/aws-docs-mcp-server` (documentation), `claude mcp add aws-cdk -- npx @awslabs/aws-cdk-mcp-server` (CDK), plus additional per-service servers.
- **Claude Code usage:** Query AWS documentation inline during planning. Generate CDK constructs with security scanning. Read DynamoDB tables safely. Estimate costs before deployment. Each server adds with a single `claude mcp add` command.

### [Terraform Cloud MCP](https://mcpservers.org/servers/severity1/terraform-cloud-mcp)
- **What:** MCP server for Terraform Cloud / HCP Terraform. Enables Claude Code to interact with workspaces, runs, state, and plan outputs from Terraform Cloud without leaving the coding session.
- **Loop phase:** plan / verify
- **Install:** Configure via `.mcp.json` or `claude mcp add` with Terraform Cloud API token.
- **Claude Code usage:** List workspaces, trigger plans, review plan output, check run status. Useful for teams using Terraform Cloud as their execution backend.

### General CLI Integration
- **What:** Claude Code can invoke any CLI tool directly via its Bash tool. All tools in this catalog that have a command-line interface can be used by Claude Code without an MCP server. MCP servers add richer tool descriptions and structured interactions but are not required for basic usage.
- **Loop phase:** all phases
- **Claude Code usage:** Claude Code runs `terraform plan`, `kubectl get pods`, `trivy image`, `helm lint`, etc. directly. Combine with `--output json` or `-f json` flags for structured analysis. Chain tools: `kustomize build . | kubeconform | tee validation.log`.

---

## Sources

- [Terraform Tools to Know in 2026 - env0](https://www.env0.com/blog/top-terraform-tools-to-know)
- [26 Most Useful Terraform Tools - Spacelift](https://spacelift.io/blog/terraform-tools)
- [Top 7 Terraform Scanning Tools - Spacelift](https://spacelift.io/blog/terraform-scanning-tools)
- [pre-commit-terraform - GitHub](https://github.com/antonbabenko/pre-commit-terraform)
- [Hadolint - GitHub](https://github.com/hadolint/hadolint)
- [Dive - GitHub](https://github.com/wagoodman/dive)
- [Docker Scout Documentation](https://docs.docker.com/scout/)
- [actionlint - GitHub](https://github.com/rhysd/actionlint)
- [Checkov - GitHub](https://github.com/bridgecrewio/checkov)
- [Terratest - GitHub](https://github.com/gruntwork-io/terratest)
- [BATS-core - GitHub](https://github.com/bats-core/bats-core)
- [kubeconform - GitHub](https://github.com/yannh/kubeconform)
- [kube-linter - GitHub](https://github.com/stackrox/kube-linter)
- [Polaris - GitHub](https://github.com/FairwindsOps/polaris)
- [k9s - GitHub](https://github.com/derailed/k9s)
- [stern - GitHub](https://github.com/stern/stern)
- [kubectx - GitHub](https://github.com/ahmetb/kubectx)
- [Ansible Lint Documentation](https://ansible.readthedocs.io/projects/lint/)
- [Molecule - GitHub](https://github.com/ansible/molecule)
- [promtool - Prometheus](https://prometheus.io/docs/prometheus/latest/command-line/promtool/)
- [Prometheus Unit Testing Rules](https://prometheus.io/docs/prometheus/latest/configuration/unit_testing_rules/)
- [Grafana Synthetic Monitoring](https://grafana.com/docs/grafana-cloud/testing/synthetic-monitoring/)
- [Terraform MCP Server - GitHub](https://github.com/hashicorp/terraform-mcp-server)
- [Kubernetes MCP Server - GitHub](https://github.com/containers/kubernetes-mcp-server)
- [AWS MCP Servers - GitHub](https://github.com/awslabs/mcp)
- [Infracost - GitHub](https://github.com/infracost/infracost)
- [OpenTofu - GitHub](https://github.com/opentofu/opentofu)
- [Pulumi CLI Documentation](https://www.pulumi.com/docs/iac/cli/)
- [AWS MCP Servers Complete Reference - Sati Technology](https://www.satitechnology.com/guides/aws-mcp-servers-complete-reference/)
- [MCP Servers for DevOps Guide 2026 - CloudshipAI](https://www.cloudshipai.com/blog/mcp-servers-devops-complete-guide-2026)
