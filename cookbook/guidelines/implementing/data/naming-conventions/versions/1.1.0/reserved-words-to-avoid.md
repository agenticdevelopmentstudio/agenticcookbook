
SQLite has 147 reserved keywords. These are common traps:

| Avoid | Use instead |
|-------|-------------|
| `order` | `sort_order`, `display_order` |
| `group` | `team`, `grouping` |
| `index` | `position`, `sort_index` |
| `key` | `lookup_key`, `api_key` |
| `value` | `setting_value`, `metric_value` |
| `action` | `operation`, `activity` |
| `check` | `validation`, `check_result` |
| `default` | `default_value`, `fallback` |
| `filter` | `criterion`, `filter_expr` |
| `plan` | `execution_plan` |
| `row` | `record`, `entry` |
| `query` | `search_query` |

If you must use a reserved word, quote it with double quotes (`"order"`), but this adds friction to every query. Renaming is always preferred.

SQLite adds new keywords over time. The official docs recommend quoting any English word used as an identifier, even if not currently reserved.

