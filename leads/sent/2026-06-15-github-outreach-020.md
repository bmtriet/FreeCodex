# GitHub Outreach 020

- Date: 2026-06-15
- Channel: GitHub issue comment
- Public URL: https://github.com/NousResearch/hermes-agent/issues/14000#issuecomment-4709650326
- Thread: https://github.com/NousResearch/hermes-agent/issues/14000
- Repository: NousResearch/hermes-agent
- Lead fit: Large public AI agent repo with an open dependency-audit/security issue and existing supply-chain workflows.
- Offer stage: Proof-of-work only. No payment link, Ko-fi link, audit pitch, or follow-up request.
- Follow-up status: Do not follow up unless a maintainer replies or explicitly invites help.

## Exact Message Sent

```md
Given this looks like a recurring automated dependency-audit issue, a PR may be premature until there is a single tracker and a clear remediation policy.

A concrete next slice could be:

1. Create or confirm one canonical dependency-audit tracking issue.
2. In that issue, list each currently affected ecosystem/lockfile separately:
   - root `package-lock.json`
   - `website/package-lock.json`
   - Python/UV via `uv.lock`
3. For each advisory, record:
   - package name and advisory link
   - direct vs transitive dependency
   - affected path/workspace
   - whether a fix is available without major upgrades
   - whether it is runtime-reachable or build/dev-only
4. Close duplicate recurring audit issues in favor of that tracker.
5. Optionally add a short maintainer note explaining that Dependabot is intentionally limited for pinned source deps, while OSV scanning runs weekly/on lockfile changes with `fail-on-vuln: false`.

I also noticed current `main` no longer has `bun.lock`, so older comments mentioning Bun may be stale. The active lockfiles appear to be `package-lock.json`, `website/package-lock.json`, and `uv.lock`.

Lightweight readiness note: this is just dependency-triage from public repo metadata, not a certified pentest or exploitability assessment, and it does not require credentials or account access. No worries if not useful.
```
