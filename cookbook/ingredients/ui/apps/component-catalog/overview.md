
A navigable catalog of every implemented UI component, showing each component in all the states its spec defines so they can be reviewed visually and verified with snapshots. The root `ComponentCatalogView` adapts its navigation to the platform; each entry view lays out one component's states in labeled sections and carries a preview. This ingredient owns the catalog behavior and the procedure for adding a component; the project that builds it is the XcodeGen Apple Project ingredient.

### Terminology

| Term | Definition |
|------|-----------|
| Catalog | A navigable list of all implemented components, each showing every state from its spec |
| Catalog entry | A single view showing one component in all its states |

