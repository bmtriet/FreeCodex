# Public Security Policy PR Loop Evaluation

Date: 2026-06-12

## What Was Checked

The public security policy PR workflow after three public-safe attempts:

- Dify: source issue plus merged docs PR.
- Aider: source issue plus open docs PR.
- mem0: source issue closed as fixed, docs PR closed unmerged.

## Evidence

- Dify PR merged, which validates that a small `SECURITY.md` contribution can be acceptable proof-of-work.
- Aider PR remains open, so it is not yet a success or failure signal.
- mem0 issue closed as fixed after maintainers provided or enabled the private reporting path, while the docs PR closed without merge.
- LLMGate `gpt-5.5` reviewed the pattern and recommended narrower preflight rules, stop conditions, and outcome labels.

## Passed

- The workflow avoids public vulnerability details.
- The docs-only PR shape is small and reviewable.
- At least one large public repo accepted the contribution.

## Failed Or Mixed

- Counting every opened PR as positive evidence would overstate the skill quality.
- mem0 shows that a valid trigger can still produce a stale or unnecessary PR once maintainers solve the need elsewhere.
- The previous workflow did not explicitly require a last-minute issue timeline and linked-PR recheck before opening.

## Changes

- Keep `public-security-policy-pr` as `candidate`, not formal.
- Add preflight checks for closed issues, active maintainer fixes, linked PRs, and newly added policy files.
- Treat closed-unmerged PRs tied to fixed issues as trigger validation only.
- Do not repeat this pattern unless the issue is still open and no maintainer-owned fix path is visible.

## Next Decision

Run at most one more carefully preflighted public security policy PR before promoting, retiring, or narrowing this candidate further.
