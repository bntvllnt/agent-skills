# Security

- Never commit secrets, credentials, API keys, or `.env` files. Use the repo's secret store / CI
  secrets instead.
- Validate and sanitize input at system boundaries (user input, network, files).
- Avoid the OWASP Top 10: injection, broken auth/access control, SSRF, insecure deserialization.
- Pin and review new dependencies; check for known CVEs before adding.
- Don't leak internal state, stack traces, or PII in responses or logs.
- Report security issues privately per `SECURITY.md`, not in public issues.
