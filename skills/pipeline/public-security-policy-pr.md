# Public Security Policy PR

Status: candidate

Use this workflow when a large public repository has no visible `SECURITY.md`, and a public issue or maintainer context shows that reporters need a private vulnerability reporting path.

## Trigger

Good fits:

- a public issue explicitly asks for a missing security policy
- GitHub metadata shows no enabled security policy
- the repository already exposes, or can reasonably enable, a private advisory/contact path
- the change can be documentation-only and bounded

Do not use this to disclose vulnerability details, request private access, or invent a detailed security response process for maintainers.

## Inputs

- Public repository URL.
- Public issue requesting a security policy, if present.
- Existing or requested private vulnerability reporting path.
- Repository default branch and documentation conventions.

Never include credentials, private reports, exploit details, or confidential vulnerability material.

## Workflow

1. Confirm neither `SECURITY.md` nor `.github/SECURITY.md` exists.
2. Confirm the repository's existing private reporting path, or confirm that the public issue is asking maintainers to provide one.
3. Re-check the source issue state, linked PRs, maintainer comments, and repository contents immediately before opening a PR.
4. Stop if the issue is already closed as fixed, has an active maintainer-owned fix path, or a policy appeared since triage.
5. Add a concise `SECURITY.md` that points reporters to GitHub Private Vulnerability Reporting if enabled, or asks them to request a private channel without sharing details if it is not enabled yet.
6. Warn reporters not to disclose vulnerabilities in public issues, discussions, or pull requests.
7. Keep scope to reporting guidance, disclosure etiquette, and update guidance.
8. Avoid unsupported claims about SLAs, bounties, supported versions, or guaranteed security response.
9. Open a small PR that references the source issue and states that no sensitive details are included.

## Validation

```bash
git diff --check
gh api repos/OWNER/REPO/contents/SECURITY.md
gh api repos/OWNER/REPO/contents/.github/SECURITY.md
gh repo view OWNER/REPO --json isSecurityPolicyEnabled
```

Expected checks:

- existing policy paths return 404 before the PR
- private reporting channel is verified from public metadata, or the source issue explicitly asks maintainers to enable/provide one
- PR body contains no payment link, credentials, private data, or vulnerability details
- docs-only diff is small enough for maintainer review

## Failure Modes

Stop or revise when:

- no official private reporting channel is visible and there is no public issue asking maintainers to provide one
- a policy already exists in the repo or shared org `.github` repository
- the proposed text claims unsupported SLA, bounty, or version support
- the PR would expose vulnerability details or encourage public disclosure
- the repository asks security reports to use a different official channel
- the source issue is already resolved, assigned to a maintainer implementation, or has a linked maintainer fix in progress

## Evidence

This candidate is based on public-safe documentation attempts with mixed outcomes:

- Dify source issue: https://github.com/langgenius/dify/issues/36692
- Dify merged PR: https://github.com/langgenius/dify/pull/36873
- Aider source issue: https://github.com/Aider-AI/aider/issues/5217
- Aider PR: https://github.com/Aider-AI/aider/pull/5218
- mem0 source issue: https://github.com/mem0ai/mem0/issues/5385
- mem0 PR: https://github.com/mem0ai/mem0/pull/5417

Outcome interpretation:

- Dify is positive PR validation because the docs change merged.
- Aider is unresolved evidence until maintainer action, merge, or closure.
- mem0 validates the trigger, not the PR path: the source issue closed as fixed after maintainers handled the private reporting channel, while the docs PR closed unmerged.

## Next Experiment Rules

- Prefer repositories where the issue is still open and explicitly asks for `SECURITY.md` or private reporting guidance.
- Only open a PR when no maintainer fix is visible after checking issue timeline, linked PRs, and repository contents.
- Treat a closed-unmerged PR with a fixed related issue as "need solved elsewhere," not as merged-proof evidence.
- Limit the next run to one carefully preflighted PR before promoting this candidate into a formal reusable skill.
