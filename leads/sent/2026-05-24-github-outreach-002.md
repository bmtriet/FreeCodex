# GitHub Outreach Run 002

Date: 2026-05-24 12:59 +07
Channel: GitHub public PRs and issue comments
Mode: Autonomous, within `docs/autonomous-outreach-policy.md`
Outbound count: 3

## Summary

This run prioritized proof-of-work over sales copy:

- Opened 2 small public PRs that directly address open security/readiness issues.
- Sent 1 opt-in audit comment on an explicit security-audit request.
- Did not mention payment links in outbound messages.
- Used LLMGate once for public-safe lead scoring on public issue summaries only.

## 1. RoshanDavis/whisper

Public context:

- Issue: https://github.com/RoshanDavis/whisper/issues/8
- PR opened: https://github.com/RoshanDavis/whisper/pull/9

Why it fit:

- Open public issue requesting a bounded Web Crypto hardening change.
- No private data or account access required.
- A small PR could deliver value immediately.

Action:

- Forked `RoshanDavis/whisper` to `bmtriet/whisper`.
- Opened PR `Lock session crypto keys as non-extractable`.

Exact PR body:

```markdown
## Summary
- Set session-only derived/imported Web Crypto keys to non-extractable.
- Covers the ECDH shared secret, unwrapped ECDH private key, unwrapped ECDSA private key, and imported public keys called out in #8.
- Leaves registration/export paths unchanged so key wrapping/storage flows can still work.

## Verification
- `npm run build` passes in `frontend`.
- `npm run lint` still fails on existing unrelated lint issues outside this crypto patch. I did not change those files.

## Scope note
This is a small public-code contribution, not a certified pentest or security guarantee. I used only public repo code; no private credentials or account access needed. Feel free to close if not useful.

Closes #8.
```

Verification:

- `npm ci` completed in `frontend`.
- `npm run build` passed.
- `npm run lint` failed on pre-existing unrelated lint issues outside the changed file.

Follow-up status:

- No follow-up unless the maintainer replies.

## 2. ag-tech-group/hera-streamer-invitational-2026-web

Public context:

- Issue: https://github.com/ag-tech-group/hera-streamer-invitational-2026-web/issues/64
- PR opened: https://github.com/ag-tech-group/hera-streamer-invitational-2026-web/pull/75

Why it fit:

- Open public issue from 2026-05-23 requesting a production-readiness security review.
- The issue explicitly called out tightening `img-src` from wildcard `https:`.
- The repo is a public event frontend with no private access required.

Action:

- Ran a lightweight FreeCodex mini-audit locally.
- Ran `npx pnpm@10.24.0 audit --prod`: no known vulnerabilities found.
- Opened PR `Tighten CSP image sources` to remove broad `img-src https:` from both Netlify headers and the HTML meta CSP.

Exact PR body:

```markdown
## Summary
- Remove the broad `https:` allowance from `img-src` in the production Netlify headers.
- Mirror the same CSP change in the development/meta CSP in `index.html`.
- Keep local images, generated asset images, favicons, and data URIs allowed via `img-src 'self' data:`.

## Verification
- `npx pnpm@10.24.0 run build` passes.
- `npx pnpm@10.24.0 audit --prod` reports no known vulnerabilities.
- `npx pnpm@10.24.0 exec prettier --check index.html` passes.
- `git diff --check` passes.

## Scope note
This is a small public-code contribution, not a certified pentest or security guarantee. I used only public repo code; no private credentials or account access needed. Feel free to close if not useful.

Part of #64.
```

Verification:

- `npx pnpm@10.24.0 install --frozen-lockfile` completed.
- `npx pnpm@10.24.0 run build` passed.
- `npx pnpm@10.24.0 audit --prod` found no known vulnerabilities.
- `npx pnpm@10.24.0 exec prettier --check index.html` passed.
- `git diff --check` passed.

Follow-up status:

- No follow-up unless the maintainer replies.

## 3. mailpile/python-passcrow

Public context:

- Issue: https://github.com/mailpile/python-passcrow/issues/16
- Comment sent: https://github.com/mailpile/python-passcrow/issues/16#issuecomment-4527551073

Why it fit:

- Open public issue explicitly asking for security audits.
- The project is public and security-focused.
- The message is framed as opt-in because the repo has been quiet since 2022.

Action:

- Ran a lightweight FreeCodex mini-audit locally.
- Sent an opt-in comment without payment link or pressure.

Exact message sent:

```markdown
Hi! If this audit request is still relevant, I can do a free lightweight public-repo pass on Passcrow.

I ran a very small first sweep locally: no obvious committed token/key patterns jumped out from tracked files. The first low-noise items I would start with are repo-level review plumbing: add a `SECURITY.md` with reporting/scope guidance and add a minimal CI workflow so future crypto/recovery-flow changes get at least a repeatable smoke check.

Scope-wise, I would keep this to public code and docs only: protocol/threat-model notes, secret-handling paths, recovery-flow edge cases, dependency/CI hygiene, and docs that might confuse operators into unsafe config. No private credentials or account access needed, and this would be a lightweight review, not a certified pentest. No worries if this is stale or not useful.
```

Follow-up status:

- No follow-up unless the maintainer replies.

## Held Or Skipped

- `leedium/wc-2026-fantasy#55`: skipped after review and LLMGate scoring because the project already had a detailed remediation workflow; unsolicited lightweight-audit comment would likely add noise.
- `animishraa05/educationMirror#31`: skipped because education/real-user-data context could involve minors or sensitive users.
- `RohiRIK/fleetwatch#6`: skipped because fleet/location-style context may involve sensitive operational data and the issue was older.
- Broad or exploit-oriented security issues from search results were skipped when they involved offensive tooling, stealth, persistence, or unclear authorization.

## LLMGate Use

- Model used: `gemini-2.5-flash-lite`.
- Input: public issue summaries only.
- Purpose: lead scoring and draft assistance for `mailpile/python-passcrow#16` and `leedium/wc-2026-fantasy#55`.
- No private data, credentials, raw chat logs, or local secrets were sent.
