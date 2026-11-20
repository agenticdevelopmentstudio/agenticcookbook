# Phase 2, batch 6: security topics as roled parts

Format change only: each topic's text is now roled parts with one named-rules part and three bar parts, checked against base `0005775`. Every topic passes `cookr roles lossless --draft` and `cookr roles check`, and approve.py prints `RESULT: APPROVED`. No topic has an `obsolete` entry, because `roles lossless` never lets a base sentence be obsolete. The contradictions under R4 are quoted and left as they are.

## cookbook/guidelines/implementing/security/agent-guardrails

commit 067a0119; rules 19; moved 6; obsolete 0

not promoted, reworded: must-enforce-guardrails-as-code (intro "They MUST be enforced...")

existing rule names kept.

**promoted** (5):
- `should-validate-and-moderate-model-input`: before "Validate and moderate everything reaching the model." → after "Everything reaching the model **SHOULD** be validated and moderated."
- `should-treat-model-output-as-untrusted`: before "Treat all model output as untrusted until it has passed checks (see ...)." → after "All model output **SHOULD** be treated as untrusted until it has passed checks (see [adc.guideline.implementing.security.llm-application-security](cookbook:a8088a6a-4542-4f6c-b74a-7c7ef7dcc63d))."
- `should-constrain-agency-to-minimum`: before "Constrain agency to the minimum required (OWASP LLM06:2025 Excessive Agency)." → after "Agency **SHOULD** be constrained to the minimum required (OWASP LLM06:2025 Excessive Agency)."
- `should-confirm-privacy-obligations-with-counsel`: before "> Privacy and PII handling here is engineering guidance, not legal advice; confirm obligations with counsel." → after "Privacy and PII handling here is engineering guidance, not legal advice; obligations **SHOULD** be confirmed with counsel."
- `should-start-with-in-process-checks`: before "Heavy controls (...) are adopt-when-measured-need-justifies per YAGNI — start with in-process deterministic checks." → after "Heavy controls (managed moderation services, dedicated policy engines, sidecar enforcement) are adopt-when-measured-need-justifies per YAGNI — guardrails **SHOULD** start with in-process deterministic checks."

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions** (R4, left unfixed):
- three promoted SHOULD section lead-ins restate MUST rules beneath them (validate/moderate input vs off-band-input MUST; output untrusted vs deterministic-output-checks MUST; constrain agency vs allow-list/least-privilege MUST).
  - `off-band-input`: "The system **MUST** screen input for prompt injection, jailbreaks, off-topic requests, and unsafe content before it reaches the model."
  - `deterministic-output-checks`: "Output guardrails **MUST** be enforced deterministically — schema/JSON validation, PII and secret detection, and unsafe-content moderation run in code, not by asking the model to self-certify."
  - `least-privilege`: "Each tool **MUST** run with the narrowest scopes, credentials, and data access needed — no shared admin tokens."

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/authentication

commit ccc37621; rules 10; moved 13; obsolete 0

rationale line added restating "per platform" so the lead-in "**Per-platform auth flow:**" maps; "References:" kept verbatim in references part.

**promoted** (8):
- `should-use-oauth-oidc-with-pkce-for-public-clients`: before "Use OAuth 2.0 / OpenID Connect with PKCE for all public clients." kept also as intro statement → after "OAuth 2.0 / OpenID Connect with PKCE **SHOULD** be used for all public clients."
- `should-use-system-browser-auth-flow-on-native-platforms`: before "**Native apps (iOS/Android/Windows):** Authorization Code + PKCE via the system browser (...)" → after "Native apps (iOS/Android/Windows) **SHOULD** use Authorization Code + PKCE via the system browser (`ASWebAuthenticationSession`, Custom Tabs, `WebAuthenticationBroker`)."
- `should-use-auth-code-pkce-flow-on-spa-platforms`: before "**SPAs:** Authorization Code + PKCE." → after "SPAs **SHOULD** use Authorization Code + PKCE."
- `should-consider-bff-for-spas`: before "Consider a Backend-for-Frontend (BFF) pattern ..." → after "SPAs **SHOULD** consider a Backend-for-Frontend (BFF) pattern where the SPA never handles tokens directly — the BFF holds tokens server-side in HttpOnly cookies."
- `should-use-client-credentials-flow-on-server-platforms`: before "**Server-to-server:** Client Credentials flow." → after "Server-to-server auth **SHOULD** use the Client Credentials flow."
- `should-use-short-lived-access-tokens-in-session-management`: before "Short-lived access tokens (5-15 minutes)" → after "Access tokens **SHOULD** be short-lived (5-15 minutes)."
- `should-invalidate-token-family-on-refresh-reuse`: before "Detect reuse of a revoked refresh token and invalidate the entire token family." → after "Reuse of a revoked refresh token **SHOULD** be detected, and the entire token family invalidated."
- `should-enforce-absolute-session-timeouts`: before "Absolute session timeouts server-side" → after "Absolute session timeouts **SHOULD** be enforced server-side."

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions**: none found.

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/authorization

commit d5b66531; rules 9; moved 13; obsolete 0

**promoted** (6):
- `should-enforce-all-access-control-server-side`: before "Enforce all access control server-side." also kept as intro statement → after "All access control **SHOULD** be enforced server-side."
- `must-not-use-client-side-checks-as-security-controls`: before "...are UX conveniences — never security controls." never→MUST NOT → after "Client-side checks (hiding buttons, disabling fields) are UX conveniences and **MUST NOT** be used as security controls."
- `should-enforce-permission-check-per-endpoint`: before "Each endpoint enforces its own permission check." → after "Each endpoint **SHOULD** enforce its own permission check."
- `should-define-roles-with-minimal-permissions`: before "**RBAC** — define roles with minimal permissions." → after "RBAC roles **SHOULD** be defined with minimal permissions."
- `should-prefer-fine-grained-permissions-in-roles`: before "Prefer fine-grained permissions composed into roles over monolithic role checks." → after "Fine-grained permissions composed into roles **SHOULD** be preferred over monolithic role checks."
- `must-not-treat-known-id-as-access`: before "Never assume "if they know the ID, they have access."" → after "Code **MUST NOT** assume "if they know the ID, they have access.""

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions** (R4, left unfixed):
- intro "Enforce all access control server-side" promoted to SHOULD while the rationale says server-side authorization is the only real authorization and client checks MUST NOT be controls.

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/consent-management

commit 50e0aac0; rules 22; moved 11; obsolete 0

level from lead-in (not promoted): must-be-informed / must-be-unambiguous / must-be-freely-given take MUST from "Per GDPR Art. 7 (and similar regimes), consent **MUST** be:"; the lead-in maps to [rationale, must-be-freely-given] (4 targets refused, not read as framing).

