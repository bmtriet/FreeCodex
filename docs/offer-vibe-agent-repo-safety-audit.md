# Agent Repo Safety Audit

Agent Safety Lab by StevenB offers lightweight public-repo audits to help identify launch-readiness gaps in AI-built apps, agent workflows, and MCP servers.

Fast AI-built apps can launch before their safety basics catch up. This offer is for public GitHub repos built with AI coding agents, MCP servers, agent skills, Lovable, Bolt, Replit, Cursor, Codex, Claude Code, or similar workflows.

## What You Get

- A concise markdown report for one repository.
- Obvious leaked-secret pattern checks.
- Public launch readiness checks for README, license, security policy, gitignore, CI, dependency metadata, and environment examples.
- Agent/MCP/skill risk notes when relevant.
- Vibe-app risk hints such as frontend-exposed secret names, Supabase service-role confusion, wildcard CORS, and webhook signature review prompts.
- A prioritized fix list.

See `reports/samples/vibe-agent-demo-audit.md` for a synthetic public-safe example of the report shape and finding style.

## Pricing

- Free fit check: quick scope review for one public repo; no full report.
- Optional donation: pay what you want on Ko-fi if a public PR, triage note, checklist, or mini-audit helped and no scoped audit is needed.
- Starter report: USD 49 for one small public repo, deterministic checks, concise notes, and top launch risks.
- Standard audit: USD 149 for a manual launch-readiness review, prioritized markdown report, and concrete fix plan.
- Report plus one bounded public fix PR: starts at USD 299 and includes the standard audit plus one small public PR, confirmed only after fit and scope review.

First-contact outreach does not include payment links. The public landing page may list pricing, the optional donation path, and the payment destination for ready buyers, but paid audit work starts only after a positive reply, fit confirmation, scope confirmation, and consent to proceed.

## Turnaround

Typical lightweight report turnaround is 24-48 hours after repo permission and payment, if payment applies, subject to current queue. Rush delivery may require a separate scope decision.

## Scope

Included:

- Public GitHub repository review.
- Local deterministic checks.
- Manual review of generated findings.
- Redacted evidence in the report.

Not included:

- Certified penetration testing.
- Compliance attestation.
- Production infrastructure access.
- Private repo access without explicit permission.
- Secret storage, credential handling, or account login.
- Broad automated outreach, spam, or public representation outside the autonomous outreach policy.

## How To Request

Book the fit check by opening the public GitHub issue form:

- `https://github.com/bmtriet/FreeCodex/issues/new?template=audit-fit-check.yml`

Include:

- Public repository URL.
- Launch context.
- Any specific concern, such as secrets, MCP config, agent workflow, Supabase, auth, or webhooks.

First contact stays public-safe and does not require payment. Listed prices are for public repos. If the repo is a fit, paid work starts only after a positive reply, scope confirmation, and consent to proceed.

Optional donations are welcome at `https://ko-fi.com/freecodex` when public proof-of-work was useful but no paid audit is needed. Donations do not create an audit queue slot, support obligation, or guaranteed deliverable.

Do not send secrets, passwords, tokens, cookies, or private keys.

## Sales Pack

- `docs/sales/vibe-launch-safety-sprint.md` - packaged offer.
- `docs/sales/vibe-launch-safety-scope.md` - scope, boundaries, and done criteria.
- `docs/sales/vibe-launch-safety-intake.md` - public-safe intake questions.
- `docs/sales/vibe-launch-safety-outreach.md` - first-contact templates with no payment links.
- `docs/sales/vibe-launch-safety-followup.md` - positive-reply and paid-path follow-ups.
- `docs/sales/proof-of-work-prs.md` - proof-of-work PR guidelines.
- `docs/sales/off-github-channel-kit.md` - public-safe non-GitHub sales channels, copy, and operating rules.
- `templates/vibe-launch-safety-report.md` - delivery report template.

## Disclaimer

This is a lightweight launch/readiness audit. It is not a certified penetration test, legal advice, compliance guarantee, or proof that a repository is secure.
