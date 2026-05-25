# GitHub Outreach Run 005

Date: 2026-05-25 21:18 +07
Channel: GitHub public PR
Mode: Autonomous, within `docs/autonomous-outreach-policy.md`
Outbound count: 1

## Summary

This run prioritized proof-of-work over a sales message on an explicit public security-hardening issue.

- Opened 1 small public PR related to JWT localStorage blast-radius reduction.
- Did not include payment links in outbound content.
- Used only public repository code and issue context.
- No credentials, account access, private data, or secrets were requested.

## 1. Sayap-Garuda-Indah/inventory

Public context:

- Issue: https://github.com/Sayap-Garuda-Indah/inventory/issues/41
- PR opened: https://github.com/Sayap-Garuda-Indah/inventory/pull/45

Why it fit:

- Open public issue from 2026-05-06 explicitly describes JWT access tokens stored in `localStorage`.
- The issue asks for compensating controls if cookie-based auth is not immediately adopted.
- The repo has a Docker/Nginx frontend deployment where browser security headers can be added without private access.

Action:

- Forked `Sayap-Garuda-Indah/inventory` to `bmtriet/inventory`.
- Opened PR `fix(frontend): add browser security headers`.

Exact PR body:

```markdown
## Summary
- Add a conservative Content-Security-Policy to the frontend Nginx config.
- Add X-Content-Type-Options, Referrer-Policy, and Permissions-Policy headers.
- Keep camera available for same-origin scanner flows while disabling microphone and geolocation.

## Context
This is a small hardening slice related to #41. It does not replace the larger fix of moving bearer tokens out of localStorage into HttpOnly/Secure/SameSite cookie-based session handling. It reduces the browser attack surface while that auth-storage migration is planned.

The CSP assumes the Docker deployment serves the frontend and API same-origin via /api. If another deployment calls a different API origin or adds third-party scripts, connect-src/script-src will need an explicit allowlist update.

## Validation
- PASS: npm ci
- PASS: npm run build
- PASS: git diff --check
- NOT RUN: nginx -t via Docker image; local Docker daemon was unavailable in my environment.
- PRE-EXISTING: npm run lint currently fails on unrelated no-explicit-any/no-unused-vars/react-hooks/react-refresh issues in existing frontend files.
- PRE-EXISTING: npm audit --audit-level=critical --omit=dev reports existing dependency advisories.
```

Verification:

- `npm ci` passed.
- `npm run build` passed.
- `git diff --check` passed.
- `npm run lint` failed on pre-existing unrelated frontend lint errors.
- `npm audit --audit-level=critical --omit=dev` failed on pre-existing dependency advisories.
- `nginx -t` via Docker image could not run because the local Docker daemon was unavailable.
- The PR currently has no GitHub checks reported.

Follow-up status:

- No follow-up unless the maintainer replies.

## LLMGate Use

- Model used: `gpt-5.4`.
- Input: public issue context, public package/deployment facts, and the proposed Nginx header snippet only.
- Purpose: review CSP and `Permissions-Policy` caveats before opening the PR.
- No private data, credentials, raw chat logs, or local secrets were sent.
