---
id: 9edd68fb-29e3-44d6-951a-e668a2e9dfda
title: Deployment & Hosting Tools
domain: agenticdevelopercookbook://appendix/research/developer-tools/infrastructure/deployment-hosting-tools
type: reference
version: 1.0.0
status: draft
language: en
created: '2026-06-09'
modified: '2026-06-09'
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: Deployment & Hosting Tools
platforms: []
tags: []
depends-on: []
related: []
references: []
---
# Deployment & Hosting Tools

**Date:** 2026-03-29
**Context:** Deployment platforms, cloud providers, and infrastructure-as-code tools that integrate with Claude Code via plugins, MCP servers, or CLI shell-out. Focused on tools with first-class Claude Code integration (official plugins, MCP servers) and the platforms most commonly used in agentic development workflows.

**Integration methods:**
- **Plugin** -- Claude Code plugin bundles MCP + hooks + skills; install via `/plugin install`
- **MCP server** -- tool exposes a Model Context Protocol server for direct integration
- **CLI shell-out** -- Claude Code runs the tool via Bash
- **Hook** -- Claude Code pre/post-tool hook triggers the tool automatically
- **Skill** -- community skill available via marketplace or manual install

---

## Platform-as-a-Service with Claude Code Plugins

These platforms have official Claude Code plugins in the `claude-plugins-official` marketplace, giving Claude direct access to deploy, configure, and manage applications without leaving the conversation.

### Vercel

- **Plugin:** `vercel@claude-plugins-official`
- **Install:** `/plugin install vercel@claude-plugins-official`
- **What it does:** Frontend and serverless deployment platform. The plugin gives Claude Code tools to deploy projects, manage environment variables, configure domains, check deployment status, and inspect build logs. Vercel specializes in Next.js, React, Svelte, and other frontend frameworks with automatic preview deployments on every push.
- **Good for:** Frontend apps, Next.js projects, serverless API routes, edge functions, preview deployments for PR review.
- **Integration type:** Plugin (MCP server + skills)
- **Pricing:** Free tier (hobby) with unlimited static sites, 100 GB bandwidth, serverless function execution limits. Pro starts at $20/user/month. Enterprise pricing available.
- **Notes:** Vercel has the tightest Next.js integration of any platform (they maintain the framework). Automatic preview URLs for every git push make it ideal for Claude Code workflows where you deploy and verify in the same session. Edge Functions run on Cloudflare's network under the hood.

### Railway

- **Plugin:** `railway@claude-plugins-official`
- **Install:** `/plugin install railway@claude-plugins-official`
- **What it does:** Container-based deployment platform with automatic builds from Dockerfiles or Nixpacks (auto-detected buildpacks). The plugin enables Claude Code to deploy services, manage databases (Postgres, MySQL, Redis, MongoDB), configure environment variables, view logs, and manage project resources.
- **Good for:** Full-stack apps with databases, backend services, Docker-based deployments, microservices, internal tools.
- **Integration type:** Plugin (MCP server + skills)
- **Pricing:** Free trial with $5 credit. Usage-based pricing: $0.000463/vCPU-minute, $0.000231/GB-minute for memory. No per-seat fees. Most small projects run $5-10/month.
- **Notes:** Railway is the simplest path from "I have a Dockerfile" to a running service with a URL. Nixpacks auto-detection means Claude Code can deploy most projects without writing deployment config. Built-in Postgres, Redis, and MySQL provisioning eliminates the need for separate database hosting.

### Netlify

- **Plugin:** `netlify-skills@claude-plugins-official`
- **Install:** `/plugin install netlify-skills@claude-plugins-official`
- **What it does:** Serverless and edge deployment platform. The plugin provides skills for deploying sites, managing serverless functions, configuring edge functions, managing environment variables, and working with Netlify's built-in services (forms, identity, large media). Also supports Netlify's Deno-based edge functions and database connectors.
- **Good for:** Static sites, JAMstack apps, serverless functions, form handling without a backend, edge computing, A/B testing via split testing.
- **Integration type:** Plugin (skills)
- **Pricing:** Free tier with 100 GB bandwidth, 300 build minutes/month, 125K serverless function invocations. Pro at $19/member/month. Enterprise available.
- **Notes:** Netlify pioneered the JAMstack deployment model. The platform's build plugins ecosystem allows custom build steps (image optimization, sitemap generation, etc.). Edge functions run on Deno Deploy's global network. The `netlify dev` CLI provides a local development server that simulates the production environment.

