# Acquisition Plan

Agent Safety Lab by StevenB grows through public proof, useful checklists, and a booking path that asks for only public-safe context.

## How Buyers Find Us

1. **Proof-of-work PRs**
   - Contribute small, relevant fixes to large public repos in AI agents, MCP, security, and developer tools.
   - Keep PRs independently useful and free of sales links.
   - Promote only merged PRs, maintainer praise, or public artifacts that clearly show the work pattern.

2. **Searchable public assets**
   - Keep GitHub Pages as the canonical service page.
   - Publish practical checklists that builders can use before requesting an audit.
   - Make the fit-check issue the primary booking path.
   - Add value-after-consumption CTAs on owned resources: after a checklist, sample report,
     or local audit instructions, offer optional Ko-fi support for public work or a public
     fit-check issue for scoped review. Do not put payment links in first-contact outreach.

3. **Policy-safe channel presence**
   - GitHub: issues, discussions, and small PRs where there is visible context.
   - Hacker News, Reddit, Indie Hackers, and Product Hunt: short helpful replies only when the thread invites launch, repo, or security feedback.
   - Ko-fi: payment/service confirmation after positive fit confirmation, not cold first contact.

4. **Referral loop**
   - Deliver concise reports within 24-48 hours.
   - Ask permission before publishing testimonials, samples, or anonymized learnings.
   - Turn repeated fixes into reusable skills and public checklist improvements.

## 14-Day Execution Cadence

- **Days 1-2:** finalize the Ko-fi listing copy, publish the first checklist page, and make homepage resources easier to find.
- **Days 3-7:** find large, relevant repos and open or prepare up to 5 high-quality proof-of-work PRs or comments.
- **Days 8-10:** convert accepted patterns into reusable skills and update public docs.
- **Days 11-14:** attempt the first paid conversion only after a prospect replies, the repo fits, and scope is clear.

## Validation Gates

Do not scale outreach volume until the current loop shows at least one of:

- a maintainer reply on a proof-of-work PR or comment
- a fit-check issue opened from a public path
- a free audit accepted by a strong-fit public repo
- a paid starter or standard audit conversation with explicit buyer interest

Cut or rewrite a channel if it produces no useful conversation after two weekly review cycles.

## Conversion Path

First contact stays useful and low-pressure:

1. Public project/thread context.
2. Front-desk issue, fit-check issue, or public repo URL.
3. Free fit check, optional donation/support, USD 49 starter report, or USD 149 standard audit.
4. Scope confirmation.
5. Ko-fi donation if the public work helped, or Ko-fi payment if the buyer wants to proceed with scoped paid work.
6. Optional USD 299+ standard-audit-plus-one-PR package after fit and scope confirmation.

## LLMGate Division of Labor

Use LLMGate for heavy public-safe work:

- Lead scoring and summarization.
- Outreach draft review.
- Checklist synthesis.
- Audit reasoning over explicitly selected public files.
- Code co-worker proposals through `scripts/llm_coworker.py`.

Defaults:

- `gpt-5.5` for primary reasoning and code review.
- `gpt-5.4` as fallback.
- `gpt-5.4-mini` only for small checks.
- Do not use Gemini.

Never send secrets, private user data, raw private conversations, credentials, private repo material, or confidential customer context to LLMGate.

Review this plan weekly while the acquisition loop is active.
