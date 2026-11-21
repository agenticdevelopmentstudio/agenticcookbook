
# Cookbook Formatting

A cookbook's `cookbook.json` is UTF-8 JSON that validates against `references/cookbook.schema.json` and carries the cookbook's identity (`format`, `id`, `rdid`); a project cookbook adds the fields and the structure tree it assembles. The schema checks the shape; cookr's code checks what a schema cannot, such as paths that resolve and a `depends-on` graph without cycles, and reports every error it finds.

