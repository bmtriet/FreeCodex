# Dependency Migration Baseline Check

Status: candidate

Use this workflow when a public repository asks for dependency replacement or security migration analysis, but the existing validation baseline may already be failing.

## Trigger

Good fits:

- A public issue asks for dependency audit, stale dependency analysis, or replacement evaluation.
- The maintainers explicitly care about avoiding breaking validation behavior.
- The repo has public validation commands.
- A safe first contribution is current-state evidence rather than a dependency PR.

Do not use this for private advisories, production exploit reproduction, or migrations that require private package registries or credentials.

## Inputs

- Public issue URL.
- `package.json` scripts and dependency tree.
- Local install/audit results.
- Current validation command results.

Never include secrets, private registry tokens, hidden local files, or exploit instructions.

## Workflow

1. Confirm the issue is open and asks for analysis or migration.
2. Clone into ignored `local/`.
3. Run install using the repo's package manager.
4. Run audit and record only aggregate/public package findings.
5. Run the current validation commands before changing dependencies.
6. If baseline validation is red, do not open a dependency replacement PR.
7. Leave a concise public comment with:
   - current install/audit summary
   - which validation commands pass/fail
   - the smallest safe next slice
   - no payment link or private-access request
8. Log the exact message under `leads/sent/`.

## Validation

Expected checks:

- Existing baseline command output is specific enough to be actionable.
- The comment avoids overstating exploitability.
- The next step separates baseline fixes from dependency replacement.
- No private or ignored local artifacts are committed.

## Failure Modes

Stop or revise when:

- the repository requires private credentials to install or validate
- audit output is too broad and no actionable baseline signal exists
- the issue already has recent maintainer-owned migration work
- a PR would change dependencies before existing validation is green

## Evidence

- MCP browser-tools dependency issue: https://github.com/ahelme/mcp-claude-code-browser-tools/issues/61
- Baseline analysis comment: https://github.com/ahelme/mcp-claude-code-browser-tools/issues/61#issuecomment-4701919064

Outcome interpretation:

- Count as useful if maintainer acknowledges the baseline issue, fixes it, or asks for a focused PR.
- Do not count as proof-of-work PR evidence unless a follow-up code change is accepted.
