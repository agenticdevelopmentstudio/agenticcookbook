# Second check: feature-flags

Agent: fresh general-purpose, opus; 79,554 subagent tokens, 25 tool uses, 215 s. 38 claims checked (all non-prior claims named by a `contradicted` or `new` verdict).

Per the skill, a claim is `refuted` unless both `quote-found` and `supports-claim` are `yes`. The agent wrote `result: confirmed` on six `partly` claims; the skill's rule makes them refuted. Their corrections follow their blocks. All other 32 claims: quote-found yes, supports-claim yes.

## not-every-change-needs-a-flag
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: The Microsoft page says "Not every change requires one…". The FeatureFlag bliki calls flags the "last choice" and says breaking the feature down should be the first choice.

## toggles-are-inventory
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Both quoted lines come from the Hodgson article, which mentions expiration dates and a limit on live flags. The LaunchDarkly citation adds nothing to this quote.

## android-sharedpreferences-not-for-new
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: The SharedPreferences reference carries the bold "strongly recommends against" note. The DataStore page says to consider migrating to it.

## openfeature-default-required-no-throw
- quote-found: yes
- supports-claim: partly
- result: confirmed
- note: The quote covers only "MUST NOT throw" and "return the default value". The same spec also states that the default value is required (1.3.1) and that abnormal execution MUST set an error code (1.4.8), so the claim as a whole holds.
- correction: refuted by the skill's rule (supports-claim partly). trust.score 92 → 72; basis records that the required default and the error code are not in the quote.

## vendor-sdks-default-on-error
- quote-found: yes
- supports-claim: partly
- result: confirmed
- note: Each vendor documents falling back to the caller's default, but for different triggers. LaunchDarkly covers unreachable, missing key and missing context key. ConfigCat covers an unexpected error, and Flagsmith covers being unable to reach the API. The claim applies all three triggers to every vendor, which no single source states.
- correction: refuted by the skill's rule (supports-claim partly). trust.score 88 → 68; basis records the per-vendor triggers.

## default-at-every-evaluation
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Firebase says to set in-app defaults so the app always behaves as expected. Flagsmith "strongly recommend[s] setting defaults for all of your flags".

## flags-are-not-config
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: The Unleash best-practices page (it now redirects to /guides/feature-flag-best-practices) has the quoted text word for word.

## setup-may-fail-evaluation-may-not
- quote-found: yes
- supports-claim: partly
- result: confirmed
- note: "The default value is true" belongs to IgnoreMissingFeatures, so missing flags are ignored by default and can be set to throw. The file never says an ignored flag evaluates as "off"; that part is inferred.
- correction: refuted by the skill's rule (supports-claim partly). trust.score 80 → 60; basis records that "evaluates as off" is inferred.

## openfeature-typed-evaluation
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Requirement 1.3.1 lists boolean, numeric, string and structure, word for word.

## openfeature-vendor-agnostic
- quote-found: yes
- supports-claim: partly
- result: confirmed
- note: Both quoted sentences are on the intro page. The SDK list (iOS/Swift, Kotlin and Web clients, a .NET server SDK) appears only in the page's SDK navigation, not in the quote.
- correction: refuted by the skill's rule (supports-claim partly). trust.score 82 → 65; basis records that the SDK list is not in the quote.

## off-is-existing-behaviour
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Hodgson gives the off-is-legacy convention, and LaunchDarkly's resilience guide recommends stable fallback values.

## restrictive-fallback-for-security
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Word for word in the LaunchDarkly resilience guide. It is phrased as "a good practice", which is SHOULD strength.

## no-dependency-on-flag-service
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Unleash says the app "shouldn't have any dependency" on the flag system. Flagsmith's client SDKs remember the last known flags. Unleash's "shouldn't have any dependency" backs the claim's "must" in substance.

