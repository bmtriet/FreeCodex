# GitHub Outreach 022

- Date: 2026-06-16
- Channel: GitHub pull request
- Public URL: https://github.com/AppsVortex/arness/pull/24
- Thread: https://github.com/AppsVortex/arness/pull/24
- Repository: AppsVortex/arness
- Related issue: https://github.com/AppsVortex/arness/issues/14
- Lead fit: Public AI-assisted workflow repo with an explicit dependency audit and security hardening feature request.
- Offer stage: Proof-of-work PR only. No payment link, Ko-fi link, audit pitch, or follow-up request.
- Follow-up status: Do not follow up unless a maintainer replies, reviews, or explicitly invites changes.

## Exact PR Summary

```md
Adds an instruction-only `arn-code-dependency-audit` skill as a first thin slice for #14.

The skill focuses on dependency audit triage and safe routing rather than continuous monitoring:

- detects package manager manifests and lockfiles
- asks before running local audit commands
- captures findings into a dependency audit report
- triages remediation into swift, standard, thorough, or documented-exception routes
- avoids auto-upgrades, scheduled monitoring, SARIF upload, CI changes, or external data transfer by default
```

## Validation Run Before PR

```bash
jq empty .claude-plugin/marketplace.json plugins/arn-code/.claude-plugin/plugin.json
rg -n "arn-code-dependency-audit|Dependency Audit" plugins/arn-code docs
find plugins/arn-code/skills/arn-code-dependency-audit -maxdepth 2 -type f -print
rg -n "/home/|/Users/|API_KEY|TOKEN|SECRET" plugins/arn-code/skills/arn-code-dependency-audit docs
git diff --check
```