**promoted** (6):
- `should-confirm-obligations-with-counsel-per-jurisdiction`: before "...not legal advice — confirm obligations with counsel for each jurisdiction." → after "This is engineering guidance for building consent flows, not legal advice — obligations **SHOULD** be confirmed with counsel for each jurisdiction."
- `should-persist-decisions-append-only`: before "Persist each decision as an **append-only, immutable** record." → after "Each decision **SHOULD** be persisted as an **append-only, immutable** record."
- `should-store-consent-notice-text-or-hash`: before "Store the exact consent-notice text or a content hash so you can prove what the user saw." → after "The exact consent-notice text or a content hash **SHOULD** be stored so you can prove what the user saw."
- `should-pin-policy-to-versioned-revision`: before "Pin the policy to a dated, versioned revision." → after "The policy **SHOULD** be pinned to a dated, versioned revision."
- `should-re-request-consent-on-change`: before "Re-request consent when the purpose changes, ..." → after "Consent **SHOULD** be re-requested when the purpose changes, a new data category is added, or a new processor is introduced."
- `should-set-reconfirmation-cadence`: before "Set a re-confirmation cadence for long-lived consent (commonly revisited at 12–24 months) per applicable guidance and risk." → after "A re-confirmation cadence **SHOULD** be set for long-lived consent (commonly revisited at 12–24 months) per applicable guidance and risk."

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions** (R4, left unfixed):
- should-persist-decisions-append-only (SHOULD, promoted from "Persist...") sits beside must-not-overwrite-consent-entries (MUST NOT overwrite or delete) — the MUST NOT makes append-only effectively mandatory.
  - `should-persist-decisions-append-only`: "Each decision **SHOULD** be persisted as an **append-only, immutable** record."
  - `must-not-overwrite-consent-entries`: "**MUST NOT** overwrite or delete prior entries — withdrawal is a new event, not a mutation."

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/content-security-policy

commit 6e4e7717; rules 9; moved 16; obsolete 0

"Harden those sinks separately:" lead-in maps to the four TT rules; rationale part carries it and the DOM-XSS sentence.

**promoted** (2):
- `should-start-strict-from-default-src-none`: before "**Start strict:** `default-src 'none'` then add only what is needed" → after "A policy **SHOULD** start strict: `default-src 'none'` then add only what is needed."
- `should-set-frame-ancestors-self`: before "**`frame-ancestors 'self'`** to prevent clickjacking (replaces X-Frame-Options)" → after "A policy **SHOULD** set `frame-ancestors 'self'` to prevent clickjacking (replaces X-Frame-Options)."

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions**: none found.

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/cors

commit 190a6a8e; rules 9; moved 11; obsolete 0

"Wildcard origin with credentials" (misconfiguration item) maps to the existing MUST NOT rule must-not-use-wildcard-with-credentials plus rationale.

**promoted** (6):
- `should-not-enable-cors-unless-configured-correctly`: before "Cross-Origin Resource Sharing — get it right or don't enable it." kept also as intro → after "CORS **SHOULD** be configured correctly or not enabled at all."
- `should-maintain-explicit-origin-allowlist`: before "Maintain an explicit allowlist of origins." → after "An explicit allowlist of origins **SHOULD** be maintained."
- `should-minimize-exposed-headers`: before "**Minimize exposed headers:** Only what the client actually needs." → after "Exposed headers **SHOULD** be minimized: only what the client actually needs."
- `should-not-match-origins-with-unanchored-regex`: before "Regex matching without anchoring (...)" under "Common misconfigurations:" → after "Origins **SHOULD NOT** be matched by regex without anchoring (`evil-example.com` matching `example.com`)."
- `should-not-allow-null-origin`: before "Allowing `null` origin (exploitable via sandboxed iframes)" → after "The `null` origin **SHOULD NOT** be allowed (exploitable via sandboxed iframes)."
- `should-not-allow-broad-methods-and-headers`: before "Overly broad allowed methods and headers" → after "Allowed methods and headers **SHOULD NOT** be overly broad."

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions**: none found.

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/data-subject-rights

commit 7636ea62; rules 23; moved 12; obsolete 0

level from lead-in: six must-support-*-requests rules take MUST from "Under GDPR Chapter 3 (...), an agent **MUST** be able to satisfy each request type:"; must-erase-every-derived-copy / must-propagate-erasure-to-processors / must-document-backup-rescrub-window take MUST from "Deletion **MUST** reach every derived copy, not just the primary row:" (its "document the rotation window" imperative is read at that MUST). should-pseudonymize-or-crypto-shred-logs keeps "prefer" as SHOULD under the MUST reach.

rights table kept verbatim as how-to part the-rights-to-support (its rows also carried by the six rules).

**promoted** (3):
- `should-confirm-rights-with-counsel`: before "> Engineering guidance only — NOT legal advice." / "Confirm rights, scope, exemptions, and deadlines with counsel for your jurisdictions." → after "Engineering guidance only — NOT legal advice. Rights, scope, exemptions, and deadlines **SHOULD** be confirmed with counsel for your jurisdictions."
- `should-authenticate-against-session-or-verified-channel`: before "Authenticate against an existing session or a verified channel; ..." → after "The requester **SHOULD** be authenticated against an existing session or a verified channel."
- `should-track-per-request-sla`: before "Track per-request SLA and alert before breach." → after "You **SHOULD** track per-request SLA and alert before breach."

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions**: none found.

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/dependency-security

commit 4a47aba2; rules 16; moved 25; obsolete 0

rationale line "These constrain what an agent can pull." added so the "Constrain what it can pull:" lead-in maps.

**promoted** (8):
- `should-manage-dependencies-actively`: before "Manage them actively." → after "Dependencies **SHOULD** be managed actively."
- `should-use-locked-installs-in-ci`: before "Use `--frozen-lockfile` / `npm ci` / `dotnet restore --locked-mode` in CI." → after "CI **SHOULD** use `--frozen-lockfile` / `npm ci` / `dotnet restore --locked-mode`."
- `should-pin-dependencies`: before "**Pin dependencies** — exact versions or narrow ranges." → after "Dependencies **SHOULD** be pinned: exact versions or narrow ranges."
- `should-use-sri-for-cdn-assets`: before "**Subresource Integrity (SRI)** — for any CDN-hosted scripts/styles, use `integrity` attributes with SHA-384/SHA-512 hashes." → after "For any CDN-hosted scripts/styles, `integrity` attributes with SHA-384/SHA-512 hashes **SHOULD** be used (Subresource Integrity, SRI)."
- `should-watch-for-supply-chain-attacks`: before "**Watch for supply chain attacks** — typosquatting, ..." → after "Supply chain attacks **SHOULD** be watched for — typosquatting, maintainer compromise, malicious post-install scripts, dependency confusion (internal/public name collisions)."
- `should-enforce-package-allowlist-deterministically`: before "**Allowlist, enforced deterministically** — scope an explicit package/registry allowlist ... NOT prompt text." → after "An explicit package/registry allowlist **SHOULD** be scoped to the task or session and enforced through DETERMINISTIC gates (pre-install hooks, CI checks, sandbox policy), NOT prompt text."
- `should-apply-registry-cooldown`: before "**Registry cooldown** — apply a cooldown window ..." → after "A cooldown window (e.g. pip's dependency cooldown) **SHOULD** be applied so brand-new releases are not auto-pulled, reducing exposure to freshly compromised versions."
- `should-verify-package-exists-and-is-maintained`: before "before adding a candidate package, confirm it actually exists and is actively maintained" → after "Before adding a candidate package, the agent **SHOULD** confirm it actually exists and is actively maintained (verify existence and maintenance: anti-slopsquatting)."

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions** (R4, left unfixed):
- should-pin-dependencies (SHOULD, promoted) vs must-not-use-wildcard-versions (MUST NOT): consistent but levels differ. "Lockfiles are mandatory" + MUST committed fine. Duplicate References list (in both base parts) merged into one references part; the cross-reference link moved there.
  - `should-pin-dependencies`: "Dependencies **SHOULD** be pinned: exact versions or narrow ranges."
  - `must-not-use-wildcard-versions`: "Wildcard (`*`) or overly broad semver MUST NOT be used."

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/input-validation

