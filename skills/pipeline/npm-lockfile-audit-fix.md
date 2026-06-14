# NPM Lockfile Audit Fix

Status: candidate

Use this workflow when a public JavaScript/TypeScript repository has an open dependency audit issue and the vulnerable dependency chain can be resolved by refreshing `package-lock.json` within existing semver ranges.

## Trigger

Good fits:

- A public issue reports `npm audit` findings with clear package names.
- The repository has `package.json` and `package-lock.json`.
- No open PR already fixes the same dependency chain.
- `npm audit` reproduces locally from public files.
- A lockfile-only change clears the relevant findings.

Do not use this for runtime dependency major upgrades, private advisories, or packages that require security-sensitive migration decisions.

## Inputs

- Public issue URL.
- `package.json`.
- `package-lock.json`.
- Local `npm audit` output.
- Project test command.

Never include credentials, private registry tokens, exploit instructions, or private audit output.

## Workflow

1. Confirm the issue is open and no duplicate PR exists.
2. Clone the public repo into ignored `local/` workspace.
3. Read repository instructions such as `AGENTS.md`.
4. Run `npm audit --json` to reproduce findings.
5. Prefer the smallest safe remediation:
   - `npm update <direct-parent> --package-lock-only`
   - leave `package.json` unchanged if existing ranges permit patched versions
6. Run `npm ci`.
7. Run `npm audit --audit-level=moderate`.
8. Run the narrowest relevant test command.
9. Open a PR with before/after audit and test results.
10. Log the exact PR body under `leads/sent/`.

## Validation

Expected checks:

- `npm audit --audit-level=moderate` exits successfully.
- Relevant tests pass.
- Diff is lockfile-only unless a manifest change is clearly required.
- PR body has no payment link and makes no certified security claim.

## Failure Modes

Stop or revise when:

- audit fix requires a major runtime dependency upgrade
- tests fail for reasons connected to the dependency update
- `npm audit fix --force` would be required
- lockfile refresh changes package manager format unexpectedly
- the vulnerability is dev-only and maintainers already documented it as non-actionable

## Evidence

- ms365-cli dependency issue: https://github.com/arkangelai/ms365-cli/issues/4
- Lockfile-only PR: https://github.com/arkangelai/ms365-cli/pull/7

Outcome interpretation:

- Count as proof-of-work if the PR gets merged, receives maintainer review, or triggers a concrete maintainer response.
- Keep as `candidate` until at least two public dependency-audit fixes pass review.
