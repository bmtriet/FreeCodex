# Public Security Policy PR

Status: candidate

Use this workflow when a large public repository has no visible `SECURITY.md`, but already has or can safely use a private vulnerability reporting channel such as GitHub Security Advisories.

## Trigger

Good fits:

- a public issue explicitly asks for a missing security policy
- GitHub metadata shows no enabled security policy
- the repository already exposes a private advisory/contact path
- the change can be documentation-only and bounded

Do not use this to disclose vulnerability details, request private access, or invent a security response process for maintainers.

## Inputs

- Public repository URL.
- Public issue requesting a security policy, if present.
- Existing private vulnerability reporting path.
- Repository default branch and documentation conventions.

Never include credentials, private reports, exploit details, or confidential vulnerability material.

## Workflow

1. Confirm neither `SECURITY.md` nor `.github/SECURITY.md` exists.
2. Confirm the repository's private vulnerability reporting path from public metadata or docs.
3. Add a concise `SECURITY.md` that points reporters to the private channel.
4. Warn reporters not to disclose vulnerabilities in public issues, discussions, or pull requests.
5. Keep scope to reporting guidance, disclosure etiquette, and update guidance.
6. Avoid unsupported claims about SLAs, bounties, supported versions, or guaranteed security response.
7. Open a small PR that references the source issue and states that no sensitive details are included.

## Validation

```bash
git diff --check
gh api repos/OWNER/REPO/contents/SECURITY.md
gh api repos/OWNER/REPO/contents/.github/SECURITY.md
gh repo view OWNER/REPO --json isSecurityPolicyEnabled,contactLinks
```

Expected checks:

- existing policy paths return 404 before the PR
- private reporting channel is verified from public metadata
- PR body contains no payment link, credentials, private data, or vulnerability details
- docs-only diff is small enough for maintainer review

## Failure Modes

Stop or revise when:

- no official private reporting channel is visible
- a policy already exists in the repo or shared org `.github` repository
- the proposed text claims unsupported SLA, bounty, or version support
- the PR would expose vulnerability details or encourage public disclosure
- the repository asks security reports to use a different official channel

## Evidence

This candidate is based on a merged documentation PR in `langgenius/dify`:

- Source issue: https://github.com/langgenius/dify/issues/36692
- Merged PR: https://github.com/langgenius/dify/pull/36873
- Result: maintainer approved and merged the bounded `SECURITY.md` addition.
