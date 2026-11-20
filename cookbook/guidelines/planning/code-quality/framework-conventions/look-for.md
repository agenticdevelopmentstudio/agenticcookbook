
- `should-default-to-conventional-units`: framework-conventional units (View + ViewModel, Activity + Fragment, component triplets, route segments, Controller + ViewModel) and whether the proposed groups follow them
- `should-not-decompose-below-conventional-unit`: a conventional unit split across groups with no evidence from another lens
- `should-elevate-cross-feature-units`: a ViewModel or service referenced by three or more feature modules and still kept in one feature's group
- `should-flag-convention-deviations`: logic in views, fat models, god services, or UI calling APIs with no service or repository, and whether the findings list them as violations
- `should-not-legitimize-misplacement`: a proposed scope group built around misplaced logic
- `should-treat-lazy-loaded-modules-as-independent`: lazy-loaded Angular modules, Next.js dynamic imports, or Webpack split points, and whether each is its own group
- `should-separate-plugin-registry`: the plugin or extension registry, and whether it is grouped apart from the plugins it loads
- `should-group-mediatr-handlers-by-feature`: MediatR requests and handlers, and whether they are grouped by feature domain
- `should-flag-convention-deviations`: In the code **this diff adds or changes**, identify the MVC/MVVM/MVP/TCA pattern, View+ViewModel pairs, Controller+Routes groupings, middleware chains, service/repository patterns, and plugin architectures it participates in — and flag where the change deviates from the surrounding convention.
