<!-- leaf: implement-ui/dashboard-service-is-display-only · source: guidelines/implementing/ui/dashboard-service-is-display-only.md -->

**Rules** (cite as `implement-ui/dashboard-service-is-display-only#<slug>`):

- `api-ui-layer-not-have-knowledge-git-files` MUST — The dashboard service is a generic API and UI layer. It MUST NOT have knowledge of git, files, or roadmap structure. …

# Dashboard service is display-only

The dashboard service is a generic API and UI layer. It MUST NOT have knowledge of git, files, or roadmap structure. Agents sync data to it; it MUST only display what it receives.
