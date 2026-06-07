# Agent Repo Safety Intake

Use this intake after a prospect gives a positive reply or explicitly asks for the audit.

Do not ask for secrets, passwords, tokens, cookies, private keys, private logs, account access, or production access.

## Questions

1. Public repo URL:
2. What are you launching, and when?
3. Is the app built with AI coding tools or agents? If yes, which ones?
4. Main stack and hosting platform:
5. Does the app use auth, payments, webhooks, Supabase, Firebase, MCP servers, external APIs, or agent tools?
6. What are you most worried about before launch?
7. Do you want the free fit check, USD 49 starter report, USD 149 standard audit, or a bounded fix PR after the report?
8. Are there areas you want excluded from review?
9. Are you okay with a public-safe PR if small fixes are possible?
10. Can Agent Safety Lab by StevenB reference the repo as anonymized proof-of-work, with no sensitive details?

## Internal Triage

Accept when:

- The repo is public or explicit permission is documented.
- The request fits lightweight launch/readiness review.
- No credentials or private account access are required.
- The work can be delivered with local tooling and manual review.

Decline or defer when:

- The request needs a certified pentest or compliance attestation.
- The repo handles sensitive personal-data contexts where a lightweight public review is not enough.
- The user sends secrets or asks for secret handling.
- The expected fix work is broad, urgent production incident response, or outside current capability.
