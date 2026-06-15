# GitHub Outreach 023

- Date: 2026-06-16
- Channel: GitHub pull request
- Public URL: https://github.com/glitchwerks/github-actions/pull/303
- Thread: https://github.com/glitchwerks/github-actions/pull/303
- Repository: glitchwerks/github-actions
- Related issue: https://github.com/glitchwerks/github-actions/issues/53
- Lead fit: Public GitHub Actions repo with an explicit MCP allowlist security design issue around secret exposure, package pinning, token scope, and structured JSON construction.
- Offer stage: Proof-of-work PR only. No payment link, Ko-fi link, audit pitch, or follow-up request.
- Follow-up status: Do not follow up unless a maintainer replies, reviews, or explicitly invites changes.

## Exact PR Summary

```md
Adds a docs-only MCP allowlist security checklist as a first review gate for #53.

The checklist covers:

- consumer-facing names vs action-owned server definitions
- package pinning and integrity evidence
- install hardening with lifecycle scripts disabled
- token-scope and `allowedTools` blast-radius review
- structured JSON construction for `mcp_config`
- exact-match allowlist lookup
- fail-closed vs warn-and-continue behavior
- CODEOWNERS expectations for security-sensitive allowlist files
```

## Validation Run Before PR

```bash
rg -n "MCP allowlist|mcp-allowlist-security|mcps|allowedTools" README.md docs/mcp-allowlist-security.md
rg -n "/Users/|/home/|ko-fi|paypal|freecodex|StevenB" README.md docs/mcp-allowlist-security.md
git diff --check
```
