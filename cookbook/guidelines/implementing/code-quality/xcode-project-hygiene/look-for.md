
Review project-file changes against Xcode project hygiene ([adc.guideline.implementing.code-quality.xcode-project-hygiene](cookbook:187a80eb-e2e5-4a6c-8d14-aa591840abe6)). Read the xcconfig, plist and entitlements diffs first; a large `project.pbxproj` diff is the symptom, not the change.

- `should-treat-project-files-as-source`: a project change that is large, hard to read in a diff, or defines a value in more than one place
- `should-put-build-settings-in-xcconfig`: A new or changed setting is in an `.xcconfig` file. Flag a setting added only through the project editor.
- `should-keep-shared-and-per-config-xcconfigs`: xcconfig files that repeat common settings per target, or restate settings they do not change
- `should-leave-target-level-settings-empty`: A target-level override hides an xcconfig value. Flag a setting defined at both levels.
- `should-create-xcconfig-without-targets`: an xcconfig file added to a target's bundle resources
- `should-look-up-setting-names`: Each setting name exists in the build settings reference.
- `must-share-and-check-in-schemes`: Every scheme a build or CI job uses is shared and checked in.
- `should-have-one-scheme-per-buildable-thing`: a thing people build, run or test with no scheme, or several schemes for one thing
- `should-delete-dead-schemes`: a scheme that no longer builds left in the project
- `should-name-targets-after-products`: No leftover `copy`, `Untitled` or dead scheme or target.
- `should-separate-test-targets`: test code compiled into an app target
- `should-set-deployment-target-explicitly`: Deployment targets are explicit.
- `should-add-entitlements-only-for-used-capabilities`: Every added or changed entitlement key has a reason in the change description and matches a capability the code uses. Removed capabilities have their keys removed.
- `should-keep-one-entitlements-file-per-need`: entitlements shared across targets or configurations that need different ones, or a file not referenced through `CODE_SIGN_ENTITLEMENTS`
- `must-not-copy-entitlements-wholesale`: No key was copied in from another app.
- `should-keep-info-plist-small`: an Info.plist carrying keys the app does not need
- `should-prefer-build-setting-substitution`: Versions and names come from build settings, not literals.
- `must-include-privacy-usage-descriptions`: Every API the diff starts to use has its usage-description key, with user-facing text.
- `should-remove-keys-for-removed-features`: Keys for removed features are gone.
- `should-put-team-and-signing-style-in-xcconfig`: Team ID and signing style are in the xcconfig.
- `should-use-automatic-local-explicit-release-signing`: a release build signed automatically, or with an undocumented identity
- `must-not-check-in-signing-secrets`: No certificate, private key or provisioning profile is added.
- `should-treat-xcodegen-spec-as-source`: If a project spec drives the project, the generated project is not hand-edited, and it matches the spec after regeneration.
- `should-keep-real-values-in-xcconfig-with-xcodegen`: setting values written into an XcodeGen spec's `settings` instead of the xcconfig its `configFiles` names
- `should-not-introduce-generator-in-unrelated-change`: a project generator added to a repository that had none, inside an unrelated change
