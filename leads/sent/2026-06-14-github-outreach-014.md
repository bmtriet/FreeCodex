# GitHub Outreach 014

- Date: 2026-06-14
- Channel: GitHub pull request
- Public URL: https://github.com/arkangelai/ms365-cli/pull/7
- Thread: https://github.com/arkangelai/ms365-cli/pull/7
- Related issue: https://github.com/arkangelai/ms365-cli/issues/4
- Project: arkangelai/ms365-cli
- Why fit: Public JavaScript CLI with an open dependency audit issue reporting high-severity `vite` and moderate `postcss` findings. Current audit reproduced a critical/high dev dependency chain through `vitest`, `vite`, `@vitest/mocker`, and `esbuild`. Existing `package.json` semver allowed a lockfile-only refresh to patched versions.
- Approval status: autonomous under `docs/autonomous-outreach-policy.md`
- Follow-up status: do not follow up unless the maintainer replies, requests changes, or explicitly invites more input.

## Funnel Status

- Reply received: no
- Fit-check opened: no
- Qualified lead: strong
- Audit requested: public issue requests dependency audit fix
- Paid conversion: no
- Notes: Public-safe proof-of-work PR only. No payment link, private contact info, secrets, exploit details, or raw private messages.

## Pull Request Opened

PR opened: https://github.com/arkangelai/ms365-cli/pull/7

## Exact Pull Request Body

## Summary
- refresh `package-lock.json` so `vitest` resolves to 4.1.8
- clears the current `npm audit` findings for `vitest`, `vite`, `@vitest/mocker`, and `esbuild`
- leaves `package.json` unchanged because the existing `^4.0.18` range already permits the patched version

## Context
This follows up on #4. I kept this to a lockfile-only update so the dependency change stays narrow.

## Verification
- `npm ci`
- `npm audit --audit-level=moderate`
- `npm run test:unit` -> 15 files / 187 tests passed

This is a lightweight public dependency-audit fix, not a certified security audit. No private credentials or account access were used.
