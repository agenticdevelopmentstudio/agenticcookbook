<!-- leaf: implement-ui/data-display · source: guidelines/implementing/ui/data-display.md -->

**Rules** (cite as `implement-ui/data-display#<slug>`):

- `table` MUST — comparable, multi-attribute data. Best for desktop/tablet when users need to compare values across rows (spreadsheets, …
- `collections-10-items-provide-sort-filter-controls` MUST — Collections of 10+ items SHOULD provide sort and/or filter controls. Collections of 50+ items MUST include search.

# Data Display

Choose the right pattern for the content type and user task.

- **List** — sequential, scannable content. Best for homogeneous items where the user reads
  top-to-bottom (messages, settings, search results). Support pull-to-refresh and pagination
  for dynamic data.
- **Table** — comparable, multi-attribute data. Best for desktop/tablet when users need to
  compare values across rows (spreadsheets, admin panels, logs). Tables MUST be sortable
  by column. On mobile, consider collapsing to cards or a detail-on-tap list.
- **Cards** — heterogeneous, browsable content. Best when items have varying content types
  or sizes (news feed, dashboard widgets). Cards should each be a single tappable unit with
  one primary action.
- **Grid** — uniform visual items. Best for content where the visual is primary (photos,
  products, icons). Maintain consistent aspect ratios.

Collections of **10+ items** SHOULD provide sort and/or filter controls. Collections of **50+ items**
MUST include search.

References:
- [Apple HIG: Lists and Tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)
- [Material Design: Lists](https://m3.material.io/components/lists/overview)
- [NNGroup: Cards](https://www.nngroup.com/articles/cards-component/)
