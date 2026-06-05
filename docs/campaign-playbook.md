# Campaign Playbook

## Goal

Generate the first paid FreeCodex Agent Safety Lab revenue by selling lightweight Agent Repo Safety Audits.

## Positioning

The offer is not "AI security magic." It is a fast, practical pre-launch review for builders who used AI to ship quickly and want obvious risks caught before public launch.

## Daily Loop

1. Scout public signals from GitHub, Hacker News, Product Hunt, Reddit search results, and public launch posts.
2. Record promising leads with `templates/lead-record.md`.
3. Prepare exact outreach using `templates/outreach-draft.md`.
4. Send autonomously only when the lead satisfies `docs/autonomous-outreach-policy.md`; otherwise keep it as a draft.
5. Deliver audits using `scripts/repo_audit.py`.
6. Ask permission before publishing samples, testimonials, or anonymized learnings.

For non-GitHub channels, use `docs/sales/off-github-channel-kit.md` for Ko-fi service copy, community comment templates, marketplace gig copy, and weekly channel discipline.

## Lead Filters

Prioritize leads that show at least two signals:

- Public repo or launch page exists.
- AI coding, MCP, agent skills, Lovable, Bolt, Replit, Cursor, Codex, or Claude Code are mentioned.
- The project handles auth, payments, user data, APIs, webhooks, or Supabase.
- The builder is near launch or asking for feedback.
- The problem is tied to money, deadline, trust, compliance, or reputational risk.

Avoid:

- Private repos without permission.
- Enterprise targets requiring procurement.
- Projects with no reachable public context.
- Anything that would require scraping, spam, paid APIs, or account login.

## Autonomous Outreach Limits

- Maximum 3 outbound messages per automation run.
- Prefer public GitHub issues/discussions and public launch-feedback threads.
- No repeated follow-up unless the recipient responds.
- Log every sent message under `leads/sent/`.

## Delivery Standard

- Report within 24-48 hours.
- Redact suspicious values.
- Separate confirmed issues from manual-review hints.
- Make the first fix recommendation obvious.
- Offer paid fixes only when the scope is bounded and high-confidence.