commit a7d315c7; rules 17; moved 24; obsolete 0

lowercase keyword kept at its level: must-duplicate-validation-server-side ("All validation must be duplicated server-side." → MUST).

**promoted** (7):
- `must-not-trust-client-input`: before "**Never trust client input.**" never→MUST NOT → after "Client input **MUST NOT** be trusted."
- `should-validate-sanitize-escape-in-order`: before "**Validate, sanitize, escape** — in that order." → after "Input **SHOULD** be validated, sanitized, then escaped — in that order."
- `should-encode-output-per-context`: before "**Output encoding** — context-dependent: HTML-encode for HTML, URL-encode for URLs." → after "Output encoding **SHOULD** be context-dependent: HTML-encode for HTML, URL-encode for URLs."
- `should-use-framework-auto-escaping`: before "Use framework auto-escaping (React JSX, Django templates) and understand when it does NOT apply" → after "You **SHOULD** use framework auto-escaping (React JSX, Django templates) and understand when it does NOT apply (e.g., raw HTML insertion APIs)."
- `must-sanitize-before-raw-html-insertion`: before "(e.g., raw HTML insertion APIs — always sanitize with a library like DOMPurify first)." always→MUST → after "Input to raw HTML insertion APIs **MUST** always be sanitized with a library like DOMPurify first."
- `should-limit-upload-size`: before "Limit size." → after "File upload size **SHOULD** be limited."
- `should-store-uploads-outside-web-root`: before "Store outside web root." → after "Uploaded files **SHOULD** be stored outside web root."

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions**: none found.

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/llm-application-security

commit 81cbf8bc; rules 29; moved 16; obsolete 0

level from parent: must-not-pass-output-to-shell / must-parameterize-output-in-sql / must-encode-output-for-html / must-validate-tool-arguments take MUST from their parent "You **MUST** sanitize, encode, or parameterize model output..." (sub-bullets had no keyword of their own, except the MUST NOTs).

**promoted** (8):
- `should-map-controls-to-owasp-llm-top-10-2025`: before "Map your controls to the OWASP Top 10 for LLM Applications **2025** (pin that revision; ...)" → after "You **SHOULD** map your controls to the OWASP Top 10 for LLM Applications **2025** (pin that revision; renumbering and category shifts between editions)."
- `should-apply-request-body-egress-controls`: before "Apply the same egress controls you would to a raw HTTP request body." → after "You **SHOULD** apply the same egress controls to model output you would to a raw HTTP request body."
- `should-not-count-prompt-instructions-as-control`: before "Treat "the model was told not to" as no control at all." → after "You **SHOULD** treat "the model was told not to" as no control at all."
- `should-limit-capability-permissions-autonomy`: before "Limit blast radius by limiting capability, permissions, and autonomy." → after "You **SHOULD** limit blast radius by limiting capability, permissions, and autonomy."
- `should-describe-concrete-effect-in-confirmation`: before "Make the confirmation describe the concrete effect, not just "approve?"." → after "You **SHOULD** make the confirmation describe the concrete effect, not just "approve?"."
- `should-pin-models-and-verify-provenance`: before "**LLM03 Supply Chain** / **LLM04 Data and Model Poisoning** — pin model versions, verify provenance of models, datasets, and plugins." → after "**LLM03 Supply Chain** / **LLM04 Data and Model Poisoning** — you **SHOULD** pin model versions, verify provenance of models, datasets, and plugins."
- `should-mark-generated-content-unverified`: before "**LLM09 Misinformation** — surface citations and mark generated content as unverified" → after "**LLM09 Misinformation** — you **SHOULD** surface citations and mark generated content as unverified."
- `should-not-present-output-as-authoritative`: before "do not present model output as authoritative fact in safety-critical flows" → after "You **SHOULD NOT** present model output as authoritative fact in safety-critical flows (LLM09 Misinformation)."

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions** (R4, left unfixed):
- should-apply-least-privilege-against-injection (SHOULD) vs must-grant-least-privilege (MUST) — same control at two levels. should-not-count-prompt-instructions-as-control is SHOULD (promoted plain imperative) though it states "no control at all".
  - `should-apply-least-privilege-against-injection`: "You **SHOULD** apply least-privilege so a successful injection cannot reach high-impact tools (see Excessive Agency below)."
  - `should-not-count-prompt-instructions-as-control`: "You **SHOULD** treat "the model was told not to" as no control at all."
  - `must-grant-least-privilege`: "You **MUST** grant each agent/tool the least privilege needed — scoped credentials, narrow API surface, no ambient admin access."

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/mcp-input-validation

commit f511352f; rules 25; moved 10; obsolete 0

kept verbatim with mixed levels: must-reject-unknown-properties ("Validate with a JSON Schema 2020-12 validator ... and **MUST** reject"), must-not-cache-authorization-across-privilege-boundary ("Re-check ... on **every** tool invocation ...; **MUST NOT** cache"), must-not-auto-dereference-external-refs (holds MUST NOT + SHOULD bound depth/time in one rule; the lossless matcher would not split it).

