
Use `WorkManager` for all deferrable background work — it handles constraints, retries, and chaining. Use `ForegroundService` with a persistent notification for user-visible ongoing work (music playback, navigation, uploads). Respect Doze mode and App Standby buckets. Avoid `AlarmManager` for work that `WorkManager` can handle.

