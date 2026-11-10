
| Name | Ingredient | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Package document type | [adc.ingredient.infrastructure.package-document-type](cookbook:ca56f1aa-7089-498f-8bcc-c11a0d81be3d) | Registers the UTType, conforms the document class to `ReferenceFileDocument`, declares the `DocumentGroup` scenes, and owns auto-save and session restoration | Yes | One instance per document kind: UTType identifier, file extension, document class |
| Package document storage | [adc.ingredient.infrastructure.package-document-storage](cookbook:ad558f24-29fa-430f-9ebd-0ec42f1aa9d1) | Defines the package contents, the SQLite schema, the read process with legacy JSON fallback, the atomic write process, and migration-safe Codable | Yes | Database filename, legacy JSON filename, current schema version, and domain-specific tables per document kind |
| SQLite helpers | [adc.ingredient.infrastructure.sqlite-helpers](cookbook:03df8ffb-476c-49f5-b104-33ad3c52bbe4) | Parameterized execution, row queries, temporary database URL, and the SQLite error type | Yes | None |