**promoted** (13):
- `should-pin-mcp-spec-revision`: before "Pin guidance to the MCP spec revision dated **2025-06-18** ..." → after "You **SHOULD** pin guidance to the MCP spec revision dated **2025-06-18** (tool `inputSchema` is JSON Schema **2020-12**)."
- `should-define-explicit-schema-constraints`: before "Define `inputSchema` with explicit `type`, ... and numeric bounds" → after "You **SHOULD** define `inputSchema` with explicit `type`, `required`, `enum`, `pattern`, `minLength`/`maxLength`, and numeric bounds."
- `should-scope-downstream-to-least-privilege`: before "Scope downstream actions to the least privilege the host-process identity holds" → after "You **SHOULD** scope downstream actions to the least privilege the host-process identity holds."
- `must-not-widen-privilege-from-arguments`: before "never widen privilege based on a tool argument" never→MUST NOT → after "You **MUST NOT** ever widen privilege based on a tool argument."
- `should-confine-file-paths`: before "**File paths**: canonicalize ... and confine to an allowlisted root; reject paths that escape it." → after "**File paths**: you **SHOULD** canonicalize (resolve symlinks + `..`) and confine to an allowlisted root; reject paths that escape it. Treat path traversal as a primary attack on file tools."
- `should-block-ssrf`: before "**URL arguments**: block SSRF — ..." → after "**URL arguments**: you **SHOULD** block SSRF — allowlist schemes/hosts, resolve and reject private, loopback, and link-local IP ranges, and disable redirects to disallowed targets."
- `should-use-parameterized-queries-only`: before "**Database**: use parameterized queries only" → after "**Database**: you **SHOULD** use parameterized queries only."
- `should-scope-queries-to-authorized-tenant`: before "scope every query to the authorized tenant/row set" → after "You **SHOULD** scope every query to the authorized tenant/row set."
- `must-not-interpolate-arguments-into-queries`: before "never interpolate an argument into SQL or a query path" never→MUST NOT → after "You **MUST NOT** ever interpolate an argument into SQL or a query path."
- `should-avoid-shell-invocation`: before "**Shell/OS**: avoid shell invocation; if unavoidable, pass arguments as an argv array ... and allowlist the executable." → after "**Shell/OS**: you **SHOULD** avoid shell invocation; if unavoidable, pass arguments as an argv array and allowlist the executable."
- `must-not-pass-concatenated-shell-string`: before "(never a concatenated string)" never→MUST NOT → after "Shell arguments **MUST NOT** ever be passed as a concatenated string."
- `should-log-failures-and-denials`: before "Log validation failures and authorization denials with the tool name and caller identity (not raw argument payloads)" → after "You **SHOULD** log validation failures and authorization denials with the tool name and caller identity (not raw argument payloads)."
- `should-return-non-leaky-errors`: before "Return structured, non-leaky errors on rejection — fail closed, surface a stable error code" → after "You **SHOULD** return structured, non-leaky errors on rejection — fail closed, surface a stable error code."

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions** (R4, left unfixed):
- should-confine-file-paths / should-block-ssrf / should-use-parameterized-queries-only / should-avoid-shell-invocation are promoted SHOULDs that implement must-sanitize-and-bound-before-side-effects (MUST); should-use-parameterized-queries-only (SHOULD) vs must-not-interpolate-arguments-into-queries (MUST NOT).
  - `must-sanitize-and-bound-before-side-effects`: "Handlers **MUST** sanitize and bound any argument before it reaches a side effect (filesystem, network, DB, shell, downstream API)."
  - `should-confine-file-paths`: "**File paths**: you **SHOULD** canonicalize (resolve symlinks + `..`) and confine to an allowlisted root; reject paths that escape it. Treat path traversal as a primary attack on file tools."
  - `should-block-ssrf`: "**URL arguments**: you **SHOULD** block SSRF — allowlist schemes/hosts, resolve and reject private, loopback, and link-local IP ranges, and disable redirects to disallowed targets."
  - `should-use-parameterized-queries-only`: "**Database**: you **SHOULD** use parameterized queries only."
  - `must-not-interpolate-arguments-into-queries`: "You **MUST NOT** ever interpolate an argument into SQL or a query path."
  - `should-avoid-shell-invocation`: "**Shell/OS**: you **SHOULD** avoid shell invocation; if unavoidable, pass arguments as an argv array and allowlist the executable."

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/mcp-server-security

commit 2916e738; rules 22; moved 8; obsolete 0

threat-classes table kept verbatim as a second rationale part.

**promoted** (5):
- `should-treat-server-strings-and-tokens-as-untrusted`: before "Treat every string the server emits as model-influencing input and every token it receives as untrusted." → after "You **SHOULD** treat every string the server emits as model-influencing input and every token it receives as untrusted."
- `should-pin-mcp-spec-revision`: before "Pin guidance to the MCP spec revision dated **2025-06-18** ..." → after "You **SHOULD** pin guidance to the MCP spec revision dated **2025-06-18** (Security Best Practices + Authorization), which carries the normative MUST/MUST NOT statements below."
- `should-act-as-oauth-resource-server`: before "Treat a remote MCP server as an OAuth 2.1 **resource server**." → after "You **SHOULD** treat a remote MCP server as an OAuth 2.1 **resource server**."
- `should-use-token-exchange-downstream`: before "To call a downstream service, use a token-exchange flow to obtain a distinct token, or act as its own client." → after "To call a downstream service, the server **SHOULD** use a token-exchange flow to obtain a distinct token, or act as its own client."
- `should-prefer-egress-proxy-and-dns-pinning`: before "Prefer an egress proxy and DNS-pinning over hand-rolled IP parsing, ..." → after "You **SHOULD** prefer an egress proxy and DNS-pinning over hand-rolled IP parsing, which misses octal/hex/IPv4-mapped-IPv6 encodings."

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions** (R4, left unfixed):
- threat table says token passthrough is "FORBIDDEN" and session row "never authenticate via session" (consistent with MUST NOT rules); the ACCURACY NOTE (kept in rationale) carries an author instruction "do not cite those CVEs as motivation for server authoring" — an instruction about the doc's own content, not code, so it was not made a rule; flagged.

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/passkeys-and-webauthn

commit f05c8455; rules 23; moved 13; obsolete 0

level from text: must-not-reuse-or-omit-challenge-verification ("Reusing or omitting server-side challenge verification (replay risk) — **MUST NOT**.")

