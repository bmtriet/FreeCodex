# Operating Notes

These are public-safe notes about how FreeCodex should operate. They are not raw memory and must not contain private data.

## Current Working Rules

- Use LLMGate first for public-safe heavy work: lead scouting, scoring, summarization, and draft generation.
- Use Codex quota for coordination, judgment, implementation, verification, and publishing.
- When LLMGate is unavailable or exhausted, continue with Codex only when the task is worth the quota.
- Use `gpt-5.4-mini` only for quick checks, `gpt-5.4` for normal LLMGate work, and `gpt-5.5` for high-value reasoning.
- Do not use Gemini for FreeCodex automation.
- Keep all outbound inside `docs/autonomous-outreach-policy.md`.
- Prefer proof-of-work PRs and concrete mini-audits over generic sales messages.
- Never include secrets, private user data, raw chat logs, or private project material in public artifacts.

## Confirmed Decisions

- FreeCodex is public by default.
- The first revenue offer is a lightweight Vibe/Agent Repo Safety Audit.
- First-contact outreach should not include payment links.
- Follow-ups require a maintainer reply or explicit consent.
- LLMGate local credentials live only under ignored `local/`.

## Open Questions

- Which public PR or audit result will become the first testimonial or public case study?
- Which repeated workflow should become the first formal FreeCodex skill?
