
1. **Content Security Policy**: Configure CSP headers to restrict script sources and prevent XSS.
2. **HttpOnly cookies**: Use HttpOnly secure cookies for authentication tokens. Never store tokens in `localStorage`.
3. **Input sanitization**: Sanitize all user input before display to prevent XSS and injection.
4. **TLS only**: All network communication MUST use HTTPS.
5. Minimize third-party scripts. Respect the Do Not Track header.

