# Public Evidence Bundle Prelaunch Audit

Status: candidate

Use this workflow when a public issue asks for a pre-launch security or readiness review, but the repository does not expose enough public evidence to verify the requested checklist.

## Trigger

Good fits:

- A public issue explicitly asks for security review, launch readiness, dependency audit, CI/CD review, or cloud/IaC hardening.
- The repo is public and safe to inspect.
- The visible repo lacks the IaC, workflows, dependency manifests, config examples, or tests needed to verify the request.
- A short evidence-gap comment can help the maintainer prepare a public-safe review bundle.

Do not use this to request private credentials, account access, production dashboards, raw secrets, vulnerable endpoints, or confidential architecture.

## Inputs

- Public issue URL.
- Public repository file inventory.
- Lightweight local audit output, if it contains no private data.
- The issue's requested review checklist.

Never include secrets, private user data, exploit instructions, raw private chats, or ignored local files.

## Workflow

1. Confirm the issue is open and explicitly invites review.
2. Inspect only public repository contents.
3. Identify which requested checks cannot be verified from public files.
4. Run a lightweight repo hygiene audit if appropriate.
5. Draft one concise comment that includes:
   - scope and disclaimer
   - no private credentials or account access needed
   - specific missing public artifacts
   - concrete visible hygiene gaps
   - opt-out / no-pressure close
6. Do not include payment links in the first contact.
7. Log the exact message under `leads/sent/`.

## Validation

Expected checks:

- The comment is useful even if no paid work follows.
- The artifact list asks for sanitized or public-safe evidence only.
- The comment does not imply certified pentest, compliance, or guaranteed security.
- The comment does not ask the maintainer to expose secrets or private infrastructure.

## Failure Modes

Stop or revise when:

- the repo appears to involve minors, medical patients, vulnerable users, or sensitive personal data
- the issue asks for offensive testing, exploit development, stealth, persistence, or unauthorized access
- the requested review requires private production access to be meaningful
- the maintainer has already provided a review bundle or assigned the work elsewhere

## Evidence

- prompt_hub pre-launch review issue: https://github.com/JuneKim0007/prompt_hub/issues/29
- Evidence-gap triage comment: https://github.com/JuneKim0007/prompt_hub/issues/29#issuecomment-4701880302

Outcome interpretation:

- Count as a qualified lead only if the maintainer replies with public-safe artifacts, asks for a bounded audit, or clarifies scope.
- Count as useful non-conversion if the maintainer adds the missing artifacts or closes the issue as not public-reviewable.