### Firebase

- **Plugin:** `firebase@claude-plugins-official`
- **Install:** `/plugin install firebase@claude-plugins-official`
- **What it does:** Google's backend-as-a-service platform. The plugin gives Claude Code tools to manage Firebase projects including Firestore (document database), Authentication, Cloud Storage, Hosting, Cloud Functions, and Realtime Database. Handles configuration, deployment, and resource management.
- **Good for:** Mobile app backends, real-time applications, authentication flows, serverless functions (Cloud Functions for Firebase), static site hosting, push notifications (FCM).
- **Integration type:** Plugin (MCP server + skills)
- **Pricing:** Spark (free) tier includes generous limits: 1 GiB Firestore storage, 50K reads/day, 20K writes/day, 10 GB hosting storage, 125K Cloud Functions invocations/month. Blaze (pay-as-you-go) with no fixed monthly fee -- usage-based pricing.
- **Notes:** Firebase is tightly integrated with Google Cloud Platform. Cloud Functions for Firebase are Cloud Functions under the hood. The Firebase CLI (`firebase-tools`) is required locally for the plugin to work. Firestore's real-time sync makes it particularly strong for collaborative and mobile apps. Firebase Hosting has automatic SSL and CDN distribution.

### Supabase

- **Plugin:** `supabase@claude-plugins-official`
- **Install:** `/plugin install supabase@claude-plugins-official`
- **What it does:** Open-source Firebase alternative built on Postgres. The plugin provides tools for managing Postgres databases (schema, migrations, queries), authentication (email, OAuth, magic links), file storage, edge functions (Deno-based), and real-time subscriptions via Postgres changes.
- **Good for:** Apps that need a real Postgres database, authentication, file storage, and real-time features. Full-stack apps where you want SQL access rather than NoSQL. Projects that may need to self-host later.
- **Integration type:** Plugin (MCP server + skills)
- **Pricing:** Free tier includes 500 MB database, 1 GB file storage, 50K monthly active users for auth, 500K edge function invocations. Pro at $25/month per project. Enterprise available.
- **Notes:** Supabase is the open-source alternative to Firebase with a real Postgres database instead of Firestore. Claude Code can write SQL migrations directly, which is a better fit for agents than NoSQL schema design. Row Level Security (RLS) policies are Postgres-native. The local development stack (`supabase start`) runs everything in Docker. Edge functions are Deno-based and deploy globally.

---

## Cloud Providers

### AWS (3-Plugin Suite)

AWS has three complementary official plugins covering different deployment patterns.

| Plugin | Focus | Install |
|--------|-------|---------|
| `deploy-on-aws` | Full-stack deployment to AWS (EC2, ECS, Lambda, S3, CloudFront) | `/plugin install deploy-on-aws@claude-plugins-official` |
| `aws-serverless` | Serverless-specific: Lambda, API Gateway, DynamoDB, Step Functions, EventBridge | `/plugin install aws-serverless@claude-plugins-official` |
| `migration-to-aws` | Migrate existing applications to AWS infrastructure | `/plugin install migration-to-aws@claude-plugins-official` |

