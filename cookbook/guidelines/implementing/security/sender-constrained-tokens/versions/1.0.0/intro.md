
# Sender-constrained access tokens

A plain bearer token grants access to whoever presents it: steal it, replay it. Sender-constraining binds the token to a key the legitimate client holds, so a leaked token alone is useless. The OAuth 2.0 Security Best Current Practice (RFC 9700, January 2025) recommends this for high-value APIs and public clients.

