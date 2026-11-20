
# Debug mode

Apps include a debug-only configuration panel, holding feature flag overrides, an analytics event log, an A/B test variant picker and environment info, that is compiled out of release builds, not hidden in them: guard it at compile time (`#if DEBUG`, Android's debug source set and `debugImplementation`, a bundler-replaced constant), and keep release builds non-debuggable, their debug logging off and redacted, SDK developer modes off, secrets out of the client, debug traffic out of analytics and any production override guarded. Reach the panel by each platform's access method, choose new access gestures that do not redefine system or browser ones, and add only what the platform's own developer tools do not already show.

