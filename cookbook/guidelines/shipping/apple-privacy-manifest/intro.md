
# Ship a privacy manifest and declare required-reason APIs

This is an **enforced App Store submission gate**, not best-practice advice. Since **May 1, 2024**, App Store Connect rejects uploads that use a "required-reason" API without a declared reason, or that bundle a listed third-party SDK lacking a signed manifest. Treat a missing or incomplete `PrivacyInfo.xcprivacy` as a build-breaking error, not a warning.

