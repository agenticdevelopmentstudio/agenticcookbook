
- Do not inject the Hilt-managed graph by passing `Context` around to build objects manually — that defeats the framework.
- Do not field-inject where constructor injection is possible; reserve field injection for framework-instantiated entry points.
- Do not create god modules. Split modules by feature and install them into the narrowest applicable component.

