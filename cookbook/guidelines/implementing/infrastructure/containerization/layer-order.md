
1. `FROM` and base setup.
2. Copy only the dependency manifest (e.g., `COPY package*.json ./`), then install.
3. Copy application source last (`COPY . .`).
