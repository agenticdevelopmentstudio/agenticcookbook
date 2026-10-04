
- The app **MUST** ship a `PrivacyInfo.xcprivacy` manifest declaring required-reason API usage and tracking/data-collection before submission.
- Before opening a PR that touches Foundation file/disk/uptime calls, `UserDefaults`, or adds a dependency, you **MUST** verify the manifest still covers all reached categories.
- You **MUST** match `NSPrivacyCollectedDataTypes` to the data the app actually collects; it **SHOULD** stay consistent with the App Store Connect privacy "nutrition label".
- Third-party SDKs on **Apple's list of commonly used SDKs** **MUST** ship their own signed `PrivacyInfo.xcprivacy`; you **MUST NOT** declare on their behalf. If a pinned SDK lacks one, update to a version that includes it or remove the dependency.

