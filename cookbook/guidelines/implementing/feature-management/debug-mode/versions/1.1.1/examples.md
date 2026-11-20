
Swift, iOS, shake to open, Debug only:

```swift
#if DEBUG
extension UIWindow {
    open override func motionEnded(_ motion: UIEvent.EventSubtype, with event: UIEvent?) {
        super.motionEnded(motion, with: event)
        if motion == .motionShake { DebugPanel.present(from: rootViewController) }
    }
}
#endif
```

Android, debug-only dependencies with a release no-op (Kotlin DSL):

```kotlin
android {
    buildTypes {
        release { isDebuggable = false }
    }
    // Needed on AGP 8+ only if src/main/ reads BuildConfig.DEBUG around the panel's entry point
    buildFeatures { buildConfig = true }
}

dependencies {
    debugImplementation("com.github.chuckerteam.chucker:library:<version>")
    releaseImplementation("com.github.chuckerteam.chucker:library-no-op:<version>")
}
```

C#, a debug-only helper whose calls are removed from Release, its body guarded so no panel reference remains:

```csharp
using System.Diagnostics;

static class DebugPanelLog
{
    [Conditional("DEBUG")]
    public static void Record(string eventName)
    {
#if DEBUG
        DebugPanel.EventLog.Add(eventName);
#endif
    }
}
```

TypeScript with Vite, the panel tree-shaken from production:

```typescript
if (import.meta.env.DEV) {
  const { mountDebugPanel } = await import('./debug/panel');
  mountDebugPanel();
}
```