- **What they do together:** The three plugins cover the full AWS deployment lifecycle. `deploy-on-aws` handles general infrastructure provisioning and deployment across AWS services. `aws-serverless` specializes in serverless architectures with Lambda, API Gateway, and event-driven patterns. `migration-to-aws` assists with migrating existing applications from other platforms or on-premises to AWS.
- **Good for:** Production-grade infrastructure, enterprises already on AWS, serverless applications, container orchestration (ECS/EKS), database services (RDS, DynamoDB, ElastiCache).
- **Integration type:** Plugin (MCP server + skills for each)
- **Pricing:** AWS is pay-as-you-go with a 12-month free tier. Free tier highlights: 750 hrs/month EC2 t2.micro, 1M Lambda requests/month, 25 GB DynamoDB, 5 GB S3. Costs vary widely by service and usage. The plugins themselves are free.
- **Notes:** AWS has the broadest service catalog of any cloud provider (200+ services). The plugin suite abstracts away much of the complexity, but Claude Code still benefits from knowing the AWS CLI (`aws`) for verification and debugging. IAM credentials must be configured locally (`aws configure` or environment variables). CloudFormation and CDK are commonly used alongside these plugins for infrastructure-as-code.

### Cloudflare

- **Plugin:** No official Claude Code plugin.
- **CLI:** `npx wrangler` (Cloudflare's developer CLI)
- **MCP server:** Not officially available, but community skills exist in [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills).
- **What it does:** Edge computing platform with Workers (serverless functions at the edge), Pages (static site and full-stack deployment), D1 (SQLite at the edge), R2 (S3-compatible object storage), KV (key-value store), Durable Objects (stateful edge compute), and Queues (message queues).
- **Good for:** Edge-first applications, global low-latency APIs, static sites with server-side rendering, S3-compatible storage without egress fees, applications that need to run close to users worldwide.
- **Integration type:** CLI shell-out via `wrangler`. Community skills available.
- **Install:** `npm install -g wrangler` or use `npx wrangler` per-project
- **Claude Code usage:** `wrangler dev` for local development, `wrangler deploy` for production, `wrangler d1 execute` for database operations, `wrangler r2 object put` for storage. All commands are non-interactive and work well with Claude Code shell-out.
- **Pricing:** Workers Free: 100K requests/day, 10ms CPU time. Workers Paid: $5/month for 10M requests, then $0.50/M. Pages: free for unlimited sites and bandwidth. D1: 5M rows read/day free. R2: 10 GB free, no egress fees ever.
- **Notes:** Cloudflare's zero-egress-fee model for R2 makes it significantly cheaper than S3 for read-heavy workloads. Workers run on V8 isolates (not containers), so cold starts are near-zero. The `wrangler.jsonc` config file is straightforward for Claude Code to read and modify. This cookbook's own site runs on Cloudflare Workers + Pages.

---

## Infrastructure-as-Code

### Terraform

- **Plugin:** `terraform@claude-plugins-official`
- **Install:** `/plugin install terraform@claude-plugins-official`
- **What it does:** The plugin provides Claude Code with skills for writing, validating, and applying Terraform configurations. Includes HCL generation, plan review, state inspection, and module authoring assistance. Works with both Terraform and OpenTofu.
- **Good for:** Multi-cloud infrastructure provisioning, infrastructure versioning and review, reproducible environments, managing cloud resources declaratively across AWS, GCP, Azure, Cloudflare, and 3,000+ providers.
- **Integration type:** Plugin (skills)
- **CLI companion:** `terraform` or `tofu` binary required locally. `brew install terraform` / `brew install opentofu`
- **Pricing:** Terraform CLI is free and open-source (BSL 1.1 license). OpenTofu is free and open-source (MPL 2.0). HCP Terraform (formerly Terraform Cloud) free tier: 500 managed resources. HCP Terraform Plus: $0.00014/hr per managed resource.
- **Notes:** See the companion file `devops-tools.md` in this directory for detailed coverage of Terraform ecosystem tools (TFLint, Checkov, Infracost, Terragrunt, terraform-docs, Trivy IaC scanning). The plugin complements these CLI tools by giving Claude Code higher-level skills for IaC authoring. The plugin works with both Terraform and OpenTofu interchangeably.

---

## Container & Orchestration

These tools do not have official Claude Code plugins but are commonly used in deployment workflows and have MCP servers or strong CLI integration.

### Kubernetes

- **Plugin:** No official Claude Code plugin.
- **MCP server:** Available via community MCP servers (e.g., [Kubernetes MCP](https://github.com/strowk/mcp-k8s-go) for cluster management).
- **What it does:** Container orchestration platform for deploying, scaling, and managing containerized applications. `kubectl` is the primary CLI for interacting with clusters.
- **Good for:** Production container orchestration, microservices, auto-scaling, rolling deployments, service mesh, multi-cloud portability.
- **Integration type:** CLI shell-out via `kubectl`. Community MCP servers available.
- **Install:** `brew install kubectl` / `brew install minikube` (local dev) / `brew install kind` (Kubernetes in Docker)
- **Claude Code usage:** `kubectl apply -f deployment.yaml` for deployments, `kubectl get pods` for status, `kubectl logs <pod>` for debugging, `kubectl rollout status` for deployment verification. All commands are non-interactive. Use `kubectl --output=json` for structured output Claude can parse.
- **Pricing:** Kubernetes itself is free and open-source. Managed offerings: EKS (AWS) $0.10/hr per cluster, GKE (Google) free control plane + node costs, AKS (Azure) free control plane + node costs.
- **Notes:** Kubernetes is complex and typically overkill for small projects. For Claude Code workflows, Railway or Cloudflare Workers often achieve the same result with less configuration. When Kubernetes is needed, the community MCP server provides cluster inspection and management without raw kubectl commands. Helm charts (`brew install helm`) are the standard packaging format.

### Docker

- **Plugin:** No official Claude Code plugin.
- **MCP server:** No official MCP server.
- **What it does:** Container runtime and build system. Packages applications into portable containers with `Dockerfile` and orchestrates multi-container setups with `docker compose`.
- **Good for:** Local development environments, reproducible builds, CI/CD pipelines, packaging applications for deployment to any container platform (Railway, ECS, GKE, etc.).
- **Integration type:** CLI shell-out via `docker` and `docker compose`.
- **Install:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) (macOS/Windows) or `apt-get install docker-ce` (Linux). Docker Desktop requires a paid subscription for companies with 250+ employees or $10M+ revenue.
- **Claude Code usage:** `docker build -t myapp .` for building, `docker compose up -d` for multi-service development, `docker compose logs` for debugging. See `devops-tools.md` for Docker-specific verification tools (Hadolint, Dive, Dockle, Docker Scout, Trivy).
- **Pricing:** Docker Engine is free and open-source. Docker Desktop: free for personal use and small businesses, Pro $5/month, Team $9/user/month, Business $24/user/month.
- **Notes:** Docker is the foundation that most deployment tools build on. Even serverless platforms like Railway and Render use Docker under the hood. Claude Code works well with Docker because Dockerfiles are declarative and compose files are YAML -- both formats Claude can read, write, and modify reliably. The `docker compose config` command validates compose files without starting services.

---

## Summary Comparison

| Platform | Plugin | MCP | CLI | Free Tier | Best For |
|----------|--------|-----|-----|-----------|----------|
| Vercel | Yes | Yes | `vercel` | Hobby (unlimited static) | Next.js, frontend, preview deploys |
| Railway | Yes | Yes | `railway` | $5 trial credit | Full-stack, Docker, databases |
| Netlify | Yes | -- | `netlify` | 100 GB bandwidth | JAMstack, static sites, edge |
| Firebase | Yes | Yes | `firebase` | Generous free tier | Mobile backends, real-time apps |
| Supabase | Yes | Yes | `supabase` | 500 MB Postgres | Postgres apps, auth, storage |
| AWS | Yes (3) | Yes | `aws` | 12-month free tier | Enterprise, broad service catalog |
| Cloudflare | -- | Community | `wrangler` | 100K req/day Workers | Edge-first, zero-egress storage |
| Terraform | Yes | -- | `terraform`/`tofu` | CLI free | Multi-cloud IaC |
| Kubernetes | -- | Community | `kubectl` | Open source | Container orchestration at scale |
| Docker | -- | -- | `docker` | Engine free | Local dev, CI/CD, container builds |