**promoted** (13):
- `should-target-webauthn-level-2`: before "Target the **W3C WebAuthn Level 2 Recommendation** ..." → after "You **SHOULD** target the **W3C WebAuthn Level 2 Recommendation** (`webauthn-2`) for stable, broadly-implemented behavior."
- `should-not-depend-on-webauthn-level-3-features`: before "FORECAST: treat its newer features ... as evolving; do not depend on them as universally available until they reach Recommendation." → after "**WebAuthn Level 3** (`webauthn-3`) is a **W3C Candidate Recommendation (2026-01-13)** — FORECAST: you **SHOULD** treat its newer features (e.g. refined attestation, related-origin requests) as evolving; you **SHOULD NOT** depend on them as universally available until they reach Recommendation."
- `should-set-rp-id-to-registrable-domain`: before "Set `rp.id` to the registrable domain" → after "You **SHOULD** set `rp.id` to the registrable domain."
- `should-use-opaque-user-id`: before "set `user.id` to an opaque, stable, non-PII handle (not an email)" → after "You **SHOULD** set `user.id` to an opaque, stable, non-PII handle (not an email)."
- `should-store-credential-metadata`: before "Store the credential id, public key, signature counter, transports, and the AAGUID for later UX." → after "You **SHOULD** store the credential id, public key, signature counter, transports, and the AAGUID for later UX."
- `should-issue-fresh-challenge-per-attempt`: before "Issue a fresh server-side `challenge` per attempt; verify origin, ..." → after "You **SHOULD** issue a fresh server-side `challenge` per authentication attempt; verify origin, `rp.id`, UP flag, and signature against the stored public key."
- `should-prefer-discoverable-credentials`: before "Prefer **discoverable credentials** ..." → after "You **SHOULD** prefer **discoverable credentials** (resident keys) so users authenticate without first entering a username."
- `should-request-attestation-only-when-needed`: before "Request attestation (`attestation: "direct"`) **only** when policy needs ..." → after "You **SHOULD** request attestation (`attestation: "direct"`) **only** when policy needs to verify authenticator make/model. MEASURED-NEED: adopt attestation verification ONLY when a concrete requirement (e.g. regulated environment, hardware allowlist) justifies it (per YAGNI)."
- `should-use-attestation-none-for-consumers`: before "Use `attestation: "none"` for consumer flows." → after "You **SHOULD** use `attestation: "none"` for consumer flows."
- `should-provide-account-recovery-path`: before "Provide an explicit, rate-limited account-recovery path ..." → after "You **SHOULD** provide an explicit, rate-limited account-recovery path (e.g. verified email magic link plus identity proofing) for users who lose all authenticators."
- `must-allow-registering-additional-passkeys`: before "Always allow registering additional passkeys from an authenticated session." always→MUST → after "You **MUST** always allow registering additional passkeys from an authenticated session."
- `should-not-set-rp-id-outside-auth-origin`: before anti-pattern "Setting `rp.id` to a host that doesn't cover the auth origin." → after "You **SHOULD NOT** set `rp.id` to a host that doesn't cover the auth origin."
- `should-not-treat-passkey-as-bearer-secret`: before anti-pattern "Treating a passkey as a bearer secret or syncing the RP private key (there is none server-side)." → after "You **SHOULD NOT** treat a passkey as a bearer secret or sync the RP private key (there is none server-side)."

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions** (R4, left unfixed):
- should-issue-fresh-challenge-per-attempt (SHOULD, promoted) vs must-not-reuse-or-omit-challenge-verification (MUST NOT) and must-generate-random-challenge (MUST): same requirement at two levels. should-make-passkeys-primary-factor holds "never the inverse" under a SHOULD. should-offer-passkeys-as-primary and should-make-passkeys-primary-factor overlap.
  - `should-offer-passkeys-as-primary`: "New apps **SHOULD** offer passkeys as the primary authenticator."
  - `must-generate-random-challenge`: "The RP backend **MUST** generate a cryptographically random `challenge` (≥16 bytes), bind it to the session, and verify it server-side on return."
  - `should-issue-fresh-challenge-per-attempt`: "You **SHOULD** issue a fresh server-side `challenge` per authentication attempt; verify origin, `rp.id`, UP flag, and signature against the stored public key."
  - `should-make-passkeys-primary-factor`: "Passkeys **SHOULD** be the primary factor; passwords, if kept, are a fallback — never the inverse."
  - `must-not-reuse-or-omit-challenge-verification`: "You **MUST NOT** reuse or omit server-side challenge verification (replay risk)."

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/pii-detection-and-redaction

commit 3a1ce0b9; rules 24; moved 32; obsolete 0

existing labelled bullets kept their names.

lowercase keyword kept: assume-public-credentials-compromised ("a purged credential that was public must be assumed compromised" → MUST).

**promoted** (19):
- `use-a-coverage-checklist`: before "enumerate categories against a fixed list so you do not miss a type." → after "You **SHOULD** enumerate categories against a fixed list so you do not miss a"
- `linked-and-linkable`: before "Rate each instance's confidentiality impact ... and size controls to the impact." → after "Per NIST SP 800-122, PII is anything that *distinguishes or traces*"
- `detect-in-layers`: before "combine rule-based and ML detection" → after "You **SHOULD** combine rule-based and ML detection (the approach"
- `regex-for-structured`: before "use anchored patterns for structured types ..." → after "You **SHOULD** use anchored patterns for structured types (email, phone, SSN,"
- `ner-for-unstructured`: before "use a Named-Entity-Recognition model ... and register custom recognizers" → after "You **SHOULD** use a"
- `favor-recall`: before "tune toward **recall** (optimize the F2 / β=2 score ...) and triage false positives after." → after "You **SHOULD** tune toward **recall**"
- `should-not-ship-precision-chosen-detector`: before "Do not ship a detector chosen for a clean precision number." → after "You **SHOULD NOT** ship a detector chosen for a clean precision number."
- `default-deny`: before "where feasible, allowlist what may leave the boundary rather than blocklist what must be hidden." → after "Where feasible, you **SHOULD** allowlist what may leave the boundary rather than blocklist"
- `drop-structurally`: before "remove PII-bearing fields at the schema or serialization boundary ..." → after "You **SHOULD** remove PII-bearing fields at the schema or serialization boundary, not"
- `pick-operation-by-need`: before "pick by whether you need reversibility or downstream utility." → after "You **SHOULD** pick the redaction operation by whether you need reversibility or downstream utility."
- `redact-published-data`: before "The default for published or exported data." → after "Redaction **SHOULD** be the default for published or exported data."
- `pseudonymized-is-not-anonymized`: before "do NOT treat pseudonymized data as anonymized." → after "You **SHOULD NOT** treat pseudonymized data as anonymized: it is"
- `generalize-and-suppress`: before "coarsen ... or drop entirely; bound linkage risk ..." → after "For quasi-identifiers, you **SHOULD** coarsen (year not date, 3-digit ZIP, age"
- `anonymization`: before "only call data anonymized when re-identification is not reasonably feasible" → after "You **SHOULD** only call data anonymized when re-identification is not reasonably feasible"
- `defense-in-depth`: before "layer independent gates ..." → after "You **SHOULD** layer independent gates (surface reduction → structural drop → prose"
- `golden-tests`: before "keep a known-leaky fixture and assert end-to-end that nothing survives." → after "You **SHOULD** keep a known-leaky fixture and assert end-to-end that nothing survives."
- `freeze-edge-cases`: before "Freeze real edge cases as regression tests ..." → after "You **SHOULD** freeze real edge cases as regression tests — e.g. a `git@github.com:` SSH remote that looks"
- `scan-history-not-just-the-tip`: before "Treat a public repo's history as part of the exposed surface." → after "You **SHOULD** treat a public repo's history as part of the exposed surface."
- `remediate-then-rotate`: before "purge with `git filter-repo` ..., force-update the remote, and **rotate** any exposed secret" → after "You **SHOULD** purge with `git filter-repo` (or BFG Repo-Cleaner), force-update"

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions** (R4, left unfixed):
- pseudonymized-is-not-anonymized made SHOULD NOT from emphatic "do NOT" (GDPR fact suggests MUST NOT); flagged. remediate-then-rotate (SHOULD rotate) vs assume-public-credentials-compromised (MUST).
  - `pseudonymized-is-not-anonymized`: "You **SHOULD NOT** treat pseudonymized data as anonymized: it is"
  - `remediate-then-rotate`: "You **SHOULD** purge with `git filter-repo` (or BFG Repo-Cleaner), force-update"
  - `assume-public-credentials-compromised`: "A purged credential that was public **MUST** be assumed compromised."

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/pii-handling

