# Static Security Headers Audit

Status: candidate

Current evidence is enough for candidate status, not full promotion. Promotion requires this workflow to work on at least two public-safe tasks with recorded validation.

## Trigger

Use this skill when reviewing a public static frontend, deploy config, or proof-of-work PR where browser security headers may be missing or incomplete.

Good fits:

- public repos with `_headers`, `netlify.toml`, or `vercel.json`
- static sites deployed on Netlify, Vercel, Cloudflare Pages, or similar hosts
- AI-built launch pages and fast prototypes with no visible security header notes
- small PRs that can add a conservative baseline without changing app logic

Do not use it as a certified security review or as proof that the deployed site is secure.

## Inputs

- Public repository URL or local checkout.
- Deployment target when visible.
- Existing header/deploy config files.
- App requirements that may affect CSP, such as remote images, analytics, API domains, or inline scripts.

Never request credentials, private account access, tokens, cookies, or private production settings.

## Workflow

1. Inspect existing header/deploy config files.
2. Check whether a `Content-Security-Policy` is actually configured, not just mentioned in a comment.
3. Look for related basics when in scope: `X-Frame-Options` or `frame-ancestors`, `X-Content-Type-Options`, `Referrer-Policy`, and `Permissions-Policy`.
4. If proposing a fix, keep it minimal and compatible with visible app behavior.
5. Prefer `frame-ancestors 'none'` for apps that do not need embedding.
6. Keep `connect-src`, `img-src`, and `script-src` broad enough for known public dependencies, then recommend tightening after runtime testing.
7. Label uncertain items as manual-review hints.
8. Run local tests, build checks, and `git diff --check` when editing a repo.

## Validation

For FreeCodex tooling:

```bash
python3 -m unittest discover -s tests -q
python3 scripts/validate_repo.py
python3 scripts/repo_audit.py audit --path . --output local/reports/freecodex-static-headers-audit.md
git diff --check
```

For external proof-of-work PRs:

- Build or test command from the target repo.
- Confirm no formatting-only churn unless requested.
- Confirm the app still loads expected public assets.
- Confirm the target platform is expected to emit headers from the visible config, or keep the item in report-only/manual-review mode.
- If a deployed preview is available and authorized, verify representative response headers with a browser devtools network check or `curl -I`.
- Clearly state any pre-existing test or format failures.

## Failure Modes

Stop or switch to report-only when:

- the app uses dynamic inline scripts and no safe nonce/hash strategy is visible
- deploy behavior cannot be inferred from public files
- no deployed preview or host documentation is available to confirm emitted headers
- the change could break payments, auth, analytics, embeds, or media loading
- the repo has private or sensitive context that is not explicitly authorized
- the finding depends on live production behavior that cannot be checked safely

## Evidence

This candidate is based on:

- a merged proof-of-work CSP/header PR in a public repo
- the FreeCodex `repo_audit.py` static CSP check
- LLMGate review catches for false positives around deploy config files and commented CSP lines
