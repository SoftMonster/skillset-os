# Security checklist

Read during the manual pass of a security review. Mapped to the OWASP Top 10 (2021).

## Contents
- Access control (A01)
- Cryptography and secrets (A02)
- Injection (A03)
- Design, configuration and components (A04–A06)
- Authentication and sessions (A07)
- Integrity, logging and SSRF (A08–A10)
- Frontend and infrastructure

## Access control (A01)
- Every endpoint and action checks authentication and authorisation on the server.
- Object-level checks: lookups are scoped to the requester (no IDOR).
- Deny by default; admin functions separated and protected.
- CORS allows only named origins; no `*` with credentials.
- File uploads: type and size checked, stored outside the web root, served with a safe content type and a random name.

## Cryptography and secrets (A02)
- TLS everywhere; HSTS on web apps.
- Passwords hashed with Argon2id, bcrypt or scrypt; never plain, MD5 or SHA-x alone.
- Secrets come from env or a secret manager, not code, images or logs; `.env` is gitignored.
- Tokens and IDs used for security come from a CSPRNG (`secrets`, `crypto.randomUUID`).
- Sensitive data encrypted at rest where required; no personal data in URLs.

## Injection (A03)
- SQL uses bound parameters or the ORM; no string-built queries with input.
- No shell commands with input; if unavoidable, argument lists (no `shell=True`) and allow-lists.
- Templates auto-escape; no `innerHTML`, `dangerouslySetInnerHTML` or `|safe` with user data.
- File paths built from input are normalised and confined to a base directory.
- No `eval`, `exec`, `pickle`, `yaml.load` (use `safe_load`) or unsafe deserialisation on untrusted data.
- Regexes on user input avoid catastrophic backtracking.

## Design, configuration and components (A04–A06)
- Rate limits on login, signup, password reset and expensive endpoints.
- Debug mode, stack traces and default credentials off in production.
- Security headers: CSP, `X-Content-Type-Options: nosniff`, frame-ancestors or `X-Frame-Options`, `Referrer-Policy`.
- Dependencies pinned, audited and maintained; lockfile committed for applications.
- Containers run as non-root with minimal base images.

## Authentication and sessions (A07)
- MFA available for privileged users; account lockout or backoff on repeated failures.
- Session cookies `HttpOnly`, `Secure`, `SameSite=Lax` or `Strict`; rotated on login; expire.
- CSRF protection on cookie-authenticated state-changing requests.
- JWTs: algorithm pinned (no `none`), signature verified, `exp` checked, short lifetime.
- Password reset tokens single-use, short-lived, and not revealing whether an account exists.

## Integrity, logging and SSRF (A08–A10)
- CI pipelines pin actions by SHA and give tokens least privilege.
- Webhooks verify signatures and timestamps.
- Security events (login, permission change, failed authorisation) logged without secrets or personal data.
- Server-side fetches of user-supplied URLs use an allow-list and block internal and metadata addresses (169.254.169.254, localhost, private ranges), including after redirects.

## Frontend and infrastructure
- No secrets in frontend bundles or mobile apps.
- Third-party scripts limited and covered by CSP or SRI.
- Cloud storage buckets private by default; IAM least privilege.