commit 44857735; rules 14; moved 14; obsolete 0

**promoted**: none (every labelled bullet already carried MUST/SHOULD; plain imperatives inside them — "Tag it in the schema", "Drop a field rather than keep it", "Redact or hash identifiers at the logging boundary", "pin the region in infrastructure config" — stay as detail of their keyworded rule). Intro kept verbatim (its MUST restates classify-fields). Rule text gained "(propagate the tags)" and "the minimum:" so the labels' words survive.

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions** (R4, left unfixed):
- none found.

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/privacy

commit e050e031; rules 21; moved 31; obsolete 0

platform parts (swift, kotlin, typescript, c) held only requirements, so they became "On <platform>, …" rules (like logging) and the parts were removed. The intro's duplicated "# Privacy" summary merged into the same rules.

lowercase keyword kept: must-build-privacy-in-from-day-one ("Privacy and security must be built in from day one."), must-remain-functional-when-denied ("Honor \"deny\" gracefully — the app must remain functional." / "Respect user consent: app must remain functional if optional data collection is denied").

**promoted** (16):
- `should-collect-only-what-is-needed`: before "Collect only what is needed." → after "You **SHOULD** collect only what is needed (data minimization)."
- `should-prefer-on-device-processing`: before "Prefer on-device processing." → after "You **SHOULD** prefer on-device processing."
- `should-require-opt-in-for-non-essential-data`: before "Opt-in for non-essential data collection." → after "You **SHOULD** require opt-in for non-essential data collection (consent)."
- `should-sanitize-input-before-display`: before "Sanitize all user input before display (prevent XSS, injection)." → after "You **SHOULD** sanitize all user input before display to prevent XSS and injection (input sanitization)."
- `should-support-apple-privacy-features`: before "Support App Tracking Transparency, App Privacy Report, and Private Relay compatibility." → after "On Apple platforms, you **SHOULD** support App Tracking Transparency, App Privacy Report, and Private Relay compatibility."
- `should-include-usage-descriptions`: before "Include `NS*UsageDescription` keys ..." → after "On Apple platforms, you **SHOULD** include `NS*UsageDescription` keys with human-readable explanations for all permission prompts."
- `should-respect-android-storage-language-and-denials`: before "Respect scoped storage, support per-app language preferences, and honor permission denials gracefully." → after "On Android, you **SHOULD** respect scoped storage, support per-app language preferences, and honor permission denials gracefully."
- `should-show-rationale-before-permission-requests`: before "Show rationale dialogs before runtime permission requests." → after "On Android, you **SHOULD** show rationale dialogs before runtime permission requests."
- `should-configure-csp`: before "**Content Security Policy**: Configure CSP headers ..." → after "On the web, you **SHOULD** configure Content Security Policy (CSP) headers to restrict script sources and prevent XSS."
- `should-use-httponly-cookies-for-tokens`: before "**HttpOnly cookies**: Use HttpOnly secure cookies for authentication tokens." → after "On the web, you **SHOULD** use HttpOnly secure cookies for authentication tokens."
- `must-not-store-tokens-in-localstorage`: before "Never store tokens in `localStorage`." never→MUST NOT → after "On the web, you **MUST NOT** store tokens in `localStorage` — never."
- `should-minimize-third-party-scripts`: before "Minimize third-party scripts." → after "On the web, you **SHOULD** minimize third-party scripts."
- `should-respect-do-not-track`: before "Respect the Do Not Track header." → after "On the web, you **SHOULD** respect the Do Not Track header."
- `should-declare-only-required-capabilities`: before "Declare only required capabilities in `Package.appxmanifest` — avoid `broadFileSystemAccess` unless essential" → after "On Windows, you **SHOULD** declare only required capabilities in `Package.appxmanifest` — avoid `broadFileSystemAccess` unless essential."
- `should-use-dpapi-for-local-secrets`: before "Use DPAPI for local secret storage (see secure-storage.md)" → after "On Windows, you **SHOULD** use DPAPI for local secret storage (see secure-storage.md)."
- `must-not-log-pii`: before "Never log personally identifiable information, even at debug level." never→MUST NOT → after "No PII logging: you **MUST NOT** ever log personally identifiable information (no PII in logs), even at debug level."

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions** (R4, left unfixed):
- should-use-httponly-cookies-for-tokens (SHOULD) and should-use-dpapi-for-local-secrets (SHOULD) vs must-use-platform-secure-storage (MUST, naming HttpOnly cookies and DPAPI). should-sanitize-input-before-display is promoted SHOULD though the intro calls security "by default".
  - `must-use-platform-secure-storage`: "Tokens and credentials MUST use platform secure storage (Keychain, EncryptedSharedPreferences, DPAPI, HttpOnly cookies)."
  - `should-sanitize-input-before-display`: "You **SHOULD** sanitize all user input before display to prevent XSS and injection (input sanitization)."
  - `should-use-httponly-cookies-for-tokens`: "On the web, you **SHOULD** use HttpOnly secure cookies for authentication tokens."
  - `should-use-dpapi-for-local-secrets`: "On Windows, you **SHOULD** use DPAPI for local secret storage (see secure-storage.md)."

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/secure-storage

commit 9d0ce133; rules 9; moved 7; obsolete 0

platform parts (swift, kotlin, c) held only requirements, so they became "On <platform>/In C#, …" rules and were removed. Intro kept verbatim.