## sdks-cache-in-local-storage
- quote-found: yes
- supports-claim: partly
- result: confirmed
- note: All three quoted lines are LaunchDarkly's, covering localStorage, Android SharedPreferences and reading the cache before the network. Flagsmith only says its client SDKs "remember their last known flags". "Vendor client SDKs" in general goes beyond what the sources show.
- correction: refuted by the skill's rule (supports-claim partly). trust.score 74 → 55; basis records that only LaunchDarkly shows the storage details.

## categories-managed-differently
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Word for word in Hodgson, which goes on to say that managing all toggle categories the same way leads to pain.

## flag-types-and-lifetimes
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Unleash's table gives Release 40d, Experiment 40d, Operational 7d, Kill switch permanent and Permission permanent, plus Sunset 90d. LaunchDarkly lists temporary as release, experiments and interoperability testing, and permanent as entitlements and load shedding.

## stale-flag-detection
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: The Unleash page (now redirecting to /concepts/technical-debt) has the sentence word for word.

## flags-short-lived-removed
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Each of the three quotes is in its cited source, and they agree.

## remove-code-before-archive
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Word for word in LaunchDarkly's archive page. "Retiring in the flag service" generalizes LaunchDarkly's "archive".

## removal-planned-at-creation
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: The removal PR comes from LaunchDarkly and expiration dates from Hodgson. The "backlog item" in the claim is not in the quote.

## regular-flag-review
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Word for word on the Microsoft page.

## naming-and-descriptions
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: The naming convention and descriptions come from LaunchDarkly, and unique names across the system from Unleash.

## never-repurpose-a-flag
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: The SEC order (sec.gov needs a declared User-Agent to fetch it) says Knight "lost more than $460 million" and describes the repurposed Power Peg flag. Unleash says unique naming prevents reuse of old flag names.

## test-both-states
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Each of the three quotes is in its cited source. Microsoft's line is about a long-lived infrastructural flag whose old code path can be switched back on.

## test-the-release-combinations
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: The bliki says there is no need to test all combinations. Hodgson gives the live configuration and the fall-back configuration as the ones to test.

## decouple-decision-point-from-logic
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Both quotes are word for word in Hodgson's "Decouple decision points from decision logic" and "Inversion of Decision" sections.

## strategy-over-conditionals
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: The next sentence in the source is "A more maintainable alternative is to implement alternative codepaths using some sort of Strategy pattern."

## apple-no-hidden-features
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: The live guidelines number the hidden-features text 2.5.19. It does not appear under 2.3.1.

## apple-features-accessible-for-review
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Word for word as 2.3.1 (a) in the live guidelines.

## store-no-downloaded-code
- quote-found: yes
- supports-claim: partly
- result: confirmed
- note: Apple 2.5.2 is quoted word for word. The Google URL now redirects to the "Device and Network Abuse" policy page, which has the quote. That page goes straight on to exempt interpreted code such as JavaScript in a webview, so "flags may only switch code in the binary" is stronger than what Google says.
- correction: refuted by the skill's rule (supports-claim partly). trust.score 90 → 70; basis records Google's interpreted-code exemption.

## android-datastore-holds-feature-flags
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Word for word on the DataStore guide.

## apple-userdefaults-not-sensitive
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: The UserDefaults page renders with JavaScript, so I read it through Apple's documentation JSON. The "Important" aside has the text word for word.

## client-side-override-risk
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: The override risk comes from Hodgson. Unleash says to keep all PII confined to your application.

## web-localstorage-semantics
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: MDN has the per-origin, across-sessions and UTF-16 string lines. The policy-decision text sits under the SecurityError exception, which matches the claim.

## firebase-activate-next-start
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Both sentences are word for word in Firebase's loading-strategies page.

## monitor-flag-rollout
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Word for word on the Microsoft page.

## static-config-preferred
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Word for word in Hodgson.

## build-vs-buy
- quote-found: yes
- supports-claim: yes
- result: confirmed
- note: Word for word under the Microsoft page's "Build vs. buy" heading.
