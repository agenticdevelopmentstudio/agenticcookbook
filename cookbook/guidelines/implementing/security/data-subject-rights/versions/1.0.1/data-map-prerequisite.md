
You cannot fulfill a request against data you cannot find. You **MUST** maintain a data map enumerating every place personal data lives:

- Primary databases, caches, search indexes (Elasticsearch/OpenSearch), object storage, message queues, event logs, application logs, analytics/warehouse, and backups.
- Every entry **MUST** record the store, the subject-id key (or join path), the data categories, the retention basis, and which third-party processors receive it.
- New code paths that persist personal data **MUST** update the data map; treat an un-mapped store as a defect.