**promoted** (8):
- `must-not-store-secrets-in-plaintext`: before "Never store secrets in plaintext configuration files, app settings, or unencrypted preference stores." never→MUST NOT → after "You **MUST NOT** store secrets in plaintext configuration files, app settings, or unencrypted preference stores."
- `should-use-keychain-on-apple`: before "Use Keychain Services for tokens, credentials, and any sensitive data." → after "On Apple platforms, you **SHOULD** use Keychain Services for tokens, credentials, and any sensitive data."
- `must-not-store-secrets-in-userdefaults-or-plists`: before "Never store secrets in UserDefaults or plists." → after "On Apple platforms, you **MUST NOT** store secrets in UserDefaults or plists."
- `should-use-encrypted-storage-on-android`: before "Use `EncryptedSharedPreferences` or the Android Keystore ..." → after "On Android, you **SHOULD** use `EncryptedSharedPreferences` or the Android Keystore for tokens, credentials, and sensitive data."
- `must-not-store-secrets-in-plain-sharedpreferences`: before "Never store secrets in plain SharedPreferences." → after "On Android, you **MUST NOT** store secrets in plain SharedPreferences."
- `should-use-dpapi-for-windows-local-secrets`: before "Use [DPAPI](…) (…) for Windows-only local secrets" → after "In C#, you **SHOULD** use [DPAPI](https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.protecteddata) (`ProtectedData.Protect`/`Unprotect` with `DataProtectionScope.CurrentUser`) for Windows-only local secrets."
- `should-use-user-secrets-for-development-only`: before "Use [User Secrets](…) (…) for development-time secrets only (plaintext JSON — not for production)" → after "In C#, you **SHOULD** use [User Secrets](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets) (`Microsoft.Extensions.Configuration.UserSecrets`) for development-time secrets only (plaintext JSON — not for production)."
- `must-not-store-tokens-in-plaintext-config`: before "Never store tokens or credentials in plaintext config files or app settings" → after "In C#, you **MUST NOT** store tokens or credentials in plaintext config files or app settings."

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions** (R4, left unfixed):
- platform "Use Keychain/EncryptedSharedPreferences/DPAPI" promote to SHOULD while must-use-platform-secure-storage is MUST. should-use-user-secrets-for-development-only recommends a plaintext-JSON store, beside must-not-store-secrets-in-plaintext (MUST NOT) — scoped to development, flagged.
  - `must-use-platform-secure-storage`: "Tokens, credentials, and any sensitive data MUST use platform secure storage."
  - `must-not-store-secrets-in-plaintext`: "You **MUST NOT** store secrets in plaintext configuration files, app settings, or unencrypted preference stores."
  - `should-use-user-secrets-for-development-only`: "In C#, you **SHOULD** use [User Secrets](https://learn.microsoft.com/en-us/aspnet/core/security/app-secrets) (`Microsoft.Extensions.Configuration.UserSecrets`) for development-time secrets only (plaintext JSON — not for production)."

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/security-headers-checklist

commit f6835923; rules 7; moved 0; obsolete 0

intro kept verbatim (lead-in + header block); each header became a MUST rule from the lead-in "Every web application MUST set these response headers:". No promoted rules. moved 0.

**promoted**: none.

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions** (R4, left unfixed):
- the CSP value ends in "..." so must-set-csp is open-ended; Cache-Control scoped "(for sensitive responses)" inside a block that every app MUST set.
  - `must-set-csp`: "Every web application **MUST** set `Content-Security-Policy: default-src 'none'; script-src 'nonce-{random}' 'strict-dynamic'; ...`."

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/sender-constrained-tokens

commit b119153a; rules 15; moved 3; obsolete 0

when-to-apply, dpop, mtls and limits bullets gathered into rules; mechanism table kept as two-mechanisms (how-to); the "fails if both stolen" bullet is the rationale part (heading "Limits — do not over-trust").

**promoted** (3):
- `should-pick-one-mechanism-per-surface`: before "Pick **one** mechanism per API surface and apply it consistently; do not mix ..." → after "You **SHOULD** pick **one** mechanism per API surface and apply it consistently; do not mix bearer and constrained acceptance on the same endpoint without an explicit migration plan."
- `should-present-mechanism-choice-as-trade-off`: before "Present the choice as a deliberate trade-off: ..." → after "You **SHOULD** present the choice as a deliberate trade-off: DPoP needs no PKI but adds per-request signing; mTLS reuses transport identity but needs certificate provisioning and TLS termination you control."
- `should-combine-with-other-token-controls`: before "It does not replace short token lifetimes, refresh-token rotation, audience restriction, or PKCE — combine them." → after "Sender-constraining does not replace short token lifetimes, refresh-token rotation, audience restriction, or PKCE — you **SHOULD** combine them."

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions** (R4, left unfixed):
- should-pick-one-mechanism-per-surface carries "do not mix" (a prohibition) at SHOULD. must-reject-replayed-dpop-proofs makes the server nonce conditional ("where replay risk is high") under a MUST. may-choose-mechanism-by-topology uses MAY for a statement of fact ("MAY block a mechanism"), not a permission.
  - `should-pick-one-mechanism-per-surface`: "You **SHOULD** pick **one** mechanism per API surface and apply it consistently; do not mix bearer and constrained acceptance on the same endpoint without an explicit migration plan."
  - `must-reject-replayed-dpop-proofs`: "Resource servers **MUST** reject replayed proofs — enforce a `jti`/`iat` freshness window with a server-provided `nonce` where replay risk is high."
  - `may-choose-mechanism-by-topology`: "Performance and architecture (TLS-terminating CDNs, certificate provisioning) **MAY** block a mechanism in some deployments; choose the mechanism that fits the topology rather than forcing one."

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/sensitive-data

commit 3e1e6d90; rules 6; moved 17; obsolete 0

intro keeps H1 + statement; bullets became rules; "References:" list and the "See [privacy]" link became the references part ("References:" kept verbatim there, since a base sentence can never be obsolete).

**promoted** (6):
- `must-return-only-needed-fields`: before its keyword-less part "Use explicit response DTOs, never dump database models directly." → after "Data minimization: APIs **MUST** return only fields the client needs. You **SHOULD** use explicit response DTOs and **MUST NOT** ever dump database models directly."
- `must-classify-data-by-sensitivity`: before its keyword-less part "Apply controls proportional to tier." → after "PII classification: data **MUST** be classified by sensitivity (public, internal, PII, sensitive PII). You **SHOULD** apply controls proportional to tier."
- `should-encrypt-sensitive-fields-at-application-level`: before "**Field-level encryption** — encrypt highly sensitive fields (SSN, payment info) at the application level with a KMS (AWS KMS, Azure Key Vault, GCP KMS). Separate from database-level encryption." → after "Field-level encryption: you **SHOULD** encrypt highly sensitive fields (SSN, payment info) at the application level with a KMS (AWS KMS, Azure Key Vault, GCP KMS), separate from database-level encryption."
- `must-not-log-pii`: before its keyword-less part "Mask/redact in all log outputs, including debug level." → after "No PII in logs: tokens, passwords, credit card numbers, or PII **MUST NOT** be logged. You **SHOULD** mask/redact in all log outputs, including debug level."
- `must-not-expose-internals-in-api-responses`: before its keyword-less part "Return generic errors with correlation IDs." → after "No internals in API responses: internal IDs, stack traces, or database error messages **MUST NOT** be exposed in production. You **SHOULD** return generic errors with correlation IDs."
- `should-set-no-store-on-sensitive-responses`: before "**Cache-Control: no-store** on responses containing sensitive data." → after "You **SHOULD** set `Cache-Control: no-store` on responses containing sensitive data."

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions** (R4, left unfixed):
- should-set-no-store-on-sensitive-responses (SHOULD) vs security-headers-checklist must-set-no-store-on-sensitive-responses (MUST). Masking/redacting in logs is SHOULD inside a MUST NOT log rule. Field-level encryption for SSN/payment is only SHOULD while the statement says "encrypt what you keep".
  - `should-set-no-store-on-sensitive-responses`: "You **SHOULD** set `Cache-Control: no-store` on responses containing sensitive data."
  - security-headers-checklist `must-set-no-store-on-sensitive-responses`: "Every web application **MUST** set `Cache-Control: no-store` for sensitive responses."

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/token-handling

