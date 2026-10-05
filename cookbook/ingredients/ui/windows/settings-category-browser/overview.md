
A sidebar-and-content browser for application settings. A vertical list of category names sits on the left; selecting one shows that category's settings on the right in a scrollable form. Changes apply immediately to a persistence layer, with no Apply or Save button. This ingredient owns the category list, content panel, immediate-apply behavior, and persistence abstraction. The window that hosts it (menu entry, single instance, frame persistence) is composed by the Settings Window recipe.

### Terminology

| Term | Definition |
|------|-----------|
| Category | A named group of related settings displayed in the sidebar |
| Content panel | The right-side area showing settings for the selected category |
| Frame autosave | Platform mechanism for persisting window position and size between sessions |

