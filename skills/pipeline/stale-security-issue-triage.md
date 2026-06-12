# Stale Security Issue Triage

Status: candidate

Use this workflow when a large public repository has an old open security, CSP, dependency, or hardening issue that may already be fixed on the default branch.

## Trigger

Good fits:

- The issue is open, public, and specific.
- Maintainers previously agreed the issue is valid.
- Current code search suggests the requested setting, test, or mitigation may already exist.
- A comment can help maintainers close, retitle, or narrow the issue without requiring private access.

Do not use this for unresolved vulnerability reports, exploit details, or issues where maintainers asked for no external triage.

## Inputs

- Public issue URL.
- Current default branch.
- Public file paths or tests proving the current state.
- Existing maintainer comments showing whether the issue is still wanted.

Never include secrets, private reports, credentials, exploit steps, or non-public scan output.

## Workflow

1. Confirm the issue is still open.
2. Confirm the repository is large or strategically relevant enough to justify public triage.
3. Search current default branch for the requested feature, config, mitigation, and tests.
4. Check whether the evidence is direct enough to support a short comment.
5. Stop if the issue needs product/security owner judgment and current code does not clearly answer it.
6. Post at most one concise comment with:
   - current branch checked
   - exact public file paths
   - what appears implemented
   - a clear caveat if release/docs/backport nuance may remain
7. Log the comment under `leads/sent/`.

## Validation

Expected checks:

- The comment links or names exact public paths.
- The comment does not ask for payment, private access, or a meeting.
- The comment does not claim certified security review.
- The comment is useful even if the maintainer disagrees.

## Failure Modes

Stop or revise when:

- code evidence is indirect or ambiguous
- the issue contains unreleased or confidential security context
- the comment would duplicate a recent maintainer or bot comment
- the issue is already assigned and actively being handled
- the repo has contribution guidance discouraging external triage comments

## Evidence

- Kibana CSP issue: https://github.com/elastic/kibana/issues/202429
- Triage comment: https://github.com/elastic/kibana/issues/202429#issuecomment-4689515960

Outcome interpretation:

- This is a proof-of-attention pattern, not a direct sales pattern.
- Count it as useful only if a maintainer closes, labels, replies positively, or uses the evidence to narrow the issue.
