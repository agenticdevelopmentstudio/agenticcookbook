<!-- leaf: implement-ui/design-time-data · source: guidelines/implementing/ui/design-time-data.md -->

**Rules** (cite as `implement-ui/design-time-data#<slug>`):

- `views-use-datacontext-designinstance-xaml` SHOULD — Views SHOULD use d:DataContext and d:DesignInstance for XAML designer preview data
- `xaml-hot-reload-used-live-iteration-during` SHOULD — XAML Hot Reload SHOULD be used for live iteration during development

# Design-Time Data

Wire up design-time data contexts so the XAML designer always shows realistic preview content, not empty surfaces.

- Views SHOULD use `d:DataContext` and `d:DesignInstance` for XAML designer preview data
- XAML Hot Reload SHOULD be used for live iteration during development
