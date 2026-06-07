# Proof-Of-Work PRs

Proof-of-work PRs are small, public contributions that demonstrate FreeCodex can spot and fix launch-readiness issues without making a generic sales pitch.

## When To Open One

Open a PR only when:

- The repo is public.
- The fix is obvious, narrow, and low-risk.
- The project accepts public contributions.
- The change does not require credentials, private context, or production access.
- The PR can stand alone even if no sale happens.

Good PR examples:

- Add or improve `SECURITY.md`.
- Add `.env` and local secrets to `.gitignore`.
- Clarify that service-role keys must stay server-side.
- Add a conservative CSP or CORS note when the existing app already has relevant config.
- Add webhook signature verification documentation.
- Add launch-readiness notes to README.
- Add a missing env example without real values.

Avoid:

- Deep unpaid remediation.
- Large refactors.
- Security theater.
- Anything that exposes suspected secrets publicly.
- Changes that need private testing or account access.
- Repeated PRs to the same repo without invitation.

## How To Reference The PR

Lead with the useful contribution, then mention the audit only as optional.

```text
I opened a small PR for one launch-readiness item I noticed here: [PR URL].

If useful, I also do lightweight public-repo safety reviews for AI-built apps and agent workflows. No credentials or account access needed, and it is not a certified pentest.
```

Do not include payment links in the first contact.

## How Much Value To Give Away

The PR should fix one clear issue or add one helpful guardrail. It should not become a full unpaid audit or broad fix sprint.

If the repo has many findings, deliver the small PR and offer a fit check or report scope only after the maintainer shows interest.

## Tracking

Log sent messages and PR URLs under `leads/sent/`. Mission Control summarizes outcomes in `ops/outcomes.md`.
