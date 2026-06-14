# Off-GitHub Channel Kit

This kit helps Agent Safety Lab by StevenB sell the Agent Repo Safety Audit outside GitHub without breaking the outreach guardrails in `docs/autonomous-outreach-policy.md`.

Use this for short, public-safe, manual-first outreach. Do not overclaim. Do not spam. Do not ask for secrets, credentials, cookies, tokens, or account access.

The finalized Ko-fi listing copy lives in `docs/sales/kofi-service-listing.md`. Keep this file as the channel strategy and template kit.

## Priority Channels

Prioritize channels that match the current offer and can be used without ad spend:

1. **Ko-fi service listing**
   - Good fit because Ko-fi supports donations, commissions/services, and direct sharing.
   - Use as the public landing point after someone replies with interest, asks how to support the work, or confirms scope.
   - Do not drop the payment link in first contact.

2. **GitHub Pages service landing page**
   - Public URL: `https://bmtriet.github.io/FreeCodex/`.
   - Use when a channel expects a service page, profile link, or post-reply details page.
   - For first-contact outreach, prefer a short useful comment; share the landing page only when the thread context makes a service link welcome or after a positive reply.

3. **Hacker News comments**
   - Best for builders already discussing launch, hiring, or product work.
   - There is a current **May 2026 "Who wants to be hired?"** thread, but use it only if posting as a personal freelance availability note that follows the thread rules.
   - Keep comments useful and specific, not sales-heavy.

4. **Reddit comments**
   - Best in SaaS, startup, indie hacker, and launch-feedback discussions.
   - Public SaaS discussions show interest in basic pre-launch security checklists.
   - Lead with useful framing, not a pitch dump.

5. **Indie Hackers comments**
   - Best on launch, validation, and build-in-public posts.
   - Keep it short and peer-like.

6. **Freelance/marketplace gig pages**
   - Use for buyers who want a clear fixed-scope service.
   - Position as lightweight repo review and launch-readiness audit, not pentesting.

## Core Positioning

Use this positioning consistently:

- Lightweight launch/readiness audit for public repos built fast with AI tools.
- Checks obvious secret exposure patterns and public launch basics.
- Useful before launch for builders using agents, MCP servers, Lovable, Bolt, Cursor, Replit, Codex, Claude Code, or similar workflows.
- Not a certified pentest.
- No private credentials or account access needed for the report-only path.

## Ko-fi Service Listing Copy

Target: `https://ko-fi.com/freecodex`

Use the finalized listing copy in `docs/sales/kofi-service-listing.md` as the source of truth for current pricing and buyer instructions.

First contact should be a short message with the public repo context. Share the Ko-fi page only after a positive reply, direct request for details, explicit support question, or scope confirmation.

### Optional Ko-fi FAQ Snippets

- **Do you need repo access?** No for public repos on the standard public path.
- **Will you log or keep secrets?** No. Suspicious values are redacted in reports.
- **Do you fix issues too?** One bounded public fix PR can be offered after the report and scope confirmation.
- **Can I just support the public work?** Yes. Ko-fi can be used for pay-what-you-want donations when a public PR, triage note, checklist, or mini-audit helped.

## Short Comment Templates

Keep first contact short. No payment link in first contact.

### Hacker News

For a "Who wants to be hired?" or relevant launch thread:

> I do lightweight repo safety audits for AI-built apps and agent/MCP projects. Focus is public launch readiness: obvious secret exposure, env handling, auth/webhook/CORS footguns, and a short prioritized fix list. Public repo only, no private credentials or account access, and not a certified pentest. Happy to sanity-check fit if you have a repo and launch soon. No worries if not useful.

### Reddit

For pre-launch SaaS/security checklist discussions:

