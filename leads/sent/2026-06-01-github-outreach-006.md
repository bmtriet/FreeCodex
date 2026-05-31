# GitHub Outreach 006 - Dify Security Policy PR

Date: 2026-06-01

## Channel

GitHub pull request.

## Public URL

- PR: https://github.com/langgenius/dify/pull/36873
- Source issue: https://github.com/langgenius/dify/issues/36692

## Why This Lead Fit

- `langgenius/dify` is a large public AI-agent platform repository.
- Public GitHub metadata showed no enabled security policy.
- The source issue explicitly requested a missing vulnerability reporting channel.
- The fix was bounded, public-safe, documentation-only, and did not require credentials, private access, or vulnerability details.

## Exact Message Sent

PR title:

```text
docs: add security policy
```

PR body:

```text
## Summary
- add SECURITY.md with the existing private GitHub Security Advisory reporting path
- ask reporters not to disclose vulnerabilities in public issues, discussions, or PRs
- add concise guidance on what to include in private reports and how disclosure/security updates are handled

Closes #36692.

## Verification
- Confirmed SECURITY.md and .github/SECURITY.md were not present via GitHub Contents API
- Confirmed the repo already exposes the private advisory contact link
- Ran git diff --check

This is documentation only. No credentials, account access, private data, or vulnerability details are included.
```

## LLMGate Usage

LLMGate `gpt-5.5` scored the large-repo lead shortlist and recommended this PR as the safest, most bounded high-visibility action. LLMGate also drafted the initial public-safe `SECURITY.md`; Codex reviewed and edited it before committing.

## Follow-Up Status

No follow-up unless a maintainer replies or explicitly invites additional work.
