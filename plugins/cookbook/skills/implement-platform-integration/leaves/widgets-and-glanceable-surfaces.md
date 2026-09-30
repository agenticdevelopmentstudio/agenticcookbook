<!-- leaf: implement-platform-integration/widgets-and-glanceable-surfaces · source: guidelines/implementing/platform-integration/widgets-and-glanceable-surfaces.md -->

**Rules** (cite as `implement-platform-integration/widgets-and-glanceable-surfaces#<slug>`):

- `frequently-checked-data-provide-widgets-glanceable-surfaces` SHOULD — Apps with time-sensitive or frequently checked data SHOULD provide widgets and glanceable surfaces on platforms that …
- `tapping-widget-deep-link-relevant-content` MUST — Tapping a widget MUST deep link to the relevant content in the app

# Widgets and glanceable surfaces

Apps with time-sensitive or frequently checked data SHOULD provide widgets and glanceable surfaces on platforms that support them. Widgets let users consume information and take action without launching the full app.

- Show only the most important information — widgets are not miniature apps
- Support multiple widget sizes when the platform offers them
- Tapping a widget MUST deep link to the relevant content in the app
- Update widget content on a reasonable cadence — balance freshness against battery and data usage

## Apple (iOS / macOS)

Use WidgetKit with SwiftUI views. Support small, medium, and large widget families. On iOS 17+, support interactive widgets with `AppIntent`-backed buttons and toggles. On iOS 16+, support Lock Screen widgets. Use `TimelineProvider` for scheduled updates and `WidgetCenter.shared.reloadTimelines` for event-driven refresh.

For real-time status, use Live Activities with `ActivityKit` and the Dynamic Island on supported devices.

## Android

Use Jetpack Glance with Compose-style APIs for home screen widgets. Define widget metadata in `appwidget-provider` XML. Support resizable widgets and respond to `onUpdate` broadcasts. Use `WorkManager` for background data refresh. Follow Material You theming for visual consistency with the system.

## Web (PWA)

Use the Badging API for app icon notification counts. Support periodic background sync via service workers for data freshness. Explore experimental Widget API proposals where available. On desktop PWAs, consider system tray or menu bar presence where the platform allows.
