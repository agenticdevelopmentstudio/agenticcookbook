
- Reusing or omitting server-side challenge verification (replay risk) — **MUST NOT**.
- Setting `rp.id` to a host that doesn't cover the auth origin.
- Treating a passkey as a bearer secret or syncing the RP private key (there is none server-side).

