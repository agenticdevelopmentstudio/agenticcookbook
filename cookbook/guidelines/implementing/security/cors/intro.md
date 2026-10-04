
# CORS

Cross-Origin Resource Sharing — get it right or don't enable it.

- The Origin header MUST NOT be reflected back as `Access-Control-Allow-Origin`. Maintain an
  explicit allowlist of origins.
- `*` MUST NOT be used with credentials — browsers block this, and attempting it reveals a
  design misunderstanding.
- **Preflight caching:** SHOULD set `Access-Control-Max-Age: 86400` to reduce preflight overhead.
- **Minimize exposed headers:** Only what the client actually needs.

**Common misconfigurations:**
- Wildcard origin with credentials
- Regex matching without anchoring (`evil-example.com` matching `example.com`)
- Allowing `null` origin (exploitable via sandboxed iframes)
- Overly broad allowed methods and headers

References:
- [MDN: CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
- [OWASP: CORS Testing](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/11-Client-side_Testing/07-Testing_Cross_Origin_Resource_Sharing)

