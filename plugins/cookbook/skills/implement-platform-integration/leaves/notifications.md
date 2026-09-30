<!-- leaf: implement-platform-integration/notifications · source: guidelines/implementing/platform-integration/notifications.md -->

**Rules** (cite as `implement-platform-integration/notifications#<slug>`):

- `apps-use-platform-notification-system` SHOULD — Apps SHOULD use the platform notification system for timely, actionable alerts that respect user preferences. …
- `notification-actionable-tapping-deep-links` MUST — Every notification MUST be actionable — tapping it deep links to the relevant content

# Notifications

Apps SHOULD use the platform notification system for timely, actionable alerts that respect user preferences. Notifications are a shared system resource — misuse erodes trust and leads to users disabling them entirely.

- Request permission at the moment of relevance, not at launch
- Every notification MUST be actionable — tapping it deep links to the relevant content
- Support notification grouping and categories to reduce clutter
- Respect Do Not Disturb, Focus modes, and quiet hours

## Apple (iOS / macOS)

Use `UNUserNotificationCenter` for local and push notifications. Support actionable notifications with `UNNotificationCategory` and `UNNotificationAction`. On iOS, support Notification Summary and Time Sensitive interruption levels.

## Android

Use `NotificationCompat.Builder` for backward-compatible notifications. Declare notification channels (`NotificationChannel`) so users can control categories individually. Support Direct Reply, bubbles, and conversation style for messaging apps.

## Windows

Use `AppNotificationManager` + `AppNotificationBuilder` fluent API for local notifications. Support text, images, buttons with activation arguments, progress bars, and scheduled delivery. Handle notification activation alongside protocol activation. MSIX-packaged apps get notification identity automatically.

## Web

Use the Notifications API with service workers for push notifications. Request permission contextually. Support notification actions and badges via the Badging API. Fall back gracefully when notifications are denied or unavailable.
