# GitHub Outreach 012

- Date: 2026-06-12
- Channel: GitHub issue comment
- Public URL: https://github.com/elastic/kibana/issues/202429#issuecomment-4689515960
- Thread: https://github.com/elastic/kibana/issues/202429
- Project: elastic/kibana
- Why fit: Large public developer/security project with an open CSP enhancement issue. Current `main` appeared to already contain the requested `csp.object_src` support, so the safest value-first action was a public triage comment with file-level evidence instead of a PR.
- Approval status: autonomous under `docs/autonomous-outreach-policy.md`
- Follow-up status: do not follow up unless a maintainer replies, asks a question, or explicitly invites more input.

## Funnel Status

- Reply received: no
- Fit-check opened: no
- Qualified lead: medium
- Audit requested: no
- Paid conversion: no
- Notes: Public-safe triage only. No payment link, private contact info, secrets, exploit details, or raw private messages.

## Exact Message Sent

I checked current `main` and this appears to be implemented now, unless the remaining ask is specifically docs/release tracking rather than runtime support.

Evidence:
- `src/core/packages/http/server-internal/src/csp/config.ts` defines top-level `csp.object_src` with validation.
- `src/core/packages/http/server-internal/src/csp/csp_directives.ts` includes `object-src` in `CspDirectiveName`, parses `object_src` into the enforced directive map, and default rules include `object-src 'report-sample' 'none'`.
- `src/core/packages/http/server-internal/src/csp/csp_directives.test.ts` has coverage for default `object-src 'none'` and for replacing `'none'` when `object_src` is configured.

No private access or security details involved here; this is just a lightweight public triage check. No worries if there is a release-branch/docs nuance I missed.
