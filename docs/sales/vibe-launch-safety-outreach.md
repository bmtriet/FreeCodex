# Vibe Launch Safety Outreach

This playbook is for first-contact messages only.

## Rules

- First contact never includes payment links.
- Keep the message short and specific to the public context.
- Mention that the review is lightweight and not a certified pentest.
- Say no credentials or account access are needed.
- Include an easy opt-out.
- Do not follow up unless the recipient replies or explicitly invites it.

## GitHub Issue Or Discussion

```text
Hi - saw this public repo/thread and thought the launch-readiness angle might be relevant.

I do lightweight public-repo safety reviews for AI-built apps and agent workflows: obvious leaked-secret indicators, env examples, GitHub Actions/agent review prompts, CSP/CORS hints, webhook/auth review prompts, and missing launch basics.

Not a certified pentest, and no credentials or account access needed. If useful, I can share what a small repo audit would cover. No worries if not useful.
```

## After A Small Proof-Of-Work PR

```text
Hi - I opened a small public PR for one launch-readiness item I noticed here: [PR URL].

I also do lightweight public-repo safety reviews for AI-built apps and agent workflows. The review looks for obvious leaked-secret indicators, env/example issues, CI/agent review prompts, CSP/CORS hints, and webhook/auth review prompts.

Not a certified pentest, and no credentials or account access needed. Happy to share the scope if useful. No worries if not.
```

## Short DM Or Email

Use this only when the person has publicly invited relevant contact.

```text
Hi - I saw your public launch/repo and noticed it may fit a lightweight launch-readiness review.

I review public repos for AI-built apps and agent workflows: obvious secret patterns, env/example safety, GitHub Actions/agent review prompts, CSP/CORS hints, and webhook/auth review prompts. Not a certified pentest, and no credentials or account access needed.

If helpful, I can send the small audit scope. No worries if not useful.
```

For autonomous use, follow the 3-message-per-run limit and log messages under `leads/sent/`.
