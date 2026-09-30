<!-- leaf: recipes-ui/apps-apple--logging · source: recipes/ui/apps/apple.md -->

# Apple Test App Suite

## Logging

Subsystem: `{{bundle_id}}` | Category: `ComponentCatalog`

| Event | Level | Message |
|-------|-------|---------|
| Catalog launched | debug | `ComponentCatalog: launched with {{count}} components` |
| Component selected | debug | `ComponentCatalog: selected "{{name}}"` |
| Component not available on platform | debug | `ComponentCatalog: "{{name}}" excluded on {{platform}}` |
