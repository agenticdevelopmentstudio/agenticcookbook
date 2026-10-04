
For sync-capable schemas, verify before shipping:

1. A device on the old schema can still sync with the server on the new schema
2. New columns have DEFAULT values (CRDTs require values for all rows)
3. Migrations have been tested against databases at every previous version — an offline device may skip versions
4. Server-side backup exists before applying

