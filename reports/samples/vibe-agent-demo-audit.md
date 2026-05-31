# Vibe/Agent Repo Safety Audit Demo

Date: 2026-05-31
Repository: synthetic public demo repo
Audit type: lightweight public-repo launch/readiness review

## Demo Note

This is a public-safe demonstration report. It combines common risk patterns seen in public AI-built app discussions and does not describe a real client repository. No secrets, private data, account access, or confidential findings are included.

## Disclaimer

This is a lightweight launch/readiness audit. It is not a certified penetration test, legal advice, compliance attestation, or proof that a repository is secure.

## Executive Summary

- Overall launch-readiness status: Needs fixes before wider launch
- Highest-priority concern: public code suggests tenant isolation and webhook verification need manual confirmation
- Recommended next step: fix ownership checks and webhook signature handling before inviting real users

## Summary

| Severity | Count |
| --- | ---: |
| Critical | 0 |
| High | 2 |
| Medium | 3 |
| Low | 2 |
| Info | 2 |

## Findings

### 1. Tenant isolation needs explicit ownership checks

- Severity: High
- Area: Auth / tenant isolation
- Evidence: Example request handlers query records by user-supplied ID, but the public code sample does not show an owner or workspace constraint.
- Why it matters: A working demo can still expose another user's records if authorization is only checked at login time.
- Recommendation: Require ownership or workspace checks in every read, update, delete, export, and webhook-side lookup path. Add regression tests for cross-user access.
- Fix effort: Medium

### 2. Webhook endpoint does not show signature verification

- Severity: High
- Area: Webhook
- Evidence: Public route example parses webhook JSON before any visible provider signature verification.
- Why it matters: Attackers can trigger fake payment, provisioning, or account-state events if webhook trust is not verified first.
- Recommendation: Verify provider signatures against raw request bodies before parsing event data. Fail closed and log rejected event IDs without storing payload secrets.
- Fix effort: Small

### 3. Browser-facing env names suggest privileged key confusion

- Severity: Medium
- Area: Secrets / env
- Evidence: The demo env example uses public and server-only variable names in the same block without scope labels.
- Why it matters: AI-built apps often accidentally move server-only keys into client-side config while debugging.
- Recommendation: Split `.env.example` into public-safe and server-only groups. Add a CI check that blocks privileged env names in browser bundles.
- Fix effort: Small

### 4. MCP/tool permissions are not documented as a trust boundary

- Severity: Medium
- Area: Agent workflow / MCP
- Evidence: The repository includes an agent tool configuration, but no allowlist, review note, or expected tool boundary is documented.
- Why it matters: Agent tools can read files, call local commands, or pass untrusted text into privileged workflows if permissions are treated as ordinary config.
- Recommendation: Document allowed tools, denied tools, review owner, update process, and fail-closed behavior for tool calls that touch local files or credentials.
- Fix effort: Small

### 5. Static security headers are incomplete for launch

- Severity: Medium
- Area: Browser / public readiness
- Evidence: The sample deployment config does not show a content security policy or frame protection.
- Why it matters: Missing headers rarely break demos, but they increase launch risk once untrusted content, embeds, analytics, or auth flows are added.
- Recommendation: Add a conservative CSP, frame protections, referrer policy, and permissions policy appropriate for the deployed host.
- Fix effort: Small

### 6. Security reporting path is missing

- Severity: Low
- Area: Docs
- Evidence: No `SECURITY.md` or vulnerability-reporting path is linked from the README.
- Why it matters: Helpful users and researchers need a clear route that does not require public disclosure of sensitive details.
- Recommendation: Add `SECURITY.md` with scope, no-secret instructions, and a safe reporting contact or issue triage path.
- Fix effort: Small

### 7. CI does not run the launch checklist

- Severity: Low
- Area: CI
- Evidence: The demo repo has formatting checks but no launch-readiness or public-safety validator.
- Why it matters: Manual fixes drift. A lightweight CI gate prevents obvious regressions from returning before launch.
- Recommendation: Add deterministic checks for required files, env examples, suspicious secret patterns, and high-risk config names.
- Fix effort: Small

## Positive Notes

- The project is public, inspectable, and small enough for a lightweight report.
- Payment and production credentials were not requested.
- Several concerns can be fixed with one or two bounded pull requests.

## Recommended Next Actions

1. Patch tenant isolation checks and add cross-user regression tests.
2. Fix webhook signature verification before processing event data.
3. Split public and server-only env examples, then add a CI check.
4. Document agent/MCP tool boundaries and expected review process.
5. Add `SECURITY.md` and launch-readiness headers.

## Fix Sprint Candidates

- One PR to add ownership checks and regression tests around the highest-risk routes.
- One PR to add webhook signature verification and request-body handling.
- One PR to add public-safety CI checks, env grouping, and security reporting docs.

## Public-Safe Boundary

The real audit workflow redacts suspicious values and does not store raw secrets. It reviews public repositories only unless a separate private scope is explicitly agreed.
