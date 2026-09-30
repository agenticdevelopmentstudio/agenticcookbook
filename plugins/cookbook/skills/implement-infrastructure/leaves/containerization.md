<!-- leaf: implement-infrastructure/containerization · source: guidelines/implementing/infrastructure/containerization.md -->

**Rules** (cite as `implement-infrastructure/containerization#<slug>`):

- `multi-stage` MUST
- `base-image` MUST
- `one-concern` SHOULD
- `pin-by-digest` SHOULD
- `rebuild-fresh` SHOULD
- `cache-order` MUST
- `non-root` MUST
- `no-baked-secrets` MUST
- `healthcheck` SHOULD

# Containerization

A container image is a deployment artifact: make it small, reproducible, and least-privilege. These rules apply to any OCI image built from a Dockerfile (Docker BuildKit, Buildah, or equivalent).

## Build structure

- **multi-stage**: Dockerfiles MUST use multi-stage builds so the final image contains only the runtime artifact — not compilers, build tools, dev dependencies, or source. Build in an earlier stage; `COPY --from=<stage>` only what runs.
- **base-image**: The final stage MUST use a minimal base — language-specific `slim`, `alpine`, or distroless. Avoid full OS images when a slim variant carries the runtime. A smaller base means fewer packages and a smaller attack surface.
- **one-concern**: Each image SHOULD address a single concern (one app/process). Decouple distinct services into separate images so they scale and deploy independently.
- **workdir**: Use `WORKDIR` with absolute paths rather than chained `cd`. Use `ENTRYPOINT` for the executable and `CMD` for default arguments.

## Reproducibility and supply chain

- **pin-by-digest**: Base images SHOULD be pinned by digest, not a floating tag — `FROM python:3.13-slim@sha256:<digest>`. A tag like `:latest` is mutable; a digest is immutable and reproducible. Refresh digests deliberately (e.g., via Dependabot/Renovate) to pick up security patches.
- **deterministic-deps**: Install from a locked manifest (`requirements.txt` with hashes, `package-lock.json`, `go.sum`, `Cargo.lock`) so builds are repeatable.
- **rebuild-fresh**: Periodic release builds SHOULD use `--pull` (and `--no-cache` when patching) so stale base layers and dependencies do not persist.

## Layer caching

Order instructions from least- to most-frequently changed so the dependency layer is reused when only source changes:

1. `FROM` and base setup.
2. Copy only the dependency manifest (e.g., `COPY package*.json ./`), then install.
3. Copy application source last (`COPY . .`).

- **cache-order**: Dependencies MUST be installed before application source is copied, so editing source does not invalidate the (expensive) dependency layer.
- **combine-run**: Combine `apt-get update` with `apt-get install` in one `RUN`, pin package versions where practical, and clean caches in the same layer (`rm -rf /var/lib/apt/lists/*`) to avoid stale-cache bugs and image bloat.

## Security

- **non-root**: The image MUST run as a non-root user. Create an unprivileged user/group and set `USER` before `ENTRYPOINT`. Do not install or rely on `sudo`.
- **no-baked-secrets**: The image MUST NOT bake secrets (API keys, tokens, certs, passwords) into layers, `ENV`, or build args — they persist in image history even if later removed. Inject runtime config via environment/mounted secrets (see twelve-factor-config). For build-time credentials, use BuildKit secret mounts (`RUN --mount=type=secret,...`), which do not persist in the final image.
- **least-files**: Use a `.dockerignore` to exclude `.git`, secrets, local env files, build output, and `node_modules` from the build context — this shrinks context, speeds builds, and prevents accidental secret leakage.
- **drop-extras**: Do not install packages "just in case." Fewer packages means fewer CVEs to patch.

## Observability

- **healthcheck**: The image SHOULD declare a `HEALTHCHECK` (or the orchestrator's liveness/readiness probe SHOULD cover it) so the runtime can detect an unhealthy container. Keep the check cheap and specific to the app's actual readiness.

## Adopt-when-justified

- Orchestration platforms (Kubernetes, ECS, Nomad) and per-image vulnerability scanners add real operational weight. Adopt them when a measured need justifies the cost (scale, multi-service coordination, compliance) — not by default (per YAGNI). A single image deployed to a managed container host is often sufficient early on.