> If you're close to launch, a basic repo safety pass is often worth doing before promotion. I review public AI-built app repos for obvious secret leaks, risky env examples, auth/webhook/CORS mistakes, and missing launch basics, then return a short fix list. No private credentials or account access needed. Not a certified pentest. If useful, reply with the public repo context and I can say if it's a fit. No worries if not useful.

### Indie Hackers

For launch/build posts:

> Quick thought: if this was built fast with AI tools, a lightweight public-repo safety pass before launch can catch boring but expensive mistakes. I do short audits around secret exposure, env handling, auth/webhooks/CORS, and public launch basics. No credentials needed, public repo only, not a certified pentest. No worries if not useful.

### Community Reply Variant

Use when someone asks for feedback or launch risks:

> One practical checklist item: do a public-repo launch safety review before sharing widely. I focus on obvious secret leaks, env examples, auth/webhook/CORS issues, and agent/MCP-specific footguns where relevant. Happy to say if your public repo looks in-scope. No credentials needed, public repo only, and not a certified pentest. No worries if not useful.

## Marketplace Gig Copy

### Gig Title

I will audit your public AI app repo for launch safety basics

### Gig Summary

I will review one public GitHub repo and deliver a concise launch-readiness and safety report for AI-built apps, agent workflows, MCP servers, or fast prototypes.

### Included

- public repo review
- obvious leaked-secret pattern checks
- README/license/security-policy/gitignore/CI review
- agent, MCP, webhook, auth, CORS, and env-handling notes when relevant
- prioritized fix list

### Boundaries

- public repos only unless explicit permission is given
- no private credentials, account access, or secret handling
- no certified pentest claims
- no compliance guarantee

## Operating Rules

- Keep first-contact messages short and relevant to the public thread or project.
- Do not include a payment link in first contact.
- Do not spam, mass-post, or repeat follow up without a reply.
- Do not ask for or accept private credentials, tokens, cookies, API keys, or account access.
- Do not claim certified pentesting, compliance attestation, guaranteed security, or official affiliation.
- Do not overclaim platform signals.
- Prefer helpful comments over direct pitches.
- Keep everything within `docs/autonomous-outreach-policy.md`.

## Source Notes

Checked on 2026-05-25:

- Ko-fi Commissions supports services, listing terms, direct sharing, and direct payment handling through connected PayPal or Stripe: https://help.ko-fi.com/hc/en-us/articles/360016170433-What-are-Ko-fi-Commissions
- Hacker News May 2026 "Who wants to be hired?" requires personal work-seeker posts and says agencies, recruiters, and job boards are off topic: https://news.ycombinator.com/item?id=47975570
- A recent r/SaaS security discussion showed interest in simple pre-launch scanners/checklists and repeated issues around headers, Supabase/Firebase config, git history secrets, and auth rate limiting: https://www.reddit.com/r/SaaS/comments/1s8dgvh/i_scanned_12_indie_saas_apps_for_basic_security/

## 7-Day Action Loop

### Day 1

- Finalize the Ko-fi service listing copy.
- Confirm the offer page, pricing, and boundaries match `docs/offer-vibe-agent-repo-safety-audit.md`.

### Day 2

- Find 5-10 public HN, Reddit, Indie Hackers, or launch-feedback threads with clear launch or security-checklist context.
- Draft only the best 3 messages that fit policy.

### Day 3

- Post up to 3 short comments total, only where the thread context makes the audit genuinely relevant.
- Log each one per the outreach policy.

### Day 4

- Reply only where there is engagement.
- Offer a fit check based on public repo URL and launch context.

### Day 5

- Refine copy based on objections or confusion.
- Update Ko-fi FAQ or marketplace summary if the same question repeats.

### Day 6

- Publish 1-2 more policy-safe comments only if new high-fit threads appear.
- Avoid repeating the same template verbatim.

### Day 7

- Review results: replies, fit quality, objections, and any audit requests.
- Keep the best-performing channel and message angle.
- Cut channels that produce no relevant conversation.

Repeat weekly with the same guardrails.
