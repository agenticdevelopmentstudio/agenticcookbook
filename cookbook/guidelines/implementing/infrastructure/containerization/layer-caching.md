
Order instructions from least- to most-frequently changed so the dependency layer is reused when only source changes:

1. `FROM` and base setup.
2. Copy only the dependency manifest (e.g., `COPY package*.json ./`), then install.
3. Copy application source last (`COPY . .`).

- **cache-order**: Dependencies MUST be installed before application source is copied, so editing source does not invalidate the (expensive) dependency layer.
- **combine-run**: Combine `apt-get update` with `apt-get install` in one `RUN`, pin package versions where practical, and clean caches in the same layer (`rm -rf /var/lib/apt/lists/*`) to avoid stale-cache bugs and image bloat.

