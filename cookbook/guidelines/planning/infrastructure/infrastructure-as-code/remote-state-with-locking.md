
- State MUST live in a **remote backend** (S3, GCS, AzureRM blob, or a managed IaC platform), versioned and recoverable — never committed to git or left only on a laptop.
- State writes MUST be **locked** to prevent concurrent corruption. For the S3 backend, prefer native S3 lockfile-based locking (`use_lockfile = true`, available since 2025); a DynamoDB lock table remains valid and can run alongside it during migration. GCS and AzureRM provide their own locking.
- Use a consistent state key convention (`<env>/<component>/terraform.tfstate`) so IAM policies can scope per environment.

