# Agent Repo Safety Scope

This scope keeps the offer simple enough to deliver quickly and honest enough to sell safely.

The standard offer is for public GitHub repos. Private repos are not part of the standard public-safe pack and require explicit permission plus separate scope confirmation.

## USD 49 Mini Audit

Included:

- One public GitHub repository.
- Local deterministic checks plus manual review.
- One markdown report.
- Findings labeled by priority and launch impact.
- Redacted evidence only.
- Practical fix recommendations.
- One brief clarification round after delivery.

Not included:

- Certified penetration testing.
- Compliance attestation.
- Production infrastructure review.
- Login, credential, cookie, or account handling.
- Secret rotation or incident response.
- Private repo work without explicit permission.
- Deep refactors or feature development.
- Unlimited back-and-forth consulting.

Done means:

- The report is delivered.
- Findings are redacted and prioritized.
- The client has enough information to decide whether to fix items themselves or request a bounded sprint.

## USD 199+ Fix Sprint

Included when in scope:

- One public repository.
- A bounded set of small fixes based on the delivered audit.
- One PR or patch set.
- Updated notes showing what changed.
- Repo hygiene improvements such as README, SECURITY, .gitignore, env example, CI, or docs updates.
- Small safety fixes such as safer CSP defaults, webhook verification reminders, secret-name cleanup, or agent workflow guardrails.

Out of scope unless separately agreed:

- Large architecture changes.
- Production debugging.
- New authentication or payment systems.
- Database migrations.
- Incident response.
- Secret rotation.
- Broad dependency upgrades with high regression risk.
- Work that requires private credentials or account access.

Done means:

- The agreed patch or PR is delivered.
- The change stays within the confirmed scope.
- Local checks that are available in the repo have been run or clearly reported as unavailable.

## Public-Safety Rules

- Review only public repos under the standard offer.
- Treat private repos as separate scope that requires explicit permission and confirmation before review.
- Store no secrets.
- Ask clients not to send credentials.
- Redact suspicious values in reports.
- Avoid fear-based claims or security guarantees.
