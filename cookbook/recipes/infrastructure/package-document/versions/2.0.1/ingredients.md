
| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Package document type | `agenticdevelopercookbook://ingredients/infrastructure/package-document-type` | Registers the UTType, conforms the document class to `ReferenceFileDocument`, declares the `DocumentGroup` scenes, and owns auto-save and session restoration | Yes | One instance per document kind: UTType identifier, file extension, document class |
| Package document storage | `agenticdevelopercookbook://ingredients/infrastructure/package-document-storage` | Defines the package contents, the SQLite schema, the read process with legacy JSON fallback, the atomic write process, and migration-safe Codable | Yes | Database filename, legacy JSON filename, current schema version, and domain-specific tables per document kind |
| SQLite helpers | `agenticdevelopercookbook://ingredients/infrastructure/sqlite-helpers` | Parameterized execution, row queries, temporary database URL, and the SQLite error type | Yes | None |