commit 16a4a0ed; rules 16; moved 17; obsolete 0

intro keeps H1 + statement; its H3 subsections became one rules part with the H3 headings kept verbatim as groupings; "See also [privacy]" and the "References:" list became the references part.

**promoted** (12):
- `should-keep-access-tokens-short-lived`: before "Short-lived (5-15 min)." → after "Access tokens **SHOULD** be short-lived (5-15 min)."
- `should-include-only-necessary-claims`: before "Include only necessary claims — no PII in JWTs that transit untrusted parties." → after "You **SHOULD** include only necessary claims — no PII in JWTs that transit untrusted parties."
- `should-bind-refresh-tokens-to-client`: before "Longer-lived but bound to client." → after "Refresh tokens are longer-lived but **SHOULD** be bound to the client."
- `should-rotate-refresh-tokens`: before "Use rotation (see Authentication above)." → after "You **SHOULD** use rotation for refresh tokens (see Authentication above)."
- `should-store-refresh-tokens-server-side`: before "Store server-side when possible." → after "You **SHOULD** store refresh tokens server-side when possible."
- `should-refresh-proactively`: before "Proactive refresh before expiry (e.g., at 75% of TTL)" → after "You **SHOULD** refresh proactively before expiry (e.g., at 75% of TTL)."
- `should-queue-requests-during-refresh`: before "Queue concurrent requests during refresh to avoid race conditions" → after "You **SHOULD** queue concurrent requests during refresh to avoid race conditions."
- `should-retry-refresh-with-backoff`: before "Retry with backoff on refresh failure" → after "You **SHOULD** retry with backoff on refresh failure."
- `should-use-keychain-on-apple`: before "**Apple:** Keychain Services" → after "On Apple platforms, you **SHOULD** store tokens in Keychain Services."
- `should-use-encrypted-storage-on-android`: before "**Android:** EncryptedSharedPreferences / Android Keystore" → after "On Android, you **SHOULD** store tokens in EncryptedSharedPreferences / Android Keystore."
- `should-use-dpapi-on-windows`: before "**Windows:** DPAPI (`ProtectedData`)" → after "On Windows, you **SHOULD** store tokens with DPAPI (`ProtectedData`)."
- `should-use-httponly-cookies-on-web`: before "**Web:** HttpOnly Secure SameSite cookies (never localStorage)" → after "On the web, you **SHOULD** store tokens in HttpOnly Secure SameSite cookies (never localStorage)."

**bars**: `look-for`, `a-complete-review-must-establish` and `a-build-must-establish` are all **authored**.

**contradictions** (R4, left unfixed):
- the statement says refresh tokens are rotated "on every use" and stored "in secure platform storage", while should-rotate-refresh-tokens and should-store-refresh-tokens-server-side (server-side when possible) are SHOULD and differ on where they live. should-include-only-necessary-claims carries "no PII" at SHOULD, vs pii/sensitive-data MUST NOT rules. "(see Authentication above)" points at a section this topic does not have.
  - `should-include-only-necessary-claims`: "You **SHOULD** include only necessary claims — no PII in JWTs that transit untrusted parties."
  - `should-rotate-refresh-tokens`: "You **SHOULD** use rotation for refresh tokens (see Authentication above)."
  - `should-store-refresh-tokens-server-side`: "You **SHOULD** store refresh tokens server-side when possible."

**unfinished**: nothing.

## cookbook/guidelines/implementing/security/transport-security

commit 23c42d62; rules 10; moved 11; obsolete 0

intro keeps H1 + statement; its bold-labelled paragraphs became rules. The folded copy (introduction + pre-deploy-checklist) became the review-focus part: its opening "Before deploying, verify transport security meets these requirements." kept verbatim and each checklist sentence now names its rule, plus one authored line for should-pin-only-on-mobile. verification-tools kept as how-to; the two identical References lists became one references part.

level taken from the checklist: must-enable-hsts-on-production-domains uses the checklist's "all production domains MUST have the header"; the intro's "**HSTS:** Enable on all production domains:" alone would have promoted to SHOULD.

**promoted** (6):
- `should-submit-to-hsts-preload-list`: before "Submit to the [HSTS preload list](https://hstspreload.org/)." → after "You **SHOULD** submit to the [HSTS preload list](https://hstspreload.org/)."
- `should-pin-to-intermediate-ca`: before "Pin to the intermediate CA, not the leaf (leaf certificates rotate)" → after "Certificate pinning — use with caution: you **SHOULD** pin to the intermediate CA, not the leaf (leaf certificates rotate)."
- `should-pin-only-on-mobile`: before "Acceptable for mobile apps; generally avoid for web (HPKP is deprecated)" → after "Certificate pinning is acceptable for mobile apps (mobile apps only); you **SHOULD** generally avoid it for web (HPKP is deprecated)."
- `should-consider-certificate-transparency-monitoring`: before "Consider Certificate Transparency monitoring as an alternative" → after "You **SHOULD** consider Certificate Transparency monitoring as an alternative (a lighter alternative to pinning)."
- `should-use-mozilla-tls-configuration`: before "**Cipher suites:** Use Mozilla's "Intermediate" or "Modern" TLS configuration." → after "Cipher suites: you **SHOULD** use Mozilla's "Intermediate" or "Modern" TLS configuration."
- `should-prefer-aead-ciphers`: before "Prefer AEAD ciphers (AES-GCM, ChaCha20-Poly1305)." → after "You **SHOULD** prefer AEAD ciphers (AES-GCM, ChaCha20-Poly1305)."

**bars**: `look-for` **moved** (the folded pre-deploy checklist, each line now naming its rule, plus one authored line); the other two are **authored**.

**contradictions** (R4, left unfixed):
- the intro says pinning is "acceptable for mobile apps; generally avoid for web" while the checklist says "(mobile apps only)"; the statement says "pin certificates for high-value mobile traffic" (imperative) while the body says "use with caution" and offers CT monitoring as an alternative. must-require-tls-1-2-minimum holds REQUIRED and SHOULD in one rule (not split: the tripwires keep both levels in one clause).
  - `must-require-tls-1-2-minimum`: "**TLS 1.2 minimum** is REQUIRED, TLS 1.3 SHOULD be preferred."

**unfinished**: nothing.

## Unfinished

Nothing. All 22 topics are committed (160 promoted rules in all).
