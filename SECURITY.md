# Security Policy

## Reporting a vulnerability

Use a private GitHub security advisory. Do not open a public issue containing
credentials, exploit details, private logs, user data, or infrastructure data.

If a secret is exposed, revoke or rotate it first, then clean Git history.

## Local checks

Run the documented offline unittest suite with synthetic data. Local hooks are not installed automatically. Agent instructions are not an OS sandbox; full-trust processes retain the owner’s permissions.
